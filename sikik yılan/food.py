"""
Yem (Meyve) sınıfı
"""
import pygame
import random
import math
import os
import constants


class Yem:
    # Meyve görsellerini sınıf değişkenleri olarak yükle
    _fruit_images = {}
    _images_loaded = False
    
    def __init__(self, ekran_genislik=constants.GENISLIK, ekran_yukseklik=constants.YUKSEKLIK, sahte_mi=False, hucre_boyutu=constants.HUCRE_BOYUTU):
        self.ekran_genislik = ekran_genislik
        self.ekran_yukseklik = ekran_yukseklik
        self.hucre_boyutu = hucre_boyutu  # DİNAMİK HÜCRE BOYUTU
        self.pozisyon = (0, 0)
        self.meyve_turu = 0
        self.sahte_mi = sahte_mi  # Sahte yem mi?
        self.bombaya_donustu = False  # Bombaya dönüştü mü?
        self.donusum_animasyon = 0  # Dönüşüm animasyon frame'i
        
        # Meyve görsellerini yükle (ilk kez)
        if not Yem._images_loaded:
            Yem._load_fruit_images()
            Yem._images_loaded = True
        
        self.rastgele_konumla()
    
    @classmethod
    def _load_fruit_images(cls):
        """Tüm meyve emoji PNG'lerini yükle"""
        fruit_files = {
            0: "apple.png",      # Elma
            1: "orange.png",     # Portakal
            2: "grapes.png",     # Üzüm
            3: "cherries.png",   # Kiraz
            4: "banana.png"      # Muz
        }
        
        for index, filename in fruit_files.items():
            try:
                path = os.path.join("icons", filename)
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.smoothscale(image, (32, 32))
                cls._fruit_images[index] = image
                # Windows terminal emoji sorununu önle
                try:
                    print(f"✅ {filename} yüklendi")
                except UnicodeEncodeError:
                    print(f"[OK] {filename} yuklendi")
            except Exception as e:
                try:
                    print(f"❌ {filename} yüklenemedi: {e}")
                except UnicodeEncodeError:
                    print(f"[HATA] {filename} yuklenemedi: {e}")
                cls._fruit_images[index] = None

    def rastgele_konumla(self):
        x = random.randint(0, (self.ekran_genislik // constants.HUCRE_BOYUTU) - 1) * constants.HUCRE_BOYUTU
        y = random.randint(0, (self.ekran_yukseklik // constants.HUCRE_BOYUTU) - 1) * constants.HUCRE_BOYUTU
        self.pozisyon = (x, y)
        # Rastgele meyve türü seç: 0=Elma, 1=Portakal, 2=Üzüm, 3=Kiraz, 4=Muz
        self.meyve_turu = random.randint(0, 4)
    
    def yilan_ile_ayni_hizada_mi(self, yilan_bas_x, yilan_bas_y):
        """Yılan ile yem aynı satır veya sütunda mı kontrol et"""
        # Aynı satırda mı? (y koordinatları aynı)
        ayni_satirda = (self.pozisyon[1] == yilan_bas_y)
        # Aynı sütunda mı? (x koordinatları aynı)
        ayni_sutunda = (self.pozisyon[0] == yilan_bas_x)
        
        return ayni_satirda or ayni_sutunda
    
    def yilan_mesafesi(self, yilan_bas_x, yilan_bas_y):
        """Yılan başı ile yem arasındaki blok mesafesini hesapla"""
        x_fark = abs(self.pozisyon[0] - yilan_bas_x) // constants.HUCRE_BOYUTU
        y_fark = abs(self.pozisyon[1] - yilan_bas_y) // constants.HUCRE_BOYUTU
        return max(x_fark, y_fark)  # Chebyshev mesafesi (dik açı için)
    
    def bombaya_donustur(self):
        """Sahte yemi bombaya dönüştür"""
        if self.sahte_mi and not self.bombaya_donustu:
            self.bombaya_donustu = True
            self.donusum_animasyon = 0
            return True
        return False

    def ciz(self, ekran, offset_x=0, offset_y=0):
        x = self.pozisyon[0] + self.hucre_boyutu // 2 + offset_x
        y = self.pozisyon[1] + self.hucre_boyutu // 2 + offset_y
        
        # Bombaya dönüştüyse bomba çiz
        if self.bombaya_donustu:
            self._bomba_ciz(ekran, x, y)
            self.donusum_animasyon += 1
            return
        
        # Meyve PNG'sini göster - hücre boyutuna göre ölçeklendir
        if self.meyve_turu in Yem._fruit_images and Yem._fruit_images[self.meyve_turu]:
            # Meyve boyutunu hücre boyutunun %80'i olarak ayarla (içinde biraz boşluk bırak)
            meyve_boyutu = int(self.hucre_boyutu * 0.8)
            image = pygame.transform.smoothscale(Yem._fruit_images[self.meyve_turu], (meyve_boyutu, meyve_boyutu))
            rect = image.get_rect(center=(x, y))
            ekran.blit(image, rect)
        else:
            # Fallback - basit renkli daire
            fallback_colors = {
                0: (220, 20, 60),   # Elma - kırmızı
                1: (255, 165, 0),   # Portakal - turuncu  
                2: (148, 0, 211),   # Üzüm - mor
                3: (220, 20, 60),   # Kiraz - kırmızı
                4: (255, 225, 53)   # Muz - sarı
            }
            color = fallback_colors.get(self.meyve_turu, (255, 255, 255))
            pygame.draw.circle(ekran, color, (x, y), self.hucre_boyutu // 3)
    
    def _bomba_ciz(self, ekran, merkez_x, merkez_y):
        """Bombaya dönüşmüş sahte yemi çiz"""
        # Dönüşüm animasyonu (zoom in efekti)
        if self.donusum_animasyon < 10:
            scale = 0.5 + (self.donusum_animasyon / 10) * 0.5
        else:
            scale = 1.0
        
        yaricap = int((self.hucre_boyutu * 0.4) * scale)
        
        # Gölge
        golge_offset = 2
        pygame.draw.circle(ekran, (30, 30, 30), 
                          (merkez_x + golge_offset, merkez_y + golge_offset), 
                          yaricap)
        
        # Ana gövde (koyu gri)
        pygame.draw.circle(ekran, BOMBA_RENK, (merkez_x, merkez_y), yaricap)
        
        # 3D parlama efekti
        parlama_x = merkez_x - int(yaricap * 0.3)
        parlama_y = merkez_y - int(yaricap * 0.3)
        parlama_yaricap = int(yaricap * 0.3)
        pygame.draw.circle(ekran, (100, 100, 100), 
                          (parlama_x, parlama_y), 
                          parlama_yaricap)
        
        # Fitil
        fitil_x = merkez_x
        fitil_y = merkez_y - yaricap
        fitil_yukseklik = int(constants.HUCRE_BOYUTU * 0.3 * scale)
        pygame.draw.line(ekran, BOMBA_FITIL_RENK, 
                        (fitil_x, fitil_y), 
                        (fitil_x, fitil_y - fitil_yukseklik), 
                        2)
        
        # Fitil ucu - parlayan
        parlama_animasyon = (pygame.time.get_ticks() / 300) % (2 * math.pi)
        parlama_yogunluk = abs(math.sin(parlama_animasyon))
        parlama_renk = (
            int(255 * parlama_yogunluk),
            int(100 * parlama_yogunluk),
            0
        )
        fitil_uc_y = fitil_y - fitil_yukseklik
        uc_yaricap = 3
        pygame.draw.circle(ekran, parlama_renk, 
                          (fitil_x, fitil_uc_y), 
                          uc_yaricap)
    
    def _sahte_yem_ciz(self, ekran, merkez_x, merkez_y):
        """Sahte yemi + işareti olarak çiz"""
        # + işareti boyutu
        boyut = constants.HUCRE_BOYUTU // 2 - 2
        kalinlik = 4
        
        # Parlayan animasyon
        parlama = abs(math.sin(pygame.time.get_ticks() / 200))
        renk_yogunluk = int(150 + 105 * parlama)
        plus_renk = (renk_yogunluk, renk_yogunluk, 0)  # Sarımsı
        
        # Gölge
        golge_renk = (80, 80, 0)
        pygame.draw.line(ekran, golge_renk, 
                        (merkez_x - boyut + 2, merkez_y + 2), 
                        (merkez_x + boyut + 2, merkez_y + 2), 
                        kalinlik)
        pygame.draw.line(ekran, golge_renk, 
                        (merkez_x + 2, merkez_y - boyut + 2), 
                        (merkez_x + 2, merkez_y + boyut + 2), 
                        kalinlik)
        
        # + işareti (yatay çizgi)
        pygame.draw.line(ekran, plus_renk, 
                        (merkez_x - boyut, merkez_y), 
                        (merkez_x + boyut, merkez_y), 
                        kalinlik)
        
        # + işareti (dikey çizgi)
        pygame.draw.line(ekran, plus_renk, 
                        (merkez_x, merkez_y - boyut), 
                        (merkez_x, merkez_y + boyut), 
                        kalinlik)
        
        # Parlak kenarlık efekti
        parlak_renk = (255, 255, 100)
        pygame.draw.line(ekran, parlak_renk, 
                        (merkez_x - boyut, merkez_y), 
                        (merkez_x + boyut, merkez_y), 
                        1)
        pygame.draw.line(ekran, parlak_renk, 
                        (merkez_x, merkez_y - boyut), 
                        (merkez_x, merkez_y + boyut), 
                        1)
