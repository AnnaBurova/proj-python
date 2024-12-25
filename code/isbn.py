# -*- coding: utf-8 -*-
"""
Created on Nov 2024

@author: KoreAnna
"""

import os
import requests
import re
import pdfplumber

folder_ = "C:/Data/"
prefix = ""
first_pages = 25
last_pages = 0
all_pages = False


def extract_isbn_from_pdf(file_path):
    isbn_pattern = r"""
        # WORD START
        \b
        # "ISBN-10", "ISBN-13", "ISBN" (opt)
        (?:ISBN(?:-1[03])?:?\s*)?
        # ISBN-13
        (97[89][- ]*\d{1,5}[- ]*\d{1,7}[- ]*\d{1,7}[- ]*[\dX]
        # ISBN-10 (or)
        |\d{9}[\dX])
        # Type of print (opt)
        (?:\s*\([a-z]+\))?
        \b
        # WORD END
    """

    isbn_compile = re.compile(isbn_pattern, re.VERBOSE)

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

            isbns = re.findall(isbn_compile, text)
            isbns = [isbn.replace("-", "") for isbn in isbns]
            isbns = [isbn.replace(" ", "") for isbn in isbns]
            isbns = list(set(isbns))
            print("isbns:", isbns)

            return isbns
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
        print("Wait...")
        print("-------------------------------------------------------")
        isbn_list = extract_isbn_from_pdf(folder_ + file_name)
        if isbn_list:
            print("Found ISBN:")
            i = 0
            for isbn in isbn_list:
                i += 1
                print("-------------------------------------------------------")
                print(i, "isbn: ", isbn)
                valid = validate_isbn(isbn)
                print(f"ISBN {isbn} is valid? {valid}")
                print()
                # isbn = "9780134190440"

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
                                book_v = book_v.replace("®", "")
                                book_v = book_v.replace("!", "")
                                book_v = book_v.replace("The ", "")
                                book_v = book_v.replace(" the ", " ")
                                book_v = book_v.replace(" / ", " and ")
                                book_v = book_v.replace(" & ", " and ")
                                book_v = book_v.replace(", and ", " and ")
                                book_v = book_v.replace(".js", "_JS")
                                book_v = book_v.replace("C#", "C-Sharp")
                                book_v = book_v.replace("C++", "CPP")
                                book_v = book_v.replace("JQuery", "jQuery")
                                book_v = book_v.replace(" Office", " Microsoft Office")
                                book_v = book_v.replace(" Access", " Microsoft Access")
                                book_v = book_v.replace(" Excel", " Microsoft Excel")
                                book_v = book_v.replace(" Microsoft Microsoft", " Microsoft")
                                book_v = book_v.replace(" Ai ", " AI ")
                                book_v = book_v.replace(
                                    "Artificial Intelligence", "AI")
                                book_v = prefix + book_v
                            print(book_k, ":", book_v)
                    else:
                        print("+++ no book info +++")
        else:
            print("ISBN not found.")
