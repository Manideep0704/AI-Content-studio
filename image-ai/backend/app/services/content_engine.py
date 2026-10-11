import json
import logging
from typing import Dict, Any, Optional
from backend.app.services.prompt_engine import PromptEngine
from backend.app.services.ai_gateway import AIGateway
from backend.app.services.quality_checker import QualityChecker
from backend.app.services.image_engine import ImageEngine
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class ContentEngine:
    @staticmethod
    async def generate_content(
        payload: Dict[str, Any],
        brand_profile: Optional[Dict[str, Any]] = None,
        custom_api_key: Optional[str] = None,
        max_attempts: int = 2
    ) -> Dict[str, Any]:
        """
        Orchestrates full generation:
        1. Synthesizes AI instruction via PromptEngine (zero prompt needed from user)
        2. Dispatches to AIGateway
        3. Validates via QualityChecker
        4. Re-attempts with corrected feedback if quality check fails
        5. Optionally triggers ImageEngine if requested
        """
        ai_provider = AIGateway.get_provider(custom_api_key)
        instructions = PromptEngine.build_generation_instruction(payload, brand_profile)
        
        system_instruction = instructions["system_instruction"]
        user_prompt = instructions["user_prompt"]
        
        last_result = {}
        last_report = {}
        is_approved = False
        quality_score = 0.0
        
        for attempt in range(max_attempts):
            try:
                # Call AI provider
                result = await ai_provider.generate_structured_content(system_instruction, user_prompt)
                if not payload.get("include_cta", True):
                    result["cta"] = ""
                
                # Check Quality
                is_valid, score, issues, report = QualityChecker.validate_content(result, payload, brand_profile)
                last_result = result
                last_report = report
                quality_score = score
                
                if is_valid:
                    is_approved = True
                    break
                else:
                    logger.warning(f"Generation attempt {attempt + 1} failed quality check: {issues}. Retrying...")
                    # Augment user prompt with strict correction feedback for next loop
                    user_prompt += f"\n\nSTRICT QUALITY CORRECTION (ATTEMPT {attempt + 2}):\nPlease fix the following issues immediately: {'; '.join(issues)}."
            except Exception as e:
                logger.error(f"Generation error on attempt {attempt + 1}: {e}")
                # If error, try mock provider as emergency fallback
                from backend.app.services.ai_gateway import MockAIProvider
                emergency_provider = MockAIProvider()
                result = await emergency_provider.generate_structured_content(system_instruction, user_prompt)
                if not payload.get("include_cta", True):
                    result["cta"] = ""
                is_valid, score, issues, report = QualityChecker.validate_content(result, payload, brand_profile)
                last_result = result
                last_report = report
                quality_score = score
                is_approved = True
                break

        # Generate optional image if requested in payload
        image_url = None
        image_meta = {}
        if payload.get("generate_image", False):
            suggested_prompt = last_result.get("suggested_image_prompt") or f"Premium commercial photo of {payload.get('product')}"
            try:
                img_res = await ImageEngine.generate(
                prompt=suggested_prompt,
                context={
                    "industry": payload.get("industry", "restaurant"),
                    "product": payload.get("product", ""),
                    "offer": payload.get("offer", ""),
                    "business_name": brand_profile.get("business_name") if brand_profile else ""
                },
                custom_api_key=custom_api_key
                )
            except (RuntimeError, ValueError):
                raise HTTPException(status_code=503, detail="Image providers are unavailable. Configure image credentials in backend/.env or generate without an image.")
            image_url = img_res.get("image_url")
            image_meta = img_res

        return {
            "hook": last_result.get("hook", ""),
            "caption": last_result.get("caption", ""),
            "cta": last_result.get("cta", ""),
            "hashtags": last_result.get("hashtags", []),
            "suggested_image_prompt": last_result.get("suggested_image_prompt", ""),
            "image_url": image_url,
            "image_meta": image_meta,
            "quality_score": quality_score,
            "quality_report": last_report,
            "status": "completed"
        }
