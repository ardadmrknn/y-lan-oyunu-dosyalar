"""
Windows Executable Oluşturma Scripti
PyInstaller ile yılan oyununu .exe haline getirir
"""

import os
import subprocess
import sys

def create_exe():
    """PyInstaller ile executable oluştur"""
    try:
        # PyInstaller komutu
        cmd = [
            "pyinstaller",
            "--onefile",  # Tek dosya
            "--windowed",  # Konsol penceresi gösterme
            "--name=Yilan_Oyunu",  # Executable adı
            "--icon=icons/snake.ico",  # İkon (varsa)
            "--add-data=backgrounds;backgrounds",  # Arkaplan resimleri
            "--add-data=apple_emojis;apple_emojis",  # Emoji resimleri
            "--add-data=icons;icons",  # İkonlar
            "--add-data=music;music",  # Müzikler
            "--add-data=basarimlar.json;.",  # Başarım dosyası
            "--add-data=istatistikler.json;.",  # İstatistik dosyası
            "--add-data=oyun_ayarlari.json;.",  # Ayarlar dosyası
            "main.py"  # Ana dosya
        ]

        print("Executable oluşturuluyor...")
        subprocess.run(cmd, check=True)
        print("✅ Executable başarıyla oluşturuldu: dist/Yilan_Oyunu.exe")

    except subprocess.CalledProcessError as e:
        print(f"❌ Hata: {e}")
        print("PyInstaller yüklü değilse: pip install pyinstaller")
    except FileNotFoundError:
        print("❌ PyInstaller bulunamadı. Önce yükleyin: pip install pyinstaller")

if __name__ == "__main__":
    create_exe()