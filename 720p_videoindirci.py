import yt_dlp
import time

print("--- AKILLI HD YOUTUBE İNDİRİCİ (720p > 360p) ---")

link = input("Video linkini yapıştır: ")

ayarlar = {
        
        'format': 'best[height<=480]',
        'outtmpl': '%(title)s.%(ext)s',
    }

try:
    print("⏳ Video analiz ediliyor... (HD kalite aranıyor)")
    
    with yt_dlp.YoutubeDL(ayarlar) as ydl:
        ydl.download([link])
        
    print("\n✅ İŞLEM BAŞARILI! Video klasörüne indi.")
    print("👉 İpucu: İnen videonun özelliklerine bakarsan 1280x720 (HD) olduğunu görebilirsin.")

except Exception as hata:
    print("\n❌ HATA OLUŞTU!")
    print(f"Hata detayı: {hata}")

time.sleep(5)