from typing import Dict, List, Any

# Global MVP Constants
SUPPORTED_LANGUAGES = [
    {"id": "english", "label": "English", "native": "English", "flag": "🇬🇧"},
    {"id": "telugu", "label": "Telugu", "native": "తెలుగు", "flag": "🇮🇳"},
    {"id": "hindi", "label": "Hindi", "native": "हिन्दी", "flag": "🇮🇳"}
]

SUPPORTED_TONES = [
    {"id": "professional", "label": "Professional", "description": "Polished, authoritative, business-ready"},
    {"id": "friendly", "label": "Friendly", "description": "Warm, welcoming, community-focused"},
    {"id": "premium", "label": "Premium", "description": "Exclusive, luxurious, high-end quality"},
    {"id": "funny", "label": "Funny", "description": "Witty, humorous, engaging & relatable"},
    {"id": "energetic", "label": "Energetic", "description": "Exciting, high-tempo, FOMO-inducing"},
    {"id": "minimal", "label": "Minimal", "description": "Clean, punchy, direct to the point"}
]

CONTENT_TYPES = [
    {"id": "instagram_post", "label": "Instagram Post", "platform": "instagram", "icon": "Instagram", "desc": "Visual caption with hooks, aesthetics & hashtags"},
    {"id": "facebook_post", "label": "Facebook Post", "platform": "facebook", "icon": "Facebook", "desc": "Engaging community story with details & CTA"},
    {"id": "whatsapp_message", "label": "WhatsApp Marketing Message", "platform": "whatsapp", "icon": "MessageCircle", "desc": "Direct conversational offer with emoji formatting"},
    {"id": "product_description", "label": "Product Description", "platform": "website", "icon": "FileText", "desc": "Feature-benefit spotlight for web or catalogs"},
    {"id": "ad_copy", "label": "Advertisement Copy", "platform": "ads", "icon": "Megaphone", "desc": "High-converting ad headline, body & urgency CTA"},
    {"id": "reel_script", "label": "Reel Script", "platform": "instagram", "icon": "Video", "desc": "Visual scene breakdown, spoken audio & text overlays"},
    {"id": "marketing_email", "label": "Marketing Email", "platform": "email", "icon": "Mail", "desc": "Compelling subject line, preview text & email body"}
]

