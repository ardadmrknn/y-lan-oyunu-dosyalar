# 🐍 Yılan Oyunu

Python ve Pygame ile geliştirilmiş gelişmiş yılan oyunu.

## 🎮 Özellikler

### Oyun Modları
- **Normal Mod**: Klasik yılan oyunu
- **Bomb Modu**: Bombalardan kaçarak puan kazan
- **Bot Modu**: Yapay zeka ile yarış (3 zorluk seviyesi)
- **PVP Modu**: İki oyunculu yerel multiplayer

### Özel Yemler
- 🍎 Normal meyveler (elma, portakal, üzüm, kiraz, muz)
- 💎 Elmas (yüksek puan)
- ☠️ Zehirli yem (ceza)
- ❄️ Dondurucu yem
- ⚡ Hız yemi
- 🐌 Yavaşlatma yemi
- 🛡️ Kalkan (PVP)

### Sistem Özellikleri
- 🏆 Başarım sistemi (25+ başarım)
- 📊 Detaylı istatistikler
- 🎵 Müzik sistemi (kendi müziğini ekle)
- 🎨 Özelleştirilebilir arkaplanlar
- ⚙️ Hız ayarları
- 🖥️ Tam ekran desteği

## 🚀 Kurulum

### Gereksinimler
- Python 3.9+
- Pygame
- Pillow (PIL)

### Kurulum Adımları

```bash
# Depoyu klonla
git clone [repo-url]
cd "yılan oyunu"

# Bağımlılıkları yükle
pip install pygame pillow

# Oyunu başlat
python3 main.py
# veya
./oyunu_baslat.sh
```

## 🎮 Kontroller

### Tek Oyunculu
- **Yön Tuşları**: Hareket
- **ESC**: Menüye dön
- **P**: Duraklat

### PVP Modu
**Oyuncu 1:**
- W/A/S/D: Hareket

**Oyuncu 2:**
- Yön Tuşları: Hareket

## 📁 Proje Yapısı

```
yılan oyunu/
├── main.py              # Ana dosya
├── game.py              # Oyun mantığı
├── menu.py              # Menü sistemi
├── snake.py             # Yılan sınıfı
├── ai_snake.py          # Yapay zeka yılanı
├── food.py              # Yem sistemi (meyve emojileri)
├── special_food.py      # Özel yemler
├── bomb.py              # Bomba sistemi
├── achievements.py      # Başarımlar
├── statistics.py        # İstatistikler
├── sounds.py            # Ses yönetimi
├── effects.py           # Görsel efektler
├── settings.py          # Ayarlar yöneticisi
├── utils.py             # Yardımcı fonksiyonlar
├── constants.py         # Sabitler
├── copy_emoji.py        # Emoji kopyalayıcı (bakım için)
├── EMOJI_KODLARI.md     # Emoji Unicode rehberi
├── icons/               # Oyun icon'ları (PNG)
├── backgrounds/         # Arkaplan resimleri
├── music/               # Müzik dosyaları
└── apple_emojis/        # Apple emoji arşivi (3793 emoji)
```

## 🎨 Emoji Sistemi

Oyun Apple'ın resmi emoji setini kullanır. Tüm görseller PNG formatında ve yüksek kalitede.

### Yeni Emoji Ekleme

```bash
# 1. EMOJI_KODLARI.md dosyasından Unicode kodunu bul
# 2. copy_emoji.py dosyasını düzenle
# 3. Script'i çalıştır
python3 copy_emoji.py
```

Detaylar için `EMOJI_KODLARI.md` dosyasına bakın.

## 📊 Kayıt Dosyaları

- `basarimlar.json`: Başarım ilerlemeleri
- `istatistikler.json`: Oyun istatistikleri
- `oyun_ayarlari.json`: Kullanıcı ayarları

## 🎵 Müzik Ekleme

1. MP3 dosyalarını `music/` klasörüne koy
2. Menüden "Müzik Seç" seçeneğine gir
3. İstediğin müziği seç

## 🐛 Bilinen Sorunlar

Şu anda bilinen kritik sorun yok.

## 📝 Geliştirici Notları

### Kod Kalitesi
- ✅ Tüm görseller Apple emoji PNG (el çizimi yok)
- ✅ Modüler yapı
- ✅ Temiz kod (food.py: %33, special_food.py: %80 kod azaltma)
- ✅ Performans optimizasyonları (image caching)

### Güncelleme Geçmişi
- **v2.0** - PNG emoji sistemi, kod temizleme
- **v1.5** - İstatistikler ve başarım sistemi
- **v1.0** - İlk sürüm

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır!

## 📜 Lisans

Bu proje kişisel kullanım içindir.

## 🙏 Teşekkürler

- Apple emoji seti için [emoji-data](https://github.com/iamcal/emoji-data)
- Pygame topluluğu

## ⚡ Windows Optimizasyonları

Bu proje Windows'ta optimum performans için optimize edilmiştir:

### Performans İyileştirmeleri
- **Yüksek FPS**: Maksimum 120 FPS desteği (önceden 25)
- **Hardware Acceleration**: OpenGL ile GPU kullanımı
- **Çizim Optimizasyonu**: Gereksiz efektler kaldırıldı
- **Bellek Optimizasyonu**: Surface caching sistemi
- **Smooth Gameplay**: Modern hız seviyeleri

### Windows Executable
```bash
# Executable oluşturmak için
pip install pyinstaller
python build_exe.py
```

Oluşturulan `Yilan_Oyunu.exe` dosyası tek başına çalışır ve Python kurulumuna ihtiyaç duymaz.

### Sistem Gereksinimleri
- **Windows 10/11**
- **DirectX 11+** (OpenGL için)
- **4GB RAM** minimum
- **GPU ile daha iyi performans**

---

**İyi oyunlar! 🎮🐍**
