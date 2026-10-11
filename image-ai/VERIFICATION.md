# Verification results — 10 October 2026

## Passed

- Production frontend build.
- Isolated Python environment: `pip check` reports no broken requirements.
- Four backend regression tests, including 105 combinations across five industries, seven formats, and three languages.
- Registration, login, authorization, cross-account access denial, profile updates, content creation, editing, regeneration, history, deletion, and usage accounting.
- CTA disabled behavior, image provider outages, invalid image bytes, and API-key exclusion from stored inputs.
- Browser workflows: registration, text campaign wizard, edit/save, text file download, brand profile save, mobile menu, and login persistence across a server restart.
- Live Pollinations image generation: HTTP 200 in approximately 5 seconds for a generic ceramic mug prompt; image opened from history.
- Complete browser image-agent workflow and image file download.

## Fixed during verification

- Mobile header and main content incorrectly shared a horizontal flex row.
- Disabled CTA option was ignored by the local content provider.
- Search was applied after limiting history, causing older matches to be missed.
- Nested extra fields could retain a custom API key in stored inputs.
- Missing SQLAlchemy async dependency in a clean environment.
- Isolated dependencies and added a reproducible requirements lock file.

## Verification limits

Gemini, Groq, Hugging Face, and Cloudflare live calls were not tested because their server credentials are absent. Local text/prompt fallback and Pollinations were tested. A successful Pollinations call does not guarantee future availability. The format/language matrix validates API output and the CTA setting; it does not establish editorial quality or AI accuracy.

The browser check used a local QA account (`qa-check-20261010@example.com`) and left its test campaigns and images available for review. Public deployment, billing, and password reset are not implemented. Static generated image URLs remain accessible to anyone who knows the URL.

## Repeat

```powershell
.\.venv\Scripts\python.exe -m unittest backend.test_workflows -v
.\.venv\Scripts\python.exe -m pip check
cd frontend
npm run build
```
