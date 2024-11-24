# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 12:27:16 2024

@author: KoreAnna
"""

import requests
import re
import pdfplumber
import os

folder_ = "C:/Data/"


def extract_isbn_from_pdf(file_path):
    print("=======================================================")
    print("Open:", file_path)
    # Регулярное выражение для поиска ISBN-13 или ISBN-10
    isbn_pattern1 = r"\b(?:ISBN(?:-1[03])?:?\s*)?(\d{9}[\dX]|\d{13})\b"
    isbn_pattern2 = r"\b97[89]-\d{1,5}-\d{1,7}-\d{1,6}-\d\b"

    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            i = 0
            for page in pdf.pages:
                i += 1
                if i > 10:
                    if i < (len(pdf.pages) - 10):
                        continue
                text += page.extract_text()

            isbns1 = re.findall(isbn_pattern1, text)
            isbns2 = re.findall(isbn_pattern2, text)
            return isbns1 + isbns2
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        return []


def validate_isbn(isbn):
    # Проверка ISBN-13
    if len(isbn) == 13 and isbn.isdigit():
        total = sum((3 if i % 2 else 1) * int(digit) for i,
                    digit in enumerate(isbn))
        return total % 10 == 0
    # Проверка ISBN-10
    elif len(isbn) == 10:
        total = sum((10 - i) * (10 if digit == 'X' else int(digit)) for i,
                    digit in enumerate(isbn))
        return total % 11 == 0
    return False


def get_book_info(isbn):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            book = data["items"][0]["volumeInfo"]
            result = {}
            for info_k, info_v in book.items():
                if isinstance(info_v, str):
                    if info_k == "description":
                        info_v = "== description =="
                    result[info_k] = info_v
                elif isinstance(info_v, int):
                    result[info_k] = info_v
                elif isinstance(info_v, bool):
                    result[info_k] = info_v
                elif isinstance(info_v, list):
                    result[info_k] = info_v
            return result
    return None


# Iterate through each PDF file in the folder
for file_name in os.listdir(folder_):
    if file_name.endswith(".pdf"):
        isbn_list = extract_isbn_from_pdf(folder_ + file_name)
        if isbn_list:
            print("Найденные ISBN:")
            i = 0
            for isbn in isbn_list:
                i += 1
                print("-------------------------------------------------------")
                print(i, "isbn: ", isbn)
                isbn = isbn.replace("-", "")
                valid = validate_isbn(isbn)
                print(f"ISBN {isbn} валиден? {valid}")
                print()
                # isbn = "9780134190440"  # Пример ISBN

                book_info = False
                if valid:
                    book_info = get_book_info(isbn)

                if book_info:
                    for book_k, book_v in book_info.items():
                        if book_k == "previewLink":
                            continue
                        if book_k == "infoLink":
                            continue
                        if book_k == "canonicalVolumeLink":
                            continue
                        if book_k == "description":
                            continue
                        if book_k == "title":
                            print(book_k, "::", book_v)
                            book_v = book_v.replace("The ", "")
                            book_v = book_v.replace(" the ", " ")
                        print(book_k, ":", book_v)
                else:
                    print("+++ no book info +++")
        else:
            print("ISBN не найдены.")
        print()
        print()
        input(">>> ")
