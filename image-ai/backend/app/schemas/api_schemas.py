from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Auth Schemas ---
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# --- Business / Brand Schemas ---
class BusinessProfileBase(BaseModel):
    business_name: str = ""
    industry: str = "restaurant"
    description: Optional[str] = ""
    location: Optional[str] = ""
    phone: Optional[str] = ""
    website: Optional[str] = ""
    logo_url: Optional[str] = ""
    brand_colors: Optional[str] = "#4F46E5, #06B6D4"
    preferred_language: Optional[str] = "english"
    preferred_tone: Optional[str] = "premium"
    default_cta: Optional[str] = "Order Now or Visit Us Today!"

class BusinessProfileCreate(BusinessProfileBase):
    pass

class BusinessProfileUpdate(BusinessProfileBase):
    pass

class BusinessProfileResponse(BusinessProfileBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Content Generation Schemas ---
class GenerationRequest(BaseModel):
    industry: str = "restaurant"
    content_type: str = "instagram_post"
    product: str = Field(min_length=1, max_length=500)
    objective: Optional[str] = "promotion"
    offer: Optional[str] = ""
    tone: Optional[str] = "premium"
    language: Optional[str] = "telugu"
    platform: Optional[str] = "instagram"
    length: Optional[str] = "medium"
    include_cta: Optional[bool] = True
    generate_image: Optional[bool] = False
    
    # Optional extra industry parameters (e.g. occasion, dietary, bedrooms, category, etc.)
    extra_fields: Optional[Dict[str, Any]] = None
    custom_api_key: Optional[str] = None

class RegenerationRequest(BaseModel):
    content_id: str
    tweak_instruction: Optional[str] = None
    tone: Optional[str] = None
    language: Optional[str] = None
    offer: Optional[str] = None
    custom_api_key: Optional[str] = None

class ContentUpdate(BaseModel):
    caption: Optional[str] = None
    cta: Optional[str] = None
    hashtags: Optional[List[str]] = None
    image_url: Optional[str] = None
    is_saved: Optional[bool] = None

class GenerationResponse(BaseModel):
    id: str
    caption: str
    cta: Optional[str] = None
    hashtags: List[str] = []
    image_url: Optional[str] = None
    status: str = "completed"
    quality_score: Optional[float] = 1.0
    quality_report: Optional[Dict[str, Any]] = None
    industry: Optional[str] = None
    content_type: Optional[str] = None
    product_or_subject: Optional[str] = None
    language: Optional[str] = None
    tone: Optional[str] = None
    created_at: Optional[datetime] = None

class ImageGenerateRequest(BaseModel):
    prompt: Optional[str] = None
    content_id: Optional[str] = None
    industry: Optional[str] = "restaurant"
    product: Optional[str] = ""
    offer: Optional[str] = ""
    business_name: Optional[str] = ""
    custom_api_key: Optional[str] = None

class ImageGenerateResponse(BaseModel):
    image_url: str
    provider: str
    status: str
    prompt: Optional[str] = None

class AgentPromptRequest(BaseModel):
    user_input: str = Field(min_length=1, max_length=2000)
    custom_api_key: Optional[str] = None

class AgentPromptResponse(BaseModel):
    product: Optional[str] = None
    industry: Optional[str] = None
    offer: Optional[str] = None
    suggested_prompt: Optional[str] = None
