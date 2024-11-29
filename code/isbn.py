# -*- coding: utf-8 -*-
"""
Created on Nov 2024

@author: KoreAnna
"""

import requests
import re
import pdfplumber
import os

folder_ = "C:/Data/"
first_pages = 10
last_pages = 0
all_pages = False


def extract_isbn_from_pdf(file_path):
    # Регулярное выражение для поиска ISBN-13 или ISBN-10
    isbn_pattern1 = r"\b(?:ISBN(?:-1[03])?:?\s*)?(\d{9}[\dX]|\d{13})\b"
    isbn_pattern2 = r"\b(?:ISBN(?:[-\s]?(?:1[03])?)?:?\s*)?(97[89]-\d{1,5}-\d{1,7}-\d{1,7}-\d)\b"
    isbn_pattern3 = r"\b97[89]-\d{1,5}-\d{1,7}-\d{1,7}-?\d\b"
    isbn_pattern4 = r"\b97[89]-\d{10}\b"

    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            i = 0
            for page in pdf.pages:
                i += 1
                if not all_pages:
                    if i > first_pages:
                        if i < (len(pdf.pages) - last_pages):
                            continue
                text += page.extract_text()

            isbns1 = re.findall(isbn_pattern1, text)
            isbns2 = re.findall(isbn_pattern2, text)
            isbns3 = re.findall(isbn_pattern3, text)
            isbns4 = re.findall(isbn_pattern4, text)
            isbns1 = [isbn.replace("-", "") for isbn in isbns1]
            isbns2 = [isbn.replace("-", "") for isbn in isbns2]
            isbns3 = [isbn.replace("-", "") for isbn in isbns3]
            isbns4 = [isbn.replace("-", "") for isbn in isbns4]
            isbn = list(set(isbns1 + isbns2 + isbns3 + isbns4))
            print(isbn)
            return isbn
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
    if file_name.endswith(".pdf") and file_name.startswith("_"):
        print()
        print("=======================================================")
        print("Open:", folder_ + file_name)
        print("=======================================================")
        input(">>> ")
        isbn_list = extract_isbn_from_pdf(folder_ + file_name)
        if isbn_list:
            print("Найденные ISBN:")
            i = 0
            for isbn in isbn_list:
                i += 1
                print("-------------------------------------------------------")
                print(i, "isbn: ", isbn)
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
                            book_v = book_v.replace(", Second Edition", "")
                            book_v = book_v.replace(", Third Edition", "")
                            book_v = book_v.replace("The ", "")
                            book_v = book_v.replace(" the ", " ")
                            book_v = book_v.replace(" & ", " and ")
                            book_v = book_v.replace(".js", "_JS")
                            book_v = book_v.replace(
                                "Artificial Intelligence", "AI")
                            book_v = prefix + book_v
                        print(book_k, ":", book_v)
                else:
                    print("+++ no book info +++")
        else:
            print("ISBN не найдены.")
