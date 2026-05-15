"""
Agen #1: AI Article Generator
Menggunakan Google Gemini 1.5 Flash (GRATIS — 1 juta token/hari)
Menghasilkan artikel 1.200–1.800 kata berkualitas tinggi
"""

import os
import json
import datetime
import requests

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def load_today_topic():
    """Pilih topik berdasarkan hari ke berapa (rotasi)"""
    with open("config/topics.json") as f:
        config = json.load(f)
    topics = config["topics"]
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    topic = topics[day_of_year % len(topics)]
    print(f"[AI Agent] Topik hari ini: {topic['title']}")
    return topic

def generate_article(topic: dict) -> dict:
    """Panggil Gemini API untuk generate artikel"""
    
    prompt = f"""You are an expert content writer for Medium, Dev.to, and tech blogs. 
Write a comprehensive, engaging article with the following specifications:

TITLE: {topic['title']}
KEYWORDS: {', '.join(topic['keywords'])}
TARGET AUDIENCE: {topic['target_audience']}
TONE: {topic['tone']}
NICHE: {topic['niche']}

ARTICLE REQUIREMENTS:
- Length: 1,200–1,600 words
- Structure: TL;DR (3 bullet points) → Introduction → 4-6 main sections with H2 headers → Conclusion
- Writing style: Conversational yet authoritative, like a smart friend sharing real insights
- Include: specific examples, data points, and actionable takeaways
- End with: a question to readers that encourages comments
- SEO: naturally weave in keywords without keyword stuffing
- No fluff: every sentence must add value

OUTPUT FORMAT (JSON only, no markdown wrapper):
{{
  "title": "exact article title",
  "subtitle": "compelling 1-sentence subtitle under 120 chars",
  "tldr": ["point 1", "point 2", "point 3"],
  "body_markdown": "full article in markdown format",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "seo_description": "meta description under 160 chars",
  "reading_time_minutes": 6
}}

Write the complete article now. Return ONLY valid JSON."""

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 4096,
            "responseMimeType": "application/json"
        }
    }
    
    print("[AI Agent] Memanggil Gemini API...")
    response = requests.post(GEMINI_URL, json=payload, params=params)
    response.raise_for_status()
    
    raw = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    
    # Bersihkan jika ada markdown wrapper
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    
    article = json.loads(raw)
    print(f"[AI Agent] Artikel generated: {article['title']} ({article['reading_time_minutes']} menit baca)")
    return article

def save_article(article: dict, topic: dict):
    """Simpan artikel ke file untuk dipakai script publish"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    output = {
        "date": today,
        "topic": topic,
        "article": article,
        "status": {
            "medium": "pending",
            "devto": "pending", 
            "hashnode": "pending"
        }
    }
    
    os.makedirs("logs", exist_ok=True)
    filename = f"logs/article_{today}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # Juga simpan ke file shared untuk script lain
    with open("logs/today_article.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"[AI Agent] Artikel disimpan: {filename}")
    return filename

def main():
    print("=" * 50)
    print("[AI Content Engine] Mulai generate artikel...")
    print("=" * 50)
    
    topic = load_today_topic()
    article = generate_article(topic)
    save_article(article, topic)
    
    print("[AI Agent] ✓ Generate selesai — siap dipublish ke semua platform")

if __name__ == "__main__":
    main()
