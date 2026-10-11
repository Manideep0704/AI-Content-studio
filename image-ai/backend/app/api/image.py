from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.db.session import get_db
from backend.app.db.models import User, BusinessProfile, GeneratedContent
from backend.app.api.deps import get_current_user
from backend.app.services.image_engine import ImageEngine
from backend.app.schemas.api_schemas import ImageGenerateRequest, ImageGenerateResponse
from backend.app.db.models import UsageLog
import json

async def run_image_generation(**kwargs):
    try:
        return await ImageEngine.generate(**kwargs)
    except (RuntimeError, ValueError):
        raise HTTPException(status_code=503, detail="Image providers are unavailable. Configure HF_API_KEY or Cloudflare credentials in backend/.env, then retry.")

router = APIRouter(prefix="/image", tags=["image"])

@router.post("/generate", response_model=ImageGenerateResponse)
async def generate_image(
    payload: ImageGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    business_name = payload.business_name
    content_item = None
    if payload.content_id:
        res = await db.execute(select(GeneratedContent).where(GeneratedContent.id == payload.content_id, GeneratedContent.user_id == current_user.id))
        content_item = res.scalars().first()
        if content_item is None:
            raise HTTPException(status_code=404, detail="Content not found")
    if not business_name:
        res = await db.execute(select(BusinessProfile).where(BusinessProfile.user_id == current_user.id))
        prof = res.scalars().first()
        if prof and prof.business_name:
            business_name = prof.business_name

    prompt = payload.prompt or f"Ultra realistic high-end marketing photo of {payload.product or 'special item'}, {payload.industry} theme, 8k resolution"
    
    result = await run_image_generation(
        prompt=prompt,
        context={
            "industry": payload.industry,
            "product": payload.product,
            "offer": payload.offer,
            "business_name": business_name
        },
        custom_api_key=payload.custom_api_key
    )

    if content_item:
        content_item.image_url = result.get("image_url")
    else:
        db.add(GeneratedContent(
            user_id=current_user.id, industry=payload.industry or "general",
            content_type="image", platform="instagram", language="english", tone="premium",
            product_or_subject=payload.product or "Generated image", caption=prompt,
            image_url=result.get("image_url"), hashtags_json="[]", quality_report_json="{}",
            raw_inputs_json=json.dumps({"industry": payload.industry, "product": payload.product or prompt, "generate_image": False}),
            status="completed"
        ))
    db.add(UsageLog(user_id=current_user.id, action="generate_image", meta_json="{}"))
    await db.commit()

    return {
        "image_url": result.get("image_url", ""),
        "provider": result.get("provider", "banner_engine"),
        "status": result.get("status", "success"),
        "prompt": prompt
    }
