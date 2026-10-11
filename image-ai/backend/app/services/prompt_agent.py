"""
Prompt Agent — powered by Groq (LLaMA 3.3 70B) with local fallback.

Uses Groq's ultra-fast inference to parse the user's free-text description
and generate a professional, detailed image prompt. Falls back to the
built-in local prompt library if Groq is unavailable.
"""

import re
import asyncio
import json
import random
import logging
from typing import Dict, Any, Optional, List

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Local fallback — keyword-based industry detection & prompt library
# (used when Groq is unavailable)
# ---------------------------------------------------------------------------
INDUSTRY_KEYWORDS: Dict[str, List[str]] = {
    "restaurant": [
        "biryani", "thali", "food", "restaurant", "cafe", "coffee", "pizza", "burger",
        "chicken", "paneer", "kebab", "dessert", "bakery", "sweet", "meal", "dish",
        "curry", "noodles", "shawarma", "dosa", "idli", "paratha", "roti", "rice",
        "lunch", "dinner", "breakfast", "snack", "cloud kitchen", "tiffin", "chai",
        "tea", "juice", "smoothie", "sambar", "rasam", "dal"
    ],
    "clothing": [
        "saree", "kurta", "dress", "shirt", "fashion", "apparel", "clothing",
        "wear", "outfit", "hoodie", "jeans", "denim", "lehenga", "suit",
        "ethnic", "silk", "cotton", "fabric", "boutique", "collection",
        "tshirt", "pant", "trouser", "jacket", "coat", "blazer", "kurti",
        "anarkali", "salwar", "pajama", "nightwear", "sportswear",
    ],
    "real_estate": [
        "apartment", "flat", "villa", "property", "bhk", "house", "plot",
        "real estate", "home", "penthouse", "office", "commercial", "project",
        "gated", "tower", "residential", "investment", "builder", "emi",
        "possession", "sqft", "sq.ft", "vastu", "clubhouse",
    ],
    "salon": [
        "salon", "spa", "beauty", "hair", "facial", "makeup", "skin",
        "bridal", "keratin", "balayage", "manicure", "pedicure", "massage",
        "glow", "hydrafacial", "waxing", "threading", "nails", "lashes",
        "highlights", "coloring", "treatment", "parlour", "parlor",
    ],
    "electronics": [
        "phone", "smartphone", "laptop", "tv", "earbuds", "headphone",
        "tablet", "smartwatch", "gadget", "electronics", "camera", "gaming",
        "speaker", "appliance", "washing machine", "refrigerator", "ac",
        "air conditioner", "processor", "gpu", "5g", "4k", "oled", "amoled",
    ],
}

# Explicitly crafted for genuine, unedited real-world photography (no CGI, no 3D render)
PROMPT_TEMPLATES: Dict[str, List[str]] = {
    "restaurant": [
        "Authentic real-life photograph of genuine {product}, served fresh on traditional tableware or banana leaf, real food textures, glistening natural juices and aromatic spices, natural bright ambient restaurant daylight, shot on Canon DSLR 50mm lens, sharp focus on real food, true-to-life colors, genuine food photograph, no 3D render, no CGI",
        "Overhead flat-lay real camera photo of delicious {product}, traditional authentic dining table setting, natural indoor daylight, real food textures, fresh cilantro and garnishes, crisp details, documentary food photography, real life photograph",
        "Close-up real photo of hot appetizing {product}, authentic restaurant presentation, steam gently rising, natural dining room lighting, shot on Sony Alpha camera, sharp optical focus on real ingredients, authentic appetizing Indian food photography",
    ],
    "clothing": [
        "Real-life photograph of an elegant Indian woman wearing an authentic {product}, genuine drape and real woven fabric texture with intricate craftsmanship, natural golden hour sunlight, shot on high-resolution DSLR camera, real person photo, sharp realistic textile weave, no CGI, no cartoon",
        "Authentic fashion editorial photograph of {product}, genuine textile material and real-world drape, natural soft window daylight, true fabric color, real camera photo, razor-sharp fabric detail",
    ],
    "real_estate": [
        "Authentic real-world architectural photograph of {product}, genuine residential property, natural daylight, real sky and landscaping, shot on wide-angle DSLR lens, sharp authentic real estate photo, no CGI, no 3D render",
        "Real photograph of luxury {product}, warm evening interior lights glowing through real glass windows, genuine landscaping and driveway, authentic architectural photograph",
    ],
    "salon": [
        "Authentic real photograph of a woman with radiant skin and healthy hair after {product}, natural soft daylight, genuine human skin texture with pores, real salon setting, high-detail camera portrait, authentic photograph",
        "Real photo of {product} treatment, serene spa interior, soft warm ambient lighting, authentic wellness photograph, real life photo",
    ],
    "electronics": [
        "Authentic real photograph of {product}, sitting on a real modern wooden desk, natural daylight from window, sharp product photograph, shot on Sony A7R camera, realistic reflections and genuine materials, no CGI",
        "Real-world photograph of {product}, crisp clear detail, natural office table setting, realistic camera photo",
    ],
    "general": [
        "Authentic real-world photograph of {product}, natural ambient daylight, true-to-life colors and genuine textures, shot on Canon DSLR camera, real life photograph, no 3D render, no CGI",
    ],
}


def _detect_industry(text: str) -> str:
    text_lower = text.lower()
    scores: Dict[str, int] = {}
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score:
            scores[industry] = score
    return max(scores, key=lambda k: scores[k]) if scores else "general"


