import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc, or_
from backend.app.db.session import get_db
from backend.app.db.models import User, BusinessProfile, GeneratedContent, UsageLog
from backend.app.api.deps import get_current_user
from backend.app.services.content_engine import ContentEngine
from backend.app.schemas.api_schemas import (
    GenerationRequest,
    GenerationResponse,
    RegenerationRequest,
    ContentUpdate,
    AgentPromptRequest,
    AgentPromptResponse
)
from backend.app.services.prompt_agent import PromptAgent

router = APIRouter(prefix="/content", tags=["content"])

@router.post("/agent-prompt", response_model=AgentPromptResponse)
async def generate_agent_prompt(
    payload: AgentPromptRequest,
    current_user: User = Depends(get_current_user)
):
    agent = PromptAgent(api_key=payload.custom_api_key)
    result = await agent.analyze_and_generate_prompt(payload.user_input)
    return result

@router.post("/generate", response_model=GenerationResponse)
async def generate_content(
    payload: GenerationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Retrieve user's brand profile to inject brand memory
    res = await db.execute(select(BusinessProfile).where(BusinessProfile.user_id == current_user.id))
    brand_profile_obj = res.scalars().first()
    brand_profile = None
    if brand_profile_obj:
        brand_profile = {
            "business_name": brand_profile_obj.business_name,
            "industry": brand_profile_obj.industry,
            "description": brand_profile_obj.description,
            "location": brand_profile_obj.location,
            "phone": brand_profile_obj.phone,
            "website": brand_profile_obj.website,
            "brand_colors": brand_profile_obj.brand_colors,
            "preferred_language": brand_profile_obj.preferred_language,
            "preferred_tone": brand_profile_obj.preferred_tone,
            "default_cta": brand_profile_obj.default_cta
        }

    # Flatten payload parameters including extra fields
    generation_dict = payload.model_dump(exclude={"custom_api_key", "extra_fields"})
    if payload.extra_fields:
        generation_dict.update({k: v for k, v in payload.extra_fields.items() if k not in generation_dict and k != "custom_api_key"})

    # Generate content through engine
    result = await ContentEngine.generate_content(
        payload=generation_dict,
        brand_profile=brand_profile,
        custom_api_key=payload.custom_api_key
    )

    # Store in database for History & Reusability
    content_record = GeneratedContent(
        user_id=current_user.id,
        industry=payload.industry,
        content_type=payload.content_type,
        platform=payload.platform or "instagram",
        language=payload.language or "english",
        tone=payload.tone or "premium",
        product_or_subject=payload.product,
        objective=payload.objective,
        offer=payload.offer,
        raw_inputs_json=json.dumps(generation_dict),
        caption=result.get("caption", ""),
        cta=result.get("cta", ""),
        hashtags_json=json.dumps(result.get("hashtags", [])),
        image_url=result.get("image_url"),
        quality_score=result.get("quality_score", 1.0),
        quality_report_json=json.dumps(result.get("quality_report", {})),
        status="completed"
    )
    db.add(content_record)

    # Usage Log
    log = UsageLog(
        user_id=current_user.id,
        action="generate_content",
        meta_json=json.dumps({
            "industry": payload.industry,
            "content_type": payload.content_type,
            "language": payload.language,
            "quality_score": result.get("quality_score", 1.0)
        })
    )
    db.add(log)

    await db.commit()
    await db.refresh(content_record)

    return {
        "id": content_record.id,
        "caption": content_record.caption,
        "cta": content_record.cta,
        "hashtags": json.loads(content_record.hashtags_json),
        "image_url": content_record.image_url,
        "status": content_record.status,
        "quality_score": content_record.quality_score,
        "quality_report": json.loads(content_record.quality_report_json),
        "industry": content_record.industry,
        "content_type": content_record.content_type,
        "product_or_subject": content_record.product_or_subject,
        "language": content_record.language,
        "tone": content_record.tone,
        "created_at": content_record.created_at
    }

@router.post("/regenerate", response_model=GenerationResponse)
async def regenerate_content(
    payload: RegenerationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(GeneratedContent).where(
            GeneratedContent.id == payload.content_id,
            GeneratedContent.user_id == current_user.id
        )
    )
    record = result.scalars().first()
    if not record:
        raise HTTPException(status_code=404, detail="Content record not found")

    raw_inputs = json.loads(record.raw_inputs_json)
    raw_inputs.pop("custom_api_key", None)
    if isinstance(raw_inputs.get("extra_fields"), dict):
        raw_inputs["extra_fields"].pop("custom_api_key", None)
    if payload.tone:
        raw_inputs["tone"] = payload.tone
    if payload.language:
        raw_inputs["language"] = payload.language
    if payload.offer is not None:
        raw_inputs["offer"] = payload.offer
    if payload.tweak_instruction:
        raw_inputs["tweak_instruction"] = payload.tweak_instruction

    # Retrieve brand profile
    res = await db.execute(select(BusinessProfile).where(BusinessProfile.user_id == current_user.id))
    brand_profile_obj = res.scalars().first()
    brand_profile = None
    if brand_profile_obj:
        brand_profile = {
            "business_name": brand_profile_obj.business_name,
            "industry": brand_profile_obj.industry,
            "description": brand_profile_obj.description,
            "location": brand_profile_obj.location,
            "phone": brand_profile_obj.phone,
            "website": brand_profile_obj.website,
            "brand_colors": brand_profile_obj.brand_colors,
            "preferred_language": brand_profile_obj.preferred_language,
            "preferred_tone": brand_profile_obj.preferred_tone,
            "default_cta": brand_profile_obj.default_cta
        }

    # Re-generate with updated inputs
    new_result = await ContentEngine.generate_content(
        payload=raw_inputs,
        brand_profile=brand_profile,
        custom_api_key=payload.custom_api_key
    )

    record.caption = new_result.get("caption", record.caption)
    record.cta = new_result.get("cta", record.cta)
    record.hashtags_json = json.dumps(new_result.get("hashtags", []))
    record.quality_score = new_result.get("quality_score", record.quality_score)
    record.quality_report_json = json.dumps(new_result.get("quality_report", {}))
    record.tone = raw_inputs.get("tone", record.tone)
    record.language = raw_inputs.get("language", record.language)
    record.offer = raw_inputs.get("offer", record.offer)
    record.raw_inputs_json = json.dumps(raw_inputs)

    # Usage Log
    log = UsageLog(
        user_id=current_user.id,
        action="regenerate_content",
        meta_json=json.dumps({"content_id": record.id})
    )
    db.add(log)

    await db.commit()
    await db.refresh(record)

    return {
        "id": record.id,
        "caption": record.caption,
        "cta": record.cta,
        "hashtags": json.loads(record.hashtags_json),
        "image_url": record.image_url,
        "status": record.status,
        "quality_score": record.quality_score,
        "quality_report": json.loads(record.quality_report_json),
        "industry": record.industry,
        "content_type": record.content_type,
        "product_or_subject": record.product_or_subject,
        "language": record.language,
        "tone": record.tone,
        "created_at": record.created_at
    }

@router.get("/history", response_model=List[GenerationResponse])
async def get_history(
    industry: Optional[str] = None,
    platform: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(GeneratedContent).where(GeneratedContent.user_id == current_user.id)
    if industry and industry != "all":
        query = query.where(GeneratedContent.industry == industry)
    if platform and platform != "all":
        query = query.where(GeneratedContent.platform == platform)
    if search:
        query = query.where(or_(
            GeneratedContent.product_or_subject.ilike(f"%{search}%"),
            GeneratedContent.caption.ilike(f"%{search}%")
        ))
    
    query = query.order_by(desc(GeneratedContent.created_at)).limit(limit)
    res = await db.execute(query)
    records = res.scalars().all()

    items = []
    for r in records:
        if search and search.lower() not in (r.product_or_subject or "").lower() and search.lower() not in r.caption.lower():
            continue
        items.append({
            "id": r.id,
            "caption": r.caption,
            "cta": r.cta,
            "hashtags": json.loads(r.hashtags_json) if r.hashtags_json else [],
            "image_url": r.image_url,
            "status": r.status,
            "quality_score": r.quality_score,
            "quality_report": json.loads(r.quality_report_json) if r.quality_report_json else {},
            "industry": r.industry,
            "content_type": r.content_type,
            "product_or_subject": r.product_or_subject,
            "language": r.language,
            "tone": r.tone,
            "created_at": r.created_at
        })
    return items

@router.get("/{content_id}", response_model=GenerationResponse)
async def get_content_by_id(
    content_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    res = await db.execute(
        select(GeneratedContent).where(
            GeneratedContent.id == content_id,
            GeneratedContent.user_id == current_user.id
        )
    )
    r = res.scalars().first()
    if not r:
        raise HTTPException(status_code=404, detail="Content not found")

    return {
        "id": r.id,
        "caption": r.caption,
        "cta": r.cta,
        "hashtags": json.loads(r.hashtags_json) if r.hashtags_json else [],
        "image_url": r.image_url,
        "status": r.status,
        "quality_score": r.quality_score,
        "quality_report": json.loads(r.quality_report_json) if r.quality_report_json else {},
        "industry": r.industry,
        "content_type": r.content_type,
        "product_or_subject": r.product_or_subject,
        "language": r.language,
        "tone": r.tone,
        "created_at": r.created_at
    }

@router.put("/{content_id}", response_model=GenerationResponse)
async def update_content(
    content_id: str,
    payload: ContentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    res = await db.execute(
        select(GeneratedContent).where(
            GeneratedContent.id == content_id,
            GeneratedContent.user_id == current_user.id
        )
    )
    r = res.scalars().first()
    if not r:
        raise HTTPException(status_code=404, detail="Content not found")

    if payload.caption is not None:
        r.caption = payload.caption
    if payload.cta is not None:
        r.cta = payload.cta
    if payload.hashtags is not None:
        r.hashtags_json = json.dumps(payload.hashtags)
    if payload.image_url is not None:
        r.image_url = payload.image_url
    if payload.is_saved is not None:
        r.is_saved = payload.is_saved

    await db.commit()
    await db.refresh(r)

    return {
        "id": r.id,
        "caption": r.caption,
       "cta": r.cta,
        "hashtags": json.loads(r.hashtags_json) if r.hashtags_json else [],
        "image_url": r.image_url,
        "status": r.status,
        "quality_score": r.quality_score,
        "quality_report": json.loads(r.quality_report_json) if r.quality_report_json else {},
        "industry": r.industry,
        "content_type": r.content_type,
        "product_or_subject": r.product_or_subject,
        "language": r.language,
        "tone": r.tone,
        "created_at": r.created_at
    }

@router.delete("/{content_id}")
async def delete_content(
    content_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    res = await db.execute(
        select(GeneratedContent).where(
            GeneratedContent.id == content_id,
            GeneratedContent.user_id == current_user.id
        )
    )
    r = res.scalars().first()
    if not r:
        raise HTTPException(status_code=404, detail="Content not found")

    await db.delete(r)
    await db.commit()
    return {"message": "Content successfully deleted", "id": content_id}
