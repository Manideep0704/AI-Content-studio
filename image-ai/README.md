# Content Studio

React and FastAPI application for marketing content, brand profiles, and image generation.

## Run on Windows

Requires Python 3.11+ and Node.js 18+ with npm.

From this folder, run:

```powershell
.\start.ps1
```

Open http://127.0.0.1:8000. Create an account using Sign In → Register. The launcher installs the tested dependencies from `backend/requirements.lock.txt`, creates a local signing secret, builds the frontend, and starts the server. Press Ctrl+C to stop.

## AI configuration

Edit `backend/.env` using `backend/.env.example` as a reference. Keep the generated SECRET_KEY stable so logins survive restarts.

- GEMINI_API_KEY enables AI content generation. Without it, content uses the existing local template engine; this is sample content and should be reviewed.
- GROQ_API_KEY enables AI prompt analysis. Without it, the agent uses the local keyword and prompt library.
- HF_API_KEY or CLOUDFLARE_API_TOKEN plus CLOUDFLARE_ACCOUNT_ID enables authenticated image generation. An external Pollinations fallback is attempted, but its availability is not guaranteed.
- The Gemini key in Settings applies only to content generation. Image and Groq credentials stay on the server.

The credential previously embedded in the archive has been removed from source. Revoke that old Hugging Face token in its provider account.

## Development and verification

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload
```

In a second terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Frontend: http://localhost:5173. API documentation: http://127.0.0.1:8000/docs.

```powershell
.\.venv\Scripts\python.exe -m unittest backend.test_workflows -v
cd frontend
npm run build
```

The regression suite uses a temporary database and mocked image providers. It covers account access, content CRUD, profile updates, regeneration, usage, invalid image rejection, provider outages, and 105 industry/format/language combinations. Live Pollinations output and downloads were verified. Other providers require your own credentials and remain unverified. See `VERIFICATION.md` for results and limits.

## Delivery notes

Restored dashboard, content wizard, and history navigation. Agent images are saved to history and downloadable. Fixed anonymous shared-account access, unsafe chat HTML rendering, provider credential routing, secret storage in generation inputs, missing dependencies, image response validation, provider timeouts, and database paths. Added a single-server launcher and frontend hosting.

This is a local application. Public hosting, billing, quotas, password reset, private image delivery, and production infrastructure are outside this completed local workflow. Generated static image URLs are accessible to anyone who has their URL; do not use this deployment for sensitive images.