def _extract_offer(text: str) -> str:
    patterns = [
        r"(\d+\s*%\s*off)", r"(flat\s+₹?\$?\d[\d,]*\s*off)",
        r"(buy\s+\d+\s+get\s+\d+)", r"(free\s+\w+(?:\s+\w+)?)",
        r"(up\s+to\s+\d+\s*%)", r"(₹[\d,]+\s+(?:off|discount|cashback))",
        r"(starting\s+(?:at|from)\s+₹?[\d,]+)", r"(no[- ]cost\s+emi)",
        r"(complimentary\s+\w+(?:\s+\w+)?)",
    ]
    for pattern in patterns:
        m = re.search(pattern, text.lower())
        if m:
            return m.group(1).strip().title()
    return ""


def _local_fallback(user_input: str) -> Dict[str, Any]:
    industry = _detect_industry(user_input)
    offer = _extract_offer(user_input)
    
    # Strip marketing and intent boilerplate to extract the real physical subject
    noise = [
        "festive promotion banner for", "festive promotion banner", "festive promotion",
        "promotional banner for", "promotional banner", "promotion banner for",
        "promotion banner", "elegant showcase of", "showcase of", "banner for",
        "image for", "photo of", "picture of", "poster for", "i need a", "i need an",
        "i need", "i want a", "i want an", "i want", "create a", "create an",
        "create", "generate a", "generate an", "generate", "give me a", "give me",
        "please make", "please", "for my", "for a", "of a", "of my", "this weekend",
        "this week", "promotion for", "promotional", "promotion", "advertisement",
        "commercial", "marketing", "banner", "poster", "special offer", "festive",
        "with discount", "with offer"
    ]
    cleaned = user_input.lower()
    for n in sorted(noise, key=len, reverse=True):
        cleaned = cleaned.replace(n, " ")

    # Remove discount expressions like "with 20% discount", "20% off"
    cleaned = re.sub(r"with\s+\d+%.*|\d+\s*%\s*(?:off|discount)|flat\s+₹?\d[\d,]*|free\s+\w+|starting\s+from\s+₹?[\d,]+", " ", cleaned)
    cleaned = re.sub(r"[^\w\s-]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    words = [w for w in cleaned.split() if len(w) > 1]
    
    # Prioritize industry nouns if present so key food/clothing items aren't dropped
    if industry in INDUSTRY_KEYWORDS:
        matching_kws = [w for w in words if w in INDUSTRY_KEYWORDS[industry]]
        if matching_kws:
            last_idx = max(words.index(k) for k in matching_kws)
            words = words[:last_idx + 2]

    product = " ".join(words[:6]).title() if words else "Authentic Item"

    templates = PROMPT_TEMPLATES.get(industry, PROMPT_TEMPLATES["general"])
    prompt = random.choice(templates).format(product=product, context=offer)
    return {"product": product, "industry": industry, "offer": offer, "suggested_prompt": prompt}


# ---------------------------------------------------------------------------
# Groq-powered PromptAgent
# ---------------------------------------------------------------------------
GROQ_SYSTEM_PROMPT = """You are an expert commercial photo director.

The user will describe an image they need.

Your goals:
1. Extract the core PRODUCT or SERVICE being depicted (e.g., "South Indian Thali Meal", "Hyderabadi Dum Biryani", "Kanchipuram Silk Saree").
2. Extract the INDUSTRY (restaurant, clothing, real_estate, salon, electronics, or general).
3. Extract any OFFER (e.g. "20% OFF", or empty string).
4. Write a REAL-WORLD PHOTOGRAPHIC PROMPT that looks like a GENUINE, AUTHENTIC CAMERA PHOTOGRAPH taken in real life.
   - Do NOT use words like "3D render", "CGI", "digital illustration", "artstation", "hyper-detailed artwork".
   - Use REAL PHOTOGRAPHY terms: "Authentic real-life photograph", "shot on Canon EOS DSLR camera", "natural indoor dining daylight", "tangible real textures", "real food plating on steel platter or banana leaf", "real fabric weave".
   - It must look completely real, believable, and authentic.

Respond ONLY with valid JSON:
{
  "product": "short product name",
  "industry": "one of: restaurant | clothing | real_estate | salon | electronics | general",
  "offer": "extracted offer or empty string",
  "suggested_prompt": "real photographic prompt here"
}"""


class PromptAgent:
    def __init__(self, api_key: Optional[str] = None):
        self._api_key = settings.GROQ_API_KEY
        self._client = None
        if self._api_key:
            try:
                from groq import Groq
                self._client = Groq(api_key=self._api_key, timeout=30, max_retries=0)
                logger.info("PromptAgent: Groq client initialized.")
            except Exception as e:
                logger.warning(f"PromptAgent: Could not init Groq client: {e}")

    async def analyze_and_generate_prompt(self, user_input: str) -> Dict[str, Any]:
        if self._client:
            try:
                return await asyncio.to_thread(self._call_groq, user_input)
            except Exception as e:
                logger.warning(f"Groq call failed, using local fallback: {e}")

        logger.info("PromptAgent: using local fallback.")
        return _local_fallback(user_input)

    def _call_groq(self, user_input: str) -> Dict[str, Any]:
        completion = self._client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": GROQ_SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
            max_tokens=512,
            response_format={"type": "json_object"},
        )
        text = completion.choices[0].message.content.strip()
        result = json.loads(text)

        for key in ("product", "industry", "offer", "suggested_prompt"):
            if key not in result:
                raise ValueError(f"Missing key '{key}' in Groq response")

        logger.info(
            f"PromptAgent [Groq]: industry={result['industry']}, product={result['product']}"
        )
        return result
