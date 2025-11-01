import json
import os
from constants import BASARIMLAR

class BasarimYoneticisi:
    def __init__(self):
        self.basarimlar = {}
        self.yeni_acilan = []  # Son açılan başarımlar
        self.dosya_yolu = "basarimlar.json"
        self._basarimlari_yukle()
    
    def _basarimlari_yukle(self):
        """Kaydedilmiş başarımları yükle"""
        if os.path.exists(self.dosya_yolu):
            try:
                with open(self.dosya_yolu, 'r', encoding='utf-8') as f:
                    self.basarimlar = json.load(f)
            except:
                self._varsayilan_basarimlari_olustur()
        else:
            self._varsayilan_basarimlari_olustur()
    
    def _varsayilan_basarimlari_olustur(self):
        """Tüm başarımları kilitsiz olarak başlat"""
        for anahtar in BASARIMLAR.keys():
            self.basarimlar[anahtar] = {
                "acildi": False,
                "ilerleme": 0
            }
        self._basarimlari_kaydet()
    
    def _basarimlari_kaydet(self):
        """Başarımları dosyaya kaydet"""
        try:
            with open(self.dosya_yolu, 'w', encoding='utf-8') as f:
                json.dump(self.basarimlar, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Başarımlar kaydedilemedi: {e}")
    
    def ilerleme_kaydet(self, basarim_adi, deger):
        """Başarım ilerlemesini güncelle - HER ZAMAN EN YÜKSEK DEĞERİ SAKLAR"""
        if basarim_adi not in BASARIMLAR:
            return
        
        if basarim_adi not in self.basarimlar:
            self.basarimlar[basarim_adi] = {"acildi": False, "ilerleme": 0}

        # Önceki değeri al
        onceki = self.basarimlar[basarim_adi].get("ilerleme", 0)

        # İlerlemeyi güncelle - HER ZAMAN MAKSIMUM DEĞER SAKLANIR
        # (Eğer yeni değer daha düşükse, eski değer korunur)
        yeni_deger = max(onceki, deger)
        self.basarimlar[basarim_adi]["ilerleme"] = yeni_deger

        # Başarım zaten açılmış mı kontrol et (açılma durumunu güncelleme için)
        zaten_acildi = self.basarimlar[basarim_adi]["acildi"]

        # Eğer ilerleme artmışsa, disk'e kaydet (başarım açık olsa bile!)
        if yeni_deger > onceki:
            # Kaydet - böylece ilerleme kalıcı olur (diğer başarımlar için gerekebilir)
            self._basarimlari_kaydet()

        # Hedef değerine ulaşıldı mı? (sadece ilk kez açılıyorsa yeni_acilan listesine ekle)
        hedef = BASARIMLAR[basarim_adi]["hedef"]
        if yeni_deger >= hedef and not zaten_acildi:
            self.basarimlar[basarim_adi]["acildi"] = True
            self.yeni_acilan.append(basarim_adi)
            # Başarım açıldığında mutlaka kaydet
            self._basarimlari_kaydet()
    
    def arttir(self, basarim_adi, miktar=1):
        """Başarım ilerlemesini belirli miktarda artır"""
        if basarim_adi not in BASARIMLAR:
            return
        
        if basarim_adi not in self.basarimlar:
            self.basarimlar[basarim_adi] = {"acildi": False, "ilerleme": 0}
        
        if self.basarimlar[basarim_adi]["acildi"]:
            return
        
        yeni_deger = self.basarimlar[basarim_adi]["ilerleme"] + miktar
        self.ilerleme_kaydet(basarim_adi, yeni_deger)
    
    def yeni_acilan_basarimlari_al(self):
        """Yeni açılan başarımları al ve listeyi temizle"""
        yeni = self.yeni_acilan.copy()
        self.yeni_acilan.clear()
        return yeni
    
    def acik_basarim_sayisi(self):
        """Açık başarım sayısını döndür"""
        return sum(1 for b in self.basarimlar.values() if b["acildi"])
    
    def toplam_basarim_sayisi(self):
        """Toplam başarım sayısını döndür"""
        return len(BASARIMLAR)
    
    def ilerleme_yuzdesi(self, basarim_adi):
        """Belirli bir başarımın tamamlanma yüzdesini döndür"""
        if basarim_adi not in BASARIMLAR or basarim_adi not in self.basarimlar:
            return 0
        
        if self.basarimlar[basarim_adi]["acildi"]:
            return 100
        
        hedef = BASARIMLAR[basarim_adi]["hedef"]
        ilerleme = self.basarimlar[basarim_adi]["ilerleme"]
        return int((ilerleme / hedef) * 100)
    
    def sifirla(self):
        """Tüm başarımları sıfırla"""
        self._varsayilan_basarimlari_olustur()
        self.yeni_acilan.clear()
