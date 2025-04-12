# -*- coding: utf-8 -*-
"""
Created on 12 Apr 2025

@author: KoreAnna
"""

from PIL import Image, ImageDraw, ImageFont
import random

# Путь к шрифту Pangolin
# FONT_PATH = "SofiaSans.ttf"
FONT_PATH = "SourceSans3.ttf"

# Размеры
WIDTH, HEIGHT = 1200, 675
MARGIN = 40

# Сайт
WEBSITE = "yourwebsite.com"


# Функция для генерации не-черно-бело-серого цвета
def random_color():
    while True:
        r = random.randint(50, 205)
        g = random.randint(50, 205)
        b = random.randint(50, 205)
        if abs(r - g) > 15 or abs(g - b) > 15 or abs(b - r) > 15:
            return (r, g, b)


def create_image(text, output_path="output.png"):
    # Создаём изображение
    background_color = random_color()
    img = Image.new("RGB", (WIDTH, HEIGHT), color=background_color)
    draw = ImageDraw.Draw(img)

    # Загружаем шрифт
    font_size = 60
    font = ImageFont.truetype(FONT_PATH, font_size)
    website_font = ImageFont.truetype(FONT_PATH, 28)

    # Центрируем основной текст
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_position = ((WIDTH - text_width) // 2, (HEIGHT - text_height) // 2)

    # Пишем текст
    draw.text(text_position, text, font=font, fill="white")

    # Сайт внизу справа
    site_bbox = draw.textbbox((0, 0), WEBSITE, font=website_font)
    site_width = site_bbox[2] - site_bbox[0]
    site_height = site_bbox[3] - site_bbox[1]
    site_position = (WIDTH - site_width - MARGIN, HEIGHT - site_height - MARGIN)

    draw.text(site_position, WEBSITE, font=website_font, fill=(180, 180, 180))

    # Сохраняем
    img.save(output_path)
    print(f"Изображение сохранено как {output_path}")


text = """
"""

# Пример использования
create_image(text)
