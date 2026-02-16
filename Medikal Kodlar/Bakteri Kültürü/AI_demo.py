import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import time

def canli_demo_baslat():
   
    boyut = 150
    ai_sinir_degeri = 60
    
    plt.ion() 
    fig = plt.figure(figsize=(12, 8))
    fig.canvas.manager.set_window_title('Canlı AI Teşhis Simülasyonu')
    
    
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)

    
    bakteri_zemin = np.random.rand(boyut, boyut) * 0.4 + 0.6
    ilac_etki_alani = np.zeros((boyut, boyut))
    ilac_etki_alani[boyut//2, boyut//2] = 1.0 

    zamanlar = []
    skorlar = []
    aktif_skor = np.mean(bakteri_zemin) * 100

    print("=========================================================")
    print(" 🔴 CANLI SİMÜLASYON BAŞLADI: EKRANA ODAKLANIN")
    print("=========================================================\n")

    
    for t in range(0, 151, 5): 
        
        
        if t > 0:
            
            yayilim = gaussian_filter(ilac_etki_alani, sigma=t/2.0)
            yayilim = yayilim / (yayilim.max() + 1e-9) 
            
            guncel_petri = bakteri_zemin - (yayilim * 0.9)
            guncel_petri = np.clip(guncel_petri, 0, 1)
        else:
            guncel_petri = bakteri_zemin.copy()

        aktif_skor = np.mean(guncel_petri) * 100
        zamanlar.append(t)
        skorlar.append(aktif_skor)

        ax1.clear()
        ax2.clear()

        ax1.imshow(guncel_petri, cmap='jet', vmin=0, vmax=1)
        ax1.set_title(f"Lazer Analizi - Geçen Süre: {t} Dakika\nGüncel Hücre Canlılığı: %{aktif_skor:.1f}", fontsize=14, fontweight='bold')
        ax1.axis('off')

        ax2.plot(zamanlar, skorlar, marker='o', color='darkblue', linewidth=3, label='Gerçek Zamanlı Yapay Zeka Ölçümü')
        
        ax2.axhline(y=ai_sinir_degeri, color='red', linestyle='--', linewidth=2, label=f'Teşhis Sınırı (%{ai_sinir_degeri})')
        
        ax2.set_xlim(0, 150)
        ax2.set_ylim(0, 100)
        ax2.set_xlabel("Zaman (Dakika)", fontsize=12)
        ax2.set_ylabel("Canlılık Skoru (%)", fontsize=12)
        ax2.set_title("Canlılık Düşüş Grafiği", fontsize=14)
        ax2.legend(loc="upper right")
        ax2.grid(True, linestyle=':', alpha=0.7)

        plt.tight_layout()
        plt.pause(0.5) 

        if aktif_skor <= ai_sinir_degeri:
            ax2.text(t/2, ai_sinir_degeri/2, f"TEŞHİS ONAYLANDI!\nİlaç Etkili (Süre: {t} Dk)", 
                     color='green', fontsize=20, fontweight='bold', ha='center', va='center',
                     bbox=dict(facecolor='white', alpha=0.9, edgecolor='green', boxstyle='round,pad=1'))
            plt.draw() 
            print(f"\n[!!!] YAPAY ZEKA TEŞHİSİ KOYDU: İlaç işe yarıyor. Süre: {t} Dakika.")
            break 

    
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    canli_demo_baslat()

    #Bu simülasyon, yapay zekanın gerçek zamanlı olarak bir ilacın etkisini değerlendirdiği bir senaryoyu canlandırır.