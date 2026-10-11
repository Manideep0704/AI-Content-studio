import httpx, urllib.parse

prompt = 'Ultra-realistic 8K photo of dum biryani'
encoded = urllib.parse.quote(prompt)

for model in ['flux', 'flux-realism', 'flux-pro', 'turbo', 'stable-diffusion']:
    url = f'https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024&nologo=true&model={model}'
    try:
        r = httpx.get(url, timeout=30, follow_redirects=True)
        ct = r.headers.get('content-type', '?')
        print(f"Model {model}: status={r.status_code} size={len(r.content)} type={ct}")
    except Exception as e:
        print(f"Model {model}: ERROR {e}")
