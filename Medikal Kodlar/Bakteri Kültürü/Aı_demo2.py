import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import matplotlib.gridspec as gridspec
import time
import os
import datetime 

def tam_otomasyon_demo():
    boyut = 150
    ai_sinir_degeri = 20 
    
    plt.ion() 
    fig = plt.figure(figsize=(15, 9))
    fig.canvas.manager.set_window_title('Lazer Biospeckle Klinik Dashboard V4.0')
    
    
    fig.suptitle("HASTANE OTOMASYONU | Hasta ID: #84729 | Numune: Kan Kültürü | Tarih: Bugün", 
                 fontsize=14, fontweight='bold', color='black', backgroundcolor='lightgray')

    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1.2])
    ax_duyarli = fig.add_subplot(gs[0, 0])  
    ax_direncli = fig.add_subplot(gs[0, 1]) 
    ax_grafik = fig.add_subplot(gs[1, :])   

    zemin_duyarli = np.random.rand(boyut, boyut) * 0.4 + 0.6
    zemin_direncli = np.random.rand(boyut, boyut) * 0.4 + 0.6
    
    ilac_damlasi = np.zeros((boyut, boyut))
    ilac_damlasi[boyut//2, boyut//2] = 1.0 

    zamanlar = []
    skorlar_duyarli = []
    skorlar_direncli = []

    print("----------------------------------------------------------")
    print(" 🏥 HBYS ENTEGRELİ KLİNİK SİMÜLASYON BAŞLADI")
    print("----------------------------------------------------------\n")

    for t in range(0, 151, 5): 
        
        if t > 0:
            yayilim = gaussian_filter(ilac_damlasi, sigma=t/2.0)
            yayilim = yayilim / (yayilim.max() + 1e-9) 
            
           
            guncel_duyarli = zemin_duyarli - (yayilim * 1.5)
            
            guncel_direncli = zemin_direncli - (yayilim * 0.1)
        else:
            guncel_duyarli = zemin_duyarli.copy()
            guncel_direncli = zemin_direncli.copy()

        guncel_duyarli = np.clip(guncel_duyarli, 0, 1)
        guncel_direncli = np.clip(guncel_direncli, 0, 1)

        
        gurultu_1 = np.random.uniform(-1.2, 1.2)
        gurultu_2 = np.random.uniform(-1.5, 1.5)

        aktif_skor_duyarli = (np.mean(guncel_duyarli) * 100) + gurultu_1
        aktif_skor_direncli = (np.mean(guncel_direncli) * 100) + gurultu_2
        
       
        guven_skoru = min(99.9, max(12.5, 100 - (aktif_skor_duyarli - ai_sinir_degeri) * 1.2))

        zamanlar.append(t)
        skorlar_duyarli.append(aktif_skor_duyarli)
        skorlar_direncli.append(aktif_skor_direncli)

        ax_duyarli.clear()
        ax_direncli.clear()
        ax_grafik.clear()

        ax_duyarli.imshow(guncel_duyarli, cmap='jet', vmin=0, vmax=1)
        ax_duyarli.set_title(f"💊 İLAÇ A (Duyarlı)\nHücre Canlılığı: %{aktif_skor_duyarli:.1f}", fontsize=12, fontweight='bold', color='green')
        ax_duyarli.axis('off')

        ax_direncli.imshow(guncel_direncli, cmap='jet', vmin=0, vmax=1)
        ax_direncli.set_title(f"⚠️ İLAÇ B (Dirençli)\nHücre Canlılığı: %{aktif_skor_direncli:.1f}", fontsize=12, fontweight='bold', color='red')
        ax_direncli.axis('off')

        ax_grafik.plot(zamanlar, skorlar_duyarli, marker='o', color='green', linewidth=3, label='İlaç A (Etkili)')
        ax_grafik.plot(zamanlar, skorlar_direncli, marker='s', color='darkred', linewidth=3, label='İlaç B (Etkisiz/Dirençli)')
        
        ax_grafik.axhline(y=ai_sinir_degeri, color='black', linestyle='--', linewidth=2, label=f'Klinik İnhibisyon Eşiği (%{ai_sinir_degeri})')
        
        ax_grafik.set_xlim(0, 150)
        ax_grafik.set_ylim(0, 100)
        ax_grafik.set_xlabel("Analiz Süresi (Dakika)", fontsize=12)
        ax_grafik.set_ylabel("Ortalama Canlılık Skoru (%)", fontsize=12)
        
        ax_grafik.set_title(f"Gerçek Zamanlı Karar Destek Paneli | Yapay Zeka Teşhis Güveni: %{guven_skoru:.1f}", 
                            fontsize=14, fontweight='bold', color='darkblue')
        ax_grafik.legend(loc="upper right")
        ax_grafik.grid(True, linestyle=':', alpha=0.7)

        plt.tight_layout()
        plt.pause(0.3) 

       
        if aktif_skor_duyarli <= ai_sinir_degeri:
           
            ax_grafik.text(t/2, ai_sinir_degeri + 30, f"✅ ONAY: İlaç A Etkili (Süre: {t} Dk)\n❌ İPTAL: İlaç B Dirençli\n📄 Sistem Raporu Oluşturuldu!", 
                     color='white', fontsize=16, fontweight='bold', ha='center', va='center',
                     bbox=dict(facecolor='darkgreen', alpha=0.9, edgecolor='black', boxstyle='round,pad=1'))
            plt.draw()
            
            
            zaman_etiketi = datetime.datetime.now().strftime("%H%M%S") # Örn: 142530 (Saat:Dakika:Saniye)
            rapor_adi = f"Hasta_Klinik_Raporu_{zaman_etiketi}.txt"
            
           
            with open(rapor_adi, "w", encoding="utf-8") as dosya:
                dosya.write("==================================================\n")
                dosya.write("   LAZER BIOSPECKLE HIZLI ANTİBİYOGRAM RAPORU\n")
                dosya.write("==================================================\n")
                dosya.write("Hasta ID      : #84729\n")
                dosya.write("Numune Tipi   : Kan Kültürü\n")
                dosya.write(f"Rapor Saati   : {datetime.datetime.now().strftime('%H:%M:%S')}\n")
                dosya.write("==================================================\n")
                dosya.write(f"Analiz Süresi : {t} Dakika\n")
                dosya.write(f"Yapay Zeka Güven Skoru : %{guven_skoru:.1f}\n")
                dosya.write("--------------------------------------------------\n")
                dosya.write("[SONUÇLAR]\n")
                dosya.write("-> İLAÇ A : DUYARLI (Hücre canlılığı eşiğin altına indi)\n")
                dosya.write("-> İLAÇ B : DİRENÇLİ (Hücre canlılığı devam ediyor)\n")
                dosya.write("==================================================\n")
                dosya.write("Sistem Onayı: OTOMATİK ONAYLANDI\n")
                dosya.write("Hekim Kaşe/İmza: ................................\n")
            
            
            tam_yol = os.path.abspath(rapor_adi)
            print(f"\n[!!!] TEŞHİS KONULDU VE RAPOR HAZIRLANDI [!!!]")
            print(f"📍 Rapor Dosyası Şuraya Kaydedildi: \n-> {tam_yol}")
            break

    plt.ioff()
    plt.show()

if __name__ == "__main__":
    tam_otomasyon_demo()