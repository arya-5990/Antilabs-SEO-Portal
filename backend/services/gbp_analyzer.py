import os
import json
import re
import requests
from datetime import datetime

# Gemini client import – guarded in case the package is missing during local dev
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None  # Fallback: analysis will use mock data


def _get_mock_gbp_data() -> dict:
    """Returns mock data when no API keys are set."""
    return {
        "business_name": "Sample Business",
        "overall_score": 68,
        "category_scores": {
            "profile_completeness": 75,
            "keyword_optimization": 55,
            "reviews_engagement": 72,
            "visual_content": 50,
            "local_seo": 65
        },
        "trending_keywords": [
            "near me", "best in town", "affordable services",
            "top rated", "open now", "free consultation"
        ],
        "recommended_changes": [
            {
                "area": "Business Description",
                "current_state": "Generic description with no targeted keywords",
                "recommendation": "Rewrite description to include trending keywords like 'top rated', 'affordable services', and location-specific terms",
                "priority": "High",
                "estimated_impact": "20-30% more profile views"
            },
            {
                "area": "Business Categories",
                "current_state": "Only primary category is set",
                "recommendation": "Add 2-3 relevant secondary categories to appear in more search results",
                "priority": "High",
                "estimated_impact": "15-25% more discovery searches"
            },
            {
                "area": "Photos & Visual Content",
                "current_state": "Less than 5 photos uploaded",
                "recommendation": "Upload at least 10-15 high-quality photos including interior, exterior, team, and product shots",
                "priority": "Medium",
                "estimated_impact": "35% more clicks to website"
            },
            {
                "area": "Review Responses",
                "current_state": "Only 40% of reviews have owner responses",
                "recommendation": "Respond to all reviews within 24 hours, mentioning relevant keywords naturally",
                "priority": "Medium",
                "estimated_impact": "Improved trust signals and local ranking"
            },
            {
                "area": "Posts & Updates",
                "current_state": "No recent Google Posts found",
                "recommendation": "Publish weekly Google Posts with offers, events, or updates using trending keywords",
                "priority": "Low",
                "estimated_impact": "10-15% more engagement"
            }
        ],
        "quick_wins": [
            "Add business hours for holidays and special events",
            "Upload a cover photo and logo if missing",
            "Add all services/products with descriptions",
            "Enable messaging to allow direct customer inquiries",
            "Add a short business description (750 characters max)",
            "Respond to your 3 most recent reviews today"
        ],
        "competitor_keywords_to_target": [
            "best [your service] in [city]",
            "[service] near me",
            "affordable [service]",
            "top rated [service] [city]"
        ],
        "summary": "Your Google Business Profile has a solid foundation but is missing several optimization opportunities. The biggest gaps are in keyword optimization and visual content. Implementing the recommended changes — especially rewriting your description with trending keywords and adding more photos — could significantly boost your local search visibility."
    }


