"""
Oyun sabitleri ve ayarları
"""

# Renkler
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KIRMIZI = (255, 0, 0)
KOYUKIRMIZI = (139, 0, 0)
YESIL = (34, 139, 34)
KOYUYESIL = (0, 100, 0)
ACIK_YESIL = (144, 238, 144)
MAVI = (0, 0, 255)
TURUNCU = (255, 165, 0)
KAHVERENGI = (139, 69, 19)
GRI = (128, 128, 128)
ACIK_GRI = (192, 192, 192)
LACIVERT = (25, 25, 112)

# Ekran boyutları - Varsayılan değerler
GENISLIK = 800
YUKSEKLIK = 520  # 26 hücre * 20 = 520
HUCRE_BOYUTU = 20

# Çözünürlük seçenekleri - 10 farklı seçenek + Tam Ekran
COZUNURLUK_SECENEKLERI = [
    ("800x600", 800, 600),
    ("1024x768", 1024, 768),
    ("1280x720", 1280, 720),
    ("1280x800", 1280, 800),
    ("1366x768", 1366, 768),
    ("1440x900", 1440, 900),
    ("1600x900", 1600, 900),
    ("1680x1050", 1680, 1050),
    ("1920x1080", 1920, 1080),
    ("2560x1440", 2560, 1440),
    ("Tam Ekran", 0, 0)  # 0,0 = sistem tam ekran çözünürlüğü
]

