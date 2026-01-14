import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

#  RADAR MOTORU (BACKEND)
# Bu dosya sadece veri üretir ve yapay zekayı eğitir.

def radar_tarama_yap():
    """
    Bu fonksiyon çağrıldığında o anki hava sahasını tarar,
    rastgele veriler üretir ve yapay zekayı eğitip geri gönderir.
    """
    
    # 1. Düşman Simülasyonu (Hızlı ve Yüksek İrtifa)
    tehdit_hiz = np.random.randint(2200, 3800, 200) 
    tehdit_irtifa = np.random.randint(25000, 65000, 200)
    tehdit_etiket = np.ones(200) # 1 = TEHDİT

    # 2. Dost Simülasyonu (Yavaş ve Alçak/Orta İrtifa)
    dost_hiz = np.random.randint(500, 1100, 200)
    dost_irtifa = np.random.randint(5000, 28000, 200)
    dost_etiket = np.zeros(200) # 0 = DOST

    # Verileri Birleştir (Pandas DataFrame)
    egitim_verisi = pd.DataFrame({
        'HIZ_KMH': np.concatenate([tehdit_hiz, dost_hiz]),
        'IRTIFA_FT': np.concatenate([tehdit_irtifa, dost_irtifa])
    })
    sonuclar = np.concatenate([tehdit_etiket, dost_etiket])

    # Modeli Eğit (Beyin burada çalışıyor)
    rf_model = RandomForestClassifier(n_estimators=50) 
    rf_model.fit(egitim_verisi, sonuclar)

    # Arayüze paketleri geri gönder
    return rf_model, tehdit_hiz, tehdit_irtifa, dost_hiz, dost_irtifa