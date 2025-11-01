"""
Görsel efektler - Parçacık sistemleri ve animasyonlar
"""
import pygame
import random
import math
from constants import *


class Parcacik:
    """Tek bir parçacık"""
    def __init__(self, x, y, renk, hiz_x=0, hiz_y=0, omur=30):
        self.x = x
        self.y = y
        self.renk = renk
        self.hiz_x = hiz_x
        self.hiz_y = hiz_y
        self.omur = omur
        self.max_omur = omur
        self.boyut = random.randint(2, 4)
    
    def guncelle(self, dt_multiplier=1.0):
        """Parçacığı güncelle - dt_multiplier ile FPS'ten bağımsız"""
        self.x += self.hiz_x * dt_multiplier
        self.y += self.hiz_y * dt_multiplier
        self.omur -= 1 * dt_multiplier
        # Yerçekimi efekti
        self.hiz_y += 0.1 * dt_multiplier
        return self.omur > 0
    
    def ciz(self, ekran, offset_x=0, offset_y=0):
        """Parçacığı çiz - OFFSET İLE"""
        # Ömre göre alpha hesapla
        alpha = int(255 * (self.omur / self.max_omur))
        renk_alpha = (*self.renk[:3], alpha)
        
        # Parçacık boyutu ömre göre küçülür
        boyut = max(1, int(self.boyut * (self.omur / self.max_omur)))
        
        # Geçici surface (alpha için)
        temp_surface = pygame.Surface((boyut * 2, boyut * 2), pygame.SRCALPHA)
        pygame.draw.circle(temp_surface, renk_alpha, (boyut, boyut), boyut)
        ekran.blit(temp_surface, (int(self.x - boyut + offset_x), int(self.y - boyut + offset_y)))


class BaseEffect:
    """Tüm efekt sınıfları için temel sınıf - FPS-bağımsız güncelleme"""
    
    def __init__(self, fps_hedef=30.0):
        self.fps_hedef = fps_hedef
    
    def _dt_multiplier_hesapla(self, current_fps):
        """FPS'e göre delta time multiplier hesapla"""
        return self.fps_hedef / max(1, current_fps)


class YilanIziEfekti(BaseEffect):
    """Yılanın arkasından çıkan parçacık efekti"""
    def __init__(self):
        super().__init__(fps_hedef=30.0)
        self.parcaciklar = []
    
    def parcacik_ekle(self, x, y, yilan_renk=YESIL):
        """Yılan hücresinden parçacık oluştur"""
        # Her frame'de 2 parçacık - daha dolgun görünüm
        for _ in range(2):
            # Rastgele pozisyon offset
            offset_x = random.randint(-6, 6)
            offset_y = random.randint(-6, 6)
            
            # Rastgele hız (biraz daha yavaş ama görünür)
            hiz_x = random.uniform(-0.6, 0.6)
            hiz_y = random.uniform(-0.6, 0.6)
            
            # Renk varyasyonu (daha canlı)
            renk_var = random.randint(-30, 30)
            renk = (
                max(0, min(255, yilan_renk[0] + renk_var)),
                max(0, min(255, yilan_renk[1] + renk_var)),
                max(0, min(255, yilan_renk[2] + renk_var))
            )
            
            parcacik = Parcacik(
                x + HUCRE_BOYUTU // 2 + offset_x,
                y + HUCRE_BOYUTU // 2 + offset_y,
                renk,
                hiz_x,
                hiz_y,
                omur=random.randint(25, 45)  # Daha uzun ömür (15-30 → 25-45)
            )
            self.parcaciklar.append(parcacik)
    
    def guncelle(self, current_fps=60):
        """Tüm parçacıkları güncelle - FPS'ten bağımsız"""
        dt_multiplier = self._dt_multiplier_hesapla(current_fps)
        self.parcaciklar = [p for p in self.parcaciklar if p.guncelle(dt_multiplier)]
    
    def ciz(self, ekran, offset_x=0, offset_y=0):
        """Tüm parçacıkları çiz - OFFSET İLE"""
        for parcacik in self.parcaciklar:
            parcacik.ciz(ekran, offset_x, offset_y)
    
    def temizle(self):
        """Tüm parçacıkları temizle"""
        self.parcaciklar.clear()