def dinamik_cozunurluk_hesapla(ekran_genislik, ekran_yukseklik):
    """
    Ekran boyutuna göre optimal oyun çözünürlüğü hesapla
    Sabit çözünürlük döndürür, scaling tam ekranda yapılır
    """
    # Ekran boyutuna göre uygun bir temel çözünürlük seç
    if ekran_genislik >= 2560:
        # 4K ve üstü
        oyun_genislik = 1920
        oyun_yukseklik = 1080
        hucre_boyutu = 30
    elif ekran_genislik >= 1920:
        # Full HD
        oyun_genislik = 1600
        oyun_yukseklik = 900
        hucre_boyutu = 30
    elif ekran_genislik >= 1440:
        # HD+
        oyun_genislik = 1280
        oyun_yukseklik = 720
        hucre_boyutu = 30
    elif ekran_genislik >= 1280:
        # HD
        oyun_genislik = 1200
        oyun_yukseklik = 675
        hucre_boyutu = 25
    else:
        # Düşük çözünürlük
        oyun_genislik = 800
        oyun_yukseklik = 520
        hucre_boyutu = 20
    
    # Hücre boyutuna göre yuvarla (grid sistemine uyumlu olması için)
    oyun_genislik = (oyun_genislik // hucre_boyutu) * hucre_boyutu
    oyun_yukseklik = (oyun_yukseklik // hucre_boyutu) * hucre_boyutu
    
    return oyun_genislik, oyun_yukseklik, hucre_boyutu

# Oyun hızı seviyeleri - Windows optimizasyonu için artırıldı
HIZ_ISIMLERI = ["Yavaş", "Normal", "Hızlı", "Çok Hızlı", "Ultra"]
HIZ_FPS = [8, 15, 30, 45, 60]  # %50 yavaşlatılmış FPS seviyeleri
VARSAYILAN_HIZ_SEVIYESI = 1  # Normal (12 FPS)

# Arka plan resimleri klasörü
ARKAPLAN_KLASORU = "backgrounds"
VARSAYILAN_MENU_ARKAPLAN = None  # None = gradient
VARSAYILAN_OYUN_ARKAPLAN = None  # None = gradient
ARKAPLAN_ALPHA = 128  # Transparan değeri (0-255, 128 = %50)

# Yılan renkleri (slither.io tarzı) - GENİŞLETİLDİ
YILAN_RENKLERI = [
    ("Yeşil", (70, 240, 70), (40, 180, 40), (0, 80, 0)),         # Varsayılan
    ("Mavi", (70, 180, 255), (40, 120, 200), (0, 60, 120)),      # Mavi
    ("Kırmızı", (255, 100, 100), (200, 50, 50), (120, 0, 0)),    # Kırmızı
    ("Mor", (200, 100, 255), (150, 50, 200), (80, 0, 120)),      # Mor
    ("Turuncu", (255, 180, 70), (200, 130, 40), (120, 70, 0)),   # Turuncu
    ("Pembe", (255, 150, 200), (200, 100, 150), (120, 50, 80)),  # Pembe
    ("Sarı", (255, 255, 100), (200, 200, 50), (120, 120, 0)),    # Sarı
    ("Turkuaz", (70, 255, 220), (40, 200, 170), (0, 120, 100)),  # Turkuaz
    ("Altın", (255, 215, 0), (218, 165, 32), (184, 134, 11)),    # Altın
    ("Gümüş", (192, 192, 192), (169, 169, 169), (128, 128, 128)), # Gümüş
    ("Bronz", (205, 127, 50), (160, 82, 45), (139, 69, 19)),     # Bronz
    ("Neon Yeşil", (57, 255, 20), (0, 255, 0), (0, 128, 0)),     # Neon Yeşil
    ("Neon Pembe", (255, 16, 240), (255, 0, 255), (139, 0, 139)), # Neon Pembe
    ("Gökkuşağı", (255, 127, 80), (135, 206, 235), (138, 43, 226)), # Gökkuşağı
    ("Lava", (255, 69, 0), (220, 20, 60), (139, 0, 0)),          # Lava
    ("Buz", (173, 216, 230), (135, 206, 250), (70, 130, 180)),   # Buz
    ("Yeşim", (0, 168, 107), (60, 179, 113), (46, 125, 50)),     # Yeşim
    ("Ametist", (153, 102, 204), (138, 43, 226), (75, 0, 130))   # Ametist
]

# Yılan yüzleri (emoji tarzı) - GENİŞLETİLDİ
YILAN_YUZLERI = [
    ("Normal", "normal"),
    ("Mutlu", "mutlu"),
    ("Şaşkın", "saskın"),
    ("Sinirli", "sinirli"),
    ("Havalı", "havali"),
    ("Uyuyan", "uyuyan"),
    ("Aşık", "asik"),
    ("Deli", "deli"),
    ("Robot", "robot"),
    ("Pirat", "pirat")
]

# Yılan aksesuarları (YENİ!)
YILAN_AKSESUARLARI = [
    ("Yok", "yok"),
    ("Gözlük", "gozluk"),
    ("Güneş Gözlüğü", "gunes_gozluk"),
    ("Şapka", "sapka"),
    ("Kral Tacı", "tac"),
    ("Bandana", "bandana"),
    ("Papyon", "papyon"),
    ("Kol Saati", "saat"),
    ("Küpe", "kupe"),
    ("Zincir", "zincir")
]

VARSAYILAN_YILAN_RENK = 0  # Yeşil
VARSAYILAN_YILAN_YUZ = 0   # Normal
VARSAYILAN_YILAN_AKSESUAR = 0  # Yok

# Bomba modu ayarları
BOMBA_SAYISI = 10  # Haritada başlangıçta 10 bomba
BOMBA_RENK = (50, 50, 50)  # Koyu gri gövde
BOMBA_FITIL_RENK = (139, 69, 19)  # Kahverengi fitil
BOMBA_PARLAMA_RENK = (255, 100, 0)  # Turuncu parlama
SAHTE_YEM_ORANI = 4  # Her 4 yemden 1'i sahte yem ile birlikte spawn olur
DONUSUM_MESAFESI = 2  # Sahte yem 2 blok yakınlıkta bombaya dönüşür
PATLAMA_SÜRESI = 45  # Patlama efekti süresi (frame) - 45 frame = 1.5 saniye

# Özel yemler
ALTIN_ELMA_RENK = (255, 215, 0)  # Altın sarısı
ELMAS_RENK = (0, 191, 255)  # Parlak mavi
ZEHIRLI_YEM_RENK = (128, 0, 128)  # Mor
DONDURUCU_YEM_RENK = (135, 206, 250)  # Açık mavi

ALTIN_ELMA_PUAN = 50
ELMAS_PUAN = 100
ZEHIRLI_CEZA = -20
DONDURUCU_SURE = 90  # 3 saniye (30 FPS'de)

OZEL_YEM_SPAWN_SANSI = 0.15  # %15 şans

# Temalar
TEMALAR = {
    "Klasik": {
        "arkaplan": (20, 20, 40),
        "izgara": (40, 40, 50)
    },
    "Gece": {
        "arkaplan": (10, 10, 25),
        "izgara": (30, 30, 45)
    },
    "Neon": {
        "arkaplan": (0, 0, 30),
        "izgara": (255, 0, 255)
    },
    "Retro": {
        "arkaplan": (50, 20, 0),
        "izgara": (100, 60, 20)
    },
    "Doğa": {
        "arkaplan": (34, 139, 34),
        "izgara": (0, 100, 0)
    }
}

# Başarımlar
BASARIMLAR = {
    "ilk_adim": {"isim": "İlk Adım", "aciklama": "İlk oyununu oyna", "hedef": 1},
    "yemci": {"isim": "Yemci", "aciklama": "10 yem ye", "hedef": 10},
    "acikmis": {"isim": "Açıkmış!", "aciklama": "50 yem ye", "hedef": 50},
    "usta_avcı": {"isim": "Usta Avcı", "aciklama": "100 yem ye", "hedef": 100},
    "puan_avcisi": {"isim": "Puan Avcısı", "aciklama": "100 puan topla", "hedef": 100},
    "puanlama_ustasi": {"isim": "Puanlama Ustası", "aciklama": "500 puan topla", "hedef": 500},
    "efsane": {"isim": "Efsane", "aciklama": "1000 puan topla", "hedef": 1000},
    "kucuk_yilan": {"isim": "Küçük Yılan", "aciklama": "Uzunluğun 10 olsun", "hedef": 10},
    "orta_yilan": {"isim": "Orta Boy Yılan", "aciklama": "Uzunluğun 20 olsun", "hedef": 20},
    "dev_yilan": {"isim": "Dev Yılan", "aciklama": "Uzunluğun 50 olsun", "hedef": 50},
    "bomba_ustasi": {"isim": "Bomba Ustası", "aciklama": "200 kez bombaya çarp", "hedef": 200},
    "altin_avcisi": {"isim": "Altın Avcısı", "aciklama": "5 altın elma ye", "hedef": 5},
    "elmas_toplama": {"isim": "Elmas Toplayıcı", "aciklama": "3 elmas ye", "hedef": 3},
    "hizli_oyuncu": {"isim": "Hızlı Oyuncu", "aciklama": "Çok Hızlı modda 100 puan", "hedef": 100},
    "tecrubeli": {"isim": "Tecrübeli", "aciklama": "10 oyun oyna", "hedef": 10},
    "bagimsiz": {"isim": "Bağımsız", "aciklama": "50 oyun oyna", "hedef": 50},
    "maraton": {"isim": "Maraton", "aciklama": "100 oyun oyna", "hedef": 100},
    # YENİ BASARIMLAR
    "hizli_ofkeli": {"isim": "Hızlı ve Öfkeli", "aciklama": "En yüksek hızda 50 puan", "hedef": 50},
    "bomba_imha": {"isim": "Bomba İmha", "aciklama": "50 kez bombaya çarp", "hedef": 50},
    "mukemmellik": {"isim": "Mükemmellik", "aciklama": "Hiç ölmeden 200 puan", "hedef": 200},
    "uzun_maraton": {"isim": "Uzun Maraton", "aciklama": "10 dakika canlı kal", "hedef": 600},  # 600 saniye
    "zaman_ustasi": {"isim": "Zaman Ustası", "aciklama": "Zamana Karşı modda 100 puan", "hedef": 100},
    "hayatta_kalma": {"isim": "Hayatta Kalma Uzmanı", "aciklama": "Hayatta Kalma modunda 5 dakika", "hedef": 300},  # 300 saniye
    # ÖZEL YEM BASARIMLARI
    "hiz_canavarı": {"isim": "Hız Canavarı", "aciklama": "10 hız yemi ye", "hedef": 10},
    "simsek_mcqueen": {"isim": "Şimşek McQueen", "aciklama": "50 hız yemi ye", "hedef": 50},
    "kalkan_ustasi": {"isim": "Kalkan Ustası", "aciklama": "10 kalkan yemi ye", "hedef": 10},
    "savunma_uzmani": {"isim": "Savunma Uzmanı", "aciklama": "50 kalkan yemi ye", "hedef": 50},
    "yavaslatici": {"isim": "Yavaşlatıcı", "aciklama": "10 yavaşlatma yemi ye", "hedef": 10},
    "zaman_bükücü": {"isim": "Zaman Bükücü", "aciklama": "50 yavaşlatma yemi ye", "hedef": 50},
    "zehir_tadici": {"isim": "Zehir Tadıcı", "aciklama": "5 zehirli yem ye", "hedef": 5},
    "zehir_asigi": {"isim": "Zehir Aşığı", "aciklama": "25 zehirli yem ye", "hedef": 25},
    "buz_krali": {"isim": "Buz Kralı", "aciklama": "10 dondurucu yem ye", "hedef": 10},
    "buz_tanrisi": {"isim": "Buz Tanrısı", "aciklama": "50 dondurucu yem ye", "hedef": 50},
}

# Ses ayarları
SES_ACIK = True
MUZIK_ACIK = True
SES_SEVIYESI = 0.7
MUZIK_SEVIYESI = 0.5

# Bot ayarları
BOT_ZORLUKLAR = ["Kolay", "Orta", "Zor"]
BOT_ZORLUK_ACIKLAMALARI = {
    "Kolay": "Yavaş ve hatalı - Yeni başlayanlar için",
    "Orta": "Dengeli - Orta seviye oyuncular için",
    "Zor": "Hızlı ve akıllı - Uzman oyuncular için"
}
VARSAYILAN_BOT_ZORLUK = "Orta"

# PVP Özel Yem Ayarları (OPTIMIZASYON: Magic number'ları sabitlere taşıdık)
PVP_SPAWN_SKOR_ARALIGI = 50  # Her 50 skorda bir özel yem spawn olur
PVP_HIZ_SURESI = 5.0  # Hız yeminin süresi (saniye)
PVP_KALKAN_RENK_ALPHA = 100  # Kalkan göstergesi renk şeffaflığı
PVP_HIZ_RENK = (255, 255, 0)  # Hız göstergesi rengi (sarı)

# Performans Optimizasyonu Sabitleri
CACHE_BOYUTU = 100  # Pozisyon cache boyutu
MAX_PARTICLE_COUNT = 50  # Maksimum partikül sayısı
FRAME_SKIP_THRESHOLD = 5  # Frame atlama eşiği (düşük FPS'de)

# UI Sabitleri (menu.py'den taşındı)
BUTON_YUKSEKLIK = 60
BUTON_GENISLIK = 300
BUTON_BOSLUK = 20
BASLIK_BOYUT = 64
ALT_BASLIK_BOYUT = 36
TEXT_BOYUT = 24
KUCUK_TEXT_BOYUT = 18

# Yeni Oyun Modları
ZAMAN_MODU_SURE = 60  # Zamana karşı mod süresi (saniye)
HAYATTA_KALMA_BASLANGIC_FPS = 7  # Hayatta kalma mod başlangıç hızı (FPS)
HAYATTA_KALMA_HIZ_ARTIS_FPS = 1  # Her 5 saniyede +1 FPS
HAYATTA_KALMA_HIZ_INTERVAL = 5  # Hız artış aralığı (saniye)
HAYATTA_KALMA_BOMBA_INTERVAL = 10  # Bomba spawn aralığı (saniye)
HAYATTA_KALMA_MIN_BOMBA_MESAFE = 3  # Bombalar yılandan en az bu kadar blok uzakta spawn olur

# Power-up Ayarları
YAVASLAMA_SURESI = 5.0  # Yavaşlatma süresi (saniye)
YAVASLAMA_CARPAN = 0.5  # Yavaşlatma çarpanı (rakibin hızı yarıya iner)
