"""
Yardımcı fonksiyonlar
"""
import pygame
import os
from constants import *


# Windows optimizasyonu: Surface cache
_surface_cache = {}

def arkaplan_yukle(resim_yolu, genislik, yukseklik):
    """Arka plan resmini yükler ve boyutlandırır, transparan yapar - Cache ile optimize"""
    cache_key = f"{resim_yolu}_{genislik}_{yukseklik}"
    
    # Cache'de varsa döndür
    if cache_key in _surface_cache:
        return _surface_cache[cache_key]
    
    try:
        if resim_yolu and os.path.exists(resim_yolu):
            resim = pygame.image.load(resim_yolu)
            resim = pygame.transform.scale(resim, (genislik, yukseklik))
            # Transparan surface oluştur
            transparan_resim = resim.copy()
            transparan_resim.set_alpha(ARKAPLAN_ALPHA)
            
            # Cache'e ekle
            _surface_cache[cache_key] = transparan_resim
            return transparan_resim
    except:
        pass
    return None


def gradient_arkaplan_ciz(ekran):
    """Gradient arkaplan çizer"""
    for y in range(YUKSEKLIK):
        renk_deger = int(20 + (y / YUKSEKLIK) * 20)
        pygame.draw.line(ekran, (renk_deger, renk_deger, renk_deger + 20), 
                       (0, y), (GENISLIK, y))


def izgara_ciz(ekran, renk=(40, 40, 50), offset_x=0, offset_y=0):
    """Izgara çizer"""
    for x in range(0, GENISLIK, HUCRE_BOYUTU):
        pygame.draw.line(ekran, renk, (x + offset_x, offset_y), (x + offset_x, YUKSEKLIK + offset_y))
    for y in range(0, YUKSEKLIK, HUCRE_BOYUTU):
        pygame.draw.line(ekran, renk, (offset_x, y + offset_y), (GENISLIK + offset_x, y + offset_y))
