import os
from datetime import datetime
from xai_sdk import Client
from xai_sdk.chat import user
from xai_sdk.tools import x_search

def main():
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        print("XAI_API_KEY bulunamadı!")
        return

    client = Client(api_key=api_key)
    
    chat = client.chat.create(
        model="grok-4.1-fast-reasoning",   # veya grok-4.3   (ucuz olsun diye fast öneririm)
        tools=[x_search()],
    )
    
    prompt = """
    Son 24 saatte X'te İslamofobik, anti-Muslim, genelleyici olumsuz içerikleri semantic olarak ara.
    'İslam = cancer/evil/istila/terör', Muslims = grooming/rape/takeover gibi temaları bul.
    En çarpıcı 5-10 örneği listele, özetle ve genel trend hakkında kısa yorum yap.
    """
    
    chat.append(user(prompt))
    response = chat.sample()
    
    # Sonuçları dosyaya kaydet
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    with open(f"results_{timestamp}.md", "w", encoding="utf-8") as f:
        f.write(f"# İslamofobi Monitor - {timestamp}\n\n")
        f.write(response.content)
    
    print("✅ İşlem tamamlandı. Sonuçlar kaydedildi.")

if __name__ == "__main__":
    main()
