"""
Ana oyun sınıfı ve oyun döngüsü
"""
import pygame
import sys
import os
import random
import math
from constants import *
from snake import Yilan
from ai_snake import AIYilan
from food import Yem
from menu import Menu
from utils import izgara_ciz, arkaplan_yukle
from settings import AyarYoneticisi
from effects import YilanIziEfekti, YemYemeEfekti, PuanEfekti
from bomb import BombManager
from special_food import OzelYem, PVPOzelYem
from achievements import BasarimYoneticisi
from statistics import IstatistikTakipci
from sounds import SesYoneticisi
import time


class Oyun:
    def __init__(self):
        pygame.init()
        
        # macOS Retina Display desteği
        import platform
        if platform.system() == 'Darwin':  # macOS
            try:
                # Retina ekranlar için high DPI desteği
                import os
                os.environ['SDL_VIDEO_ALLOW_SCREENSAVER'] = '1'
            except:
                pass
        
        # Hardware acceleration için OpenGL (Windows ve macOS)
        try:
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
            pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)
        except:
            pass  # OpenGL desteklenmiyorsa devam et
        
        # Ayar yöneticisini başlat
        self.ayar_yoneticisi = AyarYoneticisi()
        ayarlar = self.ayar_yoneticisi.ayarlari_yukle()
        
        # Ekran ayarlarını yükle
        self.cozunurluk_ayari = ayarlar.get("cozunurluk", "Tam Ekran")
        
        # Ekran bilgisini al
        ekran_bilgisi = pygame.display.Info()
        
        # Platform kontrolü
        import platform
        self.platform = platform.system()  # 'Darwin' (macOS), 'Windows', 'Linux'
        
        # Çözünürlük ayarına göre ekran oluştur
        if self.cozunurluk_ayari == "Tam Ekran":
            # Tam ekran modu - Native çözünürlük kullan
            # Platform bazlı tam ekran modu
            if self.platform == 'Darwin':  # macOS
                # macOS için önce ekran boyutunu al, sonra SCALED ile oluştur
                native_w = ekran_bilgisi.current_w
                native_h = ekran_bilgisi.current_h
                if hasattr(pygame, 'SCALED') and native_w and native_h:
                    fullscreen_flag = pygame.FULLSCREEN | pygame.SCALED
                    self.ekran = pygame.display.set_mode((native_w, native_h), fullscreen_flag)
                else:
                    self.ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            elif self.platform == 'Windows':  # Windows
                # Windows için standart tam ekran
                self.ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:  # Linux ve diğerleri
                self.ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

            self.ekran_genislik = self.ekran.get_width()
            self.ekran_yukseklik = self.ekran.get_height()
            self.tam_ekran = True
            print(f"Tam ekran ({self.platform}): {self.ekran_genislik}x{self.ekran_yukseklik}")
        else:
            # Seçilen çözünürlük - tam ekran modunda
            # Çözünürlük listesinden bul
            cozunurluk_bulundu = False
            for isim, genislik, yukseklik in COZUNURLUK_SECENEKLERI:
                if isim == self.cozunurluk_ayari:
                    self.ekran_genislik = genislik
                    self.ekran_yukseklik = yukseklik
                    cozunurluk_bulundu = True
                    break
            
            if not cozunurluk_bulundu:
                # Varsayılan - ekran boyutunu al
                self.ekran_genislik = ekran_bilgisi.current_w
                self.ekran_yukseklik = ekran_bilgisi.current_h
            
            # Platform bazlı borderless fullscreen
            if self.platform == 'Darwin':  # macOS
                if hasattr(pygame, 'SCALED'):
                    fullscreen_flag = pygame.FULLSCREEN | pygame.SCALED
                else:
                    fullscreen_flag = pygame.FULLSCREEN
                self.ekran = pygame.display.set_mode((self.ekran_genislik, self.ekran_yukseklik), fullscreen_flag)
            elif self.platform == 'Windows':  # Windows
                self.ekran = pygame.display.set_mode((self.ekran_genislik, self.ekran_yukseklik), pygame.FULLSCREEN)
            else:  # Linux
                self.ekran = pygame.display.set_mode((self.ekran_genislik, self.ekran_yukseklik), pygame.FULLSCREEN)
            
            self.tam_ekran = True
            print(f"Çözünürlük modu ({self.platform}): {self.ekran_genislik}x{self.ekran_yukseklik}")
        
        # Oyun alanı için DİKDÖRTGEN bölge hesapla - ekranın tamamını kullan
        # Hücre boyutunu DİNAMİK olarak hesapla - ekran boyutuna göre optimize et
        # KARE HÜCRELER için en küçük boyutu baz al
        min_boyut = min(self.ekran_genislik, self.ekran_yukseklik)
        min_grid_sayisi = 25  # Minimum grid hücresi (çok küçük olmasın)
        max_grid_sayisi = 50  # Maksimum grid hücresi (çok fazla olmasın)
        
        # En uygun hücre boyutunu bul - KARE için
        ideal_hucre_boyutu = min_boyut // min_grid_sayisi
        ideal_hucre_boyutu = max(20, min(50, ideal_hucre_boyutu))  # 20-50 px arası
        
        self.hucre_boyutu = ideal_hucre_boyutu
        
        # Grid boyutlarını hesapla - KARE HÜCRELER
        self.grid_genislik = self.ekran_genislik // self.hucre_boyutu
        self.grid_yukseklik = self.ekran_yukseklik // self.hucre_boyutu
        
        # Oyun alanı boyutlarını grid'e göre hesapla - KARE GRID
        self.oyun_genislik = self.grid_genislik * self.hucre_boyutu
        self.oyun_yukseklik = self.grid_yukseklik * self.hucre_boyutu
        
        # Merkezi hizalama için offset hesapla
        self.oyun_offset_x = (self.ekran_genislik - self.oyun_genislik) // 2
        self.oyun_offset_y = (self.ekran_yukseklik - self.oyun_yukseklik) // 2
        
        # Global değişkenleri güncelle (constants modülü zaten import edildi)
        # NOT: Bu değişkenler artık kullanılmıyor olabilir, ancak eski kod uyumluluğu için bırakıldı
        
        print(f"Oyun alanı: {self.oyun_genislik}x{self.oyun_yukseklik}, Grid: {self.grid_genislik}x{self.grid_yukseklik}, Hücre: {self.hucre_boyutu}px, Offset: ({self.oyun_offset_x}, {self.oyun_offset_y})")
        
        pygame.display.set_caption('Yılan Oyunu 🐍')
        self.saat = pygame.time.Clock()
        self.yilan = None
        self.yem = None
        
        # Menü için ölçeklendirme bilgilerini ayarla
        self.menu = Menu(self.ekran)
        self.menu.ekran_genislik = self.ekran_genislik
        self.menu.ekran_yukseklik = self.ekran_yukseklik
        self.menu.oyun_offset_x = self.oyun_offset_x
        self.menu.oyun_offset_y = self.oyun_offset_y
        
        self.oyun_bitti = False
        self.oyun_durumu = "MENU"  # MENU, MODLAR, SETTINGS, HIZ_AYAR, ARKAPLAN_AYAR, YILAN_AYAR, TEMA_AYAR, GRAFIK_AYAR, BASARIMLAR, ISTATISTIKLER, PVP_ISIM_GIRIS, BOT_ZORLUK_SECIM, PLAYING, PAUSED, GAME_OVER
        self.oyun_duraklatildi = False  # Pause durumu
        
        # PVP isim girişi için
        self.pvp_isim_input_aktif = 1  # 1: Oyuncu 1, 2: Oyuncu 2
        self.pvp_oyuncu1_isim_temp = ""
        self.pvp_oyuncu2_isim_temp = ""
        
        # Kaydedilmiş ayarları yükle
        self.en_yuksek_skor = ayarlar.get("en_yuksek_skor", 0)
        self.hiz_seviyesi = ayarlar.get("hiz_seviyesi", VARSAYILAN_HIZ_SEVIYESI)
        self.menu_arkaplan_yolu = ayarlar.get("menu_arkaplan", None)
        self.oyun_arkaplan_yolu = ayarlar.get("oyun_arkaplan", None)
        self.yilan_renk = ayarlar.get("yilan_renk", VARSAYILAN_YILAN_RENK)
        self.yilan_yuz = ayarlar.get("yilan_yuz", VARSAYILAN_YILAN_YUZ)
        self.yilan_aksesuar = ayarlar.get("yilan_aksesuar", VARSAYILAN_YILAN_AKSESUAR)
        self.bomba_modu = ayarlar.get("bomba_modu", False)  # Bomba modu ayarı
        self.pvp_modu = False  # PVP modu (başlangıçta kapalı)
        self.bot_modu = False  # Bot vs modu (başlangıçta kapalı)
        self.bot_zorluk = VARSAYILAN_BOT_ZORLUK  # Bot zorluk seviyesi
        self.pvp_bomba_modu = False  # PVP bomba modu (başlangıçta kapalı)
        self.pvp_secili_mod = "Normal"  # PVP mod seçimi (Normal veya Bomba)
        self.aktif_tema = ayarlar.get("aktif_tema", "Klasik")  # Tema ayarı
        self.menu_muzik = ayarlar.get("menu_muzik", "Normal")  # Ana menü müziği
        self.oyun_muzik = ayarlar.get("oyun_muzik", "Normal")  # Oyun içi müziği
        
        # PVP oyuncu isimleri
        self.pvp_oyuncu1_isim = "Oyuncu 1"
        self.pvp_oyuncu2_isim = "Oyuncu 2"
        self.pvp_kazanan = None  # PVP kazananı
        
        # Kazanılan başarımlar (oyun bitince göstermek için)
        self.yeni_basarimlar = []
        
        # Arka plan resimlerini yükle - ekran boyutuna göre
        self.menu_arkaplan = arkaplan_yukle(self.menu_arkaplan_yolu, self.ekran_genislik, self.ekran_yukseklik)
        self.oyun_arkaplan = arkaplan_yukle(self.oyun_arkaplan_yolu, self.ekran_genislik, self.ekran_yukseklik)
        
        # Arka plan seçim menüsü için
        self.arkaplan_menu_secim = "MENU"  # MENU veya OYUN
        self.menu_bg_secili_index = -1  # -1 = varsayılan
        self.oyun_bg_secili_index = -1
        
        # Yılan özelleştirme menüsü için
        self.yilan_ozellestirme_secim = "RENK"  # RENK veya YUZ
        
        # Müzik seçici için ayrı indexler
        self.menu_muzik_index = 0  # Ana menü müziği index
        self.oyun_muzik_index = 0  # Oyun içi müziği index
        self.muzik_secici_scroll = 0  # Scroll offset
        self.muzik_secim_modu = "MENU"  # MENU veya OYUN
        
        # Efektler
        self.yilan_izi_efekti = YilanIziEfekti()
        self.yem_yeme_efekti = YemYemeEfekti()
        self.puan_efekti = PuanEfekti()
        
        # Yeni sistemler
        self.basarim_yoneticisi = BasarimYoneticisi()
        self.istatistik_takipci = IstatistikTakipci()
        self.ses_yoneticisi = SesYoneticisi()
        
        # Başarımlar ve istatistikler için kısa erişim
        self.basarimlar = self.basarim_yoneticisi
        self.istatistikler = self.istatistik_takipci
        
        # Özel yem
        self.ozel_yem = None
        self.ozel_yem_aktif = False
        self.dondurma_sayaci = 0  # Dondurucu yem süresi
        
        # Oyun başlangıç zamanı
        self.oyun_baslangic_zamani = 0
        
        # YENİ: Oyun modları
        self.oyun_modu = "Normal"  # Normal, ZamanaKarsi, HayattaKalma
        self.zaman_modu_baslangic = 0  # Zamana karşı mod başlangıç zamanı
        self.hayatta_kalma_baslangic = 0  # Hayatta kalma mod başlangıç zamanı
        self.hayatta_kalma_fps = HAYATTA_KALMA_BASLANGIC_FPS  # Dinamik FPS
        self.hayatta_kalma_son_hiz_artis = 0  # Son hız artışı zamanı
        self.hayatta_kalma_son_bomba_spawn = 0  # Son bomba spawn zamanı
        self.hayatta_kalma_bombalar = []  # Hayatta kalma modundaki bombalar
        
        # YENİ: Power-up'lar
        self.yavaslama_aktif = False  # Rakibi yavaşlatma
        self.yavaslama_baslangic = 0  # Yavaşlatma başlangıç zamanı
        self.yavaslanan_oyuncu = None  # 1 veya 2 (hangi oyuncu yavaşladı)
        
        # YENİ: Başarım takibi - DOSYADAN YÜKLENİYOR (oyunlar arasında birikir)
        self.olum_sayisi = 0  # Hiç ölmeden başarımı için (her oyunda sıfırlanır)
        # bomba_olum_sayisi - dosyadan yüklenecek (tüm oyunlarda birikir)
        self.bomba_olum_sayisi = self.basarim_yoneticisi.basarimlar.get("bomba_imha", {}).get("ilerleme", 0)
        
        # Özel yem sayaçları (başarımlar için) - dosyadan yükleniyor
        self.hiz_yemi_sayisi = self.basarim_yoneticisi.basarimlar.get("hiz_canavarı", {}).get("ilerleme", 0)
        self.kalkan_yemi_sayisi = self.basarim_yoneticisi.basarimlar.get("kalkan_ustasi", {}).get("ilerleme", 0)
        self.yavaslama_yemi_sayisi = self.basarim_yoneticisi.basarimlar.get("yavaslatici", {}).get("ilerleme", 0)
        self.zehirli_yem_sayisi = self.basarim_yoneticisi.basarimlar.get("zehir_tadici", {}).get("ilerleme", 0)
        self.dondurucu_yem_sayisi = self.basarim_yoneticisi.basarimlar.get("buz_krali", {}).get("ilerleme", 0)
        
        # Hareket sayacı (dondurma efekti için)
        self.hareket_sayaci = 0
        
        # Bomba modu için değişkenler - DİNAMİK GRID BOYUTU
        self.bomba_yoneticisi = BombManager(
            self.grid_genislik,  # Dinamik grid genişliği
            self.grid_yukseklik,  # Dinamik grid yüksekliği
            self.hucre_boyutu     # Dinamik hücre boyutu
        )
        self.sahte_yem = None  # Sahte yem
        self.yem_sayaci = 0  # Her 3 yemde bir sahte yem spawn olur
        self.son_bomba_eklenen_skor = 0  # Son bomba hangi skorda eklendi
        
        # Patlama efekti için
        self.patlama_animasyon_sayaci = 0  # Patlama animasyonu için frame sayacı
        self.patlama_pozisyon = None  # Patlama yeri
        self.ekran_titreme_x = 0  # Ekran titremesi X
        self.ekran_titreme_y = 0  # Ekran titremesi Y
        
        # Ana menü müziğini başlat
        self.ses_yoneticisi.muzik_cal(self.menu_muzik)

    def tam_ekran_degistir(self):
        """Tam ekran modunu değiştirir (ESC ile çıkış için)"""
        # Tam ekrandan çıkmak için ESC kullan
        pygame.quit()
        sys.exit()
    
    def _yem_kontrol_ve_ye(self):
        """Yem yeme kontrolü ve işlemleri - her hareket sonrası çağrılır"""
        # Normal yem yeme
        yem_yiyen = None  # Hangi yılan yedi
        
        if self.yilan.kafa_pozisyonu() == self.yem.pozisyon:
            yem_yiyen = self.yilan
        elif (self.pvp_modu or self.bot_modu) and self.yilan2 and self.yilan2.kafa_pozisyonu() == self.yem.pozisyon:
            yem_yiyen = self.yilan2
        
        if yem_yiyen:
            # Yem yeme efekti
            yem_x, yem_y = self.yem.pozisyon
            # Meyve rengini al
            meyve_renkleri = [
                KIRMIZI,      # Elma
                (255, 165, 0), # Portakal
                (148, 63, 231), # Üzüm
                (220, 20, 60),  # Kiraz
                (255, 225, 53)  # Muz
            ]
            meyve_rengi = meyve_renkleri[self.yem.meyve_turu]
            self.yem_yeme_efekti.efekt_ekle(yem_x, yem_y, meyve_rengi)
            
            # Ses efekti
            self.ses_yoneticisi.efekt_cal("yem_ye")
            
            # Puan efekti
            self.puan_efekti.metin_ekle(
                yem_x + HUCRE_BOYUTU // 2,
                yem_y,
                10
            )
            
            yem_yiyen.buyut()
            
            # İstatistik güncelle (sadece PVP ve Bot olmayan modda)
            if not self.pvp_modu and not self.bot_modu:
                self.istatistik_takipci.yem_yenildi()
                
                # Başarılar
                self.basarim_yoneticisi.arttir("yemci", 1)
                self.basarim_yoneticisi.arttir("acikmis", 1)
                self.basarim_yoneticisi.arttir("usta_avcı", 1)
                self.basarim_yoneticisi.ilerleme_kaydet("kucuk_yilan", len(self.yilan.pozisyonlar))
                self.basarim_yoneticisi.ilerleme_kaydet("orta_yilan", len(self.yilan.pozisyonlar))
                self.basarim_yoneticisi.ilerleme_kaydet("dev_yilan", len(self.yilan.pozisyonlar))
            
            # Özel yem spawn şansı (PVP ve Bot'da yok)
            if not self.pvp_modu and not self.bot_modu and random.random() < OZEL_YEM_SPAWN_SANSI and not self.ozel_yem_aktif:
                # Rastgele özel yem türü
                turler = ["altin_elma", "elmas", "zehirli", "dondurucu"]
                secilen_tur = random.choice(turler)
                self.ozel_yem = OzelYem(secilen_tur)
                self.ozel_yem.rastgele_konumla()
                # Yılan ve yemlerden uzak olsun
                yasak_poz = set(self.yilan.pozisyonlar)
                yasak_poz.add(self.yem.pozisyon)
                while self.ozel_yem.pozisyon in yasak_poz:
                    self.ozel_yem.rastgele_konumla()
                self.ozel_yem_aktif = True
            
            # Her 100 skorda 1 bomba ekle (bomba modunda ve PVP değilse)
            if self.bomba_modu and not self.pvp_modu:
                yeni_skor = self.yilan.skor
                # 100'ün katlarını kontrol et
                if yeni_skor // 100 > self.son_bomba_eklenen_skor // 100:
                    # Yeni bomba ekle
                    yasak_poz = set(self.yilan.pozisyonlar)
                    yasak_poz.add(self.yem.pozisyon)
                    yasak_poz.update(self.bomba_yoneticisi.bomba_pozisyonlari())
                    
                    # Rastgele pozisyon bul
                    for _ in range(50):  # Max 50 deneme
                        x = random.randint(0, self.grid_genislik - 1) * self.hucre_boyutu
                        y = random.randint(0, self.grid_yukseklik - 1) * self.hucre_boyutu
                        if (x, y) not in yasak_poz:
                            from bomb import Bomb
                            yeni_bomba = Bomb(x, y)
                            self.bomba_yoneticisi.bombalar.append(yeni_bomba)
                            break
                    
                    self.son_bomba_eklenen_skor = yeni_skor
            
            # Sahte yem varsa sil (gerçek yemi yedi)
            if self.sahte_yem:
                self.sahte_yem = None
            
            # Bomba modunda: Mevcut bombaları rastgele yerlere taşı
            if self.bomba_modu:
                yasak_poz = set(self.yilan.pozisyonlar)
                yasak_poz.add(self.yem.pozisyon)
                # PVP bomba modunda ikinci yılanı da ekle
                if (self.pvp_modu or self.bot_modu) and self.yilan2:
                    yasak_poz.update(self.yilan2.pozisyonlar)
                if self.sahte_yem:
                    yasak_poz.add(self.sahte_yem.pozisyon)
                # PVP bomba modunda 3 blok minimum mesafe
                min_mesafe = 3 if (self.pvp_modu or self.bot_modu) else 0
                self.bomba_yoneticisi.bombalari_yerlestir(yasak_poz, min_mesafe)
            
            # Yeni yem spawn - bomba modu için kontrol
            self.yem_sayaci += 1
            if self.bomba_modu and not self.pvp_modu and self.yem_sayaci >= SAHTE_YEM_ORANI:
                # 2 yem spawn: 1 gerçek, 1 sahte
                self.yem = Yem(self.oyun_genislik, self.oyun_yukseklik, sahte_mi=False, hucre_boyutu=self.hucre_boyutu)
                self.sahte_yem = Yem(self.oyun_genislik, self.oyun_yukseklik, sahte_mi=True, hucre_boyutu=self.hucre_boyutu)
                
                # Bomba ve yılan pozisyonlarından uzak olsun
                yasak_pozisyonlar = set(self.yilan.pozisyonlar)
                if self.bomba_modu:
                    yasak_pozisyonlar.update(self.bomba_yoneticisi.bomba_pozisyonlari())
                
                # İki yem birbirine çok yakın olmasın
                while (self.yem.pozisyon in yasak_pozisyonlar or 
                       abs(self.yem.pozisyon[0] - self.sahte_yem.pozisyon[0]) + 
                       abs(self.yem.pozisyon[1] - self.sahte_yem.pozisyon[1]) < 5 * self.hucre_boyutu):
                    self.yem.rastgele_konumla()
                
                while (self.sahte_yem.pozisyon in yasak_pozisyonlar or 
                       self.sahte_yem.pozisyon == self.yem.pozisyon or
                       abs(self.yem.pozisyon[0] - self.sahte_yem.pozisyon[0]) + 
                       abs(self.yem.pozisyon[1] - self.sahte_yem.pozisyon[1]) < 5 * self.hucre_boyutu):
                    self.sahte_yem.rastgele_konumla()
                
                self.yem_sayaci = 0
            else:
                # Sadece gerçek yem - PVP ve Bot'ta her iki yılanı da kontrol et
                yasak_poz = set(self.yilan.pozisyonlar)
                if (self.pvp_modu or self.bot_modu) and self.yilan2:
                    yasak_poz.update(self.yilan2.pozisyonlar)
                
                self.yem.rastgele_konumla()
                while self.yem.pozisyon in yasak_poz:
                    self.yem.rastgele_konumla()

    def yeni_oyun_basla(self, pvp=False, bot=False):
        """Yeni oyun başlatır"""
        self.pvp_modu = pvp
        self.bot_modu = bot
        
        if self.pvp_modu:
            # PVP modu - 2 yılan
            # Oyuncu 1 (Mavi) - sol tarafta
            self.yilan = Yilan(self.oyun_genislik, self.oyun_yukseklik, 3, self.yilan_yuz, self.yilan_aksesuar, self.hucre_boyutu)  # Mavi renk
            self.yilan.pozisyonlar = [(10 * self.hucre_boyutu, (self.grid_yukseklik // 2) * self.hucre_boyutu)]
            self.yilan.yon = (1, 0)  # Sağa bakıyor
            
            # Oyuncu 2 (Kırmızı) - sağ tarafta
            self.yilan2 = Yilan(self.oyun_genislik, self.oyun_yukseklik, 0, self.yilan_yuz, 0, self.hucre_boyutu)  # Kırmızı renk, aksesuarsız
            self.yilan2.pozisyonlar = [((self.grid_genislik - 10) * self.hucre_boyutu, (self.grid_yukseklik // 2) * self.hucre_boyutu)]
            self.yilan2.yon = (-1, 0)  # Sola bakıyor
            
            # PVP için kazanan
            self.pvp_kazanan = None
        elif self.bot_modu:
            # Bot vs modu - Oyuncu vs AI
            # Oyuncu (sol tarafta, seçilen renk)
            self.yilan = Yilan(self.oyun_genislik, self.oyun_yukseklik, self.yilan_renk, self.yilan_yuz, self.yilan_aksesuar, self.hucre_boyutu)
            self.yilan.pozisyonlar = [(10 * self.hucre_boyutu, (self.grid_yukseklik // 2) * self.hucre_boyutu)]
            self.yilan.yon = (1, 0)  # Sağa bakıyor
            
            # Bot (sağ tarafta, turuncu renk)
            self.yilan2 = AIYilan(self.oyun_genislik, self.oyun_yukseklik, self.bot_zorluk.lower(), self.hucre_boyutu)
            
            # Bot için kazanan
            self.pvp_kazanan = None
        else:
            # Normal mod - tek yılan
            self.yilan = Yilan(self.oyun_genislik, self.oyun_yukseklik, self.yilan_renk, self.yilan_yuz, self.yilan_aksesuar, self.hucre_boyutu)
            self.yilan2 = None
        
        self.yem = Yem(self.oyun_genislik, self.oyun_yukseklik, sahte_mi=False, hucre_boyutu=self.hucre_boyutu)
        
        # Yem pozisyonunu yılanlardan uzak yerleştir
        yasak_poz = set(self.yilan.pozisyonlar)
        if (self.pvp_modu or self.bot_modu) and self.yilan2:
            yasak_poz.update(self.yilan2.pozisyonlar)
        
        while self.yem.pozisyon in yasak_poz:
            self.yem.rastgele_konumla()
        
        self.oyun_bitti = False
        self.oyun_durumu = "PLAYING"
        self.oyun_duraklatildi = False  # Pause durumunu sıfırla
        # Efektleri temizle
        self.yilan_izi_efekti.temizle()
        self.yem_yeme_efekti.temizle()
        self.puan_efekti.temizle()
        
        # Patlama animasyonunu sıfırla
        self.patlama_animasyon_sayaci = 0
        self.patlama_pozisyon = None
        self.ekran_titreme_x = 0
        self.ekran_titreme_y = 0
        
        # Özel yem sistemi
        self.ozel_yem = None
        self.ozel_yem_aktif = False
        self.dondurma_sayaci = 0
        
        # PVP özel yemleri
        self.pvp_ozel_yem_p1 = None  # Oyuncu 1'e özel yem
        self.pvp_ozel_yem_p2 = None  # Oyuncu 2'ye özel yem
        self.pvp_yem_spawn_sayaci = 0  # Özel yem spawn zamanlayıcı
        self.pvp_yem_spawn_sure = random.randint(150, 300)  # 5-10 saniye arası (30 FPS'de)
        
        # Skor bazlı özel yem spawn
        self.p1_son_ozel_yem_skoru = 0  # Oyuncu 1'in son özel yem aldığı skor
        self.p2_son_ozel_yem_skoru = 0  # Oyuncu 2'nin son özel yem aldığı skor
        self.ozel_yem_skor_araligi = 50  # Her 50 skorda özel yem
        
        # Oyuncu yetenekleri
        self.p1_kalkan_aktif = False  # Oyuncu 1'in kalkanı
        self.p2_kalkan_aktif = False  # Oyuncu 2'nin kalkanı
        self.p1_hiz_suresi = 0  # Oyuncu 1'in kalan hız süresi (saniye)
        self.p2_hiz_suresi = 0  # Oyuncu 2'nin kalan hız süresi (saniye)
        self.p1_shift_basmaya_basladi = False  # Shift basılı mı
        self.p2_shift_basmaya_basladi = False
        self.p1_hiz_boost_aktif = False  # Şu anda hızlanıyor mu
        self.p2_hiz_boost_aktif = False
        
        # İstatistik takibi başlat
        self.istatistik_takipci.oyun_basladi()
        self.oyun_baslangic_zamani = time.time()
        
        # YENİ: Oyun modu başlangıç değerleri
        if self.oyun_modu == "ZamanaKarsi":
            self.zaman_modu_baslangic = time.time()
        elif self.oyun_modu == "HayattaKalma":
            self.hayatta_kalma_baslangic = time.time()
            self.hayatta_kalma_fps = HAYATTA_KALMA_BASLANGIC_FPS
            self.hayatta_kalma_son_hiz_artis = time.time()
            self.hayatta_kalma_son_bomba_spawn = time.time()
            self.hayatta_kalma_bombalar = []
        
        # YENİ: Başarım takibi - SADECE ölüm sayısını sıfırla (bomba_olum_sayisi tüm oyunlarda birikir)
        self.olum_sayisi = 0
        
        # Özel yem sayaçları sıfırla (bunlar da oyun başına değil toplam)
        # NOT: Bunlar __init__'te tanımlanıyor, burada sıfırlamıyoruz
        
        # Başarım - İlk oyun
        self.basarim_yoneticisi.ilerleme_kaydet("ilk_adim", 1)
        
        # Bomba modu aktifse bombaları oluştur
        self.sahte_yem = None
        self.yem_sayaci = 0
        self.son_bomba_eklenen_skor = 0  # Skor takibi sıfırla
        if self.bomba_modu:
            # Bombaları tamamen temizle ve yeniden oluştur
            self.bomba_yoneticisi.bombalar.clear()
            # Her zaman ilk 10 bomba ile başla
            yasak_pozisyonlar = set(self.yilan.pozisyonlar)
            yasak_pozisyonlar.add(self.yem.pozisyon)
            # PVP bomba modunda ikinci yılanı da ekle
            if (self.pvp_modu or self.bot_modu) and self.yilan2:
                yasak_pozisyonlar.update(self.yilan2.pozisyonlar)
            # PVP bomba modunda 3 blok minimum mesafe
            min_mesafe = 3 if (self.pvp_modu or self.bot_modu) else 0
            self.bomba_yoneticisi.bombalari_olustur(yasak_pozisyonlar, min_mesafe)
            # Bomba modu müziği
            if self.oyun_muzik and self.oyun_muzik != "Normal":
                # Kullanıcı seçtiği müziği çal
                self.ses_yoneticisi.muzik_cal(self.oyun_muzik)
            else:
                # Varsayılan bomba müziği
                self.ses_yoneticisi.muzik_cal("Bomb Modu")
        else:
            # Normal mod müziği
            if self.oyun_muzik and self.oyun_muzik != "Normal":
                # Kullanıcı seçtiği müziği çal
                self.ses_yoneticisi.muzik_cal(self.oyun_muzik)
            else:
                # Varsayılan normal müzik
                self.ses_yoneticisi.muzik_cal("Normal")
        
        # Oyun başladığında fare imlecini gizle
        pygame.mouse.set_visible(False)

    def tam_ekran_degistir(self):
        """Tam ekran modunu değiştirir (ESC ile çıkış için)"""
        # Tam ekrandan çıkmak için ESC kullan
        pygame.quit()
        sys.exit()
    
    def _yem_kontrol_ve_ye(self):
        """Yem yeme kontrolü ve işlemleri - her hareket sonrası çağrılır"""
        # Normal yem yeme
        yem_yiyen = None  # Hangi yılan yedi
        
        if self.yilan.kafa_pozisyonu() == self.yem.pozisyon:
            yem_yiyen = self.yilan
        elif (self.pvp_modu or self.bot_modu) and self.yilan2 and self.yilan2.kafa_pozisyonu() == self.yem.pozisyon:
            yem_yiyen = self.yilan2
        
        if yem_yiyen:
            # Yem yeme efekti
            yem_x, yem_y = self.yem.pozisyon
            # Meyve rengini al
            meyve_renkleri = [
                KIRMIZI,      # Elma
                (255, 165, 0), # Portakal
                (148, 63, 231), # Üzüm
                (220, 20, 60),  # Kiraz
                (255, 225, 53)  # Muz
            ]
            meyve_rengi = meyve_renkleri[self.yem.meyve_turu]
            self.yem_yeme_efekti.efekt_ekle(yem_x, yem_y, meyve_rengi)
            
            # Ses efekti
            self.ses_yoneticisi.efekt_cal("yem_ye")
            
            # Puan efekti
            self.puan_efekti.metin_ekle(
                yem_x + HUCRE_BOYUTU // 2,
                yem_y,
                10
            )
            
            yem_yiyen.buyut()
            
            # İstatistik güncelle (sadece PVP ve Bot olmayan modda)
            if not self.pvp_modu and not self.bot_modu:
                self.istatistik_takipci.yem_yenildi()
                
                # Başarılar
                self.basarim_yoneticisi.arttir("yemci", 1)
                self.basarim_yoneticisi.arttir("acikmis", 1)
                self.basarim_yoneticisi.arttir("usta_avcı", 1)
                self.basarim_yoneticisi.ilerleme_kaydet("kucuk_yilan", len(self.yilan.pozisyonlar))
                self.basarim_yoneticisi.ilerleme_kaydet("orta_yilan", len(self.yilan.pozisyonlar))
                self.basarim_yoneticisi.ilerleme_kaydet("dev_yilan", len(self.yilan.pozisyonlar))
            
            # Özel yem spawn şansı (PVP ve Bot'da yok)
            if not self.pvp_modu and not self.bot_modu and random.random() < OZEL_YEM_SPAWN_SANSI and not self.ozel_yem_aktif:
                # Rastgele özel yem türü
                turler = ["altin_elma", "elmas", "zehirli", "dondurucu"]
                secilen_tur = random.choice(turler)
                self.ozel_yem = OzelYem(secilen_tur)
                self.ozel_yem.rastgele_konumla()
                # Yılan ve yemlerden uzak olsun
                yasak_poz = set(self.yilan.pozisyonlar)
                yasak_poz.add(self.yem.pozisyon)
                while self.ozel_yem.pozisyon in yasak_poz:
                    self.ozel_yem.rastgele_konumla()
                self.ozel_yem_aktif = True
            
            # Her 100 skorda 1 bomba ekle (bomba modunda ve PVP değilse)
            if self.bomba_modu and not self.pvp_modu:
                yeni_skor = self.yilan.skor
                # 100'ün katlarını kontrol et
                if yeni_skor // 100 > self.son_bomba_eklenen_skor // 100:
                    # Yeni bomba ekle
                    yasak_poz = set(self.yilan.pozisyonlar)
                    yasak_poz.add(self.yem.pozisyon)
                    yasak_poz.update(self.bomba_yoneticisi.bomba_pozisyonlari())
                    
                    # Rastgele pozisyon bul
                    for _ in range(50):  # Max 50 deneme
                        x = random.randint(0, self.grid_genislik - 1) * self.hucre_boyutu
                        y = random.randint(0, self.grid_yukseklik - 1) * self.hucre_boyutu
                        if (x, y) not in yasak_poz:
                            from bomb import Bomb
                            yeni_bomba = Bomb(x, y)
                            self.bomba_yoneticisi.bombalar.append(yeni_bomba)
                            break
                    
                    self.son_bomba_eklenen_skor = yeni_skor
            
            # Sahte yem varsa sil (gerçek yemi yedi)
            if self.sahte_yem:
                self.sahte_yem = None
            
            # Bomba modunda: Mevcut bombaları rastgele yerlere taşı
            if self.bomba_modu:
                yasak_poz = set(self.yilan.pozisyonlar)
                yasak_poz.add(self.yem.pozisyon)
                # PVP bomba modunda ikinci yılanı da ekle
                if (self.pvp_modu or self.bot_modu) and self.yilan2:
                    yasak_poz.update(self.yilan2.pozisyonlar)
                if self.sahte_yem:
                    yasak_poz.add(self.sahte_yem.pozisyon)
                # PVP bomba modunda 3 blok minimum mesafe
                min_mesafe = 3 if (self.pvp_modu or self.bot_modu) else 0
                self.bomba_yoneticisi.bombalari_yerlestir(yasak_poz, min_mesafe)
            
            # Yeni yem spawn - bomba modu için kontrol
            self.yem_sayaci += 1
            if self.bomba_modu and not self.pvp_modu and self.yem_sayaci >= SAHTE_YEM_ORANI:
                # 2 yem spawn: 1 gerçek, 1 sahte
                self.yem = Yem(self.oyun_genislik, self.oyun_yukseklik, sahte_mi=False, hucre_boyutu=self.hucre_boyutu)
                self.sahte_yem = Yem(self.oyun_genislik, self.oyun_yukseklik, sahte_mi=True, hucre_boyutu=self.hucre_boyutu)
                
                # Bomba ve yılan pozisyonlarından uzak olsun
                yasak_pozisyonlar = set(self.yilan.pozisyonlar)
                if self.bomba_modu:
                    yasak_pozisyonlar.update(self.bomba_yoneticisi.bomba_pozisyonlari())
                
                # İki yem birbirine çok yakın olmasın
                while (self.yem.pozisyon in yasak_pozisyonlar or 
                       abs(self.yem.pozisyon[0] - self.sahte_yem.pozisyon[0]) + 
                       abs(self.yem.pozisyon[1] - self.sahte_yem.pozisyon[1]) < 5 * self.hucre_boyutu):
                    self.yem.rastgele_konumla()
                
                while (self.sahte_yem.pozisyon in yasak_pozisyonlar or 
                       self.sahte_yem.pozisyon == self.yem.pozisyon or
                       abs(self.yem.pozisyon[0] - self.sahte_yem.pozisyon[0]) + 
                       abs(self.yem.pozisyon[1] - self.sahte_yem.pozisyon[1]) < 5 * self.hucre_boyutu):
                    self.sahte_yem.rastgele_konumla()
                
                self.yem_sayaci = 0
            else:
                # Sadece gerçek yem - PVP ve Bot'ta her iki yılanı da kontrol et
                yasak_poz = set(self.yilan.pozisyonlar)
                if (self.pvp_modu or self.bot_modu) and self.yilan2:
                    yasak_poz.update(self.yilan2.pozisyonlar)
                
                self.yem.rastgele_konumla()
                while self.yem.pozisyon in yasak_poz:
                    self.yem.rastgele_konumla()

    def calistir(self):
        """Ana oyun döngüsü - Windows optimizasyonu ile"""
        while True:
            self.olay_isle()
            self.guncelle()
            
            # Oyun surface'ine çiz (artık scale yok, direkt native çözünürlük)
            self.ciz()
            
            # Menu değerlerini sıfırla (scale yok artık)
            self.menu.tam_ekran = self.tam_ekran
            self.menu.scale = 1.0
            self.menu.offset_x = 0
            self.menu.offset_y = 0
            
            # Ekranı güncelle
            pygame.display.flip()
            
            # Optimize edilmiş FPS ayarı
            if self.oyun_modu == "HayattaKalma" and self.oyun_durumu == "PLAYING":
                self.saat.tick(self.hayatta_kalma_fps)
            else:
                self.saat.tick(HIZ_FPS[self.hiz_seviyesi])
    
    def olay_isle(self):
        """Olayları işler"""
        for olay in pygame.event.get():
            if olay.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif olay.type == pygame.MOUSEBUTTONDOWN:
                if olay.button == 1:  # Sol tıklama
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Mouse pozisyonu artık doğrudan kullanılabilir
                    # Çünkü menü self.ekran_genislik/yukseklik ile çalışıyor
                    
                    # Ana menü butonları
                    if self.oyun_durumu == "MENU":
                        if self.menu.basla_rect and self.menu.basla_rect.collidepoint(mouse_pos):
                            self.yeni_oyun_basla()
                        elif self.menu.modlar_rect and self.menu.modlar_rect.collidepoint(mouse_pos):
                            self.oyun_durumu = "MODLAR"
                        elif self.menu.ayarlar_rect and self.menu.ayarlar_rect.collidepoint(mouse_pos):
                            self.oyun_durumu = "SETTINGS"
                        elif hasattr(self.menu, 'basarimlar_rect') and self.menu.basarimlar_rect and self.menu.basarimlar_rect.collidepoint(mouse_pos):
                            self.oyun_durumu = "BASARIMLAR"
                        elif hasattr(self.menu, 'istatistikler_rect') and self.menu.istatistikler_rect and self.menu.istatistikler_rect.collidepoint(mouse_pos):
                            self.oyun_durumu = "ISTATISTIKLER"
                        elif hasattr(self.menu, 'krediler_rect') and self.menu.krediler_rect and self.menu.krediler_rect.collidepoint(mouse_pos):
                            self.oyun_durumu = "KREDILER"
                    
                    # Modlar menüsü butonları
                    elif self.oyun_durumu == "MODLAR":
                        if hasattr(self.menu, 'normal_rect') and self.menu.normal_rect and self.menu.normal_rect.collidepoint(mouse_pos):
                            self.bomba_modu = False
                            self.oyun_modu = "Normal"
                            self.yeni_oyun_basla(pvp=False)
                        elif hasattr(self.menu, 'bomba_rect') and self.menu.bomba_rect and self.menu.bomba_rect.collidepoint(mouse_pos):
                            self.bomba_modu = True
                            self.oyun_modu = "Normal"
                            self.yeni_oyun_basla(pvp=False)
                        elif hasattr(self.menu, 'pvp_rect') and self.menu.pvp_rect and self.menu.pvp_rect.collidepoint(mouse_pos):
                            self.oyun_durumu = "PVP_ISIM_GIRIS"
                        elif hasattr(self.menu, 'bot_rect') and self.menu.bot_rect and self.menu.bot_rect.collidepoint(mouse_pos):
                            self.oyun_durumu = "BOT_ZORLUK_SECIM"
                        elif hasattr(self.menu, 'zaman_rect') and self.menu.zaman_rect and self.menu.zaman_rect.collidepoint(mouse_pos):
                            self.oyun_modu = "ZamanaKarsi"
                            self.yeni_oyun_basla(pvp=False)
                        elif hasattr(self.menu, 'hayatta_kalma_rect') and self.menu.hayatta_kalma_rect and self.menu.hayatta_kalma_rect.collidepoint(mouse_pos):
                            self.oyun_modu = "HayattaKalma"
                            self.yeni_oyun_basla(pvp=False)
                    
                    # Ayarlar menüsü butonları
                    elif self.oyun_durumu == "SETTINGS":
                        if hasattr(self.menu, 'hiz_rect') and self.menu.hiz_rect and self.menu.hiz_rect.collidepoint(mouse_pos):
                            self.oyun_durumu = "HIZ_AYAR"
                        elif hasattr(self.menu, 'grafik_rect') and self.menu.grafik_rect and self.menu.grafik_rect.collidepoint(mouse_pos):
                            self.oyun_durumu = "GRAFIK_AYAR"
                        elif hasattr(self.menu, 'arkaplan_rect') and self.menu.arkaplan_rect and self.menu.arkaplan_rect.collidepoint(mouse_pos):
                            self.oyun_durumu = "ARKAPLAN_AYAR"
                        elif hasattr(self.menu, 'yilan_rect') and self.menu.yilan_rect and self.menu.yilan_rect.collidepoint(mouse_pos):
                            self.oyun_durumu = "YILAN_AYAR"
                        elif hasattr(self.menu, 'ses_rect') and self.menu.ses_rect and self.menu.ses_rect.collidepoint(mouse_pos):
                            # Ses efektlerini aç/kapat
                            self.ses_yoneticisi.ses_ac_kapat()
                        elif hasattr(self.menu, 'muzik_rect') and self.menu.muzik_rect and self.menu.muzik_rect.collidepoint(mouse_pos):
                            # Müzik aç/kapat
                            self.ses_yoneticisi.muzik_ac_kapat()
                            # Müzik açıldıysa menü müziğini çal
                            if self.ses_yoneticisi.muzik_acik:
                                self.ses_yoneticisi.muzik_cal(self.menu_muzik)
                        elif hasattr(self.menu, 'muzik_secici_rect') and self.menu.muzik_secici_rect and self.menu.muzik_secici_rect.collidepoint(mouse_pos):
                            self.oyun_durumu = "MUZIK_SECICI"
                    
                    # Grafik ayarları butonları
                    elif self.oyun_durumu == "GRAFIK_AYAR":
                        # Çözünürlük seçimi
                        if hasattr(self.menu, 'cozunurluk_rects') and self.menu.cozunurluk_rects:
                            for isim, rect in self.menu.cozunurluk_rects:
                                if rect.collidepoint(mouse_pos):
                                    # Eğer zaten seçili çözünürlükse değiştirme
                                    if isim == self.cozunurluk_ayari:
                                        break
                                    
                                    self.cozunurluk_ayari = isim
                                    self.ayar_yoneticisi.ayarlari_kaydet({"cozunurluk": isim})
                                    
                                    try:
                                        # Çözünürlüğü uygula - CROSS-PLATFORM (TAM EKRAN MODUNDA KAL)
                                        if isim == "Tam Ekran":
                                            # Native tam ekran moduna geç - Platform bazlı
                                            if self.platform == 'Darwin':  # macOS
                                                # macOS için önce native boyutu al
                                                info = pygame.display.Info()
                                                native_w = info.current_w
                                                native_h = info.current_h
                                                if hasattr(pygame, 'SCALED') and native_w and native_h:
                                                    fullscreen_flag = pygame.FULLSCREEN | pygame.SCALED
                                                    self.ekran = pygame.display.set_mode((native_w, native_h), fullscreen_flag)
                                                else:
                                                    self.ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                                            elif self.platform == 'Windows':  # Windows
                                                self.ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                                            else:  # Linux ve diğerleri
                                                self.ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                                            
                                            self.tam_ekran = True
                                        else:
                                            # Seçilen çözünürlükte TAM EKRAN modunda kal
                                            for coz_isim, genislik, yukseklik in COZUNURLUK_SECENEKLERI:
                                                if coz_isim == isim:
                                                    # Platform bazlı tam ekran flag'i kullan
                                                    if self.platform == 'Darwin':  # macOS
                                                        if hasattr(pygame, 'SCALED'):
                                                            fullscreen_flag = pygame.FULLSCREEN | pygame.SCALED
                                                        else:
                                                            fullscreen_flag = pygame.FULLSCREEN
                                                        self.ekran = pygame.display.set_mode((genislik, yukseklik), fullscreen_flag)
                                                    elif self.platform == 'Windows':  # Windows
                                                        self.ekran = pygame.display.set_mode((genislik, yukseklik), pygame.FULLSCREEN)
                                                    else:  # Linux
                                                        self.ekran = pygame.display.set_mode((genislik, yukseklik), pygame.FULLSCREEN)
                                                    break
                                            self.tam_ekran = True  # TAM EKRAN MODUNDA KAL!
                                        
                                        # Ekran boyutlarını güncelle
                                        self.ekran_genislik = self.ekran.get_width()
                                        self.ekran_yukseklik = self.ekran.get_height()
                                        
                                        # Hücre boyutunu DİNAMİK olarak yeniden hesapla - KARE İÇİN
                                        min_boyut = min(self.ekran_genislik, self.ekran_yukseklik)
                                        min_grid_sayisi = 25
                                        ideal_hucre_boyutu = min_boyut // min_grid_sayisi
                                        ideal_hucre_boyutu = max(20, min(50, ideal_hucre_boyutu))
                                        self.hucre_boyutu = ideal_hucre_boyutu
                                        
                                        # Grid yeniden hesapla - KARE HÜCRELER
                                        self.grid_genislik = self.ekran_genislik // self.hucre_boyutu
                                        self.grid_yukseklik = self.ekran_yukseklik // self.hucre_boyutu
                                        
                                        # Oyun alanını grid'e göre yeniden hesapla
                                        self.oyun_genislik = self.grid_genislik * self.hucre_boyutu
                                        self.oyun_yukseklik = self.grid_yukseklik * self.hucre_boyutu
                                        
                                        # Merkezi hizalama
                                        self.oyun_offset_x = (self.ekran_genislik - self.oyun_genislik) // 2
                                        self.oyun_offset_y = (self.ekran_yukseklik - self.oyun_yukseklik) // 2
                                        
                                        # Menu değişkenlerini güncelle
                                        self.menu.ekran_genislik = self.ekran_genislik
                                        self.menu.ekran_yukseklik = self.ekran_yukseklik
                                        self.menu.oyun_offset_x = self.oyun_offset_x
                                        self.menu.oyun_offset_y = self.oyun_offset_y
                                        
                                        # Arka planları yeniden yükle
                                        self.menu_arkaplan = arkaplan_yukle(self.menu_arkaplan_yolu, self.ekran_genislik, self.ekran_yukseklik)
                                        self.oyun_arkaplan = arkaplan_yukle(self.oyun_arkaplan_yolu, self.ekran_genislik, self.ekran_yukseklik)
                                        
                                        # Eğer oyun devam ediyorsa, yılan ve yem pozisyonlarını yeni grid'e uyarla
                                        if self.yilan and hasattr(self, 'yem'):
                                            # Yılanı grid sınırları içinde tut
                                            yeni_pozisyonlar = []
                                            for poz in self.yilan.pozisyonlar:
                                                x = min(poz[0], self.grid_genislik - 1)
                                                y = min(poz[1], self.grid_yukseklik - 1)
                                                yeni_pozisyonlar.append([x, y])
                                            self.yilan.pozisyonlar = yeni_pozisyonlar
                                            
                                            # Yemi yeni grid'de rastgele konumlandır
                                            if self.yem:
                                                self.yem.pozisyon = [
                                                    random.randint(0, self.grid_genislik - 1),
                                                    random.randint(0, self.grid_yukseklik - 1)
                                                ]
                                        
                                        print(f"Çözünürlük değiştirildi ({self.platform}): {isim} -> {self.ekran_genislik}x{self.ekran_yukseklik}, Grid: {self.grid_genislik}x{self.grid_yukseklik}, Hücre: {self.hucre_boyutu}px")
                                    except Exception as e:
                                        print(f"Çözünürlük değiştirme hatası ({self.platform}): {e}")
                                        import traceback
                                        traceback.print_exc()
                                        # Hata durumunda native tam ekran moduna geri dön
                                        if self.platform == 'Darwin':
                                            info = pygame.display.Info()
                                            native_w = info.current_w
                                            native_h = info.current_h
                                            if hasattr(pygame, 'SCALED') and native_w and native_h:
                                                fullscreen_flag = pygame.FULLSCREEN | pygame.SCALED
                                                self.ekran = pygame.display.set_mode((native_w, native_h), fullscreen_flag)
                                            else:
                                                self.ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                                        elif self.platform == 'Windows':
                                            self.ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                                        else:
                                            self.ekran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                                        
                                        self.ekran_genislik = self.ekran.get_width()
                                        self.ekran_yukseklik = self.ekran.get_height()
                                        self.tam_ekran = True
                                        
                                        # Grid'i yeniden hesapla - KARE İÇİN
                                        min_boyut = min(self.ekran_genislik, self.ekran_yukseklik)
                                        min_grid_sayisi = 25
                                        ideal_hucre_boyutu = min_boyut // min_grid_sayisi
                                        ideal_hucre_boyutu = max(20, min(50, ideal_hucre_boyutu))
                                        self.hucre_boyutu = ideal_hucre_boyutu
                                        self.grid_genislik = self.ekran_genislik // self.hucre_boyutu
                                        self.grid_yukseklik = self.ekran_yukseklik // self.hucre_boyutu
                                        self.oyun_genislik = self.grid_genislik * self.hucre_boyutu
                                        self.oyun_yukseklik = self.grid_yukseklik * self.hucre_boyutu
                                        self.oyun_offset_x = (self.ekran_genislik - self.oyun_genislik) // 2
                                        self.oyun_offset_y = (self.ekran_yukseklik - self.oyun_yukseklik) // 2
                                    break
                    
                    # Arka plan ayarları butonları
                    elif self.oyun_durumu == "ARKAPLAN_AYAR":
                        # Sekme değiştirme
                        if hasattr(self.menu, 'menu_bg_tab_rect') and self.menu.menu_bg_tab_rect and self.menu.menu_bg_tab_rect.collidepoint(mouse_pos):
                            self.arkaplan_menu_secim = "MENU"
                        elif hasattr(self.menu, 'oyun_bg_tab_rect') and self.menu.oyun_bg_tab_rect and self.menu.oyun_bg_tab_rect.collidepoint(mouse_pos):
                            self.arkaplan_menu_secim = "OYUN"
                        # Arka plan seçimi - MOUSE İLE ANLIK UYGULAMA
                        elif hasattr(self.menu, 'arkaplan_rects') and self.menu.arkaplan_rects:
                            for index, rect in self.menu.arkaplan_rects:
                                if rect.collidepoint(mouse_pos):
                                    dosyalar = self.menu.arkaplan_dosyalari_getir()
                                    if self.arkaplan_menu_secim == "MENU":
                                        self.menu_bg_secili_index = index
                                        if index == -1:
                                            self.menu_arkaplan_yolu = None
                                        elif 0 <= index < len(dosyalar):
                                            self.menu_arkaplan_yolu = os.path.join(ARKAPLAN_KLASORU, dosyalar[index])
                                        self.menu_arkaplan = arkaplan_yukle(self.menu_arkaplan_yolu, self.ekran_genislik, self.ekran_yukseklik)
                                        self.ayar_yoneticisi.ayarlari_kaydet({"menu_arkaplan": self.menu_arkaplan_yolu})
                                    else:
                                        self.oyun_bg_secili_index = index
                                        if index == -1:
                                            self.oyun_arkaplan_yolu = None
                                        elif 0 <= index < len(dosyalar):
                                            self.oyun_arkaplan_yolu = os.path.join(ARKAPLAN_KLASORU, dosyalar[index])
                                        self.oyun_arkaplan = arkaplan_yukle(self.oyun_arkaplan_yolu, self.ekran_genislik, self.ekran_yukseklik)
                                        self.ayar_yoneticisi.ayarlari_kaydet({"oyun_arkaplan": self.oyun_arkaplan_yolu})
                                    break
                    
                    # Yılan özelleştirme butonları
                    elif self.oyun_durumu == "YILAN_AYAR":
                        # Sekme değiştirme
                        if hasattr(self.menu, 'renk_tab_rect') and self.menu.renk_tab_rect and self.menu.renk_tab_rect.collidepoint(mouse_pos):
                            self.yilan_ozellestirme_secim = "RENK"
                        elif hasattr(self.menu, 'yuz_tab_rect') and self.menu.yuz_tab_rect and self.menu.yuz_tab_rect.collidepoint(mouse_pos):
                            self.yilan_ozellestirme_secim = "YUZ"
                        elif hasattr(self.menu, 'aksesuar_tab_rect') and self.menu.aksesuar_tab_rect and self.menu.aksesuar_tab_rect.collidepoint(mouse_pos):
                            self.yilan_ozellestirme_secim = "AKSESUAR"
                        # Seçim yapma
                        elif self.yilan_ozellestirme_secim == "RENK" and hasattr(self.menu, 'renk_rects') and self.menu.renk_rects:
                            for index, rect in self.menu.renk_rects:
                                if rect.collidepoint(mouse_pos):
                                    self.yilan_renk = index
                                    self.ayar_yoneticisi.ayarlari_kaydet({"yilan_renk": index})
                                    # Mevcut yılanın rengini güncelle
                                    if self.yilan and hasattr(self.yilan, 'renk_guncelle'):
                                        self.yilan.renk_guncelle(index)
                                    break
                        elif self.yilan_ozellestirme_secim == "YUZ" and hasattr(self.menu, 'yuz_rects') and self.menu.yuz_rects:
                            for index, rect in self.menu.yuz_rects:
                                if rect.collidepoint(mouse_pos):
                                    self.yilan_yuz = index
                                    self.ayar_yoneticisi.ayarlari_kaydet({"yilan_yuz": index})
                                    # Mevcut yılanın yüzünü güncelle
                                    if self.yilan and hasattr(self.yilan, 'yuz_guncelle'):
                                        self.yilan.yuz_guncelle(index)
                                    break
                        elif self.yilan_ozellestirme_secim == "AKSESUAR" and hasattr(self.menu, 'aksesuar_rects') and self.menu.aksesuar_rects:
                            for index, rect in self.menu.aksesuar_rects:
                                if rect.collidepoint(mouse_pos):
                                    self.yilan_aksesuar = index
                                    self.ayar_yoneticisi.ayarlari_kaydet({"yilan_aksesuar": index})
                                    # Mevcut yılanın aksesuarını güncelle
                                    if self.yilan and hasattr(self.yilan, 'aksesuar_guncelle'):
                                        self.yilan.aksesuar_guncelle(index)
                                    break
                    
                    # Hız ayarları butonları
                    elif self.oyun_durumu == "HIZ_AYAR":
                        if hasattr(self.menu, 'hiz_secenekleri_rects') and self.menu.hiz_secenekleri_rects:
                            for index, rect in self.menu.hiz_secenekleri_rects:
                                if rect.collidepoint(mouse_pos):
                                    self.hiz_seviyesi = index
                                    self.ayar_yoneticisi.ayarlari_kaydet({"hiz_seviyesi": index})
                                    break
                    
                    # Tema ayarları butonları
                    elif self.oyun_durumu == "TEMA_AYAR":
                        if hasattr(self.menu, 'tema_kartlari') and self.menu.tema_kartlari:
                            for tema_adi, rect in self.menu.tema_kartlari:
                                if rect.collidepoint(mouse_pos):
                                    self.aktif_tema = tema_adi
                                    self.ayar_yoneticisi.ayarlari_kaydet({"aktif_tema": tema_adi})
                                    break
                    
                    # Müzik seçici butonları
                    elif self.oyun_durumu == "MUZIK_SECICI":
                        # Sekme değiştirme
                        if hasattr(self.menu, 'menu_muzik_sekme_rect') and self.menu.menu_muzik_sekme_rect and self.menu.menu_muzik_sekme_rect.collidepoint(mouse_pos):
                            self.muzik_secim_modu = "MENU"
                        elif hasattr(self.menu, 'oyun_muzik_sekme_rect') and self.menu.oyun_muzik_sekme_rect and self.menu.oyun_muzik_sekme_rect.collidepoint(mouse_pos):
                            self.muzik_secim_modu = "OYUN"
                        # Müzik seçimi
                        elif hasattr(self.menu, 'muzik_rects') and self.menu.muzik_rects:
                            for index, rect in self.menu.muzik_rects:
                                if rect.collidepoint(mouse_pos):
                                    if self.muzik_secim_modu == "MENU":
                                        self.menu_muzik_index = index
                                        # Müzik değiştirme işlemi burada yapılabilir
                                    else:
                                        self.oyun_muzik_index = index
                                        # Müzik değiştirme işlemi burada yapılabilir
                                    break
                    
                    # Bot zorluk seçimi butonları
                    elif self.oyun_durumu == "BOT_ZORLUK_SECIM":
                        if hasattr(self.menu, 'zorluk_kartlari') and self.menu.zorluk_kartlari:
                            for zorluk, rect in self.menu.zorluk_kartlari:
                                if rect.collidepoint(mouse_pos):
                                    self.bot_zorluk = zorluk
                                    self.oyun_modu = "Normal"
                                    self.yeni_oyun_basla(bot=True)
                                    break
                    
                    # GAME_OVER durumunda yeni oyun başlatma (mouse click)
                    elif self.oyun_durumu == "GAME_OVER":
                        # Oyun bitti ekranında herhangi bir yere tıklayınca yeni oyun başlat (aynı modda devam et)
                        if self.pvp_modu:
                            self.yeni_oyun_basla(pvp=True)
                        elif self.bot_modu:
                            self.yeni_oyun_basla(bot=True)
                        else:
                            self.yeni_oyun_basla()
            
            elif olay.type == pygame.KEYDOWN:
                # macOS CMD+Q desteği (çıkış)
                import platform
                if platform.system() == 'Darwin':  # macOS
                    if olay.key == pygame.K_q and (olay.mod & pygame.KMOD_META):
                        pygame.quit()
                        sys.exit()
                
                if olay.key == pygame.K_ESCAPE:
                    # ESC - bir önceki menüye dön
                    if self.oyun_durumu == "PLAYING":
                        self.oyun_durumu = "MENU"
                    elif self.oyun_durumu == "GAME_OVER":
                        self.oyun_durumu = "MENU"
                    elif self.oyun_durumu in ["MODLAR", "SETTINGS", "BASARIMLAR", "ISTATISTIKLER", "KREDILER"]:
                        self.oyun_durumu = "MENU"
                    elif self.oyun_durumu in ["HIZ_AYAR", "ARKAPLAN_AYAR", "YILAN_AYAR", "TEMA_AYAR", "MUZIK_SECICI", "GRAFIK_AYAR"]:
                        self.oyun_durumu = "SETTINGS"
                    elif self.oyun_durumu in ["PVP_ISIM_GIRIS", "BOT_ZORLUK_SECIM"]:
                        self.oyun_durumu = "MODLAR"
                        # PVP isim girişini sıfırla
                        if self.oyun_durumu == "MODLAR":
                            self.pvp_isim_input_aktif = 1
                            self.pvp_oyuncu1_isim_temp = ""
                            self.pvp_oyuncu2_isim_temp = ""
                    elif self.oyun_durumu == "MENU":
                        pygame.quit()
                        sys.exit()
                    else:
                        pygame.quit()
                        sys.exit()
                elif olay.key == pygame.K_p and self.oyun_durumu == "PLAYING":
                    self.oyun_duraklatildi = not self.oyun_duraklatildi
                elif not self.oyun_duraklatildi and self.oyun_durumu == "PLAYING":
                    # İlk oyuncu yön tuşları (Arrow keys)
                    if olay.key == pygame.K_LEFT and self.yilan.yon != (1, 0):
                        self.yilan.yon_degistir((-1, 0))
                    elif olay.key == pygame.K_RIGHT and self.yilan.yon != (-1, 0):
                        self.yilan.yon_degistir((1, 0))
                    elif olay.key == pygame.K_UP and self.yilan.yon != (0, 1):
                        self.yilan.yon_degistir((0, -1))
                    elif olay.key == pygame.K_DOWN and self.yilan.yon != (0, -1):
                        self.yilan.yon_degistir((0, 1))
                    
                    # İkinci oyuncu yön tuşları (WASD) - PVP modunda
                    if self.pvp_modu and self.yilan2:
                        if olay.key == pygame.K_a and self.yilan2.yon != (1, 0):  # A - sol
                            self.yilan2.yon_degistir((-1, 0))
                        elif olay.key == pygame.K_d and self.yilan2.yon != (-1, 0):  # D - sağ
                            self.yilan2.yon_degistir((1, 0))
                        elif olay.key == pygame.K_w and self.yilan2.yon != (0, 1):  # W - yukarı
                            self.yilan2.yon_degistir((0, -1))
                        elif olay.key == pygame.K_s and self.yilan2.yon != (0, -1):  # S - aşağı
                            self.yilan2.yon_degistir((0, 1))
                # Ana menü navigasyonu için tuş kontrolleri
                elif self.oyun_durumu == "MENU":
                    if olay.key == pygame.K_RETURN or olay.key == pygame.K_SPACE:
                        self.yeni_oyun_basla()
                    elif olay.key == pygame.K_m:
                        self.oyun_durumu = "MODLAR"
                    elif olay.key == pygame.K_s:
                        self.oyun_durumu = "SETTINGS"
                # PVP isim girişi için tuş kontrolleri
                elif self.oyun_durumu == "PVP_ISIM_GIRIS":
                    if olay.key == pygame.K_RETURN:
                        # Enter - isim girişini tamamla ve oyunu başlat
                        if self.pvp_isim_input_aktif == 1:
                            self.pvp_oyuncu1_isim = self.pvp_oyuncu1_isim_temp if self.pvp_oyuncu1_isim_temp else "Oyuncu 1"
                            self.pvp_isim_input_aktif = 2  # İkinci oyuncuya geç
                        elif self.pvp_isim_input_aktif == 2:
                            self.pvp_oyuncu2_isim = self.pvp_oyuncu2_isim_temp if self.pvp_oyuncu2_isim_temp else "Oyuncu 2"
                            # PVP oyununu başlat
                            self.oyun_modu = "Normal"
                            self.yeni_oyun_basla(pvp=True)
                    elif olay.key == pygame.K_BACKSPACE:
                        # Backspace - son karakteri sil
                        if self.pvp_isim_input_aktif == 1:
                            self.pvp_oyuncu1_isim_temp = self.pvp_oyuncu1_isim_temp[:-1]
                        elif self.pvp_isim_input_aktif == 2:
                            self.pvp_oyuncu2_isim_temp = self.pvp_oyuncu2_isim_temp[:-1]
                    else:
                        # Normal karakter girişi
                        if olay.unicode and len(olay.unicode) == 1:  # Sadece tek karakter
                            if self.pvp_isim_input_aktif == 1 and len(self.pvp_oyuncu1_isim_temp) < 15:  # Max 15 karakter
                                self.pvp_oyuncu1_isim_temp += olay.unicode
                            elif self.pvp_isim_input_aktif == 2 and len(self.pvp_oyuncu2_isim_temp) < 15:  # Max 15 karakter
                                self.pvp_oyuncu2_isim_temp += olay.unicode
                # GAME_OVER durumunda yeni oyun başlatma
                elif self.oyun_durumu == "GAME_OVER":
                    if olay.key == pygame.K_SPACE:
                        # Space - yeni oyun başlat (aynı modda devam et)
                        if self.pvp_modu:
                            self.yeni_oyun_basla(pvp=True)
                        elif self.bot_modu:
                            self.yeni_oyun_basla(bot=True)
                        else:
                            self.yeni_oyun_basla()
            elif olay.type == pygame.MOUSEWHEEL:
                # Mouse wheel scroll - ayarlar menüsü için
                if self.oyun_durumu == "SETTINGS":
                    # Scroll hızını ayarla (y pozitif yukarı, negatif aşağı)
                    scroll_hizi = 30
                    self.menu.ayarlar_scroll_offset += olay.y * scroll_hizi
                    # Scroll limitlerini ayarla
                    max_scroll = 200  # Maksimum aşağı scroll
                    self.menu.ayarlar_scroll_offset = max(-max_scroll, min(0, self.menu.ayarlar_scroll_offset))
                elif self.oyun_durumu == "BASARIMLAR":
                    scroll_hizi = 30
                    self.menu.basarim_scroll_offset += olay.y * scroll_hizi
                    max_scroll = 400
                    self.menu.basarim_scroll_offset = max(-max_scroll, min(0, self.menu.basarim_scroll_offset))
                elif self.oyun_durumu == "BOT_ZORLUK_SECIM":
                    scroll_hizi = 50
                    self.menu.bot_zorluk_scroll_offset += olay.y * scroll_hizi
                    max_scroll = 200
                    self.menu.bot_zorluk_scroll_offset = max(-max_scroll, min(0, self.menu.bot_zorluk_scroll_offset))
                elif self.oyun_durumu == "MENU":
                    # Ana menü için scroll
                    scroll_hizi = 30
                    self.menu.ana_menu_scroll_offset += olay.y * scroll_hizi
                    # Ana menü için daha küçük scroll limiti
                    max_scroll = 100
                    self.menu.ana_menu_scroll_offset = max(-max_scroll, min(0, self.menu.ana_menu_scroll_offset))

    def guncelle(self):
        """Oyun mantığını günceller"""
        if self.oyun_durumu == "PLAYING":
            # Hayatta Kalma modu için hız artışı
            if self.oyun_modu == "HayattaKalma":
                gecen_sure = time.time() - self.hayatta_kalma_baslangic
                yeni_hiz_seviyesi = min(10, int(gecen_sure // 10) + 1)  # Her 10 saniyede hız artışı
                yeni_fps = HAYATTA_KALMA_BASLANGIC_FPS + (yeni_hiz_seviyesi - 1) * 2  # Her seviye için +2 FPS
                self.hayatta_kalma_fps = min(120, yeni_fps)  # Maksimum 120 FPS
                
                # Bomba spawn - her 5 saniyede bir
                if time.time() - self.hayatta_kalma_son_bomba_spawn > 5:
                    self.hayatta_kalma_son_bomba_spawn = time.time()
                    # Rastgele bomba ekle
                    bomba_x = random.randint(0, self.grid_genislik - 1) * self.hucre_boyutu
                    bomba_y = random.randint(0, self.grid_yukseklik - 1) * self.hucre_boyutu
                    self.hayatta_kalma_bombalar.append((bomba_x, bomba_y))
                    # Maksimum 5 bomba
                    if len(self.hayatta_kalma_bombalar) > 5:
                        self.hayatta_kalma_bombalar.pop(0)
            
            # Oyun duraklatıldıysa güncelleme yapma
            if self.oyun_duraklatildi:
                return
            
            # Yılan hareket ettir
            self.yilan.hareket_et()
            
            # İkinci yılan hareket ettir (PVP ve Bot modları için)
            if (self.pvp_modu or self.bot_modu) and self.yilan2:
                if self.bot_modu:
                    # Bot için AI karar verme
                    self.yilan2.ai_karar_ver(
                        self.yem.pozisyon, 
                        self.bomba_yoneticisi.bomba_pozisyonlari() if self.bomba_modu else None,
                        self.yilan.pozisyonlar
                    )
                # İkinci yılanı hareket ettir
                self.yilan2.hareket_et()
            
            # Yem kontrolü ve yeme işlemi - düzgün fonksiyon kullan
            self._yem_kontrol_ve_ye()
            
            # Yılan kendine çarptı mı kontrol et (duvara çarpma kontrolü kaldırıldı)
            if self.yilan.carpma_kontrolu():
                self.oyun_durumu = "GAME_OVER"
                self.oyun_bitti = True
                return
            
            # Bomba modu için bomba çarpma kontrolü
            if self.bomba_modu:
                kafa_x, kafa_y = self.yilan.kafa_pozisyonu()
                bomba_pozisyonlari = self.bomba_yoneticisi.bomba_pozisyonlari()
                if (kafa_x, kafa_y) in bomba_pozisyonlari:
                    self.oyun_durumu = "GAME_OVER"
                    self.oyun_bitti = True
                    return
            
            # Hayatta Kalma modu için bomba çarpma kontrolü
            if self.oyun_modu == "HayattaKalma":
                kafa_x, kafa_y = self.yilan.kafa_pozisyonu()
                for bomba_x, bomba_y in self.hayatta_kalma_bombalar:
                    if kafa_x == bomba_x and kafa_y == bomba_y:
                        self.oyun_durumu = "GAME_OVER"
                        self.oyun_bitti = True
                        return
            
            # İkinci yılan çarpma kontrolleri (PVP ve Bot modları için)
            if (self.pvp_modu or self.bot_modu) and self.yilan2:
                # İkinci yılan kendine çarptı mı? (duvara çarpma kontrolü kaldırıldı)
                if self.yilan2.carpma_kontrolu():
                    if self.pvp_modu:
                        self.pvp_kazanan = self.pvp_oyuncu1_isim
                    else:  # bot_modu
                        self.pvp_kazanan = "Sen"
                    self.oyun_durumu = "GAME_OVER"
                    self.oyun_bitti = True
                    return
                
                # Yılanlar birbirine çarptı mı?
                yilan1_kafa = self.yilan.kafa_pozisyonu()
                yilan2_kafa = self.yilan2.kafa_pozisyonu()
                
                # İkinci yılanın kafası birinci yılanın vücuduna çarptı mı?
                if yilan2_kafa in self.yilan.pozisyonlar:
                    if self.pvp_modu:
                        self.pvp_kazanan = "pvp_oyuncu1_kazandi"
                    else:  # bot_modu
                        self.pvp_kazanan = "oyuncu_kazandi"
                    self.oyun_durumu = "GAME_OVER"
                    self.oyun_bitti = True
                    return
                
                # Birinci yılanın kafası ikinci yılanın vücuduna çarptı mı?
                if yilan1_kafa in self.yilan2.pozisyonlar:
                    if self.pvp_modu:
                        self.pvp_kazanan = self.pvp_oyuncu2_isim
                    else:  # bot_modu
                        self.pvp_kazanan = f"Bot ({self.bot_zorluk})"
                    self.oyun_durumu = "GAME_OVER"
                    self.oyun_bitti = True
                    return
                
                # İkinci yılan bomba çarptı mı?
                if self.bomba_modu:
                    kafa_x, kafa_y = self.yilan2.kafa_pozisyonu()
                    bomba_pozisyonlari = self.bomba_yoneticisi.bomba_pozisyonlari()
                    if (kafa_x, kafa_y) in bomba_pozisyonlari:
                        if self.pvp_modu:
                            self.pvp_kazanan = self.pvp_oyuncu1_isim
                        else:  # bot_modu
                            self.pvp_kazanan = "Sen"
                        self.oyun_durumu = "GAME_OVER"
                        self.oyun_bitti = True
                        return

    def ciz(self):
        """Ekrana çizer"""
        if self.oyun_durumu == "MENU":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # Menü arka planı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            self.menu.ana_menu_ciz(self.en_yuksek_skor)
        
        elif self.oyun_durumu == "MODLAR":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # Modlar menüsü arka planı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            self.menu.modlar_menu_ciz(self.bomba_modu)
        
        elif self.oyun_durumu == "SETTINGS":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # Ayarlar arka planı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            self.menu.ayarlar_menu_ciz(
                self.hiz_seviyesi, 
                self.menu_arkaplan_yolu, 
                self.oyun_arkaplan_yolu,
                self.ses_yoneticisi.ses_acik,
                self.ses_yoneticisi.muzik_acik
            )
        
        elif self.oyun_durumu == "HIZ_AYAR":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # Hız ayarları arka planı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            self.menu.hiz_ayarlari_menu_ciz(self.hiz_seviyesi)
        
        elif self.oyun_durumu == "ARKAPLAN_AYAR":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # Arka plan ayarları arka planı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            self.menu.arkaplan_ayarlari_menu_ciz(
                self.menu_arkaplan_yolu, 
                self.oyun_arkaplan_yolu,
                self.menu_bg_secili_index,
                self.oyun_bg_secili_index,
                self.arkaplan_menu_secim
            )
        
        elif self.oyun_durumu == "GRAFIK_AYAR":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # Grafik ayarları arka planı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            self.menu.grafik_ayarlari_menu_ciz(self.tam_ekran, self.cozunurluk_ayari)
        
        elif self.oyun_durumu == "YILAN_AYAR":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # Yılan özelleştirme arka planı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            self.menu.yilan_ozellestirme_menu_ciz(
                self.yilan_renk,
                self.yilan_yuz,
                self.yilan_aksesuar,
                self.yilan_ozellestirme_secim
            )
        
        elif self.oyun_durumu == "TEMA_AYAR":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # Tema seçim arka planı - seçili temayı göster
            tema_renkleri = TEMALAR[self.aktif_tema]
            self.ekran.fill(tema_renkleri["arkaplan"])
            # İzgara efekti - dinamik boyut
            izgara_ciz(self.ekran, tema_renkleri["izgara"], 0, 0, self.hucre_boyutu, self.ekran_genislik, self.ekran_yukseklik)
            self.menu.tema_menu_ciz(self.aktif_tema)
        
        elif self.oyun_durumu == "MUZIK_SECICI":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # Müzik seçici arka planı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            # Aktif indexi belirle
            aktif_index = self.menu_muzik_index if self.muzik_secim_modu == "MENU" else self.oyun_muzik_index
            self.menu.muzik_secici_menu_ciz(self.ses_yoneticisi, aktif_index, self.muzik_secici_scroll, self.muzik_secim_modu)
        
        elif self.oyun_durumu == "BASARIMLAR":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # Başarımlar ekranı arka planı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            self.menu.basarimlar_ekrani_ciz(self.basarimlar)
        
        elif self.oyun_durumu == "ISTATISTIKLER":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # İstatistikler ekranı arka planı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            self.menu.istatistikler_ekrani_ciz(self.istatistikler)
        
        elif self.oyun_durumu == "KREDILER":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # Krediler ekranı arka planı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            self.menu.krediler_ekrani_ciz()
        
        elif self.oyun_durumu == "PVP_ISIM_GIRIS":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # PVP isim giriş ekranı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            self.menu.pvp_isim_giris_ciz(
                self.pvp_isim_input_aktif,
                self.pvp_oyuncu1_isim_temp,
                self.pvp_oyuncu2_isim_temp
            )
        
        elif self.oyun_durumu == "PVP_MOD_SECIM":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # PVP mod seçim ekranı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            self.menu.pvp_mod_secim_ciz(self.pvp_secili_mod)
        
        elif self.oyun_durumu == "BOT_ZORLUK_SECIM":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # Bot zorluk seçim ekranı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            self.menu.bot_zorluk_secim_ciz(self.bot_zorluk)
        
        elif self.oyun_durumu == "PLAYING":
            # Mouse imlecini gizle
            pygame.mouse.set_visible(False)
            # Tema renklerini al
            tema_renkleri = TEMALAR[self.aktif_tema]
            
            # Arka planı ekrana çiz
            self.ekran.fill((0, 0, 0))  # Siyah kenarlıklar
            if self.oyun_arkaplan:
                # Arka planı sadece oyun alanına çiz
                arkaplan_scaled = pygame.transform.smoothscale(self.oyun_arkaplan, (self.oyun_genislik, self.oyun_yukseklik))
                self.ekran.blit(arkaplan_scaled, (self.oyun_offset_x, self.oyun_offset_y))
            else:
                # Oyun alanını tema rengi ile doldur
                oyun_alani_rect = pygame.Rect(self.oyun_offset_x, self.oyun_offset_y, self.oyun_genislik, self.oyun_yukseklik)
                pygame.draw.rect(self.ekran, tema_renkleri["arkaplan"], oyun_alani_rect)
            
            # İzgara çizgilerini çiz - SADECE OYUN ALANINDA, OFFSET İLE
            cizgi_kalinligi = max(1, self.hucre_boyutu // 25)
            for x in range(0, self.oyun_genislik + 1, self.hucre_boyutu):
                pygame.draw.line(self.ekran, tema_renkleri["izgara"], 
                               (x + self.oyun_offset_x, self.oyun_offset_y), 
                               (x + self.oyun_offset_x, self.oyun_yukseklik + self.oyun_offset_y), 
                               cizgi_kalinligi)
            for y in range(0, self.oyun_yukseklik + 1, self.hucre_boyutu):
                pygame.draw.line(self.ekran, tema_renkleri["izgara"], 
                               (self.oyun_offset_x, y + self.oyun_offset_y), 
                               (self.oyun_genislik + self.oyun_offset_x, y + self.oyun_offset_y), 
                               cizgi_kalinligi)
            
            # Parçacık efektini çiz - OFFSET İLE
            self.yilan_izi_efekti.ciz(self.ekran, self.oyun_offset_x, self.oyun_offset_y)
            
            # Bomba modu aktifse bombaları çiz - OFFSET İLE
            if self.bomba_modu:
                self.bomba_yoneticisi.ciz(self.ekran, self.oyun_offset_x, self.oyun_offset_y)
            
            # Hayatta Kalma modu için dinamik bombaları çiz - OFFSET İLE
            if self.oyun_modu == "HayattaKalma":
                for bomba_x, bomba_y in self.hayatta_kalma_bombalar:
                    ekran_x = bomba_x + self.oyun_offset_x
                    ekran_y = bomba_y + self.oyun_offset_y
                    bomba_rect = pygame.Rect(ekran_x, ekran_y, self.hucre_boyutu, self.hucre_boyutu)
                    pygame.draw.rect(self.ekran, KIRMIZI, bomba_rect)
                    # Bomba ikonu
                    bomba_emoji = self.menu.render_emoji("💣", self.hucre_boyutu - 4, BEYAZ)
                    self.ekran.blit(bomba_emoji, (ekran_x + 2, ekran_y + 2))
            
            # Oyun elemanlarını çiz - OFFSET İLE
            self.yilan.ciz(self.ekran, self.oyun_offset_x, self.oyun_offset_y)
            # PVP veya Bot modunda 2. yılanı da çiz - OFFSET İLE
            if (self.pvp_modu or self.bot_modu) and self.yilan2:
                self.yilan2.ciz(self.ekran, self.oyun_offset_x, self.oyun_offset_y)
            
            self.yem.ciz(self.ekran, self.oyun_offset_x, self.oyun_offset_y)
            
            # Özel yem varsa çiz - OFFSET İLE
            if self.ozel_yem_aktif and self.ozel_yem:
                self.ozel_yem.ciz(self.ekran, self.oyun_offset_x, self.oyun_offset_y)
            
            # PVP özel yemleri çiz - OFFSET İLE
            if (self.pvp_modu or self.bot_modu):
                if self.pvp_ozel_yem_p1:
                    self.pvp_ozel_yem_p1.ciz(self.ekran, self.oyun_offset_x, self.oyun_offset_y)
                if self.pvp_ozel_yem_p2:
                    self.pvp_ozel_yem_p2.ciz(self.ekran, self.oyun_offset_x, self.oyun_offset_y)
            
            # Sahte yem varsa çiz - OFFSET İLE
            if self.sahte_yem:
                self.sahte_yem.ciz(self.ekran, self.oyun_offset_x, self.oyun_offset_y)
            
            # Yem yeme ve puan efektlerini çiz (en üstte) - OFFSET İLE
            self.yem_yeme_efekti.ciz(self.ekran, self.oyun_offset_x, self.oyun_offset_y)
            self.puan_efekti.ciz(self.ekran, self.oyun_offset_x, self.oyun_offset_y)
            
            # Patlama animasyonu çiz (en üstte)
            if self.patlama_animasyon_sayaci > 0 and self.patlama_pozisyon:
                self._patlama_animasyonu_ciz(self.ekran)
            
            # Skor gösterimi - ANA EKRANA ÇİZ (oyun alanının dışında)
            if self.pvp_modu:
                # PVP modunda her iki oyuncunun skorunu ve yeteneklerini göster
                self.menu.pvp_skorlar_goster(
                    self.yilan.skor, 
                    self.yilan2.skor if self.yilan2 else 0,
                    self.pvp_oyuncu1_isim,
                    self.pvp_oyuncu2_isim,
                    self.p1_kalkan_aktif,
                    self.p2_kalkan_aktif,
                    self.p1_hiz_suresi,
                    self.p2_hiz_suresi
                )
            elif self.bot_modu:
                # Bot modunda oyuncu vs bot skorları ve yetenekleri
                self.menu.pvp_skorlar_goster(
                    self.yilan.skor, 
                    self.yilan2.skor if self.yilan2 else 0,
                    "Sen",
                    f"Bot ({self.bot_zorluk})",
                    self.p1_kalkan_aktif,
                    self.p2_kalkan_aktif,
                    self.p1_hiz_suresi,
                    self.p2_hiz_suresi
                )
            else:
                self.menu.skor_goster(self.yilan.skor, self.en_yuksek_skor)
            
            # Zamana Karşı modu için süre göstergesi - ANA EKRANA ÇİZ ARKA PLANLI
            if self.oyun_modu == "ZamanaKarsi" and self.oyun_durumu == "PLAYING":
                gecen_sure = time.time() - self.zaman_modu_baslangic
                kalan_sure = max(0, 60 - gecen_sure)  # 60 saniye
                
                # Süre göstergesi - ekranın üst orta kısmında
                if kalan_sure > 10:
                    sure_renk = YESIL
                    bg_renk = (20, 50, 20, 200)
                    border_renk = YESIL
                elif kalan_sure > 5:
                    sure_renk = TURUNCU
                    bg_renk = (50, 35, 20, 200)
                    border_renk = TURUNCU
                else:
                    sure_renk = KIRMIZI
                    bg_renk = (50, 20, 20, 200)
                    border_renk = KIRMIZI
                
                # Arka plan kutusu
                sure_bg_rect = pygame.Rect(self.ekran_genislik // 2 - 120, 10, 240, 50)
                pygame.draw.rect(self.ekran, bg_renk, sure_bg_rect, border_radius=10)
                pygame.draw.rect(self.ekran, border_renk, sure_bg_rect, 3, border_radius=10)
                
                sure_text = self.menu.buyuk_font.render(f"Süre: {int(kalan_sure)}", True, sure_renk)
                sure_rect = sure_text.get_rect(center=(self.ekran_genislik // 2, 35))
                self.ekran.blit(sure_text, sure_rect)
            
            # Hayatta Kalma modu için hız göstergesi - ANA EKRANA ÇİZ ARKA PLANLI
            if self.oyun_modu == "HayattaKalma" and self.oyun_durumu == "PLAYING":
                gecen_sure = time.time() - self.hayatta_kalma_baslangic
                hiz_seviyesi = min(10, int(gecen_sure // 10) + 1)  # Her 10 saniyede hız artışı
                
                # Arka plan kutusu
                hiz_bg_rect = pygame.Rect(self.ekran_genislik // 2 - 100, 10, 200, 45)
                pygame.draw.rect(self.ekran, (50, 20, 20, 200), hiz_bg_rect, border_radius=10)
                pygame.draw.rect(self.ekran, KIRMIZI, hiz_bg_rect, 3, border_radius=10)
                
                hiz_text = self.menu.font.render(f"Hız: {hiz_seviyesi}", True, KIRMIZI)
                hiz_rect = hiz_text.get_rect(center=(self.ekran_genislik // 2, 32))
                self.ekran.blit(hiz_text, hiz_rect)
            
            # Pause ekranı (en üstte)
            if self.oyun_duraklatildi:
                self._pause_ekrani_ciz()
        
        elif self.oyun_durumu == "GAME_OVER":
            # Mouse imlecini göster
            pygame.mouse.set_visible(True)
            # Oyun bitti arka planı
            if self.menu_arkaplan:
                self.ekran.blit(self.menu_arkaplan, (0, 0))
            else:
                self.ekran.fill(LACIVERT)
            
            if self.pvp_modu:
                # PVP oyun bitti ekranı - kazananı göster
                self.menu.pvp_oyun_bitti_ekrani(
                    self.yilan.skor, 
                    self.yilan2.skor if self.yilan2 else 0,
                    self.pvp_kazanan if hasattr(self, 'pvp_kazanan') else "Bilinmiyor",
                    self.pvp_oyuncu1_isim,
                    self.pvp_oyuncu2_isim
                )
            elif self.bot_modu:
                # Bot oyun bitti ekranı - kazananı göster
                self.menu.pvp_oyun_bitti_ekrani(
                    self.yilan.skor, 
                    self.yilan2.skor if self.yilan2 else 0,
                    self.pvp_kazanan if hasattr(self, 'pvp_kazanan') else "Bilinmiyor",
                    "Sen",
                    f"Bot ({self.bot_zorluk})"
                )
            else:
                self.menu.oyun_bitti_ekrani(self.yilan.skor, self.en_yuksek_skor, self.yeni_basarimlar)
    
    def _patlama_animasyonu_ciz(self, surface):
        """Patlama animasyonunu çizer"""
        if not self.patlama_pozisyon:
            return
        
        patlama_x, patlama_y = self.patlama_pozisyon
        frame = self.patlama_animasyon_sayaci
        
        # Patlama animasyonu (basit daireler)
        for i in range(3):
            radius = int((frame + i * 5) * 2)
            alpha = max(0, 255 - frame * 20)
            color = (255, alpha // 2, 0)
            pygame.draw.circle(surface, color, (patlama_x, patlama_y), radius, 3)
    
    def _pause_ekrani_ciz(self):
        """Pause ekranını çizer"""
        # Yarı saydam overlay
        overlay = pygame.Surface((self.ekran_genislik, self.ekran_yukseklik))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.ekran.blit(overlay, (0, 0))
        
        # PAUSE yazısı
        pause_text = self.menu.buyuk_font.render('DURAKLAT ILD I', True, BEYAZ)
        pause_rect = pause_text.get_rect(center=(self.ekran_genislik // 2, self.ekran_yukseklik // 2))
        self.ekran.blit(pause_text, pause_rect)
        
        # Devam et mesajı
        devam_text = self.menu.kucuk_font.render('ESC - Devam Et', True, ACIK_GRI)
        devam_rect = devam_text.get_rect(center=(self.ekran_genislik // 2, self.ekran_yukseklik // 2 + 60))
        self.ekran.blit(devam_text, devam_rect)