INDUSTRY_CONFIGS: Dict[str, Dict[str, Any]] = {
    "restaurant": {
        "id": "restaurant",
        "name": "Restaurant & Food",
        "icon": "Utensils",
        "description": "Cafes, fine-dining, cloud kitchens, fast food, and bakeries",
        "popular_items": ["Biryani", "Paneer Tikka", "Artisan Coffee", "Gourmet Burgers", "Thali Specials", "Pastries & Desserts"],
        "fields": [
            {
                "key": "product",
                "label": "Food / Dish / Special Item",
                "type": "text_or_select",
                "required": True,
                "placeholder": "e.g. Hyderabadi Dum Biryani, Cold Brew Coffee",
                "options": ["Dum Biryani", "Butter Chicken", "Wood-fired Pizza", "South Indian Thali", "Cheesecake", "Shawarma Platter", "Filter Coffee & Tiffin"]
            },
            {
                "key": "objective",
                "label": "Campaign Objective",
                "type": "select",
                "required": True,
                "options": [
                    {"id": "promotion", "label": "Special Offer / Discount"},
                    {"id": "new_launch", "label": "New Menu Item Launch"},
                    {"id": "weekend_special", "label": "Weekend Special Vibe"},
                    {"id": "festival", "label": "Festival / Holiday Celebration"},
                    {"id": "brand_story", "label": "Chef's Signature Story"}
                ],
                "default": "promotion"
            },
            {
                "key": "offer",
                "label": "Offer / Promotion",
                "type": "text_or_select",
                "required": False,
                "placeholder": "e.g. 20% OFF, Buy 1 Get 1 Free, Free Dessert with Meal",
                "options": ["20% OFF", "Buy 1 Get 1 Free", "Flat ₹100 OFF", "Free Starter with Family Meal", "Flat 15% OFF on Online Orders", "Complimentary Dessert"]
            },
            {
                "key": "occasion",
                "label": "Occasion / Special Context",
                "type": "text_or_select",
                "required": False,
                "placeholder": "e.g. Sunday Brunch, IPL Match Night, Eid Specials",
                "options": ["Weekend Feast", "Dinner Date", "Family Dining", "IPL Match Screening", "Festival Feast", "Midnight Cravings"]
            },
            {
                "key": "dietary_or_feature",
                "label": "Special Feature / Dietary",
                "type": "select",
                "required": False,
                "options": [
                    {"id": "authentic", "label": "Authentic Traditional Recipe"},
                    {"id": "pure_veg", "label": "100% Pure Veg & Fresh"},
                    {"id": "spicy_aromatic", "label": "Rich Spices & Aromatic Rice"},
                    {"id": "halal_organic", "label": "Farm-Fresh & Organic"},
                    {"id": "chef_crafted", "label": "Handcrafted by Master Chef"}
                ],
                "default": "authentic"
            }
        ]
    },
    "clothing": {
        "id": "clothing",
        "name": "Clothing & Fashion",
        "icon": "Shirt",
        "description": "Boutiques, apparel stores, ethnic wear, streetwear, and designer labels",
        "popular_items": ["Festive Sarees", "Oversized Streetwear Tees", "Kurta Sets", "Denim Jackets", "Party Dresses", "Formal Suits"],
        "fields": [
            {
                "key": "product",
                "label": "Product / Apparel Name",
                "type": "text_or_select",
                "required": True,
                "placeholder": "e.g. Silk Zari Saree, Oversized Graphic Hoodie",
                "options": ["Kanchipuram Silk Saree", "Linen Summer Shirt", "Embroidered Anarkali Kurta", "Slim-fit Chinos", "Oversized Streetwear Tee", "Floral Maxi Dress"]
            },
            {
                "key": "category",
                "label": "Fashion Category",
                "type": "select",
                "required": True,
                "options": [
                    {"id": "ethnic_wear", "label": "Ethnic & Festive Wear"},
                    {"id": "casual_streetwear", "label": "Casual & Streetwear"},
                    {"id": "formal_business", "label": "Formal & Office Wear"},
                    {"id": "bridal_luxury", "label": "Bridal & Luxury Couture"},
                    {"id": "seasonal_collection", "label": "Seasonal Daily Wear"}
                ],
                "default": "ethnic_wear"
            },
            {
                "key": "gender",
                "label": "Target Audience / Gender",
                "type": "select",
                "required": True,
                "options": [
                    {"id": "women", "label": "Women's Collection"},
                    {"id": "men", "label": "Men's Collection"},
                    {"id": "unisex", "label": "Unisex / Gen Z"},
                    {"id": "kids", "label": "Kids Wear"},
                    {"id": "couples", "label": "Matching Couples Wear"}
                ],
                "default": "women"
            },
            {
                "key": "collection",
                "label": "Collection / Season",
                "type": "text_or_select",
                "required": False,
                "placeholder": "e.g. Festive Diwali 2026, Summer Breeze, Monsoon Drop",
                "options": ["Summer Breeze 2026", "Festive Royal Drop", "Wedding Season Edition", "Monsoon Daily Wear", "Winter Chic"]
            },
            {
                "key": "style_or_fabric",
                "label": "Fabric & Style Highlight",
                "type": "text_or_select",
                "required": False,
                "placeholder": "e.g. 100% Pure Mulberry Silk, Breathable Cotton",
                "options": ["Pure Handloom Silk", "100% Breathable Organic Cotton", "Heavy Gold Zari Work", "Premium French Terry Cotton", "Wrinkle-free Linen"]
            },
            {
                "key": "offer",
                "label": "Offer / Sale",
                "type": "text_or_select",
                "required": False,
                "placeholder": "e.g. Flat 30% OFF, Buy 2 Get 1 Free",
                "options": ["Flat 30% OFF", "Buy 2 Get 1 Free", "Flat ₹500 OFF on First Order", "End of Season Sale - Up to 50% OFF", "Free Shipping on Prepaid Orders"]
            }
        ]
    },
    "real_estate": {
        "id": "real_estate",
        "name": "Real Estate & Housing",
        "icon": "Building",
        "description": "Property developers, brokers, luxury apartments, villas, and plots",
        "popular_items": ["Luxury 3 BHK Flats", "Gated Community Villas", "Commercial Office Spaces", "Open Residential Plots"],
        "fields": [
            {
                "key": "product",
                "label": "Property Name / Project Title",
                "type": "text_or_select",
                "required": True,
                "placeholder": "e.g. Green Meadows Luxury 3BHK, Skyline Tower",
                "options": ["Luxury 3 BHK High-Rise Apartment", "4 BHK Premium Gated Villa", "2 BHK Budget Friendly Flat", "Premium Commercial Office", "HMDA Approved Open Villa Plots"]
            },
            {
                "key": "property_type",
                "label": "Property Type",
                "type": "select",
                "required": True,
                "options": [
                    {"id": "apartment", "label": "Gated High-Rise Apartment"},
                    {"id": "villa", "label": "Independent Luxury Villa"},
                    {"id": "plot", "label": "Residential Layout / Plots"},
                    {"id": "commercial", "label": "Commercial Retail / Office"},
                    {"id": "penthouse", "label": "Sky Penthouse"}
                ],
                "default": "apartment"
            },
            {
                "key": "bedrooms",
                "label": "Bedrooms / Configuration",
                "type": "select",
                "required": False,
                "options": [
                    {"id": "2bhk", "label": "2 BHK (1200 - 1450 Sq.Ft)"},
                    {"id": "3bhk", "label": "3 BHK (1800 - 2400 Sq.Ft)"},
                    {"id": "4bhk", "label": "4 BHK Luxury (3200+ Sq.Ft)"},
                    {"id": "plots", "label": "Plots (150 - 500 Sq.Yds)"},
                    {"id": "studio", "label": "Studio / 1 BHK"}
                ],
                "default": "3bhk"
            },
            {
                "key": "price",
                "label": "Price / Starting Range",
                "type": "text_or_select",
                "required": False,
                "placeholder": "e.g. Starting from ₹75 Lakhs, ₹1.2 Cr onwards",
                "options": ["Starting at ₹65 Lakhs*", "₹1.10 Cr Onwards*", "₹2.5 Cr+ Luxury Segment", "Flexible ₹4,500/Sq.Ft*", "Easy 10:90 Payment Scheme"]
            },
            {
                "key": "amenities",
                "label": "Top Amenities & Highlights",
                "type": "text_or_select",
                "required": False,
                "placeholder": "e.g. 50,000 sq.ft Clubhouse, Infinity Pool, Metro 5 mins",
                "options": ["50,000 Sq.Ft Clubhouse & Pool", "100% Vastu Compliant & 80% Open Green Space", "5 Mins from Tech Hub / Metro", "EV Charging & Solar Powered", "Smart Home Automation"]
            },
            {
                "key": "offer",
                "label": "Special Booking Offer",
                "type": "text_or_select",
                "required": False,
                "placeholder": "e.g. Zero Pre-EMI till Possession, Free Modular Kitchen",
                "options": ["Zero Stamp Duty & Registration", "Free Modular Kitchen on Spot Booking", "No Pre-EMI till Possession", "Pre-Launch Price Benefit - Save ₹5 Lakhs", "Complimentary AC in All Bedrooms"]
            }
        ]
    },
    "salon": {
        "id": "salon",
        "name": "Salon, Spa & Beauty",
        "icon": "Scissors",
        "description": "Hair salons, beauty parlours, aesthetic spas, and bridal makeover studios",
        "popular_items": ["Bridal Makeover Package", "Keratin Hair Spa", "HydraFacial Glow", "Balayage Hair Color", "Aroma Therapy Massage"],
        "fields": [
            {
                "key": "product",
                "label": "Service / Treatment Name",
                "type": "text_or_select",
                "required": True,
                "placeholder": "e.g. HydraFacial Glow Therapy, Advanced Keratin Treatment",
                "options": ["Hydra Glow Deep Cleansing Facial", "Keratin Hair Smoothing Treatment", "Luxury Bridal Makeover Package", "Balayage & Hair Glossing", "Signature Swedish Full Body Spa", "Pedicure & Gel Nail Art"]
            },
            {
                "key": "service_type",
                "label": "Service Category",
                "type": "select",
                "required": True,
                "options": [
                    {"id": "hair_care", "label": "Hair Care & Styling"},
                    {"id": "skin_facial", "label": "Skin, Glow & Facials"},
                    {"id": "bridal_glam", "label": "Bridal & Party Makeup"},
                    {"id": "spa_wellness", "label": "Spa & Body Wellness"},
                    {"id": "nails_lashes", "label": "Nails & Lash Extensions"}
                ],
                "default": "hair_care"
            },
            {
                "key": "occasion",
                "label": "Occasion / Target Goal",
                "type": "text_or_select",
                "required": False,
                "placeholder": "e.g. Wedding Season, Festive Glow, Weekend Pamper",
                "options": ["Wedding & Pre-Bridal Glow", "Weekend Pamper Session", "Festival Special Glow", "Post-Sun Damage Repair", "Transformational Hair Makeover"]
            },
            {
                "key": "stylist_or_specialty",
                "label": "Specialty / Product Line",
                "type": "text_or_select",
                "required": False,
                "placeholder": "e.g. L'Oréal Professional, Organic Korean Skincare",
                "options": ["100% Organic & Chemical-Free", "L'Oréal & Olaplex Certified Stylists", "Celebrity Bridal Makeover Artist", "Dermatologically Tested Korean Actives"]
            },
            {
                "key": "offer",
                "label": "Promotion / Combo Deal",
                "type": "text_or_select",
                "required": False,
                "placeholder": "e.g. Flat 25% OFF on Combos, Free Hair Cut with Keratin",
                "options": ["Flat 25% OFF on First Visit", "Free Haircut + Wash with Color", "Full Glam Combo @ ₹1,999 Only", "Bridal Early Bird Discount - 20% OFF", "Book 2 Services, Get 1 Free"]
            }
        ]
    },
    "electronics": {
        "id": "electronics",
        "name": "Electronics & Gadgets",
        "icon": "Smartphone",
        "description": "Smartphones, laptops, smart TVs, home appliances, and audio gear",
        "popular_items": ["Flagship 5G Smartphone", "ANC Wireless Earbuds", "OLED Smart TV", "Gaming Laptop", "Smart Washing Machine"],
        "fields": [
            {
                "key": "product",
                "label": "Gadget / Product Name",
                "type": "text_or_select",
                "required": True,
                "placeholder": "e.g. Ultra 5G Smartphone 256GB, Sonic ANC Earbuds",
                "options": ["Next-Gen 5G Smartphone (256GB / 120Hz AMOLED)", "Active Noise Cancelling Wireless Earbuds", "55-inch 4K Ultra HD Smart TV", "RTX 4060 Gaming Laptop", "AI Direct Drive Smart Washing Machine"]
            },
            {
                "key": "category",
                "label": "Product Category",
                "type": "select",
                "required": True,
                "options": [
                    {"id": "smartphones", "label": "Smartphones & Tablets"},
                    {"id": "audio_wearables", "label": "Audio & Smartwatches"},
                    {"id": "laptops_computers", "label": "Laptops & Computing"},
                    {"id": "tv_appliances", "label": "TV & Home Appliances"},
                    {"id": "gaming_accessories", "label": "Gaming Gear & Accessories"}
                ],
                "default": "smartphones"
            },
            {
                "key": "specs_or_features",
                "label": "Key Specifications / USPs",
                "type": "text_or_select",
                "required": False,
                "placeholder": "e.g. 50MP Sony OIS Camera, 5000mAh Battery, Snapdragon 8 Gen 3",
                "options": ["50MP OIS Triple Camera + 120W Fast Charging", "40-Hour Playtime + 45dB Active Noise Cancellation", "144Hz Refresh Rate + Intel Core i7 14th Gen", "Dolby Vision + Atmos 60W Soundbar Included", "10-Year Motor Warranty + 5-Star Energy Rating"]
            },
            {
                "key": "offer",
                "label": "Offer / Exchange / Warranty",
                "type": "text_or_select",
                "required": False,
                "placeholder": "e.g. ₹5,000 Exchange Bonus, No-Cost EMI from ₹1,499/mo",
                "options": ["₹5,000 Instant Bank Discount", "No-Cost EMI Starting @ ₹1,499/mo", "Up to ₹8,000 Old Phone Exchange Bonus", "Free 2-Year Extended Warranty + Accidental Cover", "Free ₹2,499 Earbuds on Pre-Order"]
            }
        ]
    }
}

