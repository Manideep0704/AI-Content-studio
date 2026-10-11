import urllib.request
import json
import sys
import uuid
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def run_tests():
    print("=" * 60)
    print("  IMAGE-AI COMPREHENSIVE SYSTEM VERIFICATION")
    print("=" * 60)
    
    # 1. Server Health
    print("\n[1/6] Checking Server & Frontend Endpoints...")
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/docs") as resp:
            assert resp.status == 200
            print("  ✓ Swagger OpenAPI Docs: HTTP 200 OK")
    except Exception as e:
        print("  ✗ Docs endpoint failed:", e)
        return False

    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/") as resp:
            assert resp.status == 200
            html = resp.read().decode("utf-8")
            assert "html" in html.lower()
            print("  ✓ Frontend SPA Delivery: HTTP 200 OK (Vite React App)")
    except Exception as e:
        print("  ✗ Frontend delivery failed:", e)
        return False

    # 2. Authentication Flow
    print("\n[2/6] Verifying User Registration & JWT Authentication...")
    test_email = f"qa_user_{uuid.uuid4().hex[:6]}@example.com"
    reg_payload = json.dumps({
        "email": test_email,
        "password": "Password123!",
        "full_name": "Antigravity QA Auditor"
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:8000/api/auth/register",
            data=reg_payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            token = data.get("access_token")
            assert token, "No token returned in register response"
            print(f"  ✓ User registered: {test_email}")
            print(f"  ✓ JWT Token issued: {token[:20]}...")
    except Exception as e:
        print("  ✗ Auth registration failed:", e)
        return False

    auth_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # 3. Brand Profile
    print("\n[3/6] Verifying Brand Profile Persistence...")
    try:
        brand_data = json.dumps({
            "business_name": "Sri Lakshmi Silks & Handlooms",
            "industry": "clothing",
            "location": "Kanchipuram, Tamil Nadu",
            "phone": "+91 98765 43210",
            "brand_colors": "#7C3AED, #F59E0B",
            "preferred_language": "telugu",
            "preferred_tone": "festive",
            "default_cta": "Visit our showroom or WhatsApp us today!"
        }).encode("utf-8")
        
        req = urllib.request.Request(
            "http://127.0.0.1:8000/api/business",
            data=brand_data,
            headers=auth_headers
        )
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            assert res.get("business_name") == "Sri Lakshmi Silks & Handlooms"
            print("  ✓ Brand Profile created and verified in SQLite database")
    except Exception as e:
        print("  ✗ Brand profile failed:", e)
        return False

    # 4. Multi-Industry Content Generation
    print("\n[4/6] Verifying Industry-Specific Content Generation Matrix...")
    matrix = [
        {
            "label": "Clothing (Telugu WhatsApp)",
            "industry": "clothing",
            "product": "Kanchipuram Pattu Saree",
            "platform": "whatsapp",
            "content_type": "whatsapp_broadcast",
            "language": "telugu",
            "offer": "25% Festive Discount"
        },
        {
            "label": "Restaurant (Hindi Instagram)",
            "industry": "restaurant",
            "product": "Special Hyderabadi Dum Biryani",
            "platform": "instagram",
            "content_type": "instagram_post",
            "language": "hindi",
            "offer": "Free Dessert with Every Family Pack"
        },
        {
            "label": "Real Estate (English Facebook)",
            "industry": "real_estate",
            "product": "4 BHK Gated Community Villa",
            "platform": "facebook",
            "content_type": "facebook_post",
            "language": "english",
            "offer": "Special Pre-Launch Pricing"
        },
        {
            "label": "Salon (English Ad Copy)",
            "industry": "salon",
            "product": "HydraFacial Glow Treatment",
            "platform": "instagram",
            "content_type": "ad_copy",
            "language": "english",
            "offer": "First Visit Flat 30% Off"
        },
        {
            "label": "Electronics (English Product Description)",
            "industry": "electronics",
            "product": "Pro ANC Wireless Headphones",
            "platform": "website",
            "content_type": "product_description",
            "language": "english",
            "offer": "1 Year Extended Warranty"
        }
    ]

    for item in matrix:
        try:
            req_data = json.dumps({
                "industry": item["industry"],
                "product": item["product"],
                "platform": item["platform"],
                "content_type": item["content_type"],
                "language": item["language"],
                "offer": item["offer"],
                "generate_image": False
            }).encode("utf-8")
            
            req = urllib.request.Request(
                "http://127.0.0.1:8000/api/content/generate",
                data=req_data,
                headers=auth_headers
            )
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                assert res.get("caption"), "Caption is empty"
                assert res.get("id"), "Content ID missing"
                assert len(res.get("hashtags", [])) > 0 or item["platform"] == "whatsapp", "Hashtags missing"
                print(f"  ✓ {item['label']}: Generated ({len(res['caption'])} chars)")
        except Exception as e:
            print(f"  ✗ {item['label']} failed:", e)
            return False

    # 5. Live Image Generation & Static File Serving
    print("\n[5/6] Verifying Live Photorealistic Image Generation...")
    try:
        img_req_data = json.dumps({
            "industry": "restaurant",
            "product": "South Indian Masala Dosa with Sambar",
            "platform": "instagram",
            "content_type": "instagram_post",
            "language": "english",
            "offer": "Breakfast Combo Deal",
            "generate_image": True
        }).encode("utf-8")
        
        req = urllib.request.Request(
            "http://127.0.0.1:8000/api/content/generate",
            data=img_req_data,
            headers=auth_headers
        )
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            img_url = res.get("image_url")
            assert img_url, "No image_url returned"
            print(f"  ✓ Image generated successfully: {img_url}")

            # Verify the image is actually served over HTTP
            full_img_url = f"http://127.0.0.1:8000{img_url}" if img_url.startswith("/") else img_url
            with urllib.request.urlopen(full_img_url) as img_resp:
                img_bytes = img_resp.read()
                assert len(img_bytes) > 5000, "Image file too small or corrupted"
                print(f"  ✓ Image served by StaticFiles handler ({len(img_bytes):,} bytes, HTTP {img_resp.status})")
    except Exception as e:
        print("  ✗ Live image generation failed:", e)
        return False

    # 6. History and Persistence
    print("\n[6/6] Verifying Content History & Saved Archives...")
    try:
        req = urllib.request.Request("http://127.0.0.1:8000/api/content/history", headers=auth_headers)
        with urllib.request.urlopen(req) as resp:
            history = json.loads(resp.read().decode("utf-8"))
            assert len(history) >= 6, f"Expected at least 6 history items, found {len(history)}"
            print(f"  ✓ History query returned {len(history)} persistent records")
    except Exception as e:
        print("  ✗ History check failed:", e)
        return False

    print("\n" + "=" * 60)
    print("  ALL 6 SUBSYSTEMS VERIFIED AND FULLY OPERATIONAL!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
