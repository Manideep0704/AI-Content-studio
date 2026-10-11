import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean, Integer, Float
from sqlalchemy.orm import relationship
from backend.app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    business_profile = relationship("BusinessProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    generated_contents = relationship("GeneratedContent", back_populates="user", cascade="all, delete-orphan")
    usage_logs = relationship("UsageLog", back_populates="user", cascade="all, delete-orphan")

class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), unique=True, nullable=False)
    
    business_name = Column(String(255), nullable=False, default="")
    industry = Column(String(100), nullable=False, default="restaurant")
    description = Column(Text, nullable=True, default="")
    location = Column(String(255), nullable=True, default="")
    phone = Column(String(50), nullable=True, default="")
    website = Column(String(255), nullable=True, default="")
    logo_url = Column(Text, nullable=True, default="")
    brand_colors = Column(String(255), nullable=True, default="#4F46E5, #06B6D4")
    preferred_language = Column(String(50), nullable=True, default="english")
    preferred_tone = Column(String(50), nullable=True, default="premium")
    default_cta = Column(String(255), nullable=True, default="Order Now or Visit Us Today!")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="business_profile")

class GeneratedContent(Base):
    __tablename__ = "generated_contents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    
    industry = Column(String(100), nullable=False)
    content_type = Column(String(100), nullable=False)
    platform = Column(String(100), nullable=False)
    language = Column(String(50), nullable=False)
    tone = Column(String(50), nullable=False)
    
    product_or_subject = Column(String(255), nullable=True)
    objective = Column(String(100), nullable=True)
    offer = Column(String(255), nullable=True)
    
    # Store complete input payload as JSON string
    raw_inputs_json = Column(Text, nullable=False, default="{}")
    
    # Generated outputs
    caption = Column(Text, nullable=False)
    cta = Column(Text, nullable=True)
    hashtags_json = Column(Text, nullable=False, default="[]")
    image_url = Column(Text, nullable=True)
    
    # Quality score and diagnostics
    quality_score = Column(Float, default=1.0)
    quality_report_json = Column(Text, default="{}")
    
    is_saved = Column(Boolean, default=True)
    status = Column(String(50), default="completed")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="generated_contents")

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    action = Column(String(100), nullable=False)
    meta_json = Column(Text, default="{}")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="usage_logs")