def analyze_gbp(profile_data: dict) -> dict:
    """
    Sends scraped Google Business Profile data to Groq or Gemini
    for deep GBP-specific SEO and trending keyword analysis.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    system_prompt = f"""
    You are an expert Google Business Profile (GBP) optimization specialist and local SEO consultant.
    Your goal is to analyze a Google Business Profile and generate a comprehensive optimization report
    with actionable recommendations based on latest trending keywords and SEO best practices.
    
    Current Date: {current_date}
    
    You will receive scraped data from a Google Business Profile page. The data may include:
    - business_name: The name of the business
    - title: The page title (usually "Business Name - Google Maps")
    - meta_description: Contains rating stars, business type, address
    - rating: The Google rating (e.g. "4.5")
    - review_count: Number of reviews
    - address: Physical address
    - categories: Business categories
    - phone: Phone number
    - website: Business website URL
    - text: Visible page text
    - og_image: Profile/cover image URL
    
    Use ALL available data to provide specific, data-driven recommendations.
    If the business name, rating, or address is available, reference them directly.
    If data is missing or thin, note that as an issue and provide educated recommendations
    based on the business type and location you can detect.
    
    Analyze the provided scraped data from a Google Business Profile page.
    Return a structured JSON response EXACTLY matching this format:
    
    {{
      "business_name": "The business name extracted from the profile",
      "overall_score": 78,
      "category_scores": {{
        "profile_completeness": 85,
        "keyword_optimization": 60,
        "reviews_engagement": 72,
        "visual_content": 55,
        "local_seo": 68
      }},
      "trending_keywords": [
        "keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5", "keyword 6"
      ],
      "recommended_changes": [
        {{
          "area": "Business Description",
          "current_state": "What is currently there or missing",
          "recommendation": "Specific actionable recommendation",
          "priority": "High",
          "estimated_impact": "20-30% more profile views"
        }},
        {{
          "area": "Another Area",
          "current_state": "Current state description",
          "recommendation": "Specific recommendation",
          "priority": "Medium",
          "estimated_impact": "Expected impact description"
        }}
      ],
      "quick_wins": [
        "Quick actionable item 1",
        "Quick actionable item 2",
        "Quick actionable item 3"
      ],
      "competitor_keywords_to_target": [
        "keyword competitors are ranking for 1",
        "keyword competitors are ranking for 2"
      ],
      "summary": "Brief executive summary of the profile's SEO health and top priorities."
    }}
    
    Guidelines:
    - Scores should be 0-100 based on how well optimized each area is
    - Include at least 4-6 recommended changes covering different areas (description, categories, photos, reviews, posts, Q&A, attributes, etc.)
    - Trending keywords should be specific to the business's industry and location if detectable
    - Quick wins should be things that can be done in under 10 minutes
    - Priority levels: "High", "Medium", "Low"
    - Be specific and actionable, not generic
    - If the scraped data is thin, make educated recommendations based on the business type/industry you can detect
    
    DO NOT include markdown formatting like ```json in the output, just return the raw JSON object.
    """

    user_prompt = f"""
    === GOOGLE BUSINESS PROFILE DATA ===
    {json.dumps(profile_data, indent=2)}
    """

    # 1. Check for OpenAI API Key first
    openai_api_key = os.environ.get("OPENAI_API_KEY", "")
    if openai_api_key and openai_api_key != "your_openai_api_key_here":
        try:
            model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
            print(f"[GBP-AI] Using OpenAI ({model}) for GBP analysis...")
            headers = {
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "response_format": {"type": "json_object"}
            }
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result_content = response.json()["choices"][0]["message"]["content"].strip()

            # Clean markdown wrappers if returned
            if result_content.startswith("```"):
                result_content = re.sub(r"^```json\s*|```$", "", result_content, flags=re.MULTILINE).strip()

            return json.loads(result_content)
        except Exception as e:
            print(f"[GBP-AI] OpenAI API call failed: {e}")
            return {"error": f"Failed to analyze GBP data with OpenAI: {str(e)}"}

    # 2. Check for Groq API Key fallback
    groq_api_key = os.environ.get("GROQ_API_KEY", "")
    if groq_api_key and groq_api_key != "your_groq_api_key_here":
        try:
            model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
            print(f"[GBP-AI] Using Groq ({model}) for GBP analysis...")
            headers = {
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "response_format": {"type": "json_object"}
            }
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            result_content = response.json()["choices"][0]["message"]["content"].strip()

            # Clean markdown wrappers if returned
            if result_content.startswith("```"):
                result_content = re.sub(r"^```json\s*|```$", "", result_content, flags=re.MULTILINE).strip()

            return json.loads(result_content)
        except Exception as e:
            print(f"[GBP-AI] Groq API call failed: {e}")
            return {"error": f"Failed to analyze GBP data with Groq: {str(e)}"}

    # 3. Check for Gemini API Key fallback
    gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
    if gemini_api_key and gemini_api_key != "your_gemini_api_key_here":
        try:
            if not genai:
                raise ImportError("google-genai SDK is not installed")

            print("[GBP-AI] Using Gemini (gemini-2.5-flash) for GBP analysis...")
            client = genai.Client(api_key=gemini_api_key)
            prompt = system_prompt + "\n\n" + user_prompt

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    response_mime_type="application/json",
                ),
            )
            result_content = response.text.strip()

            # Clean markdown wrappers if returned
            if result_content.startswith("```"):
                result_content = re.sub(r"^```json\s*|```$", "", result_content, flags=re.MULTILINE).strip()

            return json.loads(result_content)
        except Exception as e:
            print(f"[GBP-AI] Gemini API call failed: {e}")
            return {"error": f"Failed to analyze GBP data with Gemini: {str(e)}"}

    # 4. Fallback to mock data if no keys are set
    print("[GBP-AI] No API keys configured. Returning mock GBP report data.")
    return _get_mock_gbp_data()
