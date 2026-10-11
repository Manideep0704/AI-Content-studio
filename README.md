# 🚀 AI Content Studio — Multimodal Marketing SaaS

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB.svg?style=flat&logo=react)](https://vitejs.dev/)
[![Diffusion Models](https://img.shields.io/badge/AI%20Vision-Sana%20%7C%20FLUX%20%7C%20SDXL-FF6F00.svg?style=flat)](https://pollinations.ai)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade, zero-prompt AI content & visual generation SaaS built for small businesses and modern brands. It eliminates the "prompt engineering" barrier by converting structured business inputs directly into high-converting copy across **5 key industries** paired with **authentic DSLR-quality camera photography**.

---

## 📽️ Demo Video Walkthrough

A complete end-to-end interactive recording of the platform in action is included in the repository:
* **[Watch Walkthrough Demo (saas_studio_demo_v2.webp)](./saas_studio_demo_v2.webp)**

---

## 🌟 Key Capabilities

### 1. 🎯 Zero-Prompt Multimodal Generation
* **Business-First Selection:** Users select Industry, Platform (WhatsApp, Instagram, Facebook, Ads, Email), Language, and Product.
* **Deterministic Copy Isolation:**
  * **Clothing & Fashion:** Artisanal handloom weaves, pure silk, gold zari borders, and festive bridal styling.
  * **Restaurants & Dining:** Authentic culinary preparation, hygiene standards, aromas, and festive platter menus.
  * **Electronics & Tech:** Performance metrics, build quality, refresh rates, and manufacturer warranty.
  * **Real Estate:** Prime locations, vastu compliance, lifestyle amenities, and transparent documentation.
  * **Salon & Wellness:** Aesthetic therapies, clinical hygiene, organic formulations, and rejuvenation.

### 2. 📸 True-to-Life Commercial Photography Pipeline
* **Natural Optical Realism:** Explicit prompt engineering suppresses CGI, 3D cartoons, and plastic rendering artifacts, prioritizing Canon DSLR / Sony Alpha natural daylight and depth-of-field.
* **Automated Watermark Trimming:** High-resolution post-processing automatically crops third-party corner watermarks and reapplies Lanczos resampling for pristine output.
* **Resilient Multi-Model Chain:** Hierarchical provider fallback (`sana` ➔ `flux` ➔ `turbo` ➔ `local canvas generator`) ensures 99.9% demo uptime without breaking on rate limits.

### 3. 🌐 Multilingual & Regional Fluency
* Native script generation across **Telugu (తెలుగు)**, **Hindi (हिन्दी)**, and **English**.
* Culture-specific hooks, respectful salutations, and region-tailored calls to action.

### 4. 🧠 Brand Memory & Campaign History
* Stores brand logos, custom color tokens, physical locations, phone numbers, and default CTAs.
* SQLite persistent campaign archive with instant clipboard copying and high-resolution JPEG downloads.

---

## ⚡ Quick Start (Windows / One-Click)

### Prerequisites
* **Python 3.11+**
* **Node.js 18+** with `npm`

### Launch the Application
Simply run from PowerShell in the project directory:

```powershell
.\start.ps1
```

Or double-click `start.bat`.

The launcher automatically:
1. Verifies/creates the Python virtual environment (`.venv`)
2. Installs backend dependencies from `backend/requirements.lock.txt`
3. Builds the React/Vite frontend into static assets
4. Resolves any port conflicts on `8000`
5. Launches the unified Uvicorn server on **`http://127.0.0.1:8000`** and opens your default browser!

---

## 🏗️ Architecture

```
AI-Content-studio/
├── image-ai/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── api/             # REST endpoints (auth, content, business, image)
│   │   │   ├── core/            # App configuration & security settings
│   │   │   ├── db/              # SQLAlchemy models & SQLite session
│   │   │   ├── schemas/         # Pydantic validation schemas
│   │   │   └── services/        # AI Gateway, ContentEngine, ImageEngine, QualityChecker
│   │   └── static/              # High-resolution generated images
│   ├── frontend/
│   │   ├── src/                 # React components (CreateWizard, StudioCopilot, ResultView)
│   │   └── package.json
│   ├── start.ps1                # Subfolder launcher
│   └── verify_system.py         # 6-tier automated subsystem verification test
├── saas_studio_demo_v2.webp     # High-definition animated walkthrough
├── start.ps1                    # Root launcher
├── start.bat                    # One-click Windows batch runner
└── README.md
```

---

## 🧪 Verification & Test Suite

The platform includes an automated regression test matrix validating 105 industry/format/language combinations:

```powershell
cd image-ai
.\.venv\Scripts\python.exe -m backend.test_workflows
```

Run end-to-end subsystem validation:

```powershell
cd image-ai
.\.venv\Scripts\python.exe verify_system.py
```

---

## 📄 License
Released under the [MIT License](LICENSE).
