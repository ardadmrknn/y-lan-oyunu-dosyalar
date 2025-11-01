#!/usr/bin/env python3
"""
Apple Emoji Kopyalayıcı
Kullanım: python3 copy_emoji.py
"""

from PIL import Image
import os

# Apple emoji arşiv yolu
EMOJI_ARSIV = "apple_emojis"
ICONS_KLASOR = "icons"

# Emoji tanımları: (emoji_unicode_kodu, hedef_dosya_adi, boyut)
EMOJI_LISTESI = [
    # Meyveler
    ("1f34e", "apple", 32),          # 🍎
    ("1f34a", "orange", 32),         # 🍊
    ("1f347", "grapes", 32),         # 🍇
    ("1f352", "cherries", 32),       # 🍒
    ("1f34c", "banana", 32),         # 🍌
    
    # Özel Yemler
    ("1f6e1-fe0f", "shield", 32),    # 🛡️
    ("1f48e", "diamond", 32),        # 💎
    ("2620-fe0f", "poison", 32),     # ☠️
    ("2744-fe0f", "freeze", 32),     # ❄️
    ("26a1", "lightning", 32),       # ⚡
    ("1f40c", "snail", 32),          # 🐌
    
    # İstatistik İkonları
    ("1f3ae", "gamepad", 24),        # 🎮
    ("1f4ca", "stats", 40),          # 📊
    ("1f3c6", "trophy", 24),         # 🏆
    ("1f4c8", "chart", 24),          # 📈
    ("1f451", "crown", 24),          # 👑
    ("1f40d", "snake", 24),          # 🐍
    ("2620-fe0f", "skull", 24),      # ☠️
    ("23f1-fe0f", "stopwatch", 24),  # ⏱️
    
    # Diğer
    ("1f4a3", "bomb", 24),           # 💣
    ("1f3b5", "music", 32),          # 🎵
    ("1f507", "mute", 32),           # 🔇
    ("1f50a", "volume", 32),         # 🔊
    ("1f916", "robot", 32),          # 🤖
    ("2694-fe0f", "swords", 32),     # ⚔️
    ("1f5b1-fe0f", "mouse", 24),     # 🖱️
    ("2b50", "star", 32),            # ⭐
    ("1f512", "lock", 32),           # 🔒
    ("2705", "check", 32),           # ✅
    ("1f504", "refresh", 32),        # 🔄
    ("1f5bc-fe0f", "picture", 32),   # 🖼️
    ("1f3b8", "guitar", 32),         # 🎸
    ("2764-fe0f", "heart", 32),      # ❤️
]

def kopyala_emoji(unicode_kod, hedef_ad, boyut):
    """Emoji dosyasını arşivden alıp icons klasörüne kopyala"""
    kaynak = os.path.join(EMOJI_ARSIV, f"{unicode_kod}.png")
    hedef = os.path.join(ICONS_KLASOR, f"{hedef_ad}.png")
    
    if not os.path.exists(kaynak):
        print(f"❌ {unicode_kod}.png bulunamadı")
        return False
    
    try:
        # Resmi aç ve boyutlandır
        img = Image.open(kaynak)
        img_resized = img.resize((boyut, boyut), Image.Resampling.LANCZOS)
        img_resized.save(hedef, "PNG")
        print(f"✅ {hedef_ad}.png ({boyut}x{boyut})")
        return True
    except Exception as e:
        print(f"❌ {hedef_ad}.png: {e}")
        return False

def main():
    """Tüm emojileri kopyala"""
    print("🎨 Apple Emoji Kopyalayıcı\n")
    
    if not os.path.exists(EMOJI_ARSIV):
        print(f"❌ {EMOJI_ARSIV} klasörü bulunamadı!")
        print("Önce emoji-data.zip'i indirip açmanız gerekiyor.")
        return
    
    if not os.path.exists(ICONS_KLASOR):
        os.makedirs(ICONS_KLASOR)
        print(f"📁 {ICONS_KLASOR} klasörü oluşturuldu\n")
    
    basarili = 0
    basarisiz = 0
    
    for unicode_kod, hedef_ad, boyut in EMOJI_LISTESI:
        if kopyala_emoji(unicode_kod, hedef_ad, boyut):
            basarili += 1
        else:
            basarisiz += 1
    
    print(f"\n📊 Sonuç: {basarili} başarılı, {basarisiz} başarısız")

if __name__ == "__main__":
    main()
