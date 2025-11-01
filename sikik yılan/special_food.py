import pygame
import random
import os
from constants import *
from food import Yem

class OzelYem(Yem):
    # Özel yem görsellerini sınıf değişkenleri olarak yükle
    _special_images = {}
    _images_loaded = False
    
    def __init__(self, tur="normal"):
        super().__init__()
        self.tur = tur  # "kalkan", "elmas", "zehirli", "dondurucu", "hiz", "yavaslama"
        self.parlama_sayaci = 0
        
        # Özel yem görsellerini yükle (ilk kez)
        if not OzelYem._images_loaded:
            OzelYem._load_special_images()
            OzelYem._images_loaded = True
    
    @classmethod
    def _load_special_images(cls):
        """Tüm özel yem emoji PNG'lerini yükle"""
        special_files = {
            "kalkan": "shield.png",      # 🛡️
            "elmas": "diamond.png",       # 💎
            "zehirli": "poison.png",      # ☠️
            "dondurucu": "freeze.png",    # ❄️
            "hiz": "lightning.png",       # ⚡
            "yavaslama": "snail.png"      # 🐌
        }
        
        for tur, filename in special_files.items():
            try:
                path = os.path.join("icons", filename)
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.smoothscale(image, (32, 32))
                cls._special_images[tur] = image
                print(f"✅ {filename} yüklendi")
            except Exception as e:
                print(f"❌ {filename} yüklenemedi: {e}")
                cls._special_images[tur] = None
        
    def ciz(self, ekran):
        x_px, y_px = self.pozisyon
        x = x_px + HUCRE_BOYUTU // 2
        y = y_px + HUCRE_BOYUTU // 2
        
        # Özel yem PNG'sini göster
        if self.tur in OzelYem._special_images and OzelYem._special_images[self.tur]:
            image = OzelYem._special_images[self.tur]
            rect = image.get_rect(center=(x, y))
            ekran.blit(image, rect)
        else:
            # Fallback - renkli daire
            fallback_colors = {
                "kalkan": (192, 192, 192),  # Gümüş
                "elmas": (135, 206, 250),   # Açık mavi
                "zehirli": (128, 0, 128),   # Mor
                "dondurucu": (173, 216, 230), # Açık mavi
                "hiz": (255, 255, 0),       # Sarı
                "yavaslama": (144, 238, 144) # Açık yeşil
            }
            color = fallback_colors.get(self.tur, (255, 255, 255))
            pygame.draw.circle(ekran, color, (x, y), HUCRE_BOYUTU // 3)
    
    def puan_dondur(self):
        """Yenildiğinde kazanılan puanı döndürür"""
        if self.tur == "altin_elma":
            return ALTIN_ELMA_PUAN
        elif self.tur == "elmas":
            return ELMAS_PUAN
        elif self.tur == "zehirli":
            return ZEHIRLI_CEZA
        elif self.tur == "dondurucu":
            return 10  # Normal puan
        return 10  # Normal yem puanı


class PVPOzelYem(Yem):
    """PVP modunda oyunculara özel yetenekli yemler"""
    def __init__(self, tur="kalkan", sahip_oyuncu=1, yilan_renk=(0, 255, 0)):
        super().__init__()
        self.tur = tur  # "kalkan", "hiz" veya "yavaslama"
        self.sahip_oyuncu = sahip_oyuncu  # 1 veya 2
        self.yilan_renk = yilan_renk  # Sahibinin yılan rengi
        self.parlama_sayaci = 0
        
    def ciz(self, ekran):
        """PVP özel yemlerini PNG olarak çizer"""
        if not OzelYem._images_loaded:
            OzelYem._load_special_images()
        
        x_px, y_px = self.pozisyon
        radius = HUCRE_BOYUTU // 2 - 1
        x = x_px + HUCRE_BOYUTU // 2
        y = y_px + HUCRE_BOYUTU // 2
        
        # Yem türüne göre PNG göster
        if self.tur in OzelYem._special_images and OzelYem._special_images[self.tur]:
            img = OzelYem._special_images[self.tur]
            rect = img.get_rect(center=(x, y))
            ekran.blit(img, rect)
        else:
            # PNG yoksa fallback renk
            fallback_colors = {
                "kalkan": self.yilan_renk,  # Oyuncu renginde
                "hiz": (255, 0, 0),
                "yavaslama": (128, 128, 128)
            }
            color = fallback_colors.get(self.tur, (200, 200, 200))
            pygame.draw.circle(ekran, color, (x, y), radius)
    
    def puan_dondur(self):
        """Yenildiğinde kazanılan puanı döndürür"""
        return 15  # PVP özel yemleri biraz daha değerli
