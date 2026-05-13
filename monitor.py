import os
import json
from datetime import datetime
from xai_sdk import Client
from xai_sdk.chat import user
from xai_sdk.tools import x_search

def main():
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        print("❌ XAI_API_KEY bulunamadı!")
        return

    print("✅ API Key bulundu, işlem başlıyor...")
    client = Client(api_key=api_key)

    chat = client.chat.create(
        model="grok-4.3",
        tools=[x_search()],
    )

    prompt = """
    Search X (Twitter) for the last hour for content that expresses Islamophobia or anti-Muslim hatred.
    
    Include content that:
    - Portrays Islam or Muslims as an existential threat to Western civilization
    - Associates Muslims collectively with terrorism, grooming, rape, invasion, or crime
    - Dehumanizes Muslims as a group (vermin, cancer, plague, infestation, etc.)
    - Promotes great replacement / demographic replacement fears targeting Muslims
    - Calls for discrimination, deportation, or violence against Muslims as a group
    - Uses dog whistles: "they", "these people", "the religion of peace" (sarcastically), "medieval", "7th century", etc.
    - Frames any news event as proof that all Muslims are dangerous
    
    Do NOT include:
    - Criticism of specific political Islamic movements (Hamas, Taliban, etc.) without generalizing to all Muslims
    - Academic or journalistic analysis
    - Satire clearly not promoting hatred
    
    For each post found, return JSON array only, no explanation, format:
    [
      {
        "url": "https://x.com/...",
        "author": "@username",
        "content_summary": "what the post says",
        "category": "dehumanization | threat_narrative | crime_association | replacement_theory | dog_whistle | direct_hatred",
        "severity": 1-5,
        "engagement_estimate": "low|medium|high|viral"
      }
    ]
    
    If nothing found, return empty array: []
    """

    chat.append(user(prompt))
    response = chat.sample()

    # JSON parse et
    raw = response.content.strip()
    # Grok bazen ```json ``` ile sarar
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    
    try:
        results = json.loads(raw.strip())
    except json.JSONDecodeError:
        print(f"⚠️ JSON parse hatası, ham içerik kaydediliyor")
        results = [{"raw": raw}]

    # data/ klasörüne kaydet
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-00-00")
    filename = f"data/{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": timestamp,
            "count": len(results),
            "results": results
        }, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(results)} post bulundu → {filename}")

    # Mevcut index'i oku
    index_file = "data/index.json"
    try:
        with open(index_file, "r", encoding="utf-8") as f:
            index = json.load(f)
    except:
        index = []

    # Duplicate ekleme — zaten varsa ekleme
    if filename not in index:
        index.append(filename)
    index = sorted(set(index))[-168:]  # dedupe + sırala + son 168

    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

if __name__ == "__main__":
    main()
