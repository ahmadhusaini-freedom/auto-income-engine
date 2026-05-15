"""
Agen #3: Dev.to Auto-Publisher
Dev.to: platform developer, 1M+ pembaca aktif
API Key: dapatkan di dev.to/settings/extensions → DEV Community API Keys
Dev.to TIDAK membayar per read, tapi mendatangkan traffic ke Gumroad produk
"""

import os
import json
import requests

DEVTO_API_KEY = os.environ["DEVTO_API_KEY"]
BASE_URL = "https://dev.to/api"

def add_gumroad_cta(body_markdown: str, title: str) -> str:
    """Tambahkan CTA ke produk Gumroad di akhir artikel"""
    cta = f"""

---

## 🎁 Free Resource

If you found this article helpful, I've put together a complete **200 AI Prompts Pack** that covers marketing, content creation, business automation, and more — available on Gumroad.

👉 **[Get the 200 AI Prompts Pack ($7)](https://gumroad.com/l/YOUR-PRODUCT-SLUG)**

*Over 200 ready-to-use prompts for ChatGPT and Claude — organized by use case so you can start using them immediately.*

---

*If this helped you, consider following me for more AI productivity content. Drop a comment with your biggest takeaway!*
"""
    return body_markdown + cta

def publish_to_devto(article: dict) -> dict:
    """Publish artikel ke Dev.to"""
    headers = {
        "api-key": DEVTO_API_KEY,
        "Content-Type": "application/json"
    }
    
    # Tambah CTA ke Gumroad
    body_with_cta = add_gumroad_cta(article["body_markdown"], article["title"])
    
    # Format TL;DR sebagai markdown callout
    tldr_md = "\n".join([f"- {p}" for p in article["tldr"]])
    full_body = f"""**TL;DR:**
{tldr_md}

---

{body_with_cta}"""
    
    payload = {
        "article": {
            "title": article["title"],
            "body_markdown": full_body,
            "published": True,
            "tags": [t.lower().replace(" ", "")[:20] for t in article["tags"][:4]],
            "description": article["seo_description"],
            "canonical_url": None  # hapus jika ada canonical dari platform lain
        }
    }
    
    resp = requests.post(f"{BASE_URL}/articles", json=payload, headers=headers)
    resp.raise_for_status()
    
    result = resp.json()
    url = f"https://dev.to{result.get('path', '')}"
    print(f"[Dev.to Agent] ✓ Published: {url}")
    return result

def main():
    print("[Dev.to Agent] Memulai publish ke Dev.to...")
    
    with open("logs/today_article.json") as f:
        data = json.load(f)
    
    article = data["article"]
    result = publish_to_devto(article)
    
    # Update status
    data["status"]["devto"] = "published"
    data["devto_url"] = f"https://dev.to{result.get('path', '')}"
    data["devto_id"] = result.get("id", "")
    
    with open("logs/today_article.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[Dev.to Agent] ✓ Selesai — {data['devto_url']}")

if __name__ == "__main__":
    main()
