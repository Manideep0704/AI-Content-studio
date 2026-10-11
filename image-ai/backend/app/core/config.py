import os
from pathlib import Path
import secrets
from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "No-Prompt AI Content SaaS"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(48))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"
    
    # Database: Supports SQLite by default or PostgreSQL via DATABASE_URL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///" + str(Path(__file__).resolve().parents[3] / "saas_platform.db").replace("\\", "/"))
    
    # Gemini API
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY", ""))
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    # Groq API (for prompt generation)
    GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # Cloudflare Workers AI
    CLOUDFLARE_API_TOKEN: Optional[str] = os.getenv("CLOUDFLARE_API_TOKEN", "")
    CLOUDFLARE_ACCOUNT_ID: Optional[str] = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
    CLOUDFLARE_IMAGE_MODEL: str = os.getenv("CLOUDFLARE_IMAGE_MODEL", "@cf/stabilityai/stable-diffusion-xl-base-1.0")
    
    # Hugging Face API
    HF_API_KEY: Optional[str] = os.getenv("HF_API_KEY", "")
    HF_IMAGE_MODEL: str = os.getenv("HF_IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell")

    
    # Storage for generated images
    STATIC_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    class Config:
        case_sensitive = True
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")

settings = Settings()
os.makedirs(settings.STATIC_DIR, exist_ok=True)
os.makedirs(os.path.join(settings.STATIC_DIR, "generated_images"), exist_ok=True)
