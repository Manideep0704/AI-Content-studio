import re
from typing import Dict, Any, List, Tuple

class QualityChecker:
    @staticmethod
    def validate_content(
        content_data: Dict[str, Any],
        request_payload: Dict[str, Any],
        brand_profile: Dict[str, Any] = None
    ) -> Tuple[bool, float, List[str], Dict[str, Any]]:
        issues: List[str] = []
        score_deductions = 0.0
        checks: Dict[str, Any] = {}
        
        caption = content_data.get("caption", "")
        cta = content_data.get("cta", "")
        hashtags = content_data.get("hashtags", [])
        hook = content_data.get("hook", "")
        full_text = f"{hook} {caption} {cta}"
        
        # 1. Structure Check
        has_structure = bool(caption and len(caption.strip()) > 20 and isinstance(hashtags, list) and len(hashtags) >= 2)
        checks["structure_valid"] = has_structure
        if not has_structure:
            issues.append("Generated content does not have sufficient structure or hashtags.")
            score_deductions += 0.3
            
        # 2. Product Name Check
        product = request_payload.get("product", "")
        if product:
            product_words = [w.lower() for w in re.findall(r'\w+', product) if len(w) > 2]
            # If in non-English script, check either English product word or general content relevance
            lang = request_payload.get("language", "english").lower()
            if lang == "english":
                matched = any(w in full_text.lower() for w in product_words)
            else:
                # In Telugu or Hindi, either the script or the product transliteration or original word should match
                matched = any(w in full_text.lower() for w in product_words) or len(caption) > 30
            
            checks["product_present"] = matched
            if not matched:
                issues.append(f"Product '{product}' was not prominently featured in generated text.")
                score_deductions += 0.2
        else:
            checks["product_present"] = True

        # 3. Offer Check
        offer = request_payload.get("offer", "")
        if offer and offer.strip() and "no special" not in offer.lower():
            # Check offer keywords (numbers, discounts, words)
            offer_tokens = [t for t in re.findall(r'\d+%|\d+|[A-Za-z]+', offer) if len(t) > 1]
            offer_matched = any(token.lower() in full_text.lower() for token in offer_tokens) or "%" in full_text or "off" in full_text.lower() or "ఆఫర్" in full_text or "छूट" in full_text or "ऑफर" in full_text
            checks["offer_present"] = offer_matched
            if not offer_matched:
                issues.append(f"Offer '{offer}' was not found in the generated text.")
                score_deductions += 0.15
        else:
            checks["offer_present"] = True

        # 4. Language Fidelity Check
        language = request_payload.get("language", "english").lower()
        if language == "telugu":
            # Telugu unicode range: \u0C00-\u0C7F
            telugu_chars = len(re.findall(r'[\u0C00-\u0C7F]', full_text))
            is_telugu_script = telugu_chars >= 15
            checks["language_fidelity"] = is_telugu_script
            if not is_telugu_script:
                issues.append("Language was requested as Telugu, but response lacks Telugu script characters.")
                score_deductions += 0.4
        elif language == "hindi":
            # Devanagari unicode range: \u0900-\u097F
            hindi_chars = len(re.findall(r'[\u0900-\u097F]', full_text))
            is_hindi_script = hindi_chars >= 15
            checks["language_fidelity"] = is_hindi_script
            if not is_hindi_script:
                issues.append("Language was requested as Hindi, but response lacks Devanagari script characters.")
                score_deductions += 0.4
        else:
            checks["language_fidelity"] = True

        # 5. CTA Check
        include_cta = request_payload.get("include_cta", True)
        if include_cta:
            has_cta = bool(cta and len(cta.strip()) > 3)
            checks["cta_present"] = has_cta
            if not has_cta:
                issues.append("CTA was requested, but generated CTA is empty.")
                score_deductions += 0.15
        else:
            checks["cta_present"] = True

        # 6. Platform Suitability
        platform = request_payload.get("platform", "instagram").lower()
        if platform == "instagram":
            checks["platform_suitability"] = bool(len(hashtags) >= 3 and len(caption) < 2200)
        elif platform == "whatsapp":
            checks["platform_suitability"] = bool("*" in caption or "\n" in caption or len(caption) < 1000)
        else:
            checks["platform_suitability"] = True

        # Calculate final score
        final_score = max(0.0, round(1.0 - score_deductions, 2))
        is_valid = final_score >= 0.70 and (checks.get("language_fidelity", True))

        report = {
            "checks": checks,
            "score": final_score,
            "issues": issues,
            "is_approved": is_valid
        }
        
        return is_valid, final_score, issues, report
