"""
Bomba sınıfı - Bomba modu için
"""
import pygame
import random
import math
import os
from constants import *

class Bomb:
    # Bomba emoji'sini sınıf değişkeni olarak yükle
    _bomb_image = None
    _image_loaded = False
    
    def __init__(self, x, y):
        """Bomba oluştur"""
        self.x = x
        self.y = y
        self.animasyon_sayaci = 0
        self.parlama_animasyon = 0  # Fitil parlama animasyonu
        
        # İlk kez bomba emoji'sini yükle
        if not Bomb._image_loaded:
            Bomb._load_bomb_image()
            Bomb._image_loaded = True
    
    @classmethod
    def _load_bomb_image(cls):
        """Bomba emoji PNG'sini yükle"""
        try:
            path = os.path.join("icons", "bomb.png")
            image = pygame.image.load(path).convert_alpha()
            cls._bomb_image = pygame.transform.smoothscale(image, (25, 25))
            print(f"✅ bomb.png yüklendi")
        except Exception as e:
            print(f"❌ bomb.png yüklenemedi: {e}")
            cls._bomb_image = None
        
    def guncelle(self):
        """Animasyonları güncelle"""
        self.animasyon_sayaci += 1
        self.parlama_animasyon = (self.parlama_animasyon + 0.2) % (2 * math.pi)
        
    def ciz(self, ekran, offset_x=0, offset_y=0, scale=1.0):
        """Bombayı emoji PNG olarak çiz"""
        # Gerçek ekran pozisyonunu hesapla
        ekran_x = int(self.x * scale + offset_x)
        ekran_y = int(self.y * scale + offset_y)
        boyut = int(HUCRE_BOYUTU * scale)
        
        merkez_x = ekran_x + boyut // 2
        merkez_y = ekran_y + boyut // 2
        
        # Bomba emoji PNG'sini göster
        if Bomb._bomb_image:
            # 30x30 boyutunda emoji
            scaled_size = int(30 * scale)
            if scale != 1.0:
                scaled_image = pygame.transform.smoothscale(Bomb._bomb_image, (scaled_size, scaled_size))
            else:
                scaled_image = Bomb._bomb_image
            
            rect = scaled_image.get_rect(center=(merkez_x, merkez_y))
            ekran.blit(scaled_image, rect)
        else:
            # Fallback - eski 3D bomba görüntüsü
            yaricap = int(boyut * 0.4)
            
            # Gölge
            golge_offset = int(2 * scale)
            pygame.draw.circle(ekran, (30, 30, 30), 
                              (merkez_x + golge_offset, merkez_y + golge_offset), 
                              yaricap)
            
            # Ana gövde (koyu gri)
            pygame.draw.circle(ekran, BOMBA_RENK, (merkez_x, merkez_y), yaricap)
            
            # 3D parlama efekti (sol üst)
            parlama_x = merkez_x - int(yaricap * 0.3)
            parlama_y = merkez_y - int(yaricap * 0.3)
            parlama_yaricap = int(yaricap * 0.3)
            pygame.draw.circle(ekran, (100, 100, 100), 
                              (parlama_x, parlama_y), 
                              parlama_yaricap)
            
            # Fitil
            fitil_x = merkez_x
            fitil_y = merkez_y - yaricap
            fitil_yukseklik = int(boyut * 0.3)
            pygame.draw.line(ekran, BOMBA_FITIL_RENK, 
                            (fitil_x, fitil_y), 
                            (fitil_x, fitil_y - fitil_yukseklik), 
                            int(2 * scale))
            
            # Fitil ucu - parlayan animasyon
            parlama_yogunluk = abs(math.sin(self.parlama_animasyon))
            parlama_renk = (
                int(255 * parlama_yogunluk),
                int(100 * parlama_yogunluk),
                0
            )
            fitil_uc_y = fitil_y - fitil_yukseklik
            uc_yaricap = int(3 * scale)
            pygame.draw.circle(ekran, parlama_renk, 
                              (fitil_x, fitil_uc_y), 
                              uc_yaricap)
            
            # Parlama halkası (pulse efekti)
            if parlama_yogunluk > 0.7:
                halka_yaricap = int(uc_yaricap * 2)
                halka_renk = (255, 150, 0, int(100 * parlama_yogunluk))
                # Pygame'de alpha için surface kullanmak gerekir
                halka_surface = pygame.Surface((halka_yaricap * 2, halka_yaricap * 2), pygame.SRCALPHA)
                pygame.draw.circle(halka_surface, halka_renk, 
                                 (halka_yaricap, halka_yaricap), 
                                 halka_yaricap, int(1 * scale))
                ekran.blit(halka_surface, 
                          (fitil_x - halka_yaricap, fitil_uc_y - halka_yaricap))
    
    def patlama_efekti_olustur(self):
        """Patlama için parçacık listesi döndür (effects.py ile uyumlu)"""
        # Bu fonksiyon game.py'den çağrılacak
        return {
            'x': self.x,
            'y': self.y,
            'renk': BOMBA_PARLAMA_RENK
        }


