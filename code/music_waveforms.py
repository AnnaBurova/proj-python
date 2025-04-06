# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 15:07:53 2025

@author: SeliCat
"""
import os
import librosa
import librosa.display
import matplotlib.pyplot as plt

# Укажи здесь путь к папке с файлами
folder_path = "path/to/your/folder"

# Поддерживаемые форматы
audio_extensions = ('.mp3', '.wav')

# Проходим по всем файлам в папке
for filename in os.listdir(folder_path):
    if filename.lower().endswith(audio_extensions) and filename.startswith("_"):
        file_path = os.path.join(folder_path, filename)
        print(f"Обрабатываю: {filename}")

        # Загружаем аудио
        y, sr = librosa.load(file_path, sr=None)

        # Создаём график
        plt.figure(figsize=(10, 4))
        librosa.display.waveshow(y, sr=sr)
        plt.title(f"Waveform: {filename}")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.ylim(-1.5, 1.5)
        plt.tight_layout()

        # Сохраняем рядом с оригинальным файлом
        output_filename = os.path.splitext(filename)[0] + "_waveform.png"
        output_path = os.path.join(folder_path, output_filename)
        plt.savefig(output_path)
        plt.close()

        print(f"Сохранено: {output_filename}")
