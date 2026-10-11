from fastapi import APIRouter
from backend.app.services.industry_registry import get_all_industries, get_industry_options

router = APIRouter(prefix="/industries", tags=["industries"])

@router.get("")
async def list_industries():
    return get_all_industries()

@router.get("/{industry}/options")
async def get_options_for_industry(industry: str):
    return get_industry_options(industry)
