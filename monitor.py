import os
from datetime import datetime
from xai_sdk import Client
from xai_sdk.chat import user
from xai_sdk.tools import x_search

def main():
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        print("❌ XAI_API_KEY bulunamadı! Secrets kısmını kontrol et.")
        return

    print("✅ API Key bulundu, işlem başlıyor...")

    client = Client(api_key=api_key)
    
    chat = client.chat.create(
        model="grok-4.3",          # En stabil model
        tools=[x_search()],
    )
    
    prompt = """
    Son 24 saatte X'te İslam, Müslümanlar hakkında en olumsuz, genelleyici ve İslamofobi içeren içerikleri semantic olarak bul.
    Örnek temalar: İslam = cancer/evil/istila, Muslims ile ilgili grooming, terror, takeover gibi genellemeler.
    En çarpıcı 5-8 örneği post linkleriyle birlikte listele ve kısa özetle.
    """
    
    chat.append(user(prompt))
    response = chat.sample()
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"results_{timestamp}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# İslamofobi Monitor - {timestamp}\n\n")
        f.write(response.content)
    
    print(f"✅ Başarılı! Sonuçlar {filename} dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
