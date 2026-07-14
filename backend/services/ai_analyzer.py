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

def _get_mock_data() -> dict:
    """Returns mock data when no API keys are set."""
    return {
      "our_score": 75,
      "competitor_score": 88,
      "content_quality": {
        "our_website": "The content covers the basics but lacks depth and modern structuring. Meta tags are missing in some areas.",
        "competitor_website": "Highly detailed content with proper H1/H2 hierarchy, semantic HTML, and excellent keyword placement."
      },
      "trending_keywords": [
        "AI analytics", "real-time metrics", "automated forecasting", "predictive modeling"
      ],
      "comparison_table": [
        {"feature": "Mobile Responsiveness", "our_status": "Average", "competitor_status": "Excellent"},
        {"feature": "Page Load Speed", "our_status": "Slow (3.5s)", "competitor_status": "Fast (1.2s)"},
        {"feature": "Keyword Density", "our_status": "Low", "competitor_status": "Optimal"}
      ],
      "strengths_weaknesses": {
        "our_strengths": ["Clean UI", "Easy navigation"],
        "our_weaknesses": ["Thin content", "Missing alt text", "Slow load times"],
        "competitor_strengths": ["Strong backlink profile", "Fast performance", "Comprehensive guides"],
        "competitor_weaknesses": ["Complex pricing page"]
      },
      "actionable_suggestions": [
        {"priority": "High", "suggestion": "Optimize images to improve page load speed to under 2 seconds."},
        {"priority": "High", "suggestion": "Add trending keywords like 'predictive modeling' to main headers."},
        {"priority": "Medium", "suggestion": "Improve content depth on product pages to match competitor's detail."}
      ]
    }

def analyze_competitors(our_data: dict, competitor_data: dict) -> dict:
    """
    Sends scraped data to Grok or Gemini for deep SEO and trending topics analysis.
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    system_prompt = f"""
    You are an expert full-stack developer and elite SEO Specialist. 
    Your goal is to compare 'Our Website' with a 'Competitor Website' and provide deep analysis, 
    especially focusing on current trending topics and keywords to make our website rank higher.
    
    Current Date: {current_date}
    
    Analyze the provided scraped data for both websites. 
    Return a structured JSON response EXACTLY matching this format:
    
    {{
      "our_score": 85,
      "competitor_score": 90,
      "content_quality": {{
        "our_website": "Brief analysis of our content quality.",
        "competitor_website": "Brief analysis of their content quality."
      }},
      "trending_keywords": [
        "keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5"
      ],
      "comparison_table": [
        {{"feature": "Meta Description Optimization", "our_status": "Good", "competitor_status": "Excellent"}},
        {{"feature": "H1/H2 Tag Usage", "our_status": "Missing H1", "competitor_status": "Well Structured"}},
        {{"feature": "Content Depth", "our_status": "Moderate", "competitor_status": "Comprehensive"}}
      ],
      "strengths_weaknesses": {{
        "our_strengths": ["Strength 1", "Strength 2"],
        "our_weaknesses": ["Weakness 1", "Weakness 2"],
        "competitor_strengths": ["Strength 1", "Strength 2"],
        "competitor_weaknesses": ["Weakness 1", "Weakness 2"]
      }},
      "actionable_suggestions": [
        {{"priority": "High", "suggestion": "Add trending keyword X to H1."}},
        {{"priority": "Medium", "suggestion": "Expand content on topic Y."}}
      ]
    }}
    
    Make the analysis industry-specific (e.g. EdTech) if you can detect it from the content, 
    or default to general best practices. DO NOT include markdown formatting like ```json in the output, 
    just return the raw JSON object.
    """
    
    user_prompt = f"""
    === OUR WEBSITE DATA ===
    {json.dumps(our_data, indent=2)}
    
    === COMPETITOR WEBSITE DATA ===
    {json.dumps(competitor_data, indent=2)}
    """
    
    # 1. Check for OpenAI API Key first
    openai_api_key = os.environ.get("OPENAI_API_KEY", "")
    if openai_api_key and openai_api_key != "your_openai_api_key_here":
        try:
            model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
            print(f"[AI] Using OpenAI ({model}) for SEO analysis...")
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
            print(f"[AI] OpenAI API call failed: {e}")
            return {"error": f"Failed to analyze data with OpenAI: {str(e)}"}

    # 2. Check for Groq (groq.com) API Key fallback
    groq_api_key = os.environ.get("GROQ_API_KEY", "")
    if groq_api_key and groq_api_key != "your_groq_api_key_here":
        try:
            model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
            print(f"[AI] Using Groq ({model}) for SEO analysis...")
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
            print(f"[AI] Groq API call failed: {e}")
            return {"error": f"Failed to analyze data with Groq: {str(e)}"}

    # 3. Check for Gemini API Key fallback
    gemini_api_key = os.environ.get("GEMINI_API_KEY", "")
    if gemini_api_key and gemini_api_key != "your_gemini_api_key_here":
        try:
            if not genai:
                raise ImportError("google-genai SDK is not installed")
                
            print("[AI] Using Gemini (gemini-2.5-flash) for SEO analysis...")
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
            print(f"[AI] Gemini API call failed: {e}")
            return {"error": f"Failed to analyze data with Gemini: {str(e)}"}

    # 4. Fallback to mock data if no keys are set
    print("[AI] No API keys configured. Returning mock report data.")
    return _get_mock_data()