class BombManager:
    """Tüm bombaları yöneten sınıf"""
    def __init__(self, grid_genislik, grid_yukseklik, hucre_boyutu=30):
        self.grid_genislik = grid_genislik
        self.grid_yukseklik = grid_yukseklik
        self.hucre_boyutu = hucre_boyutu
        self.bombalar = []
        self.min_yilan_mesafesi = 0  # Yılanlardan minimum mesafe (0 = kontrol yok)
    
    def _pozisyon_uygun_mu(self, x, y, yasak_pozisyonlar, min_yilan_mesafesi=0, min_bomba_mesafesi=5):
        """
        Pozisyonun bomba yerleştirmek için uygun olup olmadığını kontrol eder
        
        Args:
            x, y: Kontrol edilecek pozisyon
            yasak_pozisyonlar: Yasak pozisyonlar listesi
            min_yilan_mesafesi: Yılanlardan minimum mesafe (blok sayısı)
            min_bomba_mesafesi: Diğer bombalardan minimum mesafe (blok sayısı)
        
        Returns:
            bool: Pozisyon uygunsa True, değilse False
        """
        # Yasak pozisyonda mı?
        if (x, y) in yasak_pozisyonlar:
            return False
        
        # Yılanlara çok yakın mı? (PVP bomba modu için)
        if min_yilan_mesafesi > 0:
            for yasak_x, yasak_y in yasak_pozisyonlar:
                mesafe = (abs(yasak_x - x) + abs(yasak_y - y)) / self.hucre_boyutu
                if mesafe < min_yilan_mesafesi:
                    return False
        
        # Diğer bombalara çok yakın mı?
        for bomba in self.bombalar:
            mesafe = abs(bomba.x - x) + abs(bomba.y - y)
            if mesafe < min_bomba_mesafesi * self.hucre_boyutu:
                return False
        
        return True
    
    def bombalari_olustur(self, yasak_pozisyonlar, min_yilan_mesafesi=0):
        """Bombaları oluştur - PVP modunda min_yilan_mesafesi=3 kullan"""
        self.bombalar = []
        self.min_yilan_mesafesi = min_yilan_mesafesi
        denemeler = 0
        max_deneme = 100
        
        while len(self.bombalar) < BOMBA_SAYISI and denemeler < max_deneme:
            x = random.randint(0, self.grid_genislik - 1) * self.hucre_boyutu
            y = random.randint(0, self.grid_yukseklik - 1) * self.hucre_boyutu
            
            # Pozisyon uygun mu kontrol et
            if self._pozisyon_uygun_mu(x, y, yasak_pozisyonlar, min_yilan_mesafesi, min_bomba_mesafesi=5):
                self.bombalar.append(Bomb(x, y))
            
            denemeler += 1
    
    def guncelle(self):
        """Tüm bombaları güncelle"""
        for bomba in self.bombalar:
            bomba.guncelle()
    
    def ciz(self, ekran, offset_x=0, offset_y=0, scale=1.0):
        """Tüm bombaları çiz"""
        for bomba in self.bombalar:
            bomba.ciz(ekran, offset_x, offset_y, scale)
    
    def carpma_kontrol(self, x, y):
        """Verilen pozisyon bir bombaya çarptı mı?"""
        for bomba in self.bombalar:
            if bomba.x == x and bomba.y == y:
                return bomba
        return None
    
    def bomba_pozisyonlari(self):
        """Tüm bomba pozisyonlarını liste olarak döndür"""
        return [(bomba.x, bomba.y) for bomba in self.bombalar]
    
    def bombalari_yerlestir(self, yasak_pozisyonlar, min_yilan_mesafesi=0):
        """Mevcut bombaları rastgele yeni pozisyonlara taşı - PVP modunda min_yilan_mesafesi=3"""
        if not self.bombalar:
            return
        
        # Her bomba için yeni pozisyon bul
        yeni_pozisyonlar = []
        for bomba in self.bombalar:
            denemeler = 0
            max_deneme = 50
            uygun_pozisyon_bulundu = False
            
            while denemeler < max_deneme:
                x = random.randint(0, self.grid_genislik - 1) * self.hucre_boyutu
                y = random.randint(0, self.grid_yukseklik - 1) * self.hucre_boyutu
                
                # Geçici bomba listesi yeni pozisyonlarla birleştir
                tum_yasak_pozlar = list(yasak_pozisyonlar) + yeni_pozisyonlar
                
                # Yeni pozisyonlarla minimum 3 blok mesafe için geçici bomba oluştur
                eski_bombalar = self.bombalar.copy()
                self.bombalar = [Bomb(px, py) for px, py in yeni_pozisyonlar]
                
                # Pozisyon uygun mu kontrol et (yeni pozisyonlara 3 blok mesafe)
                if self._pozisyon_uygun_mu(x, y, tum_yasak_pozlar, min_yilan_mesafesi, min_bomba_mesafesi=3):
                    yeni_pozisyonlar.append((x, y))
                    uygun_pozisyon_bulundu = True
                    self.bombalar = eski_bombalar  # Restore et
                    break
                
                self.bombalar = eski_bombalar  # Restore et
                denemeler += 1
            
            # Eğer uygun pozisyon bulunamadıysa, bomba eski yerinde kalsın
            if not uygun_pozisyon_bulundu:
                yeni_pozisyonlar.append((bomba.x, bomba.y))
        
        # Bombaları yeni pozisyonlara taşı
        for i, bomba in enumerate(self.bombalar):
            if i < len(yeni_pozisyonlar):
                bomba.x, bomba.y = yeni_pozisyonlar[i]
