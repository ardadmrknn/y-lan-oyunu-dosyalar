"""
Ayarları kaydetme ve yükleme modülü
"""
import json
import os


class AyarYoneticisi:
    def __init__(self):
        self.ayar_dosyasi = "oyun_ayarlari.json"
        self.varsayilan_ayarlar = {
            "hiz_seviyesi": 1,  # Normal hız
            "en_yuksek_skor": 0,
            "menu_arkaplan": None,  # Menü arka plan resmi yolu
            "oyun_arkaplan": None,   # Oyun arka plan resmi yolu
            "yilan_renk": 0,  # Yeşil
            "yilan_yuz": 0,    # Normal
            "bomba_modu": False,  # Bomba modu kapalı
            "aktif_tema": "Klasik",  # Varsayılan tema
            "menu_muzik": "Normal",  # Ana menü müziği
            "oyun_muzik": "Normal",   # Oyun içi müziği
            "ses_acik": True,  # Ses efektleri açık
            "muzik_acik": True,  # Müzik açık
            "ses_seviyesi": 0.7,  # Ses efekti seviyesi
            "muzik_seviyesi": 0.5  # Müzik seviyesi
        }
    
    def ayarlari_yukle(self):
        """Ayarları dosyadan yükler"""
        try:
            if os.path.exists(self.ayar_dosyasi):
                with open(self.ayar_dosyasi, 'r', encoding='utf-8') as f:
                    ayarlar = json.load(f)
                    # Eski ayarları güncelle
                    for key in self.varsayilan_ayarlar:
                        if key not in ayarlar:
                            ayarlar[key] = self.varsayilan_ayarlar[key]
                    return ayarlar
            else:
                return self.varsayilan_ayarlar.copy()
        except Exception as e:
            print(f"Ayarlar yüklenirken hata: {e}")
            return self.varsayilan_ayarlar.copy()
    
    def ayarlari_kaydet(self, ayar_guncelleme=None):
        """Ayarları dosyaya kaydeder - tek ayar veya tüm ayarları"""
        try:
            # Mevcut ayarları yükle
            mevcut_ayarlar = self.ayarlari_yukle()
            
            if ayar_guncelleme is None:
                # Tüm ayarları kaydet
                ayarlar = mevcut_ayarlar
            elif isinstance(ayar_guncelleme, dict):
                # Sadece belirli ayarları güncelle
                ayarlar = mevcut_ayarlar.copy()
                ayarlar.update(ayar_guncelleme)
            else:
                # Eski format için geriye uyumluluk (tüm parametreler)
                # Bu kısım eski çağrılar için
                return
            
            with open(self.ayar_dosyasi, 'w', encoding='utf-8') as f:
                json.dump(ayarlar, f, indent=4)
        except Exception as e:
            print(f"Ayarlar kaydedilirken hata: {e}")
