import json
import os
from datetime import datetime

class IstatistikTakipci:
    def __init__(self):
        self.dosya_yolu = "istatistikler.json"
        self.istatistikler = self._varsayilan_istatistikler()
        self._istatistikleri_yukle()
        
        # Mevcut oyun istatistikleri
        self.mevcut_yem_sayisi = 0
        self.mevcut_altin_elma = 0
        self.mevcut_elmas = 0
        self.mevcut_bomba_kacinma = 0
    
    def _varsayilan_istatistikler(self):
        return {
            "toplam_oyun": 0,
            "toplam_skor": 0,
            "en_yuksek_skor": 0,
            "toplam_yem": 0,
            "toplam_altin_elma": 0,
            "toplam_elmas": 0,
            "en_uzun_yilan": 3,
            "toplam_olum": 0,
            "duvara_carpma": 0,
            "kendine_carpma": 0,
            "bombaya_carpma": 0,
            "pvp_kaybedilen": 0,  # PVP/Bot modunda kaybedilen
            "pvp_kazanilan": 0,   # PVP/Bot modunda kazanılan
            "toplam_oyun_suresi": 0,  # saniye
            "mod_istatistikleri": {
                "Normal": {"oyun": 0, "en_yuksek": 0},
                "Bomb Modu": {"oyun": 0, "en_yuksek": 0}
            },
            "ilk_oyun_tarihi": None,
            "son_oyun_tarihi": None
        }
    
    def _istatistikleri_yukle(self):
        """Kaydedilmiş istatistikleri yükle"""
        if os.path.exists(self.dosya_yolu):
            try:
                with open(self.dosya_yolu, 'r', encoding='utf-8') as f:
                    yuklenen = json.load(f)
                    # Eksik alanları varsayılanlarla doldur
                    for anahtar, deger in self._varsayilan_istatistikler().items():
                        if anahtar not in yuklenen:
                            yuklenen[anahtar] = deger
                    self.istatistikler = yuklenen
            except Exception as e:
                print(f"İstatistikler yüklenirken hata: {e}")
    
    def _istatistikleri_kaydet(self):
        """İstatistikleri dosyaya kaydet"""
        try:
            with open(self.dosya_yolu, 'w', encoding='utf-8') as f:
                json.dump(self.istatistikler, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"İstatistikler kaydedilemedi: {e}")
    
    def oyun_basladi(self):
        """Yeni oyun başladığında çağrılır"""
        self.mevcut_yem_sayisi = 0
        self.mevcut_altin_elma = 0
        self.mevcut_elmas = 0
        self.mevcut_bomba_kacinma = 0
        
        # İlk oyun tarihi
        if self.istatistikler["ilk_oyun_tarihi"] is None:
            self.istatistikler["ilk_oyun_tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def oyun_bitti(self, skor, yilan_uzunluk, mod, olum_nedeni, oyun_suresi):
        """Oyun bittiğinde istatistikleri güncelle"""
        self.istatistikler["toplam_oyun"] += 1
        self.istatistikler["toplam_skor"] += skor
        self.istatistikler["toplam_yem"] += self.mevcut_yem_sayisi
        self.istatistikler["toplam_altin_elma"] += self.mevcut_altin_elma
        self.istatistikler["toplam_elmas"] += self.mevcut_elmas
        self.istatistikler["toplam_oyun_suresi"] += int(oyun_suresi)
        self.istatistikler["son_oyun_tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # En yüksek skor
        if skor > self.istatistikler["en_yuksek_skor"]:
            self.istatistikler["en_yuksek_skor"] = skor
        
        # En uzun yılan
        if yilan_uzunluk > self.istatistikler["en_uzun_yilan"]:
            self.istatistikler["en_uzun_yilan"] = yilan_uzunluk
        
        # Mod istatistikleri
        if mod not in self.istatistikler["mod_istatistikleri"]:
            self.istatistikler["mod_istatistikleri"][mod] = {"oyun": 0, "en_yuksek": 0}
        
        self.istatistikler["mod_istatistikleri"][mod]["oyun"] += 1
        if skor > self.istatistikler["mod_istatistikleri"][mod]["en_yuksek"]:
            self.istatistikler["mod_istatistikleri"][mod]["en_yuksek"] = skor
        
        # Ölüm nedenleri
        self.istatistikler["toplam_olum"] += 1
        if olum_nedeni == "duvar":
            self.istatistikler["duvara_carpma"] += 1
        elif olum_nedeni == "kendi":
            self.istatistikler["kendine_carpma"] += 1
        elif olum_nedeni == "bomba":
            self.istatistikler["bombaya_carpma"] += 1
        elif "oyuncu_kazandi" in olum_nedeni or "pvp_oyuncu1_kazandi" in olum_nedeni:
            # Oyuncu kazandı (PVP veya Bot modunda)
            if "pvp_kazanilan" not in self.istatistikler:
                self.istatistikler["pvp_kazanilan"] = 0
            self.istatistikler["pvp_kazanilan"] += 1
        elif "bot_kazandi" in olum_nedeni or "pvp_oyuncu2_kazandi" in olum_nedeni:
            # Bot/Rakip kazandı (PVP veya Bot modunda)
            if "pvp_kaybedilen" not in self.istatistikler:
                self.istatistikler["pvp_kaybedilen"] = 0
            self.istatistikler["pvp_kaybedilen"] += 1
        
        self._istatistikleri_kaydet()
    
    def yem_yenildi(self, tur="normal"):
        """Yem yenildiğinde çağrılır"""
        self.mevcut_yem_sayisi += 1
        if tur == "altin_elma":
            self.mevcut_altin_elma += 1
        elif tur == "elmas":
            self.mevcut_elmas += 1
    
    def ortalama_skor(self):
        """Ortalama skoru hesapla"""
        if self.istatistikler["toplam_oyun"] == 0:
            return 0
        return int(self.istatistikler["toplam_skor"] / self.istatistikler["toplam_oyun"])
    
    def ortalama_yem(self):
        """Oyun başına ortalama yem sayısı"""
        if self.istatistikler["toplam_oyun"] == 0:
            return 0
        return round(self.istatistikler["toplam_yem"] / self.istatistikler["toplam_oyun"], 1)
    
    def toplam_oyun_suresi_str(self):
        """Toplam oyun süresini okunabilir formatta döndür"""
        saniye = self.istatistikler["toplam_oyun_suresi"]
        saat = saniye // 3600
        dakika = (saniye % 3600) // 60
        san = saniye % 60
        
        if saat > 0:
            return f"{saat}s {dakika}d {san}s"
        elif dakika > 0:
            return f"{dakika}d {san}s"
        else:
            return f"{san}s"