def get_all_industries() -> List[Dict[str, Any]]:
    return [
        {
            "id": ind["id"],
            "name": ind["name"],
            "icon": ind["icon"],
            "description": ind["description"],
            "popular_items": ind["popular_items"],
            "field_count": len(ind["fields"])
        }
        for ind in INDUSTRY_CONFIGS.values()
    ]

def get_industry_options(industry_id: str) -> Dict[str, Any]:
    industry = INDUSTRY_CONFIGS.get(industry_id.lower())
    if not industry:
        # Fallback to generic schema
        return {
            "industry": industry_id,
            "name": industry_id.capitalize(),
            "fields": [
                {"key": "product", "label": "Product / Service", "type": "text", "required": True},
                {"key": "objective", "label": "Campaign Objective", "type": "text", "required": False},
                {"key": "offer", "label": "Offer / Special Value", "type": "text", "required": False}
            ],
            "content_types": CONTENT_TYPES,
            "languages": SUPPORTED_LANGUAGES,
            "tones": SUPPORTED_TONES
        }
    
    return {
        "industry": industry["id"],
        "name": industry["name"],
        "icon": industry["icon"],
        "description": industry["description"],
        "fields": industry["fields"],
        "content_types": CONTENT_TYPES,
        "languages": SUPPORTED_LANGUAGES,
        "tones": SUPPORTED_TONES
    }
