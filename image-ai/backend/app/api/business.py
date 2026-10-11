from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.app.db.session import get_db
from backend.app.db.models import User, BusinessProfile
from backend.app.api.deps import get_current_user
from backend.app.schemas.api_schemas import BusinessProfileCreate, BusinessProfileUpdate, BusinessProfileResponse

router = APIRouter(prefix="/business", tags=["business"])

@router.get("", response_model=BusinessProfileResponse)
async def get_business_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(BusinessProfile).where(BusinessProfile.user_id == current_user.id))
    profile = result.scalars().first()
    if not profile:
        profile = BusinessProfile(
            user_id=current_user.id,
            business_name=f"{current_user.full_name or 'My'}'s Brand",
            industry="restaurant"
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    return profile

@router.post("", response_model=BusinessProfileResponse)
async def create_or_update_business_profile(
    profile_in: BusinessProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(BusinessProfile).where(BusinessProfile.user_id == current_user.id))
    profile = result.scalars().first()
    
    if profile:
        for field, value in profile_in.model_dump(exclude_unset=True).items():
            setattr(profile, field, value)
    else:
        profile = BusinessProfile(
            user_id=current_user.id,
            **profile_in.model_dump()
        )
        db.add(profile)
        
    await db.commit()
    await db.refresh(profile)
    return profile

@router.put("", response_model=BusinessProfileResponse)
async def update_business_profile(
    profile_in: BusinessProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await create_or_update_business_profile(profile_in, current_user, db)
