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
self_controle = False
name_start = "_"
name_end = ".pdf"


def extract_isbn_from_pdf(file_path):
    isbn_pattern = r"""
        # WORD START
        \b
        # "ISBN-10", "ISBN-13", "ISBN" (opt)
        (?:ISBN(?:-1[03])?:?\s*)?
        # (?:ISBN(?:-1[03])?(?:\s*\([a-zA-Z]+\))?:?\s*)?
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


def save_data_into_file(text):
    """ Save data into file """

    file_name = "result.txt"

    # Replace CRLF (\r\n) to LF (\n)
    text = text.replace("\r\n", "\n")

    with open(file_name, "a", encoding="utf-8", newline="\n") as outfile:
        outfile.write(text)
        outfile.write("\n")


# Iterate through each PDF file in the folder
for file_name in os.listdir(folder_):
    if file_name.endswith(name_end) and file_name.startswith(name_start):
        print()
        print("=======================================================")
        print("Open:", folder_ + file_name)
        print("=======================================================")
        if self_controle:
            input(">>> ")
        print("Wait...")
        print("-------------------------------------------------------")
        isbn_list = extract_isbn_from_pdf(folder_ + file_name)
        gather_names = []
        if isbn_list:
            print("Found ISBN:")
            i = 0
            for isbn in isbn_list:
                i += 1
                print("-------------------------------------------------------")
                print(i, "isbn: ", isbn)
                valid = validate_isbn(isbn)
                print(f"ISBN {isbn} is valid? {valid}")
                if not valid:
                    isbn_list.remove(isbn)
                print()
                # isbn = "9780134190440"

                book_info = False
                if valid:
                    try:
                        book_info = get_book_info(isbn)
                    except:
                        print("Connection aborted.")
                        break

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
                            if book_k == "publishedDate":
                                gather_names.append(book_v)
                            if book_k == "title":
                                print(book_k, "::", book_v)
                                book_v = book_v.replace(", Second Edition", "")
                                book_v = book_v.replace(", Third Edition", "")
                                book_v = book_v.replace(" - Second Edition", "")
                                book_v = book_v.replace(" - Third Edition", "")
                                book_v = book_v.replace(" - Fourth Edition", "")
                                book_v = book_v.replace("®", "")
                                book_v = book_v.replace("!", "")
                                book_v = book_v.replace(":", "")
                                book_v = book_v.replace("The ", "")
                                book_v = book_v.replace(" the ", " ")
                                book_v = book_v.replace(" / ", " and ")
                                book_v = book_v.replace(" & ", " and ")
                                book_v = book_v.replace(", and ", " and ")
                                book_v = book_v.replace(".js", "_JS")
                                book_v = book_v.replace(" .NET", " dotNET")
                                book_v = book_v.replace("#", "-Sharp")
                                book_v = book_v.replace("C++", "CPP")
                                book_v = book_v.replace("JQuery", "jQuery")
                                book_v = book_v.replace("Internet of Things", "IoT")
                                book_v = book_v.replace(" Office", " Microsoft Office")
                                book_v = book_v.replace(" Access", " Microsoft Access")
                                book_v = book_v.replace(" Excel", " Microsoft Excel")
                                book_v = book_v.replace(" Microsoft Microsoft", " Microsoft")
                                book_v = book_v.replace("Hands-on", "Hands-On")
                                book_v = book_v.replace(" Ai ", " AI ")
                                book_v = book_v.replace("Artificial Intelligence", "AI")
                                book_v = book_v.replace("Object-Oriented Programming", "OOP")
                                book_v = book_v.replace("  ", " ")
                                book_v = prefix + book_v
                                gather_names.append(book_v)
                            print(book_k, ":", book_v)
                    else:
                        print("+++ no book info +++")
        else:
            print("ISBN not found.")

        print("-------------------------------------------------------")
        save_data_into_file("-------------------------------------------------------")
        print("file_name:", file_name)
        save_data_into_file("file_name: "+file_name)
        save_data_into_file(str(isbn_list))
        for book_name in gather_names:
            print(book_name)
            save_data_into_file(book_name)
