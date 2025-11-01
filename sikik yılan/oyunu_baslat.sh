#!/bin/bash

# Yılan Oyunu Başlatıcı
# Oyunu çalıştırmak için bu dosyaya çift tıklayın

# Renk kodları
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

clear
echo -e "${GREEN}================================${NC}"
echo -e "${BLUE}   🐍 YILAN OYUNU BAŞLATIYOR 🐍${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# Oyun dizinine git
cd "$(dirname "$0")"

# Python versiyonunu kontrol et
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo -e "${GREEN}✓${NC} Python3 bulundu"
else
    echo -e "${RED}✗${NC} Python3 bulunamadı!"
    echo "Lütfen Python3'ü yükleyin: https://www.python.org/downloads/"
    read -p "Devam etmek için Enter'a basın..."
    exit 1
fi

# Pygame kontrolü
echo -n "Pygame kontrol ediliyor... "
if $PYTHON_CMD -c "import pygame" 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo ""
    echo -e "${RED}Pygame yüklü değil!${NC}"
    echo -n "Pygame'i şimdi yüklemek ister misiniz? (e/h): "
    read -r answer
    if [ "$answer" = "e" ] || [ "$answer" = "E" ]; then
        echo "Pygame yükleniyor..."
        $PYTHON_CMD -m pip install pygame
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓${NC} Pygame başarıyla yüklendi!"
        else
            echo -e "${RED}✗${NC} Pygame yüklenemedi!"
            read -p "Devam etmek için Enter'a basın..."
            exit 1
        fi
    else
        echo "Oyun başlatılamadı. Pygame gereklidir."
        read -p "Devam etmek için Enter'a basın..."
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}Oyun başlatılıyor...${NC}"
echo ""

# Eski oyun processleri varsa kapat
pkill -f "python3 main.py" 2>/dev/null

# Oyunu başlat
$PYTHON_CMD main.py

# Oyun kapandığında
echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${BLUE}   Oyun kapatıldı. Hoşça kal! 👋${NC}"
echo -e "${GREEN}================================${NC}"
sleep 2
