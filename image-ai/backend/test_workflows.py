"""Offline regression suite. Run from the project root with unittest."""
import os
import tempfile
import unittest
import sqlite3
from unittest.mock import AsyncMock, patch

tmp = tempfile.TemporaryDirectory()
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///' + tmp.name.replace('\\', '/') + '/test.db'
os.environ['GEMINI_API_KEY'] = ''
os.environ['GROQ_API_KEY'] = ''

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.services.image_engine import _save_image_bytes


class Workflows(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.client.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls.client.__exit__(None, None, None)

    def register(self, email):
        res = self.client.post('/api/auth/register', json={'email': email, 'password': 'Testpass123'})
        self.assertEqual(res.status_code, 200, res.text)
        return {'Authorization': 'Bearer ' + res.json()['access_token']}

    def test_complete_workflow(self):
        c = self.client
        self.assertEqual(c.get('/api/health').status_code, 200)
        self.assertEqual(c.get('/api/content/history').status_code, 401)
        headers = self.register('owner@example.com')
        other = self.register('other@example.com')
        self.assertEqual(c.post('/api/auth/login', json={'email': 'owner@example.com', 'password': 'Testpass123'}).status_code, 200)
        self.assertEqual(c.get('/api/business', headers=headers).status_code, 200)
        self.assertEqual(c.post('/api/business', headers=headers, json={'business_name': 'Test Studio'}).status_code, 200)
        with patch('backend.app.services.prompt_agent.PromptAgent._call_groq', side_effect=RuntimeError()):
            res = c.post('/api/content/agent-prompt', headers=headers, json={'user_input': 'Silk saree 20% off'})
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(res.json()['industry'], 'clothing')
        res = c.post('/api/content/generate', headers=headers, json={'product': 'Biryani', 'language': 'english', 'extra_fields': {'custom_api_key': 'should-not-be-saved'}})
        self.assertEqual(res.status_code, 200, res.text)
        item = res.json()['id']
        self.assertTrue(res.json()['caption'])
        self.assertEqual(c.get('/api/content/' + item, headers=other).status_code, 404)
        self.assertEqual(c.put('/api/content/' + item, headers=headers, json={'caption': 'Edited'}).json()['caption'], 'Edited')
        self.assertEqual(c.post('/api/content/regenerate', headers=headers, json={'content_id': item, 'offer': ''}).status_code, 200)
        with patch('backend.app.api.image.ImageEngine.generate', new=AsyncMock(side_effect=RuntimeError('down'))):
            self.assertEqual(c.post('/api/image/generate', headers=headers, json={'prompt': 'test'}).status_code, 503)
        with patch('backend.app.api.image.ImageEngine.generate', new=AsyncMock(return_value={'image_url': '/static/test.png', 'provider': 'test', 'status': 'success'})):
            self.assertEqual(c.post('/api/image/generate', headers=other, json={'content_id': item}).status_code, 404)
            self.assertEqual(c.post('/api/image/generate', headers=headers, json={'content_id': item}).status_code, 200)
            self.assertEqual(c.post('/api/image/generate', headers=headers, json={'prompt': 'Studio photo', 'product': 'Saree'}).status_code, 200)
        self.assertEqual(c.get('/api/content/' + item, headers=headers).json()['image_url'], '/static/test.png')
        self.assertEqual(c.get('/api/usage', headers=headers).json()['total_actions'], 4)
        with sqlite3.connect(tmp.name + '/test.db') as db:
            raw = db.execute('SELECT raw_inputs_json FROM generated_contents WHERE id = ?', (item,)).fetchone()[0]
        self.assertNotIn('custom_api_key', raw)
        self.assertNotIn('should-not-be-saved', raw)
        self.assertEqual(c.delete('/api/content/' + item, headers=headers).status_code, 200)
        history = c.get('/api/content/history', headers=headers).json()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['content_type'], 'image')

    def test_invalid_image_is_rejected(self):
        with self.assertRaises(Exception):
            _save_image_bytes(b'<html>provider failure</html>')

    def test_input_validation(self):
        self.assertEqual(self.client.post('/api/auth/register', json={'email': 'a@example.com', 'password': 'x'}).status_code, 422)

    def test_generation_matrix(self):
        headers = self.register('matrix@example.com')
        industries = self.client.get('/api/industries').json()
        count = 0
        for industry in industries:
            options = self.client.get('/api/industries/' + industry['id'] + '/options')
            self.assertEqual(options.status_code, 200)
            for kind in ['instagram_post', 'facebook_post', 'whatsapp_message', 'product_description', 'ad_copy', 'reel_script', 'marketing_email']:
                for language in ['english', 'telugu', 'hindi']:
                    with self.subTest(industry=industry['id'], kind=kind, language=language):
                        res = self.client.post('/api/content/generate', headers=headers, json={
                            'industry': industry['id'], 'content_type': kind, 'product': 'QA product',
                            'language': language, 'include_cta': False, 'generate_image': False,
                        })
                        self.assertEqual(res.status_code, 200, res.text)
                        self.assertTrue(res.json()['caption'])
                        self.assertFalse(res.json()['cta'], 'CTA must be omitted when disabled')
                        count += 1
        print(f'Checked {count} industry/format/language combinations')

if __name__ == '__main__':
    unittest.main()
