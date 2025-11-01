# Apple Emoji Arşivi Kullanım Kılavuzu

## Arşiv Konumu
`apple_emojis/` klasöründe 3793 Apple emoji PNG dosyası bulunmaktadır (64x64 boyutunda).

## Emoji Dosya İsimleri (Unicode Kodları)

### Oyunda Kullanılan Emojiler:

#### Meyveler (Yemler):
- 🍎 Elma: `1f34e.png`
- 🍊 Portakal: `1f34a.png`
- 🍇 Üzüm: `1f347.png`
- 🍒 Kiraz: `1f352.png`
- 🍌 Muz: `1f34c.png`

#### Özel Yemler:
- 🛡️ Kalkan: `1f6e1-fe0f.png`
- 💎 Elmas: `1f48e.png`
- ☠️ Zehir: `2620-fe0f.png`
- ❄️ Dondurucu: `2744-fe0f.png`
- ⚡ Yıldırım: `26a1.png`
- 🐌 Salyangoz: `1f40c.png`

#### İstatistik İkonları:
- 🎮 Gamepad: `1f3ae.png`
- 📊 Bar Chart: `1f4ca.png`
- 🏆 Kupa: `1f3c6.png`
- 📈 Grafik: `1f4c8.png`
- 👑 Taç: `1f451.png`
- 🐍 Yılan: `1f40d.png`
- ☠️ Kafatası: `2620-fe0f.png`
- ⏱️ Kronometre: `23f1-fe0f.png`

#### Diğer İkonlar:
- 💣 Bomba: `1f4a3.png`
- 🎵 Müzik: `1f3b5.png`
- 🔇 Sessiz: `1f507.png`
- 🔊 Ses: `1f50a.png`
- 🤖 Robot: `1f916.png`
- ⚔️ Kılıçlar: `2694-fe0f.png`
- 🖱️ Mouse: `1f5b1-fe0f.png`
- ⭐ Yıldız: `2b50.png`
- 🔒 Kilit: `1f512.png`
- ✅ Onay: `2705.png`
- 🔄 Yenile: `1f504.png`
- 🖼️ Resim: `1f5bc-fe0f.png`
- 🎸 Gitar: `1f3b8.png`
- ❤️ Kalp: `2764-fe0f.png`

## Kullanım

Emoji dosyalarını kullanmak için Python ile:

```python
import os
from PIL import Image

# Emoji dosyasını yükle
emoji_path = os.path.join("apple_emojis", "1f34e.png")  # Elma
img = Image.open(emoji_path)

# İstediğin boyuta resize et
img_resized = img.resize((32, 32), Image.Resampling.LANCZOS)

# icons/ klasörüne kaydet
img_resized.save("icons/apple.png", "PNG")
```

## Emoji Unicode Kodlarını Bulma

Online araçlar:
- https://emojipedia.org/ (emoji arayıp Unicode kodunu öğren)
- https://unicode.org/emoji/charts/full-emoji-list.html

Veya Python ile:
```python
emoji = "🍎"
unicode_code = hex(ord(emoji))[2:]  # "1f34e"
print(f"Dosya adı: {unicode_code}.png")
```

## Temizlik

Arşivi kullandıktan sonra:
```bash
# ZIP dosyasını sil
rm emoji-data.zip

# Açılmış klasörü sil (isteğe bağlı)
rm -rf emoji-data-master/
```
