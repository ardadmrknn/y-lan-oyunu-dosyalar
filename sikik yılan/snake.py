"""
Yılan sınıfı
"""
import pygame
from constants import *


class Yilan:
    def __init__(self, ekran_genislik=GENISLIK, ekran_yukseklik=YUKSEKLIK, renk_index=0, yuz_index=0, aksesuar_index=0, hucre_boyutu=HUCRE_BOYUTU):
        # Oyun alanı boyutları (wrap-around için)
        self.oyun_genislik = ekran_genislik
        self.oyun_yukseklik = ekran_yukseklik
        # Ekran boyutları (çizim için, eski uyumluluk)
        self.ekran_genislik = ekran_genislik
        self.ekran_yukseklik = ekran_yukseklik
        # Hücre boyutu - DİNAMİK!
        self.hucre_boyutu = hucre_boyutu
        self.uzunluk = 1
        # Başlangıç pozisyonu - ekranın ortasında ve hücre boyutuna uygun
        baslangic_x = (ekran_genislik // 2 // hucre_boyutu) * hucre_boyutu
        baslangic_y = (ekran_yukseklik // 2 // hucre_boyutu) * hucre_boyutu
        self.pozisyonlar = [(baslangic_x, baslangic_y)]
        self.yon = (0, -1)  # Yukarı başlıyor
        self.renk = YESIL
        self.skor = 0
        self.son_yon = (0, -1)  # Son hareket edilen yön (hızlı tuş basma kontrolü için)
        
        # Yılan özelleştirmeleri
        self.renk_index = renk_index
        self.yuz_index = yuz_index
        self.aksesuar_index = aksesuar_index
        
        # Renk bilgilerini al
        if 0 <= renk_index < len(YILAN_RENKLERI):
            _, self.renk_acik, self.renk_orta, self.renk_koyu = YILAN_RENKLERI[renk_index]
        else:
            _, self.renk_acik, self.renk_orta, self.renk_koyu = YILAN_RENKLERI[0]
        
        # Performans optimizasyonu: Yön değiştiğinde pozisyon cache'ini temizle
        self._offset_cache = {}
        self._cached_yon = None

    def renk_guncelle(self, yeni_renk_index):
        """Yılanın rengini günceller"""
        self.renk_index = yeni_renk_index
        if 0 <= yeni_renk_index < len(YILAN_RENKLERI):
            _, self.renk_acik, self.renk_orta, self.renk_koyu = YILAN_RENKLERI[yeni_renk_index]
        else:
            _, self.renk_acik, self.renk_orta, self.renk_koyu = YILAN_RENKLERI[0]

    def yuz_guncelle(self, yeni_yuz_index):
        """Yılanın yüzünü günceller"""
        self.yuz_index = yeni_yuz_index

    def aksesuar_guncelle(self, yeni_aksesuar_index):
        """Yılanın aksesuarını günceller"""
        self.aksesuar_index = yeni_aksesuar_index

    def kafa_pozisyonu(self):
        return self.pozisyonlar[0]

    def hareket_et(self):
        kafa_x, kafa_y = self.kafa_pozisyonu()
        yon_x, yon_y = self.yon
        # WRAP-AROUND GERİ GETİRİLDİ - kenarlardan geçiş aktif
        # OYUN ALANI boyutunu kullan, ekran boyutunu değil!
        yeni_x = (kafa_x + (yon_x * self.hucre_boyutu)) % self.oyun_genislik
        yeni_y = (kafa_y + (yon_y * self.hucre_boyutu)) % self.oyun_yukseklik
        
        # Yeni pozisyonu listenin başına ekle
        self.pozisyonlar.insert(0, (yeni_x, yeni_y))
        
        # Eğer uzunluk aşıldıysa son parçayı çıkar
        if len(self.pozisyonlar) > self.uzunluk:
            self.pozisyonlar.pop()
        
        # Son hareketi kaydet
        self.son_yon = self.yon

    def yon_degistir(self, yeni_yon):
        # Ters yöne dönmeyi engelle (son hareket edilen yöne göre)
        if (yeni_yon[0] * -1, yeni_yon[1] * -1) != self.son_yon:
            self.yon = yeni_yon
            # Yön değiştiğinde cache'i temizle (performans optimizasyonu)
            self._offset_cache.clear()
            self._cached_yon = yeni_yon

    def buyut(self):
        self.uzunluk += 1
        self.skor += 10

    def carpma_kontrolu(self):
        # Kendine çarptı mı?
        # Sadece uzunluk 5'ten fazlaysa kontrol et (oyunun başında yanlış pozitif olmasın)
        if self.uzunluk > 4:
            kafa = self.pozisyonlar[0]
            # Kafanın vücuda çarpıp çarpmadığını kontrol et
            if kafa in self.pozisyonlar[1:]:
                return True
        return False

    def ciz(self, ekran, offset_x=0, offset_y=0):
        # Windows optimizasyonu: Basitleştirilmiş 3D görünümlü yılan - gereksiz glow efektleri kaldırıldı
        for i, pozisyon in enumerate(self.pozisyonlar):
            merkez_x = pozisyon[0] + self.hucre_boyutu // 2 + offset_x
            merkez_y = pozisyon[1] + self.hucre_boyutu // 2 + offset_y
            
            if i == 0:  # Kafa - Optimizasyon: Glow katmanları azaltıldı
                # Gölge
                golge_renk = tuple(max(0, c - 80) for c in self.renk_koyu)
                pygame.draw.circle(ekran, golge_renk, (merkez_x + 2, merkez_y + 2), self.hucre_boyutu // 2 + 2)
                
                # Dış halka (3D kenar)
                pygame.draw.circle(ekran, self.renk_koyu, (merkez_x, merkez_y), self.hucre_boyutu // 2 + 2)
                
                # Orta katman
                pygame.draw.circle(ekran, self.renk_orta, (merkez_x, merkez_y), self.hucre_boyutu // 2)
                
                # İç parlak kısım
                pygame.draw.circle(ekran, self.renk_acik, (merkez_x, merkez_y), self.hucre_boyutu // 2 - 2)
                
                # Basitleştirilmiş parlama (sadece 1 katman)
                parlama_renk = (255, 255, 255)
                parlama_boyut = max(2, self.hucre_boyutu // 12)
                pygame.draw.circle(ekran, parlama_renk, (merkez_x - self.hucre_boyutu // 10, merkez_y - self.hucre_boyutu // 10), parlama_boyut)
                
                # Yüz tipine göre göz çiz
                self._goz_ciz(ekran, merkez_x, merkez_y)
                
                # Aksesuar çiz (eğer varsa)
                if self.aksesuar_index > 0:
                    self._aksesuar_ciz(ekran, merkez_x, merkez_y)
                
            else:  # Vücut - Optimizasyon: Gradient basitleştirildi
                koyuluk = min(i * 3, 60)
                
                # Gölge
                golge_renk = tuple(max(0, c - 80 - koyuluk // 4) for c in self.renk_koyu)
                pygame.draw.circle(ekran, golge_renk, (merkez_x + 1, merkez_y + 1), self.hucre_boyutu // 2 + 1)
                
                # Dış halka
                koyu_renk = tuple(max(0, c - koyuluk // 2) for c in self.renk_koyu)
                pygame.draw.circle(ekran, koyu_renk, (merkez_x, merkez_y), self.hucre_boyutu // 2 + 1)
                
                # İç katman
                acik_renk = tuple(max(0, c - koyuluk // 3) for c in self.renk_acik)
                pygame.draw.circle(ekran, acik_renk, (merkez_x, merkez_y), self.hucre_boyutu // 2 - 1)
                
    def _yon_bazli_offset_hesapla(self, merkez_x, merkez_y, ileri=0, yana1=0, yana2=0):
        """Yön bazlı offset hesaplama - KOD TEKRARINDAN KAÇINMA + CACHE
        ileri: Yılanın baktığı yöne doğru ofset
        yana1: İlk yan nokta (sol veya yukarı)
        yana2: İkinci yan nokta (sağ veya aşağı) - None ise yana1 ile simetrik
        Returns: (x1, y1, x2, y2) veya (x, y) eğer tek nokta ise
        """
        # Cache kontrolü - yön değişmediyse ve aynı parametrelerle çağrıldıysa
        cache_key = (merkez_x, merkez_y, ileri, yana1, yana2)
        if self._cached_yon == self.yon and cache_key in self._offset_cache:
            return self._offset_cache[cache_key]
        
        if yana2 is None:
            yana2 = yana1
            
        if self.yon == (0, -1):  # Yukarı
            # İleri = yukarı, yan = sağ-sol
            if yana1 == 0 and yana2 == 0:
                result = (merkez_x, merkez_y + ileri)
            else:
                result = (merkez_x - yana1, merkez_y + ileri, merkez_x + yana2, merkez_y + ileri)
        elif self.yon == (0, 1):  # Aşağı
            # İleri = aşağı, yan = sağ-sol
            if yana1 == 0 and yana2 == 0:
                result = (merkez_x, merkez_y - ileri)
            else:
                result = (merkez_x - yana1, merkez_y - ileri, merkez_x + yana2, merkez_y - ileri)
        elif self.yon == (-1, 0):  # Sol
            # İleri = sol, yan = yukarı-aşağı
            if yana1 == 0 and yana2 == 0:
                result = (merkez_x + ileri, merkez_y)
            else:
                result = (merkez_x + ileri, merkez_y - yana1, merkez_x + ileri, merkez_y + yana2)
        elif self.yon == (1, 0):  # Sağ
            # İleri = sağ, yan = yukarı-aşağı
            if yana1 == 0 and yana2 == 0:
                result = (merkez_x - ileri, merkez_y)
            else:
                result = (merkez_x - ileri, merkez_y - yana1, merkez_x - ileri, merkez_y + yana2)
        
        # Sonucu cache'le
        self._offset_cache[cache_key] = result
        return result
    
    def _goz_ciz(self, ekran, merkez_x, merkez_y):
        """Yüz tipine göre gözleri çizer - İYİLEŞTİRİLMİŞ + YÖN BAZLI + DİNAMİK BOYUT"""
        # Dinamik göz boyutları - hücre boyutuna göre
        goz_dis_yaricap = max(4, self.hucre_boyutu // 5)
        goz_ic_yaricap = max(3, self.hucre_boyutu // 7)
        goz_parlama_yaricap = max(2, self.hucre_boyutu // 15)
        goz_offset_ileri = -max(3, self.hucre_boyutu // 8)
        goz_offset_yan = max(4, self.hucre_boyutu // 5)
        
        # Gözleri hesapla (yöne göre) - gözler yılanın önünde ve yanlarda
        goz1_x, goz1_y, goz2_x, goz2_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=goz_offset_ileri, yana1=goz_offset_yan, yana2=goz_offset_yan)
        
        yuz_tipi = YILAN_YUZLERI[self.yuz_index][1] if self.yuz_index < len(YILAN_YUZLERI) else "normal"
        
        if yuz_tipi == "normal":
            # Normal gözler - DAHA BELIRGIN
            # Dış beyaz halka
            pygame.draw.circle(ekran, BEYAZ, (int(goz1_x), int(goz1_y)), goz_dis_yaricap)
            pygame.draw.circle(ekran, BEYAZ, (int(goz2_x), int(goz2_y)), goz_dis_yaricap)
            # Göz bebeği
            pygame.draw.circle(ekran, SIYAH, (int(goz1_x), int(goz1_y)), goz_ic_yaricap)
            pygame.draw.circle(ekran, SIYAH, (int(goz2_x), int(goz2_y)), goz_ic_yaricap)
            # Parlama efekti
            parlama_offset = max(1, goz_dis_yaricap // 4)
            pygame.draw.circle(ekran, BEYAZ, (int(goz1_x + parlama_offset), int(goz1_y - parlama_offset)), goz_parlama_yaricap)
            pygame.draw.circle(ekran, BEYAZ, (int(goz2_x + parlama_offset), int(goz2_y - parlama_offset)), goz_parlama_yaricap)
            
        elif yuz_tipi == "mutlu":
            # Mutlu gözler - GÜLEN GÖZ ŞEKLİ
            # Kapalı gülen gözler
            pygame.draw.arc(ekran, SIYAH, (int(goz1_x - 7), int(goz1_y - 4), 14, 8), 0, 3.14, 4)
            pygame.draw.arc(ekran, SIYAH, (int(goz2_x - 7), int(goz2_y - 4), 14, 8), 0, 3.14, 4)
            # Gülücük ağzı (yönlendirilmiş)
            agiz_x, agiz_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=2, yana1=0)
            pygame.draw.arc(ekran, SIYAH, (int(agiz_x - 8), int(agiz_y), 16, 10), 3.14, 2 * 3.14, 3)
            
        elif yuz_tipi == "saskın":
            # Şaşkın gözler - ÇOK BÜYÜK VE YUVARLAK
            pygame.draw.circle(ekran, BEYAZ, (int(goz1_x), int(goz1_y)), 9)
            pygame.draw.circle(ekran, BEYAZ, (int(goz2_x), int(goz2_y)), 9)
            pygame.draw.circle(ekran, SIYAH, (int(goz1_x), int(goz1_y)), 7)
            pygame.draw.circle(ekran, SIYAH, (int(goz2_x), int(goz2_y)), 7)
            # Parlama
            pygame.draw.circle(ekran, BEYAZ, (int(goz1_x - 2), int(goz1_y - 2)), 3)
            pygame.draw.circle(ekran, BEYAZ, (int(goz2_x - 2), int(goz2_y - 2)), 3)
            # Şaşkın ağız (açık "O") - yönlendirilmiş
            agiz_x, agiz_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=8, yana1=0)
            pygame.draw.circle(ekran, SIYAH, (int(agiz_x), int(agiz_y)), 4)
            pygame.draw.circle(ekran, (255, 150, 150), (int(agiz_x), int(agiz_y)), 3)
            
        elif yuz_tipi == "sinirli":
            # Sinirli gözler - KIZGIN BAKIŞ
            # Kızgın kırmızı gözler
            pygame.draw.circle(ekran, BEYAZ, (int(goz1_x), int(goz1_y)), 7)
            pygame.draw.circle(ekran, BEYAZ, (int(goz2_x), int(goz2_y)), 7)
            pygame.draw.circle(ekran, KIRMIZI, (int(goz1_x), int(goz1_y)), 5)
            pygame.draw.circle(ekran, KIRMIZI, (int(goz2_x), int(goz2_y)), 5)
            # Siyah göz bebeği
            pygame.draw.circle(ekran, SIYAH, (int(goz1_x), int(goz1_y)), 3)
            pygame.draw.circle(ekran, SIYAH, (int(goz2_x), int(goz2_y)), 3)
            # Kızgın kaşlar (kalın ve aşağı eğik) - yöne göre
            if self.yon[1] != 0:  # Yukarı veya aşağı
                pygame.draw.line(ekran, SIYAH, (int(goz1_x - 8), int(goz1_y - 9)), (int(goz1_x + 4), int(goz1_y - 11)), 3)
                pygame.draw.line(ekran, SIYAH, (int(goz2_x - 4), int(goz2_y - 11)), (int(goz2_x + 8), int(goz2_y - 9)), 3)
            else:  # Sol veya sağ
                pygame.draw.line(ekran, SIYAH, (int(goz1_x - 9), int(goz1_y - 8)), (int(goz1_x - 11), int(goz1_y + 4)), 3)
                pygame.draw.line(ekran, SIYAH, (int(goz2_x - 11), int(goz2_y - 4)), (int(goz2_x - 9), int(goz2_y + 8)), 3)
            # Kızgın ağız - yönlendirilmiş
            agiz_x, agiz_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=8, yana1=0)
            if self.yon[1] != 0:  # Yukarı/aşağı - yatay ağız
                pygame.draw.line(ekran, SIYAH, (int(agiz_x - 6), int(agiz_y)), (int(agiz_x + 6), int(agiz_y)), 3)
            else:  # Sol/sağ - dikey ağız
                pygame.draw.line(ekran, SIYAH, (int(agiz_x), int(agiz_y - 6)), (int(agiz_x), int(agiz_y + 6)), 3)
            
        elif yuz_tipi == "havali":
            # Havalı gözler - GÜNEŞLİK GÖZLÜK
            # Koyu gözlük camları
            pygame.draw.ellipse(ekran, (30, 30, 30), (int(goz1_x - 8), int(goz1_y - 6), 16, 12))
            pygame.draw.ellipse(ekran, (30, 30, 30), (int(goz2_x - 8), int(goz2_y - 6), 16, 12))
            # Gözlük çerçevesi (altın)
            pygame.draw.ellipse(ekran, (255, 215, 0), (int(goz1_x - 8), int(goz1_y - 6), 16, 12), 2)
            pygame.draw.ellipse(ekran, (255, 215, 0), (int(goz2_x - 8), int(goz2_y - 6), 16, 12), 2)
            # Köprü - yöne göre
            if self.yon[1] != 0:  # Yukarı/aşağı - yatay köprü
                pygame.draw.line(ekran, (255, 215, 0), (int(goz1_x + 8), int(goz1_y)), (int(goz2_x - 8), int(goz2_y)), 2)
            else:  # Sol/sağ - dikey köprü
                pygame.draw.line(ekran, (255, 215, 0), (int(goz1_x), int(goz1_y + 8)), (int(goz2_x), int(goz2_y - 8)), 2)
            # Parlama efekti
            pygame.draw.line(ekran, (150, 150, 150), (int(goz1_x - 4), int(goz1_y - 4)), (int(goz1_x - 2), int(goz1_y - 2)), 2)
            pygame.draw.line(ekran, (150, 150, 150), (int(goz2_x - 4), int(goz2_y - 4)), (int(goz2_x - 2), int(goz2_y - 2)), 2)
            # Havalı gülümseme - yönlendirilmiş
            agiz_x, agiz_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=4, yana1=0)
            pygame.draw.arc(ekran, SIYAH, (int(agiz_x - 6), int(agiz_y), 12, 8), 3.14, 2 * 3.14, 2)
            
        elif yuz_tipi == "uyuyan":
            # Uyuyan gözler - KAPALI + ZZZ
            # Kapalı gözler (çizgiler) - yöne göre
            if self.yon[1] != 0:  # Yukarı/aşağı - yatay çizgiler
                pygame.draw.line(ekran, SIYAH, (int(goz1_x - 6), int(goz1_y)), (int(goz1_x + 6), int(goz1_y)), 3)
                pygame.draw.line(ekran, SIYAH, (int(goz2_x - 6), int(goz2_y)), (int(goz2_x + 6), int(goz2_y)), 3)
                # Kirpikler
                for i in range(-2, 3, 2):
                    pygame.draw.line(ekran, SIYAH, (int(goz1_x + i), int(goz1_y)), (int(goz1_x + i), int(goz1_y + 3)), 1)
                    pygame.draw.line(ekran, SIYAH, (int(goz2_x + i), int(goz2_y)), (int(goz2_x + i), int(goz2_y + 3)), 1)
            else:  # Sol/sağ - dikey çizgiler
                pygame.draw.line(ekran, SIYAH, (int(goz1_x), int(goz1_y - 6)), (int(goz1_x), int(goz1_y + 6)), 3)
                pygame.draw.line(ekran, SIYAH, (int(goz2_x), int(goz2_y - 6)), (int(goz2_x), int(goz2_y + 6)), 3)
                # Kirpikler
                for i in range(-2, 3, 2):
                    pygame.draw.line(ekran, SIYAH, (int(goz1_x), int(goz1_y + i)), (int(goz1_x + 3), int(goz1_y + i)), 1)
                    pygame.draw.line(ekran, SIYAH, (int(goz2_x), int(goz2_y + i)), (int(goz2_x + 3), int(goz2_y + i)), 1)
            
            # Z harfleri (daha büyük ve belirgin) - yönün yanında
            font = pygame.font.Font(None, 20)
            z1 = font.render("Z", True, (100, 100, 255))
            z2 = font.render("Z", True, (120, 120, 255))
            z3 = font.render("z", True, (140, 140, 255))
            
            # Z'leri yönün yanına yerleştir
            if self.yon == (0, -1):  # Yukarı - sağda
                ekran.blit(z1, (int(merkez_x + 12), int(merkez_y - 18)))
                ekran.blit(z2, (int(merkez_x + 16), int(merkez_y - 14)))
                ekran.blit(z3, (int(merkez_x + 19), int(merkez_y - 10)))
            elif self.yon == (0, 1):  # Aşağı - sağda
                ekran.blit(z1, (int(merkez_x + 12), int(merkez_y + 2)))
                ekran.blit(z2, (int(merkez_x + 16), int(merkez_y + 6)))
                ekran.blit(z3, (int(merkez_x + 19), int(merkez_y + 10)))
            elif self.yon == (-1, 0):  # Sol - üstte
                ekran.blit(z1, (int(merkez_x - 18), int(merkez_y - 20)))
                ekran.blit(z2, (int(merkez_x - 14), int(merkez_y - 16)))
                ekran.blit(z3, (int(merkez_x - 10), int(merkez_y - 13)))
            else:  # Sağ - üstte
                ekran.blit(z1, (int(merkez_x + 2), int(merkez_y - 20)))
                ekran.blit(z2, (int(merkez_x + 6), int(merkez_y - 16)))
                ekran.blit(z3, (int(merkez_x + 10), int(merkez_y - 13)))
            
        elif yuz_tipi == "asik":
            # Aşık gözler - KALP ŞEKLİNDE PARLAK
            # Kalp şeklinde gözler
            def kalp_ciz(x, y, boyut):
                # Sol yarım daire
                pygame.draw.circle(ekran, (255, 50, 100), (int(x - boyut//3), int(y - boyut//4)), boyut//2)
                # Sağ yarım daire
                pygame.draw.circle(ekran, (255, 50, 100), (int(x + boyut//3), int(y - boyut//4)), boyut//2)
                # Alt üçgen
                pygame.draw.polygon(ekran, (255, 50, 100), [
                    (int(x - boyut), int(y)),
                    (int(x + boyut), int(y)),
                    (int(x), int(y + boyut))
                ])
            
            kalp_ciz(goz1_x, goz1_y, 6)
            kalp_ciz(goz2_x, goz2_y, 6)
            # Parlama
            pygame.draw.circle(ekran, (255, 150, 200), (int(goz1_x - 2), int(goz1_y - 2)), 2)
            pygame.draw.circle(ekran, (255, 150, 200), (int(goz2_x - 2), int(goz2_y - 2)), 2)
            # Gülümseyen ağız - yönlendirilmiş
            agiz_x, agiz_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=2, yana1=0)
            pygame.draw.arc(ekran, (255, 100, 150), (int(agiz_x - 8), int(agiz_y), 16, 10), 3.14, 2 * 3.14, 3)
            
        elif yuz_tipi == "deli":
            # Deli gözler - FARKLI YÖNLERE BAKAN SPIRAL
            # Sol göz - yukarı bakıyor
            pygame.draw.circle(ekran, BEYAZ, (int(goz1_x), int(goz1_y)), 8)
            pygame.draw.circle(ekran, SIYAH, (int(goz1_x - 2), int(goz1_y - 3)), 5)
            # Sağ göz - aşağı bakıyor
            pygame.draw.circle(ekran, BEYAZ, (int(goz2_x), int(goz2_y)), 8)
            pygame.draw.circle(ekran, SIYAH, (int(goz2_x + 2), int(goz2_y + 3)), 5)
            # Spiral efekt (göz bebeğinde)
            for r in range(1, 4):
                angle = r * 2
                x1 = int(goz1_x - 2 + r * 0.7 * pygame.math.Vector2(1, 0).rotate(angle * 60).x)
                y1 = int(goz1_y - 3 + r * 0.7 * pygame.math.Vector2(1, 0).rotate(angle * 60).y)
                pygame.draw.circle(ekran, (200, 200, 0), (x1, y1), 1)
            # Deli gülüş (yamuk) - yönlendirilmiş
            agiz_x, agiz_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=6, yana1=0)
            if self.yon[1] != 0:  # Yukarı/aşağı
                pygame.draw.line(ekran, SIYAH, (int(agiz_x - 8), int(agiz_y)), (int(agiz_x + 4), int(agiz_y + 4)), 3)
            else:  # Sol/sağ
                pygame.draw.line(ekran, SIYAH, (int(agiz_x), int(agiz_y - 8)), (int(agiz_x + 4), int(agiz_y + 4)), 3)
            
        elif yuz_tipi == "robot":
            # Robot gözler - DİJİTAL EKRAN
            # Kare LED gözler (daha büyük)
            pygame.draw.rect(ekran, (0, 255, 255), (int(goz1_x - 7), int(goz1_y - 7), 14, 14))
            pygame.draw.rect(ekran, (0, 255, 255), (int(goz2_x - 7), int(goz2_y - 7), 14, 14))
            # İç LED
            pygame.draw.rect(ekran, (0, 200, 200), (int(goz1_x - 4), int(goz1_y - 4), 8, 8))
            pygame.draw.rect(ekran, (0, 200, 200), (int(goz2_x - 4), int(goz2_y - 4), 8, 8))
            # LED nokta ortada
            pygame.draw.circle(ekran, (255, 255, 255), (int(goz1_x), int(goz1_y)), 3)
            pygame.draw.circle(ekran, (255, 255, 255), (int(goz2_x), int(goz2_y)), 3)
            # Pixelated çerçeve
            for i in range(-7, 8, 2):
                pygame.draw.rect(ekran, (0, 150, 150), (int(goz1_x + i), int(goz1_y - 8), 1, 2))
                pygame.draw.rect(ekran, (0, 150, 150), (int(goz2_x + i), int(goz2_y - 8), 1, 2))
            
        elif yuz_tipi == "pirat":
            # Pirat - TEK GÖZ + GÖZ BANDI
            # Sol göz - normal (daha büyük)
            pygame.draw.circle(ekran, BEYAZ, (int(goz1_x), int(goz1_y)), 8)
            pygame.draw.circle(ekran, SIYAH, (int(goz1_x), int(goz1_y)), 5)
            pygame.draw.circle(ekran, BEYAZ, (int(goz1_x + 2), int(goz1_y - 2)), 2)
            # Sağ göz - göz bandı (siyah patch)
            pygame.draw.circle(ekran, SIYAH, (int(goz2_x), int(goz2_y)), 9)
            # Bant çizgisi - yöne göre
            if self.yon[1] != 0:  # Yukarı/aşağı - yatay bant
                pygame.draw.line(ekran, SIYAH, (int(goz2_x - 12), int(goz2_y)), (int(goz2_x + 12), int(goz2_y)), 4)
                # Dikiş işaretleri
                for i in range(-8, 9, 4):
                    pygame.draw.line(ekran, (100, 100, 100), (int(goz2_x + i), int(goz2_y - 2)), (int(goz2_x + i), int(goz2_y + 2)), 1)
            else:  # Sol/sağ - dikey bant
                pygame.draw.line(ekran, SIYAH, (int(goz2_x), int(goz2_y - 12)), (int(goz2_x), int(goz2_y + 12)), 4)
                # Dikiş işaretleri
                for i in range(-8, 9, 4):
                    pygame.draw.line(ekran, (100, 100, 100), (int(goz2_x - 2), int(goz2_y + i)), (int(goz2_x + 2), int(goz2_y + i)), 1)
            # Korsan ağzı (şirret gülüş) - yönlendirilmiş
            agiz_x, agiz_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=4, yana1=0)
            pygame.draw.arc(ekran, SIYAH, (int(agiz_x - 6), int(agiz_y), 12, 8), 3.14, 2 * 3.14, 2)
    
    def _aksesuar_ciz(self, ekran, merkez_x, merkez_y):
        """Aksesuar tipine göre aksesuarı çizer - İYİLEŞTİRİLMİŞ + YÖN BAZLI"""
        if self.aksesuar_index >= len(YILAN_AKSESUARLARI):
            return
            
        aksesuar_tipi = YILAN_AKSESUARLARI[self.aksesuar_index][1]
        
        if aksesuar_tipi == "gozluk":
            # Gözlük - YÖN BAZLI
            goz1_x, goz1_y, goz2_x, goz2_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=-5, yana1=7, yana2=7)
            # Cam çerçevesi (daha kalın)
            pygame.draw.circle(ekran, SIYAH, (int(goz1_x), int(goz1_y)), 7, 3)
            pygame.draw.circle(ekran, SIYAH, (int(goz2_x), int(goz2_y)), 7, 3)
            # Köprü (kalın) - yöne göre
            if self.yon[1] != 0:  # Yukarı/aşağı - yatay köprü
                pygame.draw.line(ekran, SIYAH, (int(goz1_x + 7), int(goz1_y)), (int(goz2_x - 7), int(goz2_y)), 3)
            else:  # Sol/sağ - dikey köprü
                pygame.draw.line(ekran, SIYAH, (int(goz1_x), int(goz1_y + 7)), (int(goz2_x), int(goz2_y - 7)), 3)
            # Camda parlama efekti
            pygame.draw.circle(ekran, (200, 200, 255), (int(goz1_x - 3), int(goz1_y - 3)), 2)
            pygame.draw.circle(ekran, (200, 200, 255), (int(goz2_x - 3), int(goz2_y - 3)), 2)
            
        elif aksesuar_tipi == "gunes_gozlugu":
            # Güneş gözlüğü - YÖN BAZLI
            goz1_x, goz1_y, goz2_x, goz2_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=-5, yana1=7, yana2=7)
            # Koyu camlar (daha büyük)
            pygame.draw.circle(ekran, (30, 30, 30), (int(goz1_x), int(goz1_y)), 9)
            pygame.draw.circle(ekran, (30, 30, 30), (int(goz2_x), int(goz2_y)), 9)
            # Altın çerçeve
            pygame.draw.circle(ekran, (255, 215, 0), (int(goz1_x), int(goz1_y)), 9, 2)
            pygame.draw.circle(ekran, (255, 215, 0), (int(goz2_x), int(goz2_y)), 9, 2)
            # Köprü - yöne göre
            if self.yon[1] != 0:  # Yukarı/aşağı - yatay
                pygame.draw.line(ekran, (255, 215, 0), (int(goz1_x + 9), int(goz1_y)), (int(goz2_x - 9), int(goz2_y)), 3)
            else:  # Sol/sağ - dikey
                pygame.draw.line(ekran, (255, 215, 0), (int(goz1_x), int(goz1_y + 9)), (int(goz2_x), int(goz2_y - 9)), 3)
            # Parlama çizgileri
            pygame.draw.line(ekran, (100, 100, 100), (int(goz1_x - 5), int(goz1_y - 5)), (int(goz1_x - 3), int(goz1_y - 3)), 2)
            pygame.draw.line(ekran, (100, 100, 100), (int(goz2_x - 5), int(goz2_y - 5)), (int(goz2_x - 3), int(goz2_y - 3)), 2)
            
        elif aksesuar_tipi == "sapka":
            # Şapka - YÖN BAZLI (kafanın üstünde/arkasında)
            sapka_x, sapka_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=-16, yana1=0)
            
            if self.yon[1] != 0:  # Yukarı/aşağı - normal şapka
                # Siperlik
                pygame.draw.ellipse(ekran, (200, 0, 0), (int(sapka_x - 14), int(sapka_y), 28, 8))
                # Üst kısım
                pygame.draw.rect(ekran, KIRMIZI, (int(sapka_x - 10), int(sapka_y - 8), 20, 10))
                # Tepe (yuvarlak)
                pygame.draw.ellipse(ekran, KIRMIZI, (int(sapka_x - 8), int(sapka_y - 10), 16, 6))
                # Logo/şerit
                pygame.draw.rect(ekran, (255, 215, 0), (int(sapka_x - 9), int(sapka_y - 2), 18, 3))
            else:  # Sol/sağ - yan görünüm
                # Siperlik
                pygame.draw.ellipse(ekran, (200, 0, 0), (int(sapka_x), int(sapka_y - 14), 8, 28))
                # Üst kısım
                pygame.draw.rect(ekran, KIRMIZI, (int(sapka_x - 8), int(sapka_y - 10), 10, 20))
                # Tepe (yuvarlak)
                pygame.draw.ellipse(ekran, KIRMIZI, (int(sapka_x - 10), int(sapka_y - 8), 6, 16))
                # Logo/şerit
                pygame.draw.rect(ekran, (255, 215, 0), (int(sapka_x - 2), int(sapka_y - 9), 3, 18))
            
        elif aksesuar_tipi == "tac":
            # Taç - YÖN BAZLI (kafanın üstünde)
            tac_x, tac_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=-12, yana1=0)
            
            if self.yon[1] != 0:  # Yukarı/aşağı - normal taç
                noktalar = [
                    (tac_x - 14, tac_y),
                    (tac_x - 11, tac_y - 8),
                    (tac_x - 6, tac_y - 2),
                    (tac_x, tac_y - 10),
                    (tac_x + 6, tac_y - 2),
                    (tac_x + 11, tac_y - 8),
                    (tac_x + 14, tac_y)
                ]
                pygame.draw.polygon(ekran, (255, 215, 0), [(int(x), int(y)) for x, y in noktalar])
                pygame.draw.polygon(ekran, (218, 165, 32), [(int(x), int(y)) for x, y in noktalar], 2)
                # Taşlar
                pygame.draw.circle(ekran, KIRMIZI, (int(tac_x), int(tac_y - 8)), 3)
                pygame.draw.circle(ekran, (255, 100, 100), (int(tac_x), int(tac_y - 8)), 2)
                pygame.draw.circle(ekran, MAVI, (int(tac_x - 9), int(tac_y - 5)), 3)
                pygame.draw.circle(ekran, (100, 100, 255), (int(tac_x - 9), int(tac_y - 5)), 2)
                pygame.draw.circle(ekran, YESIL, (int(tac_x + 9), int(tac_y - 5)), 3)
                pygame.draw.circle(ekran, (100, 255, 100), (int(tac_x + 9), int(tac_y - 5)), 2)
            else:  # Sol/sağ - yan görünüm
                noktalar = [
                    (tac_x, tac_y - 14),
                    (tac_x - 8, tac_y - 11),
                    (tac_x - 2, tac_y - 6),
                    (tac_x - 10, tac_y),
                    (tac_x - 2, tac_y + 6),
                    (tac_x - 8, tac_y + 11),
                    (tac_x, tac_y + 14)
                ]
                pygame.draw.polygon(ekran, (255, 215, 0), [(int(x), int(y)) for x, y in noktalar])
                pygame.draw.polygon(ekran, (218, 165, 32), [(int(x), int(y)) for x, y in noktalar], 2)
                # Taşlar
                pygame.draw.circle(ekran, KIRMIZI, (int(tac_x - 8), int(tac_y)), 3)
                pygame.draw.circle(ekran, (255, 100, 100), (int(tac_x - 8), int(tac_y)), 2)
                pygame.draw.circle(ekran, MAVI, (int(tac_x - 5), int(tac_y - 9)), 3)
                pygame.draw.circle(ekran, (100, 100, 255), (int(tac_x - 5), int(tac_y - 9)), 2)
                pygame.draw.circle(ekran, YESIL, (int(tac_x - 5), int(tac_y + 9)), 3)
                pygame.draw.circle(ekran, (100, 255, 100), (int(tac_x - 5), int(tac_y + 9)), 2)
            
        elif aksesuar_tipi == "bandana":
            # Bandana - YÖN BAZLI (kafanın üstünde/arkasında)
            bandana_x, bandana_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=-10, yana1=0)
            
            if self.yon[1] != 0:  # Yukarı/aşağı
                noktalar = [
                    (bandana_x - 15, bandana_y),
                    (bandana_x - 10, bandana_y - 4),
                    (bandana_x + 10, bandana_y - 4),
                    (bandana_x + 15, bandana_y),
                    (bandana_x + 10, bandana_y + 2),
                    (bandana_x - 10, bandana_y + 2)
                ]
                pygame.draw.polygon(ekran, KIRMIZI, [(int(x), int(y)) for x, y in noktalar])
                # Desenler (puantiye)
                for i in range(-8, 9, 4):
                    pygame.draw.circle(ekran, BEYAZ, (int(bandana_x + i), int(bandana_y - 1)), 2)
                # Düğüm
                pygame.draw.circle(ekran, (150, 0, 0), (int(bandana_x + 16), int(bandana_y + 1)), 3)
                pygame.draw.circle(ekran, KIRMIZI, (int(bandana_x + 16), int(bandana_y + 1)), 2)
            else:  # Sol/sağ - yan görünüm
                noktalar = [
                    (bandana_x, bandana_y - 15),
                    (bandana_x - 4, bandana_y - 10),
                    (bandana_x - 4, bandana_y + 10),
                    (bandana_x, bandana_y + 15),
                    (bandana_x + 2, bandana_y + 10),
                    (bandana_x + 2, bandana_y - 10)
                ]
                pygame.draw.polygon(ekran, KIRMIZI, [(int(x), int(y)) for x, y in noktalar])
                # Desenler (puantiye)
                for i in range(-8, 9, 4):
                    pygame.draw.circle(ekran, BEYAZ, (int(bandana_x - 1), int(bandana_y + i)), 2)
                # Düğüm
                pygame.draw.circle(ekran, (150, 0, 0), (int(bandana_x + 1), int(bandana_y + 16)), 3)
                pygame.draw.circle(ekran, KIRMIZI, (int(bandana_x + 1), int(bandana_y + 16)), 2)
            
        elif aksesuar_tipi == "papyon":
            # Papyon - YÖN BAZLI (kafanın altında/önünde)
            papyon_x, papyon_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=9, yana1=0)
            
            if self.yon[1] != 0:  # Yukarı/aşağı
                # Sol kanat
                noktalar1 = [
                    (papyon_x - 10, papyon_y),
                    (papyon_x - 5, papyon_y + 3),
                    (papyon_x - 5, papyon_y - 3)
                ]
                # Sağ kanat
                noktalar2 = [
                    (papyon_x + 10, papyon_y),
                    (papyon_x + 5, papyon_y + 3),
                    (papyon_x + 5, papyon_y - 3)
                ]
                pygame.draw.polygon(ekran, KIRMIZI, [(int(x), int(y)) for x, y in noktalar1])
                pygame.draw.polygon(ekran, KIRMIZI, [(int(x), int(y)) for x, y in noktalar2])
                # Orta düğüm
                pygame.draw.circle(ekran, (200, 0, 0), (int(papyon_x), int(papyon_y)), 4)
                pygame.draw.circle(ekran, (150, 0, 0), (int(papyon_x), int(papyon_y)), 3)
                # Puantiye
                pygame.draw.circle(ekran, BEYAZ, (int(papyon_x - 7), int(papyon_y - 1)), 1)
                pygame.draw.circle(ekran, BEYAZ, (int(papyon_x + 7), int(papyon_y - 1)), 1)
            else:  # Sol/sağ - yan görünüm
                # Üst kanat
                noktalar1 = [
                    (papyon_x, papyon_y - 10),
                    (papyon_x + 3, papyon_y - 5),
                    (papyon_x - 3, papyon_y - 5)
                ]
                # Alt kanat
                noktalar2 = [
                    (papyon_x, papyon_y + 10),
                    (papyon_x + 3, papyon_y + 5),
                    (papyon_x - 3, papyon_y + 5)
                ]
                pygame.draw.polygon(ekran, KIRMIZI, [(int(x), int(y)) for x, y in noktalar1])
                pygame.draw.polygon(ekran, KIRMIZI, [(int(x), int(y)) for x, y in noktalar2])
                # Orta düğüm
                pygame.draw.circle(ekran, (200, 0, 0), (int(papyon_x), int(papyon_y)), 4)
                pygame.draw.circle(ekran, (150, 0, 0), (int(papyon_x), int(papyon_y)), 3)
                # Puantiye
                pygame.draw.circle(ekran, BEYAZ, (int(papyon_x - 1), int(papyon_y - 7)), 1)
                pygame.draw.circle(ekran, BEYAZ, (int(papyon_x - 1), int(papyon_y + 7)), 1)
            
        elif aksesuar_tipi == "saat":
            # Saat - YÖN BAZLI (yanda/kolda)
            # Saati yönün yanına yerleştir - TEK NOKTA İÇİN yana2=0
            if self.yon[1] != 0:  # Yukarı/aşağı - sağ tarafta
                # yana1=-13, yana2=0 olunca tek koordinat döner
                temp = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=10, yana1=-13, yana2=0)
                if len(temp) == 2:
                    saat_x, saat_y = temp
                else:
                    saat_x, saat_y, _, _ = temp
            else:  # Sol/sağ - alt tarafta
                saat_x, saat_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=10, yana1=0, yana2=0)
                saat_y += 3  # Biraz aşağı kaydır
            
            # Kayış
            if self.yon[1] != 0:  # Yukarı/aşağı - dikey kayış
                pygame.draw.line(ekran, (80, 80, 80), (int(saat_x - 3), int(saat_y - 8)), (int(saat_x - 3), int(saat_y + 8)), 2)
            else:  # Sol/sağ - yatay kayış
                pygame.draw.line(ekran, (80, 80, 80), (int(saat_x - 8), int(saat_y - 3)), (int(saat_x + 8), int(saat_y - 3)), 2)
            
            # Saat kasası (daha büyük)
            pygame.draw.circle(ekran, (150, 150, 150), (int(saat_x), int(saat_y)), 7)
            pygame.draw.circle(ekran, (50, 50, 50), (int(saat_x), int(saat_y)), 6)
            # Saat numaraları (12, 3, 6, 9)
            pygame.draw.circle(ekran, (200, 200, 200), (int(saat_x), int(saat_y - 4)), 1)  # 12
            pygame.draw.circle(ekran, (200, 200, 200), (int(saat_x + 4), int(saat_y)), 1)  # 3
            pygame.draw.circle(ekran, (200, 200, 200), (int(saat_x), int(saat_y + 4)), 1)  # 6
            pygame.draw.circle(ekran, (200, 200, 200), (int(saat_x - 4), int(saat_y)), 1)  # 9
            # Akrep ve yelkovan (daha belirgin)
            pygame.draw.line(ekran, (255, 200, 0), (int(saat_x), int(saat_y)), (int(saat_x + 1), int(saat_y - 4)), 2)
            pygame.draw.line(ekran, (255, 255, 255), (int(saat_x), int(saat_y)), (int(saat_x + 3), int(saat_y + 1)), 2)
            # Merkez vida
            pygame.draw.circle(ekran, (255, 215, 0), (int(saat_x), int(saat_y)), 2)
            
        elif aksesuar_tipi == "kupe":
            # Küpe - YÖN BAZLI (yanlarda)
            # İki küpe - yönün yanlarında
            kupe1_x, kupe1_y, kupe2_x, kupe2_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=2, yana1=12, yana2=12)
            
            # Sol küpe
            pygame.draw.circle(ekran, (255, 215, 0), (int(kupe1_x), int(kupe1_y)), 4, 2)
            pygame.draw.circle(ekran, (255, 255, 150), (int(kupe1_x), int(kupe1_y)), 2)
            # Taş (küpenin altında/yanında)
            if self.yon[1] != 0:  # Yukarı/aşağı - taş altta
                pygame.draw.circle(ekran, KIRMIZI, (int(kupe1_x), int(kupe1_y + 5)), 3)
                pygame.draw.circle(ekran, (255, 100, 100), (int(kupe1_x), int(kupe1_y + 5)), 2)
            else:  # Sol/sağ - taş yanda
                pygame.draw.circle(ekran, KIRMIZI, (int(kupe1_x + 5), int(kupe1_y)), 3)
                pygame.draw.circle(ekran, (255, 100, 100), (int(kupe1_x + 5), int(kupe1_y)), 2)
            
            # Sağ küpe
            pygame.draw.circle(ekran, (255, 215, 0), (int(kupe2_x), int(kupe2_y)), 4, 2)
            pygame.draw.circle(ekran, (255, 255, 150), (int(kupe2_x), int(kupe2_y)), 2)
            # Taş
            if self.yon[1] != 0:  # Yukarı/aşağı - taş altta
                pygame.draw.circle(ekran, KIRMIZI, (int(kupe2_x), int(kupe2_y + 5)), 3)
                pygame.draw.circle(ekran, (255, 100, 100), (int(kupe2_x), int(kupe2_y + 5)), 2)
            else:  # Sol/sağ - taş yanda
                pygame.draw.circle(ekran, KIRMIZI, (int(kupe2_x + 5), int(kupe2_y)), 3)
                pygame.draw.circle(ekran, (255, 100, 100), (int(kupe2_x + 5), int(kupe2_y)), 2)
            
        elif aksesuar_tipi == "zincir":
            # Zincir - YÖN BAZLI (boyunda/kafanın altında)
            zincir_x, zincir_y = self._yon_bazli_offset_hesapla(merkez_x, merkez_y, ileri=12, yana1=0)
            
            if self.yon[1] != 0:  # Yukarı/aşağı - yatay zincir
                halka_sayisi = 7
                for i in range(halka_sayisi):
                    x = zincir_x - 12 + (i * 4)
                    y = zincir_y + (2 if i % 2 == 0 else 0)  # Dalgalı efekt
                    # Altın halka
                    pygame.draw.circle(ekran, (255, 215, 0), (int(x), int(y)), 3)
                    pygame.draw.circle(ekran, (218, 165, 32), (int(x), int(y)), 2)
                    pygame.draw.circle(ekran, (255, 255, 200), (int(x - 1), int(y - 1)), 1)
                # Ortada madalyon
                pygame.draw.circle(ekran, (255, 215, 0), (int(zincir_x), int(zincir_y + 2)), 5)
                pygame.draw.circle(ekran, (218, 165, 32), (int(zincir_x), int(zincir_y + 2)), 4)
                pygame.draw.circle(ekran, KIRMIZI, (int(zincir_x), int(zincir_y + 2)), 2)
            else:  # Sol/sağ - dikey zincir
                halka_sayisi = 7
                for i in range(halka_sayisi):
                    x = zincir_x + (2 if i % 2 == 0 else 0)  # Dalgalı efekt
                    y = zincir_y - 12 + (i * 4)
                    # Altın halka
                    pygame.draw.circle(ekran, (255, 215, 0), (int(x), int(y)), 3)
                    pygame.draw.circle(ekran, (218, 165, 32), (int(x), int(y)), 2)
                    pygame.draw.circle(ekran, (255, 255, 200), (int(x - 1), int(y - 1)), 1)
                # Ortada madalyon
                pygame.draw.circle(ekran, (255, 215, 0), (int(zincir_x + 2), int(zincir_y)), 5)
                pygame.draw.circle(ekran, (218, 165, 32), (int(zincir_x + 2), int(zincir_y)), 4)
                pygame.draw.circle(ekran, KIRMIZI, (int(zincir_x + 2), int(zincir_y)), 2)
