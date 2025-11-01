#!/usr/bin/env python3
"""
Emoji ikonları oluşturmak için yardımcı script
PIL kullanarak emoji PNG dosyaları oluşturur
"""
from PIL import Image, ImageDraw, ImageFont
import os

# icons klasörü
ICONS_DIR = "icons"
os.makedirs(ICONS_DIR, exist_ok=True)

def create_gamepad_icon(size=128):
    """Gamepad ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Yeşil renk
    color = (0, 255, 0, 255)
    
    # Gamepad gövdesi
    draw.rounded_rectangle(
        [(size//6, size//3), (size*5//6, size*2//3)],
        radius=15,
        outline=color,
        width=8
    )
    
    # Sol D-pad
    d_center_x = size // 3
    d_center_y = size // 2
    d_size = size // 10
    # Yatay çizgi
    draw.rectangle(
        [(d_center_x - d_size*1.5, d_center_y - d_size//2),
         (d_center_x + d_size*1.5, d_center_y + d_size//2)],
        fill=color
    )
    # Dikey çizgi
    draw.rectangle(
        [(d_center_x - d_size//2, d_center_y - d_size*1.5),
         (d_center_x + d_size//2, d_center_y + d_size*1.5)],
        fill=color
    )
    
    # Sağ butonlar
    btn_center_x = size * 2 // 3
    btn_center_y = size // 2
    btn_r = size // 14
    
    # Üst buton
    draw.ellipse(
        [(btn_center_x - btn_r, btn_center_y - size//6 - btn_r),
         (btn_center_x + btn_r, btn_center_y - size//6 + btn_r)],
        outline=color,
        width=5
    )
    # Sağ buton
    draw.ellipse(
        [(btn_center_x + size//8 - btn_r, btn_center_y - btn_r),
         (btn_center_x + size//8 + btn_r, btn_center_y + btn_r)],
        outline=color,
        width=5
    )
    
    img.save(f"{ICONS_DIR}/gamepad.png")
    print(f"✅ {ICONS_DIR}/gamepad.png oluşturuldu")

def create_bomb_icon(size=128):
    """Bomba ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Turuncu renk
    color = (255, 165, 0, 255)
    
    # Bomba gövdesi
    center_y = size * 5 // 8
    draw.ellipse(
        [(size//4, center_y - size//3),
         (size*3//4, center_y + size//3)],
        outline=color,
        width=8
    )
    
    # Fitil
    draw.line(
        [(size//2, center_y - size//3),
         (size*2//3, size//6)],
        fill=color,
        width=6
    )
    
    # Kıvılcım (sarı)
    spark_color = (255, 200, 0, 255)
    spark_size = size // 10
    draw.ellipse(
        [(size*2//3 - spark_size, size//6 - spark_size),
         (size*2//3 + spark_size, size//6 + spark_size)],
        fill=spark_color
    )
    
    # Parlama efekti
    draw.line(
        [(size*2//3 - spark_size*1.5, size//6),
         (size*2//3 + spark_size*1.5, size//6)],
        fill=spark_color,
        width=3
    )
    draw.line(
        [(size*2//3, size//6 - spark_size*1.5),
         (size*2//3, size//6 + spark_size*1.5)],
        fill=spark_color,
        width=3
    )
    
    img.save(f"{ICONS_DIR}/bomb.png")
    print(f"✅ {ICONS_DIR}/bomb.png oluşturuldu")

def create_swords_icon(size=128):
    """Çapraz kılıçlar ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Mavi renk
    color = (0, 100, 255, 255)
    
    # Sol kılıç (\ yönünde)
    draw.line(
        [(size//4, size*3//4), (size*3//4, size//4)],
        fill=color,
        width=10
    )
    # Sol kılıç sapı
    draw.ellipse(
        [(size//4 - size//12, size*3//4 - size//12),
         (size//4 + size//12, size*3//4 + size//12)],
        outline=color,
        width=5
    )
    
    # Sağ kılıç (/ yönünde)
    draw.line(
        [(size*3//4, size*3//4), (size//4, size//4)],
        fill=color,
        width=10
    )
    # Sağ kılıç sapı
    draw.ellipse(
        [(size*3//4 - size//12, size*3//4 - size//12),
         (size*3//4 + size//12, size*3//4 + size//12)],
        outline=color,
        width=5
    )
    
    img.save(f"{ICONS_DIR}/swords.png")
    print(f"✅ {ICONS_DIR}/swords.png oluşturuldu")

def create_robot_icon(size=128):
    """Robot ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Pembe renk
    color = (255, 100, 150, 255)
    
    # Robot kafası
    head_top = size // 3
    head_bottom = size * 5 // 6
    draw.rounded_rectangle(
        [(size//4, head_top),
         (size*3//4, head_bottom)],
        radius=8,
        outline=color,
        width=8
    )
    
    # Anten
    antenna_top = size // 8
    draw.line(
        [(size//2, head_top), (size//2, antenna_top)],
        fill=color,
        width=6
    )
    # Anten topu
    antenna_size = size // 12
    draw.ellipse(
        [(size//2 - antenna_size, antenna_top - antenna_size),
         (size//2 + antenna_size, antenna_top + antenna_size)],
        fill=color
    )
    
    # Gözler
    eye_y = size // 2
    eye_size = size // 12
    # Sol göz
    draw.ellipse(
        [(size//3 - eye_size//2, eye_y - eye_size//2),
         (size//3 + eye_size//2, eye_y + eye_size//2)],
        fill=color
    )
    # Sağ göz
    draw.ellipse(
        [(size*2//3 - eye_size//2, eye_y - eye_size//2),
         (size*2//3 + eye_size//2, eye_y + eye_size//2)],
        fill=color
    )
    
    # Ağız
    mouth_y = size * 2 // 3
    draw.arc(
        [(size//3, mouth_y - size//12),
         (size*2//3, mouth_y + size//12)],
        start=0,
        end=180,
        fill=color,
        width=5
    )
    
    img.save(f"{ICONS_DIR}/robot.png")
    print(f"✅ {ICONS_DIR}/robot.png oluşturuldu")

def create_trophy_icon(size=128):
    """Kupa ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Altın renk
    color = (255, 215, 0, 255)
    
    # Kupa gövdesi
    draw.ellipse(
        [(size//4, size//3),
         (size*3//4, size*2//3)],
        outline=color,
        width=8
    )
    
    # Kulplar
    # Sol kulp
    draw.arc(
        [(size//8, size//3),
         (size//3, size//2)],
        start=90,
        end=270,
        fill=color,
        width=6
    )
    # Sağ kulp
    draw.arc(
        [(size*2//3, size//3),
         (size*7//8, size//2)],
        start=270,
        end=90,
        fill=color,
        width=6
    )
    
    # Kaide
    draw.rectangle(
        [(size//3, size*2//3),
         (size*2//3, size*3//4)],
        fill=color
    )
    # Alt kaide
    draw.rectangle(
        [(size//4, size*3//4),
         (size*3//4, size*4//5)],
        fill=color
    )
    
    img.save(f"{ICONS_DIR}/trophy.png")
    print(f"✅ {ICONS_DIR}/trophy.png oluşturuldu")

def create_music_icon(size=128):
    """Müzik notu ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color = (100, 150, 255, 255)
    
    # Sol nota
    note_x1 = size // 3
    note_y = size * 2 // 3
    # Nota başı
    draw.ellipse(
        [(note_x1 - size//12, note_y - size//12),
         (note_x1 + size//12, note_y + size//12)],
        fill=color
    )
    # Nota sapı
    draw.line(
        [(note_x1 + size//12, note_y),
         (note_x1 + size//12, size//4)],
        fill=color,
        width=6
    )
    
    # Sağ nota
    note_x2 = size * 2 // 3
    draw.ellipse(
        [(note_x2 - size//12, note_y - size//12),
         (note_x2 + size//12, note_y + size//12)],
        fill=color
    )
    draw.line(
        [(note_x2 + size//12, note_y),
         (note_x2 + size//12, size//5)],
        fill=color,
        width=6
    )
    
    # Bağlantı çizgisi
    draw.line(
        [(note_x1 + size//12, size//4),
         (note_x2 + size//12, size//5)],
        fill=color,
        width=8
    )
    
    img.save(f"{ICONS_DIR}/music.png")
    print(f"✅ {ICONS_DIR}/music.png oluşturuldu")

def create_volume_icon(size=128):
    """Hoparlör ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color = (255, 255, 255, 255)
    
    # Hoparlör
    draw.polygon(
        [(size//4, size//3),
         (size//2, size//3),
         (size*2//3, size//4),
         (size*2//3, size*3//4),
         (size//2, size*2//3),
         (size//4, size*2//3)],
        fill=color
    )
    
    # Ses dalgaları
    for i in range(1, 4):
        arc_box = [
            (size*2//3, size//2 - size//6 * i),
            (size*2//3 + size//6 * i, size//2 + size//6 * i)
        ]
        draw.arc(arc_box, start=-60, end=60, fill=color, width=5)
    
    img.save(f"{ICONS_DIR}/volume.png")
    print(f"✅ {ICONS_DIR}/volume.png oluşturuldu")

def create_mute_icon(size=128):
    """Sessiz ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color = (200, 200, 200, 255)
    
    # Hoparlör
    draw.polygon(
        [(size//4, size//3),
         (size//2, size//3),
         (size*2//3, size//4),
         (size*2//3, size*3//4),
         (size//2, size*2//3),
         (size//4, size*2//3)],
        outline=color,
        width=5
    )
    
    # X işareti (kırmızı)
    x_color = (255, 50, 50, 255)
    draw.line(
        [(size*2//3, size//3), (size*5//6, size*2//3)],
        fill=x_color,
        width=8
    )
    draw.line(
        [(size*5//6, size//3), (size*2//3, size*2//3)],
        fill=x_color,
        width=8
    )
    
    img.save(f"{ICONS_DIR}/mute.png")
    print(f"✅ {ICONS_DIR}/mute.png oluşturuldu")

def create_lightning_icon(size=128):
    """Şimşek ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color = (255, 255, 0, 255)
    
    # Şimşek şekli
    points = [
        (size*3//5, size//6),
        (size//2, size//2),
        (size*3//5, size//2),
        (size*2//5, size*5//6),
        (size//2, size//2),
        (size*2//5, size//2)
    ]
    draw.polygon(points, fill=color, outline=(255, 200, 0, 255), width=3)
    
    img.save(f"{ICONS_DIR}/lightning.png")
    print(f"✅ {ICONS_DIR}/lightning.png oluşturuldu")

def create_picture_icon(size=128):
    """Resim ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color = (150, 100, 255, 255)
    
    # Çerçeve
    draw.rectangle(
        [(size//6, size//4),
         (size*5//6, size*3//4)],
        outline=color,
        width=6
    )
    
    # Güneş
    draw.ellipse(
        [(size*2//3, size//3),
         (size*3//4, size*5//12)],
        fill=(255, 255, 0, 255)
    )
    
    # Dağlar
    draw.polygon(
        [(size//4, size*3//5),
         (size*2//5, size//2),
         (size*3//5, size*3//5)],
        fill=color
    )
    
    img.save(f"{ICONS_DIR}/picture.png")
    print(f"✅ {ICONS_DIR}/picture.png oluşturuldu")

def create_snake_icon(size=128):
    """Yılan ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color = (0, 255, 0, 255)
    
    # Yılan gövdesi (S şekli)
    # Üst kıvrım
    draw.arc(
        [(size//4, size//6),
         (size*3//4, size//2)],
        start=180,
        end=0,
        fill=color,
        width=12
    )
    # Alt kıvrım
    draw.arc(
        [(size//4, size//2),
         (size*3//4, size*5//6)],
        start=0,
        end=180,
        fill=color,
        width=12
    )
    
    # Baş
    draw.ellipse(
        [(size*3//4 - size//10, size*5//6 - size//10),
         (size*3//4 + size//10, size*5//6 + size//10)],
        fill=color
    )
    
    # Göz
    draw.ellipse(
        [(size*3//4 + size//20, size*5//6 - size//20),
         (size*3//4 + size//12, size*5//6)],
        fill=(0, 0, 0, 255)
    )
    
    img.save(f"{ICONS_DIR}/snake.png")
    print(f"✅ {ICONS_DIR}/snake.png oluşturuldu")

def create_guitar_icon(size=128):
    """Gitar ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color = (200, 100, 50, 255)
    
    # Gitar gövdesi
    draw.ellipse(
        [(size//3, size//2),
         (size*2//3, size*5//6)],
        outline=color,
        width=6
    )
    
    # Sap
    draw.rectangle(
        [(size*7//16, size//6),
         (size*9//16, size//2)],
        fill=color
    )
    
    # Teller
    for i in range(3):
        y = size//2 + i * size//12
        draw.line(
            [(size//3, y), (size*2//3, y)],
            fill=(200, 200, 200, 255),
            width=2
        )
    
    img.save(f"{ICONS_DIR}/guitar.png")
    print(f"✅ {ICONS_DIR}/guitar.png oluşturuldu")

def create_star_icon(size=128):
    """Yıldız ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color = (255, 255, 0, 255)
    
    # 5 köşeli yıldız
    import math
    center_x, center_y = size // 2, size // 2
    outer_r = size // 2 - 10
    inner_r = size // 5
    
    points = []
    for i in range(10):
        angle = math.pi * 2 * i / 10 - math.pi / 2
        r = outer_r if i % 2 == 0 else inner_r
        x = center_x + r * math.cos(angle)
        y = center_y + r * math.sin(angle)
        points.append((x, y))
    
    draw.polygon(points, fill=color, outline=(255, 200, 0, 255), width=3)
    
    img.save(f"{ICONS_DIR}/star.png")
    print(f"✅ {ICONS_DIR}/star.png oluşturuldu")

def create_crown_icon(size=128):
    """Taç ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color = (255, 215, 0, 255)
    
    # Taç tabanı
    points = [
        (size//6, size*2//3),
        (size//4, size//3),
        (size//2, size//2),
        (size*3//4, size//3),
        (size*5//6, size*2//3)
    ]
    draw.polygon(points, fill=color, outline=(200, 150, 0, 255), width=4)
    
    # Taç dibi
    draw.rectangle(
        [(size//6, size*2//3),
         (size*5//6, size*3//4)],
        fill=color
    )
    
    # Mücevherler (kırmızı)
    gem_color = (255, 0, 0, 255)
    for x in [size//4, size//2, size*3//4]:
        draw.ellipse(
            [(x - size//20, size//2 - size//20),
             (x + size//20, size//2 + size//20)],
            fill=gem_color
        )
    
    img.save(f"{ICONS_DIR}/crown.png")
    print(f"✅ {ICONS_DIR}/crown.png oluşturuldu")

def create_refresh_icon(size=128):
    """Yenile/Sıfırla ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color = (100, 150, 255, 255)
    
    # Dairesel ok
    # Saat yönünde ok
    draw.arc(
        [(size//6, size//6), (size*5//6, size*5//6)],
        start=45,
        end=315,
        fill=color,
        width=12
    )
    
    # Ok başları
    import math
    # Üst ok başı
    angle = math.radians(315)
    center_x, center_y = size // 2, size // 2
    radius = size // 3
    arrow_x = center_x + radius * math.cos(angle)
    arrow_y = center_y + radius * math.sin(angle)
    
    # Üçgen ok
    points = [
        (arrow_x, arrow_y),
        (arrow_x + size//8, arrow_y - size//12),
        (arrow_x + size//12, arrow_y + size//8)
    ]
    draw.polygon(points, fill=color)
    
    img.save(f"{ICONS_DIR}/refresh.png")
    print(f"✅ {ICONS_DIR}/refresh.png oluşturuldu")

def create_lock_icon(size=128):
    """Kilit ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color = (150, 150, 150, 255)
    
    # Kilit askısı (üst)
    draw.arc(
        [(size//3, size//4), (size*2//3, size*3//5)],
        start=180,
        end=0,
        fill=color,
        width=10
    )
    
    # Kilit gövdesi
    draw.rounded_rectangle(
        [(size//4, size//2), (size*3//4, size*4//5)],
        radius=8,
        fill=color
    )
    
    # Anahtar deliği
    draw.ellipse(
        [(size//2 - size//16, size*3//5 - size//16),
         (size//2 + size//16, size*3//5 + size//16)],
        fill=(50, 50, 50, 255)
    )
    draw.rectangle(
        [(size//2 - size//24, size*3//5),
         (size//2 + size//24, size*7//10)],
        fill=(50, 50, 50, 255)
    )
    
    img.save(f"{ICONS_DIR}/lock.png")
    print(f"✅ {ICONS_DIR}/lock.png oluşturuldu")

def create_check_icon(size=128):
    """Onay işareti ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color = (0, 255, 0, 255)
    
    # Onay işareti (✓)
    # Sol kısa çizgi
    draw.line(
        [(size//4, size//2), (size*2//5, size*2//3)],
        fill=color,
        width=15
    )
    # Sağ uzun çizgi
    draw.line(
        [(size*2//5, size*2//3), (size*3//4, size//3)],
        fill=color,
        width=15
    )
    
    img.save(f"{ICONS_DIR}/check.png")
    print(f"✅ {ICONS_DIR}/check.png oluşturuldu")

def create_mouse_icon(size=128):
    """Mouse ikonu oluştur"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    color = (200, 200, 200, 255)
    
    # Mouse gövdesi
    draw.rounded_rectangle(
        [(size//3, size//4), (size*2//3, size*3//4)],
        radius=15,
        outline=color,
        width=8
    )
    
    # Tekerlek
    draw.line(
        [(size//2, size//3), (size//2, size*2//5)],
        fill=color,
        width=6
    )
    
    # Tekerlek kaydırma işareti
    for i in range(-1, 2):
        y_offset = size//20 * i
        draw.line(
            [(size*2//5, size*3//5 + y_offset),
             (size*3//5, size*3//5 + y_offset)],
            fill=(100, 150, 255, 255),
            width=3
        )
    
    img.save(f"{ICONS_DIR}/mouse.png")
    print(f"✅ {ICONS_DIR}/mouse.png oluşturuldu")

def create_heart_icon(size=128):
    """Kalp ikonu oluştur (❤️)"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Kırmızı-pembe kalp rengi
    color = (255, 50, 80, 255)
    
    # Kalp şekli - iki daire ve bir üçgen birleşimi
    # Sol üst daire
    left_circle_center = (size * 3 // 8, size * 3 // 8)
    circle_radius = size // 5
    draw.ellipse(
        [(left_circle_center[0] - circle_radius, left_circle_center[1] - circle_radius),
         (left_circle_center[0] + circle_radius, left_circle_center[1] + circle_radius)],
        fill=color
    )
    
    # Sağ üst daire
    right_circle_center = (size * 5 // 8, size * 3 // 8)
    draw.ellipse(
        [(right_circle_center[0] - circle_radius, right_circle_center[1] - circle_radius),
         (right_circle_center[0] + circle_radius, right_circle_center[1] + circle_radius)],
        fill=color
    )
    
    # Alt üçgen (kalp ucu)
    triangle_points = [
        (size // 8, size // 3),  # Sol üst
        (size * 7 // 8, size // 3),  # Sağ üst
        (size // 2, size * 7 // 8)  # Alt orta (sivri uç)
    ]
    draw.polygon(triangle_points, fill=color)
    
    # Parlaklık efekti (highlight)
    highlight_color = (255, 150, 170, 200)
    draw.ellipse(
        [(size * 3 // 8 - circle_radius//3, size * 3 // 8 - circle_radius//2),
         (size * 3 // 8 + circle_radius//3, size * 3 // 8)],
        fill=highlight_color
    )
    
    img.save(f"{ICONS_DIR}/heart.png")
    print(f"✅ {ICONS_DIR}/heart.png oluşturuldu")

def create_banana_icon(size=128):
    """Muz ikonu oluştur (🍌)"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    import math
    
    # Basit kavisli muz - C şekli
    # Ana gövde noktaları
    steps = 15
    points_top = []
    points_bottom = []
    
    width = size * 0.25
    height = size * 0.7
    curve = size * 0.15
    
    for i in range(steps):
        t = i / (steps - 1)
        
        # Y ekseni boyunca
        y = size * 0.15 + t * height
        
        # X ekseni - kavis
        x_offset = math.sin(t * math.pi) * curve
        x_center = size * 0.5 - curve * 0.3
        
        # Üst kenar
        x_top = x_center + x_offset - width / 2
        points_top.append((int(x_top), int(y)))
        
        # Alt kenar
        x_bottom = x_center + x_offset + width / 2
        points_bottom.append((int(x_bottom), int(y)))
    
    # Tam şekil
    full_points = points_top + points_bottom[::-1]
    
    # Gölge
    shadow = [(x + 2, y + 2) for x, y in full_points]
    draw.polygon(shadow, fill=(180, 150, 0, 150))
    
    # Ana muz (sarı)
    draw.polygon(full_points, fill=(255, 225, 53))
    
    # Parlama şeridi
    highlight_points = []
    for i in range(2, steps - 2):
        t = i / (steps - 1)
        y = size * 0.15 + t * height
        x_offset = math.sin(t * math.pi) * curve
        x = size * 0.5 - curve * 0.3 + x_offset - width * 0.2
        highlight_points.append((int(x), int(y)))
    
    for i in range(len(highlight_points) - 1):
        draw.line([highlight_points[i], highlight_points[i+1]], 
                  fill=(255, 245, 140), width=int(width * 0.4))
    
    # Kenarlık
    draw.polygon(full_points, outline=(200, 160, 0), width=2)
    
    # Uçlar (kahverengi)
    tip_size = int(width * 0.8)
    draw.ellipse([
        (points_top[0][0] - tip_size//2, points_top[0][1] - tip_size//2),
        (points_top[0][0] + tip_size//2, points_top[0][1] + tip_size//2)
    ], fill=(101, 67, 33))
    
    draw.ellipse([
        (points_top[-1][0] - tip_size//2, points_top[-1][1] - tip_size//2),
        (points_top[-1][0] + tip_size//2, points_top[-1][1] + tip_size//2)
    ], fill=(101, 67, 33))
    
    img.save(f"{ICONS_DIR}/banana.png")
    print(f"✅ {ICONS_DIR}/banana.png oluşturuldu")

if __name__ == "__main__":
    print("Emoji ikonları oluşturuluyor...")
    create_gamepad_icon()
    create_bomb_icon()
    create_swords_icon()
    create_robot_icon()
    create_trophy_icon()
    create_music_icon()
    create_volume_icon()
    create_mute_icon()
    create_lightning_icon()
    create_picture_icon()
    create_snake_icon()
    create_guitar_icon()
    create_star_icon()
    create_crown_icon()
    create_refresh_icon()
    create_lock_icon()
    create_check_icon()
    create_mouse_icon()
    create_heart_icon()
    create_banana_icon()
    print("\n✅ Tüm ikonlar oluşturuldu!")
    print(f"Toplam boyut: ~20-50 KB")
