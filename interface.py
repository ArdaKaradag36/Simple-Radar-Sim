import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import radar  # radar.py 
import os

#  ARAYÜZ(FRONTEND)

plt.ion() # Canlı grafik modu
plt.style.use('dark_background')

# Pencere
fig, ax = plt.subplots(figsize=(12, 7))

# Sistem kontrol 
sistem_acik = True

def pencere_kapandi(event):
    global sistem_acik
    print("\n>> [X] PENCERE KAPATILDI. SİSTEM DURDURULUYOR...")
    sistem_acik = False

# Matplotlib(close_event)
fig.canvas.mpl_connect('close_event', pencere_kapandi)

print(">> ARAYÜZ BAŞLATILIYOR...")
print(">> RADAR MOTORUNA BAĞLANILIYOR...")

try:
    
    while sistem_acik:
        
        if not plt.fignum_exists(fig.number):
            break

         # DOSYADAN VERİ ÇEK 
        model, t_hiz, t_irtifa, d_hiz, d_irtifa = radar.radar_tarama_yap()
        
        # Ekranı Temizle 
        ax.clear()

        # 3. Arka Plan Tahmin Alanı
        xx, yy = np.meshgrid(np.arange(0, 4500, 100), np.arange(0, 70000, 1000))
        tahmin_alani = model.predict(pd.DataFrame({'HIZ_KMH': xx.ravel(), 'IRTIFA_FT': yy.ravel()}))
        tahmin_alani = tahmin_alani.reshape(xx.shape)
        ax.contourf(xx, yy, tahmin_alani, alpha=0.3, cmap="RdYlGn_r")

        # 4. Uçakları Çiz
        ax.scatter(t_hiz, t_irtifa, c='#ff3333', marker='^', s=60, label='TEHDİT (Unknown)', edgecolors='white', alpha=0.9)
        ax.scatter(d_hiz, d_irtifa, c='#00ff00', marker='o', s=60, label='DOST (Friendly)', edgecolors='black', alpha=0.9)

        # 5. Rastgele Anomali (Tespit Edilen Şüpheli Hedef)
        anomali_hiz = np.random.randint(2800, 3200)
        anomali_irtifa = np.random.randint(4000, 8000)
        
        ax.scatter(anomali_hiz, anomali_irtifa, 
                   c='cyan', marker='X', s=200, linewidth=2, label='ANOMALİ TESPİTİ')

        # 6. Yazılar 
        zaman = time.strftime('%H:%M:%S')
        ax.set_title(f"MİLLİ HAVA SAHASI - CANLI TARAMA EKRANI\n[DEV: ARDA KARADAĞ] - {zaman}", 
                     color='white', fontsize=14, fontname='Consolas')
        
        ax.set_xlabel("HEDEF HIZI (km/s)", color='lime')
        ax.set_ylabel("HEDEF İRTİFASI (ft)", color='lime')
        ax.set_xlim(0, 4500)
        ax.set_ylim(0, 70000)
        ax.grid(color='lime', linestyle=':', alpha=0.4)
        ax.legend(loc='upper left', facecolor='black', edgecolor='lime')

        print(f">> TARAMA YAPILDI: {zaman} - Veriler güncellendi.")

        #  KARA KUTU KAYDI (LOGGING)
        with open("kara_kutu_loglari.txt", "a", encoding="utf-8") as dosya:
            dosya.write(f"[{zaman}] TARAMA RAPORU:\n")
            dosya.write(f"   > GENEL DURUM: {len(t_hiz)} Tehdit | {len(d_hiz)} Dost Unsur tespit edildi.\n")
            dosya.write(f"   > [!] ANOMALİ TESPİTİ: Hız: {anomali_hiz} km/s - İrtifa: {anomali_irtifa} ft\n")
            dosya.write("-" * 60 + "\n")
            
        print(">> KARA KUTU GÜNCELLENDİ.")
        
        plt.draw()
        
        # --- DÜZELTME 3: AKILLI BEKLEME ---
        for _ in range(100):
            if not sistem_acik: # Çarpıya basıldı mı?
                break
            plt.pause(0.1) # 0.1 saniye bekle

except KeyboardInterrupt:
    print("\n>> SİSTEM KAPATILIYOR...")
    plt.close()

print(">> PROGRAM SONLANDI.")