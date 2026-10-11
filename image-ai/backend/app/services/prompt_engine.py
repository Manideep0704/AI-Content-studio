import json
from typing import Dict, Any, Optional

LANGUAGE_INSTRUCTIONS = {
    "telugu": """
CRITICAL LANGUAGE REQUIREMENT:
You MUST write the content completely and fluently in pure, natural TELUGU script (తెలుగు లిపి).
Do NOT write transliterated Telugu (like 'meeru randi'). Write authentic Telugu script (e.g. 'ఈ వారాంతం రుచికరమైన బిర్యానీతో ఆనందించండి!').
Brand names, numbers, percentages (e.g. 20% OFF) and specific product names can be written with their standard recognizable terms or Telugu translation.
The tone and vocabulary must reflect authentic Telugu marketing nuances that appeal deeply to local Telugu customers.
""",
    "hindi": """
CRITICAL LANGUAGE REQUIREMENT:
You MUST write the content completely and fluently in authentic HINDI script (देवनागरी लिपि).
Do NOT write Hinglish/Romanized Hindi. Write authentic Hindi script (e.g. 'स्वादिष्ट और लज़ीज़ बिरयानी पर विशेष छूट का आनंद लें!').
Brand names, numbers, offers (e.g. 20% OFF) can be included naturally.
The phrasing must be warm, culturally resonant, and highly engaging for Hindi-speaking customers.
""",
    "english": """
CRITICAL LANGUAGE REQUIREMENT:
You MUST write the content in polished, native, high-converting ENGLISH.
Ensure compelling hooks, smooth readability, impactful word choice, and zero fluff.
"""
}

PLATFORM_SPECIFIC_GUIDANCE = {
    "instagram_post": "Create an Instagram post caption with a magnetic first-line hook (stopping the scroll), clean line spacing, curated emojis, value-driven body, clear Call To Action, and targeted hashtags.",
    "facebook_post": "Create a Facebook post with storytelling, community warmth, detail on benefits, engagement question, and prominent CTA.",
    "whatsapp_message": "Create a WhatsApp marketing message formatted with bold styling (*text*), bullet points (•), high-urgency hook, direct business details, and a 1-tap actionable CTA.",
    "product_description": "Create an enticing, conversion-optimized product description highlighting key features, emotional customer benefits, specifications, and buying incentive.",
    "ad_copy": "Create high-converting direct-response Advertisement Copy featuring a punchy headline, clear pain/desire trigger, the irresistible offer, social proof angle, and high-urgency CTA button text.",
    "reel_script": "Create a high-energy short-form Reel/Shorts script with 3 columns: [Visual Scene / Camera Direction], [Spoken Audio / Voiceover], and [Text on Screen Overlay].",
    "marketing_email": "Create an email campaign with Subject Line, Preview Header, Engaging Body Text, and a primary CTA Button."
}

TONE_GUIDANCE = {
    "professional": "Authoritative, trustworthy, polished, and crisp.",
    "friendly": "Warm, relatable, conversational, welcoming, and delightful.",
    "premium": "Luxurious, sophisticated, exclusive, elegant, and high-status.",
    "funny": "Witty, humorous, playful, self-aware, and smile-inducing.",
    "energetic": "High-octane, urgent, hype-filled, exclamation-driven, FOMO-inducing.",
    "minimal": "Concise, punchy, elegant, modern, no-fluff."
}

class PromptEngine:
    @staticmethod
    def build_generation_instruction(payload: Dict[str, Any], brand_profile: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        industry = payload.get("industry", "restaurant")
        content_type = payload.get("content_type", "instagram_post")
        platform = payload.get("platform", "instagram")
        product = payload.get("product", "Special Offering")
        objective = payload.get("objective", "promotion")
        offer = payload.get("offer", "")
        tone = payload.get("tone", "premium")
        language = payload.get("language", "english").lower()
        length = payload.get("length", "medium")
        include_cta = payload.get("include_cta", True)
        
        # Extract any extra industry fields
        extra_details = []
        for k, v in payload.items():
            if k not in ["industry", "content_type", "platform", "product", "objective", "offer", "tone", "language", "length", "include_cta"] and v:
                extra_details.append(f"- {k.replace('_', ' ').title()}: {v}")
        
        extra_details_str = "\n".join(extra_details) if extra_details else "None specified"
        
        # Brand context injection
        brand_info = []
        if brand_profile:
            if brand_profile.get("business_name"):
                brand_info.append(f"Business Name: {brand_profile['business_name']}")
            if brand_profile.get("location"):
                brand_info.append(f"Location / Address: {brand_profile['location']}")
            if brand_profile.get("phone"):
                brand_info.append(f"Phone / WhatsApp: {brand_profile['phone']}")
            if brand_profile.get("website"):
                brand_info.append(f"Website: {brand_profile['website']}")
            if brand_profile.get("default_cta") and not payload.get("cta_override"):
                brand_info.append(f"Default Brand CTA: {brand_profile['default_cta']}")
        
        brand_str = "\n".join(brand_info) if brand_info else "Local Quality Business (No specific brand name provided)"

        system_instruction = f"""
You are the world's most talented, top-tier Small Business Marketing Copywriter and Creative Director.
Your job is to generate ready-to-publish, high-converting marketing content for small businesses based strictly on structured selections.

{LANGUAGE_INSTRUCTIONS.get(language, LANGUAGE_INSTRUCTIONS['english'])}

OUTPUT FORMAT REQUIREMENTS:
You must ALWAYS respond with a VALID, RAW JSON object containing EXACTLY these keys:
{{
  "hook": "Magnetic first sentence or headline",
  "caption": "Full body text formatted beautifully with paragraph breaks and appropriate emojis",
  "cta": "Clear call to action line (in the requested language)",
  "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5", "#tag6", "#tag7", "#tag8"],
  "suggested_image_prompt": "Detailed photorealistic commercial photography prompt in English describing the visual scene to pair with this post",
  "target_audience_appeal": "One sentence describing why this resonates with the target buyer"
}}
DO NOT include markdown code fences like ```json ... ``` in your raw text. Output only valid JSON.
"""

        user_prompt = f"""
CAMPAIGN BRIEF:
- Industry: {industry.upper()}
- Content Format: {content_type.upper()} ({PLATFORM_SPECIFIC_GUIDANCE.get(content_type, 'Marketing Post')})
- Core Product / Service: {product}
- Campaign Goal / Objective: {objective}
- Special Offer / Discount: {offer if offer else "No special discount - focus on quality & value"}
- Tone & Personality: {tone.upper()} ({TONE_GUIDANCE.get(tone, 'Engaging and professional')})
- Target Language: {language.upper()}
- Desired Length: {length.upper()}
- Include Explicit CTA: {'YES - must include clear action step' if include_cta else 'Subtle CTA'}

BRAND CONTEXT:
{brand_str}

INDUSTRY-SPECIFIC ATTRIBUTES:
{extra_details_str}

EXECUTION RULES:
1. Emphasize the core product '{product}' prominently.
2. If offer '{offer}' is provided, prominently feature '{offer}' in the copy and highlight the urgency/savings.
3. Write completely in the requested language: {language.upper()}.
4. Follow the {tone.upper()} tone strictly.
5. Create modern, human-sounding, vibrant marketing copy that drives real customer action.
6. Provide an ultra-high-quality image generation prompt in English for our companion image studio.
"""

        return {
            "system_instruction": system_instruction.strip(),
            "user_prompt": user_prompt.strip()
        }
