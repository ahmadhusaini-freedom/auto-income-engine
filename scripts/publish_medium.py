"""
Agen #2: Medium Auto-Publisher
Auto-publish artikel ke Medium Partner Program
Medium API: https://api.medium.com/v1
Token: dapatkan di medium.com/me/settings → Integration tokens
"""

import os
import json
import requests

MEDIUM_TOKEN = os.environ["MEDIUM_TOKEN"]
BASE_URL = "https://api.medium.com/v1"

def get_user_id() -> str:
    """Ambil Medium user ID dari token"""
    headers = {
        "Authorization": f"Bearer {MEDIUM_TOKEN}",
        "Content-Type": "application/json"
    }
    resp = requests.get(f"{BASE_URL}/me", headers=headers)
    resp.raise_for_status()
    user_id = resp.json()["data"]["id"]
    print(f"[Medium Agent] User ID: {user_id}")
    return user_id

def format_for_medium(article: dict) -> str:
    """Format artikel menjadi HTML untuk Medium"""
    tldr_items = "\n".join([f"<li>{p}</li>" for p in article["tldr"]])
    
    # Convert markdown headers ke HTML
    body = article["body_markdown"]
    lines = []
    for line in body.split("\n"):
        if line.startswith("## "):
            lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("- ") or line.startswith("* "):
            lines.append(f"<li>{line[2:]}</li>")
        elif line.startswith("**") and line.endswith("**"):
            lines.append(f"<strong>{line[2:-2]}</strong>")
        elif line.strip() == "":
            lines.append("<br>")
        else:
            lines.append(f"<p>{line}</p>")
    
    body_html = "\n".join(lines)
    
    content = f"""<h4>TL;DR</h4>
<ul>
{tldr_items}
</ul>
{body_html}"""
    
    return content

def publish_to_medium(article: dict) -> dict:
    """Publish artikel ke Medium"""
    user_id = get_user_id()
    
    headers = {
        "Authorization": f"Bearer {MEDIUM_TOKEN}",
        "Content-Type": "application/json"
    }
    
    content_html = format_for_medium(article)
    
    payload = {
        "title": article["title"],
        "contentFormat": "html",
        "content": content_html,
        "tags": article["tags"][:5],  # Medium max 5 tags
        "publishStatus": "public",
        "notifyFollowers": True
    }
    
    url = f"{BASE_URL}/users/{user_id}/posts"
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    
    result = resp.json()["data"]
    print(f"[Medium Agent] ✓ Published: {result['url']}")
    return result

def main():
    print("[Medium Agent] Memulai publish ke Medium...")
    
    with open("logs/today_article.json") as f:
        data = json.load(f)
    
    article = data["article"]
    result = publish_to_medium(article)
    
    # Update status
    data["status"]["medium"] = "published"
    data["medium_url"] = result.get("url", "")
    data["medium_id"] = result.get("id", "")
    
    with open("logs/today_article.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[Medium Agent] ✓ Selesai — {result.get('url')}")

if __name__ == "__main__":
    main()