class YemYemeEfekti(BaseEffect):
    """Yem yendiğinde patlama efekti"""
    def __init__(self):
        super().__init__(fps_hedef=30.0)
        self.aktif_efektler = []
    
    def efekt_ekle(self, x, y, meyve_renk=KIRMIZI):
        """Yem pozisyonunda patlama efekti oluştur"""
        efekt = {
            'parcaciklar': [],
            'sure': 20  # Daha uzun süre (12 → 20) - daha görünür
        }
        
        # Dengeli: Güzel görünüm için yeterli parçacık (35 → 40)
        parcacik_sayisi = 40
        for i in range(parcacik_sayisi):
            aci = (360 / parcacik_sayisi) * i
            aci_rad = math.radians(aci)
            
            # Daha yavaş ama düzgün yayılma
            hiz = random.uniform(6, 12)  # Daha yavaş (10-18 → 6-12)
            hiz_x = math.cos(aci_rad) * hiz
            hiz_y = math.sin(aci_rad) * hiz
            
            # Renk varyasyonu
            renk_var = random.randint(-30, 30)
            renk = (
                max(0, min(255, meyve_renk[0] + renk_var)),
                max(0, min(255, meyve_renk[1] + renk_var)),
                max(0, min(255, meyve_renk[2] + renk_var))
            )
            
            parcacik = Parcacik(
                x + HUCRE_BOYUTU // 2,
                y + HUCRE_BOYUTU // 2,
                renk,
                hiz_x,
                hiz_y,
                omur=random.randint(12, 18)  # Daha uzun ömür (6-10 → 12-18)
            )
            efekt['parcaciklar'].append(parcacik)
        
        # Yıldız parçacıkları - daha uzun ömürlü
        for _ in range(20):  # Biraz daha fazla (15 → 20)
            hiz_x = random.uniform(-8, 8)  # Daha yavaş
            hiz_y = random.uniform(-8, 8)
            
            renk = (
                random.randint(200, 255),
                random.randint(200, 255),
                random.randint(0, 100)
            )
            
            parcacik = Parcacik(
                x + HUCRE_BOYUTU // 2,
                y + HUCRE_BOYUTU // 2,
                renk,
                hiz_x,
                hiz_y,
                omur=random.randint(8, 14)  # Daha uzun (4-8 → 8-14)
            )
            efekt['parcaciklar'].append(parcacik)
        
        self.aktif_efektler.append(efekt)
    
    def guncelle(self, current_fps=60):
        """Tüm efektleri güncelle - FPS'ten bağımsız"""
        dt_multiplier = self._dt_multiplier_hesapla(current_fps)
        for efekt in self.aktif_efektler[:]:
            efekt['sure'] -= 1 * dt_multiplier
            efekt['parcaciklar'] = [p for p in efekt['parcaciklar'] if p.guncelle(dt_multiplier)]
            
            # Efekt bittiyse kaldır
            if efekt['sure'] <= 0 or len(efekt['parcaciklar']) == 0:
                self.aktif_efektler.remove(efekt)
    
    def ciz(self, ekran, offset_x=0, offset_y=0):
        """Tüm efektleri çiz - OFFSET İLE"""
        for efekt in self.aktif_efektler:
            for parcacik in efekt['parcaciklar']:
                parcacik.ciz(ekran, offset_x, offset_y)
    
    def temizle(self):
        """Tüm efektleri temizle"""
        self.aktif_efektler.clear()


class PuanEfekti(BaseEffect):
    """Puan kazanıldığında +1 animasyonu"""
    def __init__(self):
        super().__init__(fps_hedef=30.0)
        self.aktif_metinler = []
    
    def metin_ekle(self, x, y, puan=1):
        """Puan metni ekle"""
        self.aktif_metinler.append({
            'x': x,
            'y': y,
            'puan': puan,
            'omur': 30,  # Daha kısa ömür (40 → 30)
            'max_omur': 30
        })
    
    def guncelle(self, current_fps=60):
        """Metinleri güncelle - FPS'ten bağımsız"""
        dt_multiplier = self._dt_multiplier_hesapla(current_fps)
        for metin in self.aktif_metinler[:]:
            metin['omur'] -= 1 * dt_multiplier
            metin['y'] -= 2.5 * dt_multiplier  # Daha hızlı yukarı (2 → 2.5)
            
            if metin['omur'] <= 0:
                self.aktif_metinler.remove(metin)
    
    def ciz(self, ekran, offset_x=0, offset_y=0):
        """Metinleri çiz - OFFSET İLE"""
        font = pygame.font.Font(None, 36)
        
        for metin in self.aktif_metinler:
            # Ömre göre alpha
            alpha = int(255 * (metin['omur'] / metin['max_omur']))
            
            # Metin oluştur
            text = f"+{metin['puan']}"
            
            # Renk (sarı-turuncu)
            renk = (255, 215, 0)
            
            # Geçici surface
            text_surface = font.render(text, True, renk)
            text_surface.set_alpha(alpha)
            
            # Merkeze yerleştir - OFFSET İLE
            rect = text_surface.get_rect(center=(int(metin['x'] + offset_x), int(metin['y'] + offset_y)))
            ekran.blit(text_surface, rect)
    
    def temizle(self):
        """Tüm metinleri temizle"""
        self.aktif_metinler.clear()
