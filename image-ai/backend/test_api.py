import sys
import os
import asyncio
import httpx
import json

# Ensure UTF-8 output for Windows console
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000/api"

async def run_acceptance_tests():
    print("\n=======================================================")
    print("🚀 STARTING NO-PROMPT SAAS BACKEND ACCEPTANCE TESTS")
    print("=======================================================\n")

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # 1. Health check
        res = await client.get("/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        print("✅ 1. Health check passed")

        # 2. Auth - Register & Login
        test_email = "owner@royalspice.com"
        reg_res = await client.post("/auth/register", json={
            "email": test_email,
            "password": "Password123!",
            "full_name": "Royal Spice Owner"
        })
        if reg_res.status_code == 200:
            token = reg_res.json()["access_token"]
            print("✅ 2. Auth - Registration successful")
        else:
            # Login if user already exists
            login_res = await client.post("/auth/login", json={
                "email": test_email,
                "password": "Password123!"
            })
            assert login_res.status_code == 200, f"Login failed: {login_res.text}"
            token = login_res.json()["access_token"]
            print("✅ 2. Auth - Login successful")

        headers = {"Authorization": f"Bearer {token}"}

        # 3. Brand Memory - Configure Brand Profile
        brand_res = await client.post("/business", headers=headers, json={
            "business_name": "Royal Spice Kitchen",
            "industry": "restaurant",
            "description": "Authentic Hyderabadi Dum Biryani & Kebabs",
            "location": "Banjara Hills, Hyderabad",
            "phone": "+91 98765 00000",
            "website": "https://royalspice.com",
            "brand_colors": "#EA580C, #F59E0B",
            "preferred_language": "telugu",
            "preferred_tone": "premium",
            "default_cta": "Visit Banjara Hills or Call +91 98765 00000"
        })
        assert brand_res.status_code == 200, f"Brand setup failed: {brand_res.text}"
        brand_data = brand_res.json()
        assert brand_data["business_name"] == "Royal Spice Kitchen"
        print(f"✅ 3. Brand Memory setup: {brand_data['business_name']} ({brand_data['location']})")

        # 4. Industry & Dynamic Options Check
        ind_res = await client.get("/industries")
        assert ind_res.status_code == 200
        industries = ind_res.json()
        assert len(industries) == 5, f"Expected 5 industries, got {len(industries)}"
        print(f"✅ 4. Industries verified: {[i['id'] for i in industries]}")

        rest_options = await client.get("/industries/restaurant/options")
        assert rest_options.status_code == 200
        options_data = rest_options.json()
        assert "fields" in options_data and len(options_data["fields"]) >= 4
        print(f"✅ 4b. Dynamic Questionnaire fields for restaurant: {[f['key'] for f in options_data['fields']]}")

        # 5. CRITICAL ACCEPTANCE TEST:
        # Restaurant -> Instagram Post -> Biryani -> Promotion -> 20% OFF -> Premium -> Telugu -> Generate
        print("\n--- RUNNING CRITICAL ACCEPTANCE TEST SCENARIO ---")
        gen_payload = {
            "industry": "restaurant",
            "content_type": "instagram_post",
            "product": "Biryani",
            "objective": "promotion",
            "offer": "20% OFF",
            "tone": "premium",
            "language": "telugu",
            "platform": "instagram",
            "length": "medium",
            "include_cta": True,
            "generate_image": True
        }
        gen_res = await client.post("/content/generate", headers=headers, json=gen_payload)
        assert gen_res.status_code == 200, f"Generation failed: {gen_res.text}"
        gen_data = gen_res.json()
        
        print("\nGENERATED TELUGU INSTAGRAM CONTENT:")
        print(f"ID: {gen_data['id']}")
        print(f"Caption: {gen_data['caption'][:120]}...")
        print(f"CTA: {gen_data['cta']}")
        print(f"Hashtags: {gen_data['hashtags']}")
        print(f"Image URL: {gen_data['image_url']}")
        print(f"Quality Score: {gen_data['quality_score']}")

        assert gen_data["caption"], "Caption must not be empty"
        assert gen_data["cta"], "CTA must not be empty"
        assert len(gen_data["hashtags"]) >= 2, "Hashtags must be present"
        assert gen_data["quality_score"] >= 0.7, "Quality score should be >= 0.7"
        content_id = gen_data["id"]
        print("✅ 5. Critical Acceptance Test generation PASSED")

        # 6. Companion Image Generation
        img_res = await client.post("/image/generate", headers=headers, json={
            "content_id": content_id,
            "industry": "restaurant",
            "product": "Biryani",
            "offer": "20% OFF",
            "business_name": "Royal Spice Kitchen"
        })
        assert img_res.status_code == 200
        img_data = img_res.json()
        assert img_data["image_url"]
        print(f"✅ 6. Image Generation PASSED: {img_data['image_url']}")

        # 7. Edit Content
        edit_res = await client.put(f"/content/{content_id}", headers=headers, json={
            "caption": gen_data["caption"] + "\n\n[Edited by User: Don't miss this weekend!]"
        })
        assert edit_res.status_code == 200
        assert "[Edited by User" in edit_res.json()["caption"]
        print("✅ 7. In-place content edit PASSED")

        # 8. Regenerate Content
        regen_res = await client.post("/content/regenerate", headers=headers, json={
            "content_id": content_id,
            "tone": "energetic",
            "offer": "Flat 25% OFF"
        })
        assert regen_res.status_code == 200
        print(f"✅ 8. Content Regeneration PASSED (Tone updated)")

        # 9. History Retrieval
        hist_res = await client.get("/content/history", headers=headers)
        assert hist_res.status_code == 200
        history_items = hist_res.json()
        assert len(history_items) >= 1
        print(f"✅ 9. History fetch PASSED ({len(history_items)} items found)")

        # 10. Usage Metrics
        usage_res = await client.get("/usage", headers=headers)
        assert usage_res.status_code == 200
        usage_data = usage_res.json()
        assert usage_data["total_generations"] >= 1
        print(f"✅ 10. Usage metrics PASSED: Total generations = {usage_data['total_generations']}")

        # 11. Multi-Industry & Language Matrix Test
        matrix_tests = [
            {"industry": "clothing", "content_type": "facebook_post", "product": "Kanchipuram Silk Saree", "language": "telugu", "tone": "premium"},
            {"industry": "real_estate", "content_type": "ad_copy", "product": "3 BHK Luxury Villa", "language": "english", "tone": "professional"},
            {"industry": "salon", "content_type": "whatsapp_message", "product": "HydraFacial Glow", "language": "hindi", "tone": "friendly"},
            {"industry": "electronics", "content_type": "reel_script", "product": "5G Flagship Smartphone", "language": "english", "tone": "energetic"}
        ]
        for t in matrix_tests:
            res = await client.post("/content/generate", headers=headers, json=t)
            assert res.status_code == 200, f"Matrix test failed for {t}: {res.text}"
            print(f"✅ Matrix Test passed: {t['industry'].upper()} ({t['language'].upper()} - {t['content_type']})")

    print("\n=======================================================")
    print("🎉 ALL 11 BACKEND ACCEPTANCE SUITE TESTS PASSED!")
    print("=======================================================\n")

if __name__ == "__main__":
    asyncio.run(run_acceptance_tests())
