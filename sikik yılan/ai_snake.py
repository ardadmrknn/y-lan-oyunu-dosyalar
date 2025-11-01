"""
AI Yılan - Bot yılan sınıfı
3 zorluk seviyesi: Kolay, Orta, Zor
"""
import random
from snake import Yilan
from constants import *


class AIYilan(Yilan):
    """AI kontrollü yılan"""
    
    # Zorluk ayarları - merkezi yapılandırma
    ZORLUK_AYARLARI = {
        "kolay": {"karar_araligi": 3, "hata_orani": 0.12},  # %12 hata
        "orta": {"karar_araligi": 2, "hata_orani": 0.06},   # %6 hata
        "zor": {"karar_araligi": 1, "hata_orani": 0.03}     # %3 hata
    }
    
    def __init__(self, ekran_genislik=GENISLIK, ekran_yukseklik=YUKSEKLIK, zorluk="orta"):
        # Bot her zaman turuncu renkte (renk_index=4)
        super().__init__(ekran_genislik, ekran_yukseklik, renk_index=4, yuz_index=0)
        self.zorluk = zorluk
        self.karar_sayaci = 0
        self.hedef_yem = None
        
        # Zorluk ayarlarını uygula
        self._zorluk_ayarlarini_uygula(zorluk)
        
        # Başlangıç pozisyonu - sağ tarafta (DİNAMİK OYUN ALANI)
        # Oyun alanının grid boyutunu kullan
        grid_genislik = ekran_genislik // HUCRE_BOYUTU
        grid_yukseklik = ekran_yukseklik // HUCRE_BOYUTU
        baslangic_x = ((grid_genislik - 5) * HUCRE_BOYUTU)
        baslangic_y = ((grid_yukseklik // 2) * HUCRE_BOYUTU)
        self.pozisyonlar = [(baslangic_x, baslangic_y)]
        self.yon = (-1, 0)  # Sola bakıyor
        self.son_yon = (-1, 0)
    
    def ai_karar_ver(self, yem_pozisyon, bomba_pozisyonlari=None, rakip_pozisyonlar=None):
        """AI için karar verme - yeme git, tehlikelerden kaç"""
        self.karar_sayaci += 1
        
        # Belirli aralıklarla karar ver
        if self.karar_sayaci % self.karar_araligi != 0:
            return
        
        kafa_x, kafa_y = self.kafa_pozisyonu()
        
        # Hata yapma şansı (basit hatalar için)
        if random.random() < self.hata_orani:
            self._rastgele_hareket()
            return
        
        # Tehlike haritası oluştur
        tehlikeler = set(self.pozisyonlar[1:])  # Kendi vücudu
        if bomba_pozisyonlari:
            tehlikeler.update(bomba_pozisyonlari)
        if rakip_pozisyonlar:
            tehlikeler.update(rakip_pozisyonlar)
        
        # En yakın yeme git
        if yem_pozisyon:
            self.hedef_yem = yem_pozisyon
            en_iyi_yon = self._en_iyi_yon_bul(kafa_x, kafa_y, yem_pozisyon, tehlikeler)
            if en_iyi_yon:
                self.yon_degistir(en_iyi_yon)
        else:
            # Yem yoksa güvenli yönde hareket et
            guvenli_yon = self._guvenli_yon_bul(kafa_x, kafa_y, tehlikeler)
            if guvenli_yon:
                self.yon_degistir(guvenli_yon)
    
    def _en_iyi_yon_bul(self, x, y, hedef, tehlikeler):
        """Hedefe giden en iyi yönü bul - iyileştirilmiş algoritma"""
        hedef_x, hedef_y = hedef
        
        # Tüm olası yönler
        yonler = [
            (0, -1),  # Yukarı
            (0, 1),   # Aşağı
            (-1, 0),  # Sol
            (1, 0)    # Sağ
        ]
        
        # Ters yönü çıkar (geri dönme)
        ters_yon = (-self.son_yon[0], -self.son_yon[1])
        yonler = [y for y in yonler if y != ters_yon]
        
        # Önce mevcut yönde devam etmeye çalış (sabit gidiş için)
        suanki_yon = self.son_yon
        if suanki_yon in yonler:
            suanki_x = (x + suanki_yon[0] * HUCRE_BOYUTU) % self.ekran_genislik
            suanki_y = (y + suanki_yon[1] * HUCRE_BOYUTU) % self.ekran_yukseklik
            
            # Şu anki yön güvenli ve hedefe yaklaştırıyorsa devam et
            if (suanki_x, suanki_y) not in tehlikeler:
                mevcut_mesafe = abs(x - hedef_x) + abs(y - hedef_y)
                yeni_mesafe = abs(suanki_x - hedef_x) + abs(suanki_y - hedef_y)
                
                # Hedefe yaklaşıyorsa veya aynı mesafedeyse devam et
                if yeni_mesafe <= mevcut_mesafe:
                    return suanki_yon
        
        # Her yön için skor hesapla
        yon_skorlari = []
        for yon in yonler:
            yeni_x = (x + yon[0] * HUCRE_BOYUTU) % self.ekran_genislik
            yeni_y = (y + yon[1] * HUCRE_BOYUTU) % self.ekran_yukseklik
            
            # Tehlikeli mi kontrol et
            if (yeni_x, yeni_y) in tehlikeler:
                continue
            
            # Hedefe olan mesafe (Manhattan distance)
            mesafe = abs(yeni_x - hedef_x) + abs(yeni_y - hedef_y)
            
            # Öncelik: Önce X ekseni sonra Y ekseni (daha deterministik)
            x_farki = abs(yeni_x - hedef_x)
            y_farki = abs(yeni_y - hedef_y)
            
            # Güvenlik skoru (etraftaki tehlikeler)
            guvenlik = self._guvenlik_skoru(yeni_x, yeni_y, tehlikeler)
            
            # Eksen öncelikli skor (önce bir eksende hizala)
            eksen_oncelik = 0
            if x_farki > y_farki:
                # X ekseninde hareket et
                if yon[0] != 0:  # Yatay hareket
                    eksen_oncelik = 100
            else:
                # Y ekseninde hareket et
                if yon[1] != 0:  # Dikey hareket
                    eksen_oncelik = 100
            
            # Tüm zorluk seviyelerinde stratejik düşün
            if self.zorluk == "zor":
                gelecek_guvenlik = self._gelecek_pozisyon_guvenlik(yeni_x, yeni_y, yon, tehlikeler)
                skor = -mesafe + guvenlik * 15 + gelecek_guvenlik * 8 + eksen_oncelik
            elif self.zorluk == "orta":
                gelecek_guvenlik = self._gelecek_pozisyon_guvenlik(yeni_x, yeni_y, yon, tehlikeler)
                skor = -mesafe + guvenlik * 12 + gelecek_guvenlik * 4 + eksen_oncelik
            else:
                # Kolay mod - sadece etrafı kontrol et
                skor = -mesafe + guvenlik * 10 + eksen_oncelik
            
            yon_skorlari.append((yon, skor))
        
        # En yüksek skorlu yönü seç
        if yon_skorlari:
            yon_skorlari.sort(key=lambda x: x[1], reverse=True)
            return yon_skorlari[0][0]
        
        return None
    
    def _guvenli_yon_bul(self, x, y, tehlikeler):
        """Tehlikelerden uzak güvenli bir yön bul"""
        yonler = [
            (0, -1),  # Yukarı
            (0, 1),   # Aşağı
            (-1, 0),  # Sol
            (1, 0)    # Sağ
        ]
        
        # Ters yönü çıkar
        ters_yon = (-self.son_yon[0], -self.son_yon[1])
        yonler = [y for y in yonler if y != ters_yon]
        
        # Güvenli yönleri bul
        guvenli_yonler = []
        for yon in yonler:
            yeni_x = (x + yon[0] * HUCRE_BOYUTU) % self.ekran_genislik
            yeni_y = (y + yon[1] * HUCRE_BOYUTU) % self.ekran_yukseklik
            
            if (yeni_x, yeni_y) not in tehlikeler:
                guvenlik = self._guvenlik_skoru(yeni_x, yeni_y, tehlikeler)
                guvenli_yonler.append((yon, guvenlik))
        
        # En güvenli yönü seç
        if guvenli_yonler:
            guvenli_yonler.sort(key=lambda x: x[1], reverse=True)
            return guvenli_yonler[0][0]
        
        return None
    
    def _guvenlik_skoru(self, x, y, tehlikeler):
        """Bir pozisyonun güvenlik skorunu hesapla"""
        skor = 0
        
        # Etraftaki 4 yönü kontrol et
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            komsux = (x + dx * HUCRE_BOYUTU) % self.ekran_genislik
            komsuy = (y + dy * HUCRE_BOYUTU) % self.ekran_yukseklik
            
            if (komsux, komsuy) not in tehlikeler:
                skor += 1
        
        return skor
    
    def _gelecek_pozisyon_guvenlik(self, x, y, yon, tehlikeler):
        """Gelecek pozisyonun güvenliğini değerlendir (ileri bakış)"""
        skor = 0
        
        # 2 adım ileriye bak
        for i in range(1, 3):
            ileri_x = (x + yon[0] * HUCRE_BOYUTU * i) % self.ekran_genislik
            ileri_y = (y + yon[1] * HUCRE_BOYUTU * i) % self.ekran_yukseklik
            
            if (ileri_x, ileri_y) not in tehlikeler:
                skor += 1
            else:
                skor -= 2
        
        return skor
    
    def _rastgele_hareket(self):
        """Rastgele bir yöne dön (hata yaparken)"""
        yonler = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        ters_yon = (-self.son_yon[0], -self.son_yon[1])
        yonler = [y for y in yonler if y != ters_yon]
        
        if yonler:
            yeni_yon = random.choice(yonler)
            self.yon_degistir(yeni_yon)
    
    def _zorluk_ayarlarini_uygula(self, zorluk):
        """Zorluk ayarlarını uygula - DRY principle"""
        ayarlar = self.ZORLUK_AYARLARI.get(zorluk, self.ZORLUK_AYARLARI["orta"])
        self.karar_araligi = ayarlar["karar_araligi"]
        self.hata_orani = ayarlar["hata_orani"]
    
    def zorluk_degistir(self, yeni_zorluk):
        """Zorluk seviyesini değiştir"""
        self.zorluk = yeni_zorluk
        self._zorluk_ayarlarini_uygula(yeni_zorluk)
