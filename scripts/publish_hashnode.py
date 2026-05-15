"""
Agen #4: Hashnode Auto-Publisher
Hashnode: platform blog developer dengan SEO kuat
GraphQL API: hashnode.com/settings/developer → Personal Access Token
Publication ID: ada di hashnode.com/BLOG-NAME → Settings → General
"""

import os
import json
import requests

HASHNODE_TOKEN = os.environ["HASHNODE_TOKEN"]
HASHNODE_PUBLICATION_ID = os.environ["HASHNODE_PUBLICATION_ID"]
GRAPHQL_URL = "https://gql.hashnode.com"

def publish_to_hashnode(article: dict) -> dict:
    """Publish ke Hashnode via GraphQL"""
    
    headers = {
        "Authorization": HASHNODE_TOKEN,
        "Content-Type": "application/json"
    }
    
    # Format TL;DR
    tldr_items = "\n".join([f"- {p}" for p in article["tldr"]])
    full_content = f"""**TL;DR:**
{tldr_items}

---

{article['body_markdown']}

---

*Follow for more AI and productivity content. Drop a comment — I read everything!*"""
    
    # GraphQL mutation untuk create post
    mutation = """
    mutation PublishPost($input: PublishPostInput!) {
      publishPost(input: $input) {
        post {
          id
          title
          url
          slug
        }
      }
    }
    """
    
    variables = {
        "input": {
            "title": article["title"],
            "subtitle": article["subtitle"],
            "publicationId": HASHNODE_PUBLICATION_ID,
            "contentMarkdown": full_content,
            "tags": [],
            "metaTags": {
                "title": article["title"],
                "description": article["seo_description"]
            },
            "publishedAt": None  # publish sekarang
        }
    }
    
    resp = requests.post(
        GRAPHQL_URL,
        json={"query": mutation, "variables": variables},
        headers=headers
    )
    resp.raise_for_status()
    
    result = resp.json()
    if "errors" in result:
        print(f"[Hashnode Agent] ⚠ GraphQL error: {result['errors']}")
        return {}
    
    post = result["data"]["publishPost"]["post"]
    print(f"[Hashnode Agent] ✓ Published: {post['url']}")
    return post

def main():
    print("[Hashnode Agent] Memulai publish ke Hashnode...")
    
    with open("logs/today_article.json") as f:
        data = json.load(f)
    
    article = data["article"]
    result = publish_to_hashnode(article)
    
    if result:
        data["status"]["hashnode"] = "published"
        data["hashnode_url"] = result.get("url", "")
        data["hashnode_id"] = result.get("id", "")
    else:
        data["status"]["hashnode"] = "failed"
    
    with open("logs/today_article.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("[Hashnode Agent] ✓ Selesai")

if __name__ == "__main__":
    main()
