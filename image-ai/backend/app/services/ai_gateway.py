import os
import json
import logging
import re
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_structured_content(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        pass

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self._client = None
        if self.api_key:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not init Gemini GenAI client: {e}")

    async def generate_structured_content(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        if not self._client:
            raise ValueError("Gemini Client not initialized")
        
        try:
            full_prompt = f"{system_prompt}\n\nUSER CAMPAIGN REQUIREMENTS:\n{user_prompt}\n\nReturn pure JSON matching the specified schema."
            response = self._client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=full_prompt,
                config=dict(
                    response_mime_type="application/json",
                    temperature=0.7,
                )
            )
            
            text_resp = response.text.strip()
            if text_resp.startswith("```json"):
                text_resp = text_resp[7:]
            if text_resp.endswith("```"):
                text_resp = text_resp[:-3]
            text_resp = text_resp.strip()
            
            return json.loads(text_resp)
        except Exception as e:
            logger.error(f"Gemini generation error: {e}")
            raise

class MockAIProvider(BaseAIProvider):
    """
    Deterministic, human-copywriting engine with authentic industry-specific copywriting
    across Restaurant, Clothing, Real Estate, Salon, and Electronics.
    """
    async def generate_structured_content(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        prompt_lower = user_prompt.lower()
        
        is_telugu = "telugu" in prompt_lower
        is_hindi = "hindi" in prompt_lower
        
        # Detect platform / format cleanly from prompt header
        fmt_match = re.search(r"-\s*content format:\s*([a-zA-Z_]+)", prompt_lower)
        explicit_fmt = fmt_match.group(1).strip() if fmt_match else ""

        is_whatsapp = explicit_fmt in ["whatsapp_broadcast", "whatsapp_message", "whatsapp"] or (not explicit_fmt and "whatsapp" in prompt_lower)
        is_facebook = explicit_fmt in ["facebook_post", "facebook"] or (not explicit_fmt and "facebook" in prompt_lower)
        is_ad = explicit_fmt in ["ad_copy", "advertisement"] or (not explicit_fmt and ("ad_copy" in prompt_lower or "advertisement" in prompt_lower))
        is_reel = explicit_fmt in ["reel_script", "reel", "video"] or (not explicit_fmt and ("reel_script" in prompt_lower or "reel" in prompt_lower))
        is_email = explicit_fmt in ["marketing_email", "email"] or (not explicit_fmt and ("marketing_email" in prompt_lower or "email" in prompt_lower))
        is_product = explicit_fmt in ["product_description", "description"] or (not explicit_fmt and ("product_description" in prompt_lower or "description" in prompt_lower))
        
        # Detect industry cleanly from prompt header or keywords
        ind_match = re.search(r"-\s*industry:\s*([a-zA-Z_]+)", prompt_lower)
        explicit_ind = ind_match.group(1).strip() if ind_match else ""
        
        if explicit_ind == "clothing":
            is_clothing, is_real_estate, is_salon, is_electronics, is_restaurant = True, False, False, False, False
        elif explicit_ind in ["real_estate", "realestate"]:
            is_clothing, is_real_estate, is_salon, is_electronics, is_restaurant = False, True, False, False, False
        elif explicit_ind == "salon":
            is_clothing, is_real_estate, is_salon, is_electronics, is_restaurant = False, False, True, False, False
        elif explicit_ind == "electronics":
            is_clothing, is_real_estate, is_salon, is_electronics, is_restaurant = False, False, False, True, False
        elif explicit_ind == "restaurant":
            is_clothing, is_real_estate, is_salon, is_electronics, is_restaurant = False, False, False, False, True
        else:
            is_clothing = any(k in prompt_lower for k in ["clothing", "saree", "fashion", "apparel", "dress"])
            is_real_estate = any(k in prompt_lower for k in ["real estate", "real_estate", "bhk", "property", "villa", "flat", "apartment"])
            is_salon = any(k in prompt_lower for k in [" salon", "salon ", "facial", " spa ", " hair", "beauty parlor"])
            is_electronics = any(k in prompt_lower for k in ["electronic", "phone", "laptop", "gadget", "smartphone"])
            is_restaurant = not (is_clothing or is_real_estate or is_salon or is_electronics)
        
        prod_match = re.search(r"product /.*?: (.*?)\n", user_prompt, re.IGNORECASE)
        product = prod_match.group(1).strip() if prod_match else "Signature Item"
        
        offer_match = re.search(r"offer /.*?: (.*?)\n", user_prompt, re.IGNORECASE)
        offer = offer_match.group(1).strip() if offer_match and "No special discount" not in offer_match.group(1) else "Special Limited Offer"

        # Industry-specific English context
        if is_clothing:
            highlights = [
                "• Authentic handloom weave & master artisan craftsmanship",
                "• Luxurious pure silk fabric with intricate traditional zari",
                "• Timeless drape designed for festive and wedding celebrations"
            ]
            intro_msg = f"We have an exclusive update for our valued patrons regarding our signature *{product}*."
            story_msg = f"Nothing embodies grace and heritage quite like authentic handloom fashion. Our signature {product} is crafted by master artisans, featuring rich traditional motifs, luxurious drape, and unmatched elegance."
            fb_hook = f"Elevate your festive wardrobe with the timeless elegance of {product}! ✨"
            ad_hook = f"✨ Limited Festive Privilege: Get {offer} on our handcrafted {product}!"
            cta_call = "👉 Reply here or visit our boutique to explore the collection"
            tags = ["#IndianFashion", "#HandloomLove", "#SareeStyle", f"#{product.replace(' ', '')}", "#EthnicElegance", "#FestiveWear"]
            img_prompt = f"Authentic real-life photograph of an elegant Indian woman wearing an authentic {product}, genuine drape, real silk fabric with gold zari border, natural daytime lighting, shot on Canon DSLR, sharp realistic photo, no CGI"
        elif is_real_estate:
            highlights = [
                "• Prime strategic location with seamless city connectivity",
                "• Vastu-compliant architecture with world-class modern lifestyle amenities",
                "• High appreciation potential with 100% transparent documentation"
            ]
            intro_msg = f"We have an exclusive preview for discerning buyers regarding *{product}*."
            story_msg = f"Find the perfect balance of luxury, comfort, and peaceful living. Our {product} is designed with expansive sunlit rooms, modern architecture, and scenic landscaped views."
            fb_hook = f"Step into a lifestyle of luxury and convenience with {product}! 🏡"
            ad_hook = f"🏡 Exclusive Booking Privilege: Book {product} with {offer} this month!"
            cta_call = "👉 Reply here to schedule a private site visit or view floor plans"
            tags = ["#RealEstate", "#DreamHome", "#LuxuryLiving", f"#{product.replace(' ', '')}", "#PropertyInvestment"]
            img_prompt = f"Authentic real-world architectural photograph of {product}, natural daylight, sharp tilt-shift camera photo, real residential property, no CGI"
        elif is_salon:
            highlights = [
                "• Certified aesthetic therapists with clinical hygiene standards",
                "• Premium organic formulations tailored to your hair and skin",
                "• Visible rejuvenation with instant natural glow and lasting care"
            ]
            intro_msg = f"Treat yourself to a moment of pure relaxation with our signature *{product}*."
            story_msg = f"Unwind and let our experts take care of your personal wellness. Our {product} combines therapeutic expertise with premium products for a radiant, refreshed look."
            fb_hook = f"Indulge in the self-care you deserve with our signature {product}! 💆‍♀️"
            ad_hook = f"🌸 Exclusive Self-Care Offer: Book your {product} session with {offer}!"
            cta_call = "👉 Reply here to book your priority appointment"
            tags = ["#SalonCare", "#GlowUp", "#SelfCare", f"#{product.replace(' ', '')}", "#BeautyTreatment"]
            img_prompt = f"Authentic real photograph of a woman with radiant skin and healthy hair after {product}, natural daylight, genuine human skin texture, real salon setting, high-detail camera portrait"
        elif is_electronics:
            highlights = [
                "• Next-generation flagship performance with unmatched efficiency",
                "• Precision aerospace-grade build with ultra-vivid display",
                "• Official manufacturer warranty with priority after-sales service"
            ]
            intro_msg = f"Upgrade your lifestyle with the cutting-edge power of *{product}*."
            story_msg = f"Experience seamless productivity and entertainment. The all-new {product} delivers lightning-fast speed, long-lasting battery life, and premium industrial design."
            fb_hook = f"Unleash next-level speed and innovation with {product}! ⚡"
            ad_hook = f"⚡ Launch Special: Upgrade to {product} today with {offer}!"
            cta_call = "👉 Reply here or visit our store to secure your launch discount"
            tags = ["#TechUpgrade", "#NextGenTech", "#GadgetLovers", f"#{product.replace(' ', '')}", "#SmartLiving"]
            img_prompt = f"Authentic real photograph of {product}, sitting on a real modern wooden desk, natural daylight, sharp product photograph, shot on Sony A7R camera, realistic reflections"
        else:
            highlights = [
                "• Authentic traditional preparation with genuine spices & ingredients",
                "• Freshly cooked to order with uncompromising hygiene standards",
                "• Savor rich, unforgettable culinary flavors in every bite"
            ]
            intro_msg = f"We have an exclusive culinary update regarding our signature *{product}*."
            story_msg = f"Nothing brings people together quite like good food, great conversations, and authentic flavors prepared with genuine love. Our signature {product} is handcrafted daily using time-honored recipes."
            fb_hook = f"Gather your family and friends for the unmatched taste of {product}! 🍲"
            ad_hook = f"🔥 Limited Time: Savor our authentic {product} with {offer}!"
            cta_call = "👉 Reply here or call us directly to place your order"
            tags = ["#FoodLovers", "#AuthenticTaste", "#LocalEats", f"#{product.replace(' ', '')}", "#SpecialOffer"]
            img_prompt = f"Authentic real-life photograph of genuine {product}, served fresh on traditional tableware or banana leaf, real food textures, natural bright ambient restaurant daylight, shot on Canon DSLR 50mm lens, no CGI"

        # ----------------------------------------------------
        # 1. TELUGU PLATFORM FORMATS
        # ----------------------------------------------------
        if is_telugu:
            if is_whatsapp:
                return {
                    "hook": f"📢 *ప్రత్యేక శుభవార్త:* {product} పై ప్రత్యేక డీల్!",
                    "caption": f"నమస్కారం! 🙏\n\nమా ప్రత్యేకమైన మరియు అత్యుత్తమ నాణ్యతతో కూడిన *{product}* ఇప్పుడు సరికొత్తగా సిద్ధంగా ఉంది.\n\n✨ *హైలైట్స్:*\n{highlights[0]}\n{highlights[1]}\n{highlights[2]}\n\n🎁 *ఈ వారం ప్రత్యేక ఆఫర్:* *{offer}*\n\nఈ ఆఫర్ పరిమిత సమయం వరకు మాత్రమే అందుబాటులో ఉంటుంది. ఇప్పుడే బుక్ చేసుకోండి!",
                    "cta": "👉 వివరాలు లేదా ఆర్డర్ కోసం ఇక్కడే రిప్లై ఇవ్వండి లేదా కాల్ చేయండి",
                    "hashtags": [],
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "High urgency WhatsApp broadcast message for direct customer action."
                }
            elif is_facebook:
                return {
                    "hook": f"మీ కుటుంబంతో కలిసి ఆనందించడానికి సరికొత్త {product}! 🌟",
                    "caption": f"మీ అభిమాన {product} ఇప్పుడు మరింత ప్రత్యేకమైన అనుభవంతో మీ ముందుకు వచ్చింది.\n\nఅత్యున్నత ప్రమాణాలు, పరిశుభ్రత మరియు ప్రామాణిక నాణ్యతతో రూపొందించబడిన మా సిగ్నేచర్ కలెక్షన్.\n\n🎉 ఆనందకరమైన ఆఫర్: ఈ రోజు మీ ఆర్డర్‌పై {offer} ఆస్వాదించండి!\n\nమీ అభిమాన అనుభవాన్ని క్రింద కామెంట్స్‌లో మాతో పంచుకోండి! 👇",
                    "cta": "👉 ఇప్పుడే ఆర్డర్ చేయడానికి / సందర్శించడానికి ఇక్కడ క్లిక్ చేయండి",
                    "hashtags": ["#TeluguCommunity", f"#{product.replace(' ', '')}", "#SpecialCelebration", "#TopQuality"],
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "Story-driven community Facebook post that drives high comments and shares."
                }
            elif is_ad:
                return {
                    "hook": f"🔥 పరిమిత కాలం: {product} పై {offer} పొందండి!",
                    "caption": f"అత్యుత్తమ నాణ్యత, సరసమైన ధర మరియు అసలైన అనుభూతి — అన్నీ ఒకే చోట!\n\nఅద్భుతమైన సంతృప్తిని అందించే మా ప్రత్యేక {product}.\n\n✅ వేలమంది సంతృప్తి చెందిన కస్టమర్లు\n✅ గ్యారెంటీ నాణ్యత & సర్వీస్\n\nఆఫర్ త్వరలోనే ముగుస్తుంది. ఆలస్యం చేయకండి!",
                    "cta": "👉 ఆఫర్ పొందడానికి ఇప్పుడే ఆర్డర్ చేయండి",
                    "hashtags": [f"#{product.replace(' ', '')}", "#SpecialOfferTelugu", "#BestDeals"],
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "High-converting direct response advertisement with strong FOMO."
                }
            elif is_reel:
                return {
                    "hook": f"👀 ఈ అద్భుతాన్ని మీరు ఎప్పుడైనా చూశారా? {product}!",
                    "caption": f"🎬 [సీన్ 1 - హుక్ 0-3 సె]: వేడి వేడి / అందమైన {product} క్లోజప్ షాట్!\n🗣️ వాయిస్‌ఓవర్: \"అసలైన నాణ్యతతో కూడిన బెస్ట్ {product} ఎక్కడుందో తెలుసా?\"\n\n🎬 [సీన్ 2 - డెమో 3-10 సె]: అసలైన మెటీరియల్ మరియు తయారీ విధానం చూపించడం.\n🗣️ వాయిస్‌ఓవర్: \"అసలైన నాణ్యత, సాంప్రదాయ విలువలు మీ ముందుకు!\"\n\n🎬 [సీన్ 3 - ఆఫర్ & CTA 10-15 సె]: ఆఫర్ బ్యాడ్జ్ స్క్రీన్ పై మెరుస్తుంది.\n🗣️ వాయిస్‌ఓవర్: \"ఇప్పుడే ఆర్డర్ చేసి {offer} సొంతం చేసుకోండి!\"",
                    "cta": "📲 వెంటనే బయో లో ఉన్న లింక్ క్లిక్ చేయండి",
                    "hashtags": ["#TeluguReels", "#TrendingTelugu", f"#{product.replace(' ', '')}"],
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "Fast-paced, viral short video format for Instagram Reels & YouTube Shorts."
                }
            elif is_email:
                return {
                    "hook": f"సబ్జెక్ట్: 🎁 మీ కోసం ప్రత్యేక సర్ప్రైజ్: {product} పై {offer}!",
                    "caption": f"ప్రియమైన కస్టమర్,\n\nమీ రోజును మరింత ప్రత్యేకంగా మార్చడానికి మేము ఒక గొప్ప అవకాశాన్ని తీసుకొచ్చాము.\n\nమా అత్యంత ప్రజాదరణ పొందిన {product} పై ఈ వారం మాత్రమే ప్రత్యేకంగా {offer} అందిస్తున్నాము.\n\nమా కస్టమర్ల సంతృప్తి మరియు అసలైన నాణ్యత మా మొదటి ప్రాధాన్యత.\n\nఈ అవకాశాన్ని మిస్ చేసుకోకండి. మీ కోడ్: SPECIAL20 ని ఉపయోగించి ఇప్పుడే పొందండి.",
                    "cta": "👉 ఇప్పుడే ఆఫర్ క్లెయిమ్ చేయండి",
                    "hashtags": [],
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "Personalized VIP newsletter style email with exclusive promo code."
                }
            else:
                return {
                    "hook": f"సరికొత్త నాణ్యతతో మీ ముందుకు! ✨ {product}",
                    "caption": f"సంప్రదాయం మరియు నవతత్వాల కలయికతో రూపొందించబడిన మా సిగ్నేచర్ {product}.\n\nప్రతి వివరంలోనూ అసలైన ప్రామాణికత మరియు ఉన్నతమైన నాణ్యతను అనుభవించండి!\n\n🎁 ప్రత్యేక ఆఫర్: ఈ రోజు మీ ఆర్డర్‌పై {offer} పొందండి.\n\nఇప్పుడే సంప్రదించండి లేదా సందర్శించండి.",
                    "cta": "👉 ఇప్పుడే ఆర్డర్ చేయండి / సందర్శించండి",
                    "hashtags": ["#TeluguTrends", f"#{product.replace(' ', '')}", "#SpecialOffer", "#QualityFirst"],
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "Appeals directly to Telugu customers looking for authentic quality and value."
                }

        # ----------------------------------------------------
        # 2. HINDI PLATFORM FORMATS
        # ----------------------------------------------------
        elif is_hindi:
            if is_whatsapp:
                return {
                    "hook": f"📢 *विशेष ऑफर:* {product} पर पाएं {offer}!",
                    "caption": f"नमस्ते! 🙏\n\nआपके पसंदीदा *{product}* पर इस सप्ताह विशेष अवसर उपलब्ध है।\n\n✨ *खासियतें:*\n{highlights[0]}\n{highlights[1]}\n{highlights[2]}\n\n🎁 *ऑफर:* आज ही आर्डर करें और पाएं *{offer}*!\n\nयह सीमित समय का ऑफर है।",
                    "cta": "👉 आर्डर करने के लिए तुरंत यहाँ रिप्लाई करें या कॉल करें",
                    "hashtags": [],
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "Direct, conversational WhatsApp broadcast for Hindi customers."
                }
            else:
                return {
                    "hook": f"परंपरा और श्रेष्ठता का बेमिसाल संगम — {product}! 🌟",
                    "caption": f"बेहतरीन गुणवत्ता और प्रामाणिक कारीगरी के साथ तैयार हमारा खास {product}.\n\nशुद्ध सामग्री, उत्कृष्ट डिज़ाइन और ग्राहकों की पहली पसंद।\n\n🎉 सीमित समय के लिए: आज ही आर्डर करें और पाएं {offer} का विशेष लाभ!",
                    "cta": "👉 अभी आर्डर करें या अधिक जानकारी प्राप्त करें",
                    "hashtags": ["#SpecialOfferHindi", f"#{product.replace(' ', '')}", "#QualityMatters", "#FestiveSpecials"],
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "Warm, relatable community tone for Hindi-speaking customers."
                }

        # ----------------------------------------------------
        # 3. ENGLISH PLATFORM FORMATS
        # ----------------------------------------------------
        else:
            hl_text = "\n".join(highlights)
            if is_whatsapp:
                return {
                    "hook": f"📢 *Special Benefit:* Enjoy {offer} on {product}!",
                    "caption": f"Hello there! 👋\n\n{intro_msg}\n\n✨ *Why you'll love it:*\n{hl_text}\n\n🎁 *Limited Privilege:* Get *{offer}* when you connect today!\n\nSimply reply to this chat to place your request or inquire.",
                    "cta": cta_call,
                    "hashtags": [],
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "Clean, direct WhatsApp broadcast with instant 1-tap reply CTA."
                }
            elif is_facebook:
                return {
                    "hook": fb_hook,
                    "caption": f"{story_msg}\n\nKey Highlights:\n{hl_text}\n\n🎉 Special Highlight: Enjoy {offer} on your visit or direct order!\n\nWhat are you most excited about? Let us know in the comments below! 👇",
                    "cta": cta_call,
                    "hashtags": tags,
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "Community storytelling that drives social interaction and engagement."
                }
            elif is_ad:
                return {
                    "hook": ad_hook,
                    "caption": f"Looking for authentic quality without compromises? Experience our crowd-favorite {product} today.\n\n{hl_text}\n\nClaim your special voucher before this limited offer ends!",
                    "cta": "👉 Claim Offer & Connect Now",
                    "hashtags": [f"#{product.replace(' ', '')}", "#ExclusiveOffer", "#TopQuality"],
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "Direct response advertising tailored to Meta & Google Sponsored ads."
                }
            elif is_reel:
                return {
                    "hook": f"👀 Have you seen the most exquisite {product} in town?",
                    "caption": f"🎬 [SCENE 1 - 0:00-0:03 HOOK]: Cinematic macro shot of {product}, highlighting intricate texture and craftsmanship.\n🗣️ VOICEOVER: \"If you love authentic quality, stop scrolling!\"\n\n🎬 [SCENE 2 - 0:03-0:10 VALUE]: Dynamic showcase of details and premium materials.\n🗣️ VOICEOVER: \"Crafted with heritage techniques and zero compromises on excellence.\"\n\n🎬 [SCENE 3 - 0:10-0:15 CTA]: Graphic popup showing '{offer}' badge.\n🗣️ VOICEOVER: \"Claim {offer} this week only. Link in bio!\"",
                    "cta": "📲 Tap the link in our bio to explore now",
                    "hashtags": ["#ReelsViral", f"#{product.replace(' ', '')}", "#TrendingNow"],
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "High-engagement viral video script with precise timestamps and visual cues."
                }
            elif is_email:
                return {
                    "hook": f"Subject: ✨ Exclusive Invitation: {offer} on our signature {product}!",
                    "caption": f"Hi there,\n\nWe wanted to share something special with our valued community.\n\n{story_msg}\n\nAs a thank you, enjoy an exclusive {offer} on your next order.\n\nUse Code at Checkout: HERITAGE20\n\nWe look forward to serving you!",
                    "cta": "👉 Claim Your VIP Special Now",
                    "hashtags": [],
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "High open-rate VIP marketing email with clear coupon code."
                }
            elif is_product:
                return {
                    "hook": f"Overview: Premium Handcrafted {product}",
                    "caption": f"Experience the pinnacle of craftsmanship and design with our signature {product}.\n\nKey Highlights:\n{hl_text}\n\nSpecial Incentive:\nOrder today to receive {offer} along with complimentary priority service.",
                    "cta": "🛒 Add to Cart / Order Now",
                    "hashtags": [f"#{product.replace(' ', '')}", "#ProductSpotlight", "#QualityGuaranteed"],
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "Conversion-optimized product page description highlighting specs and benefits."
                }
            else: # Instagram Post Default
                return {
                    "hook": f"Drape yourself in heritage and luxury with our signature {product}. ✨",
                    "caption": f"{story_msg}\n\n✨ Features:\n{hl_text}\n\n🌟 Current special: Enjoy {offer} when you order this week.\n\nDirect message us or visit in-store to explore.",
                    "cta": "👉 Send a DM or tap the link in bio to order",
                    "hashtags": tags,
                    "suggested_image_prompt": img_prompt,
                    "target_audience_appeal": "Clean, authentic human storytelling that connects directly with patrons."
                }

class AIGateway:
    @staticmethod
    def get_provider(custom_api_key: Optional[str] = None) -> BaseAIProvider:
        key = custom_api_key or settings.GEMINI_API_KEY
        if key and len(key.strip()) > 10:
            try:
                return GeminiProvider(api_key=key.strip())
            except Exception as e:
                logger.warning(f"Failed to create Gemini provider, falling back to mock: {e}")
                return MockAIProvider()
        return MockAIProvider()
