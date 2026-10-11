import React, { useState } from 'react';
import { Settings, Key, BarChart3, Save, Check } from 'lucide-react';

export default function SettingsView({ usage }) {
  const [apiKey, setApiKey] = useState(localStorage.getItem('user_gemini_key') || '');
  const [saved, setSaved] = useState(false);

  const handleSaveKey = (e) => {
    e.preventDefault();
    localStorage.setItem('user_gemini_key', apiKey.trim());
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div style={{ maxWidth: '780px', margin: '0 auto' }}>
      <div style={{ marginBottom: '1.75rem' }}>
        <h2 className="editorial-heading" style={{ fontSize: '1.75rem' }}>
          Settings
        </h2>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', marginTop: '2px' }}>
          Manage your account preferences and credentials.
        </p>
      </div>

      {saved && (
        <div style={{
          background: 'var(--accent-sage-soft)',
          border: '1px solid rgba(120, 146, 122, 0.3)',
          borderRadius: 'var(--radius-sm)',
          padding: '0.75rem 1rem',
          color: 'var(--color-success)',
          marginBottom: '1.25rem',
          fontSize: '0.85rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem'
        }}>
          <Check size={16} />
          <span>Settings saved successfully!</span>
        </div>
      )}

      {/* API Key Card */}
      <div className="card" style={{ padding: '2rem', marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
          <Key size={18} color="var(--accent-terracotta)" />
          <h3 style={{ fontSize: '1.1rem', fontWeight: '600' }}>Custom Gemini API Key (Optional)</h3>
        </div>

        <form onSubmit={handleSaveKey}>
          <div className="form-group">
            <label className="form-label">API Key</label>
            <input
              type="password"
              className="form-input"
              placeholder="AIzaSy... (Leave empty to use built-in engine)"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
            />
            <p style={{ color: 'var(--text-dim)', fontSize: '0.75rem', marginTop: '4px' }}>
              Your key is saved locally in your browser.
            </p>
          </div>

          <button
            type="submit"
            className="btn-primary"
            style={{ padding: '0.55rem 1.25rem', fontSize: '0.85rem' }}
          >
            <Save size={14} /> Save
          </button>
        </form>
      </div>

      {/* Usage Card */}
      <div className="card" style={{ padding: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
          <BarChart3 size={18} color="var(--text-main)" />
          <h3 style={{ fontSize: '1.1rem', fontWeight: '600' }}>Usage</h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
          <div style={{ background: 'var(--bg-soft)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-warm)' }}>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Plan</div>
            <div style={{ fontSize: '1.05rem', fontWeight: '600', color: 'var(--text-main)', marginTop: '2px' }}>
              Unlimited
            </div>
          </div>

          <div style={{ background: 'var(--bg-soft)', padding: '1rem', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-warm)' }}>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Created Posts</div>
            <div style={{ fontSize: '1.05rem', fontWeight: '600', color: 'var(--text-main)', marginTop: '2px' }}>
              {usage ? usage.total_generations : 0}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
