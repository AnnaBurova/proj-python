# -*- coding: utf-8 -*-
"""
Created on Nov 2024

@author: KoreAnna
"""

import os
import requests
import re
import pdfplumber
import sys

line_fatty = "================================================================================"
line_slimm = "--------------------------------------------------------------------------------"
folder = "C:/Data/"
prefix = ""
first_pages = 25
last_pages = 0
all_pages = False
self_controle = False
name_start = "_"
name_end = ".pdf"
gather_info = []


def save_data_into_log_file(text):
    print(text)

    # Replace CRLF (\r\n) to LF (\n)
    text = text.replace("\r\n", "\n")

    with open("pdf_result.txt", "a", encoding="utf-8", newline="\n") as outfile:
        outfile.write(text)
        outfile.write("\n")


def extract_isbn_from_pdf(file_path):
    # \b - WORD boundary
    # (?:TEXT_OR_PATTERN)? - optional group
    # _? - single optional symbol _
    # \s* - 0 or more empty symbols
    # \d - any digit
    isbn_pattern = r"""
        \b
        (?:ISBN(?:-13)?:?\s*)?
        97[89]
        [-\s]?
        \d{1,5}
        [-\s]?
        \d{1,7}
        [-\s]?
        \d{1,7}
        [-\s]?
        \d
        # [\dX]
        \b
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
            isbns = [isbn.replace("ISBN13", "") for isbn in isbns]
            isbns = [isbn.replace("ISBN", "") for isbn in isbns]
            isbns = [isbn.replace(":", "") for isbn in isbns]
            isbns = [isbn.replace("\n", "") for isbn in isbns]
            isbns = list(set(isbns))

            if isbns == []:
                with open("pdf_content.txt", "w", encoding="utf-8", newline="\n") as pdf_content:
                    pdf_content.write(text)
                    pdf_content.write("\n")

            return isbns

    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        return []


def validate_isbn(isbn):
    # Validation ISBN-13
    if len(isbn) == 13 and isbn.isdigit():
        total = sum((3 if i % 2 else 1) * int(digit) for i, digit in enumerate(isbn))
        return total % 10 == 0

    # Validation ISBN-10
    elif len(isbn) == 10:
        total = sum((10 - i) * (10 if digit == 'X' else int(digit)) for i, digit in enumerate(isbn))
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
                if info_k == "description":
                    info_v = "== description =="
                result[info_k] = info_v
            return result

    return None


def print_book_info(book_info):
    print()
    for book_k, book_v in book_info.items():
        if book_k == "description":
            continue
        if book_k == "imageLinks":
            continue
        if book_k == "previewLink":
            continue
        if book_k == "infoLink":
            continue
        if book_k == "canonicalVolumeLink":
            continue

        if book_k == "industryIdentifiers":
            isbn_13 = next((item['identifier'] for item in book_v
                            if item['type'] == 'ISBN_13'), None)
            book_v = isbn_13

        if book_k == "publishedDate":
            gather_info.append(book_v)

        if book_k == "title":
            book_v = book_v.replace("The ", "")
            book_v = book_v.replace(" the ", " ")
            book_v = book_v.replace("®", "")
            book_v = book_v.replace("!", "")
            book_v = book_v.replace(":", ".")
            book_v = book_v.replace(" / ", " or ")
            book_v = book_v.replace(" & ", " and ")
            book_v = book_v.replace(", and ", " and ")
            book_v = book_v.replace(" .NET", " dotNET")
            book_v = book_v.replace("#", "-Sharp")
            book_v = book_v.replace("C++", "CPP")
            book_v = book_v.replace(".js", "_JS")
            book_v = book_v.replace("Internet of Things", "IoT")
            book_v = book_v.replace("Artificial Intelligence", "AI")
            book_v = book_v.replace("Object-Oriented Programming", "OOP")
            book_v = book_v.replace("Search Engine Optimization", "SEO")
            book_v = book_v.replace(" Office", " Microsoft Office")
            book_v = book_v.replace(" Access", " Microsoft Access")
            book_v = book_v.replace(" Excel", " Microsoft Excel")
            book_v = book_v.replace("Microsoft Microsoft", "Microsoft")
            book_v = book_v.replace("Python 3", "Python")
            book_v = book_v.replace("  ", " ")

            book_v = book_v.replace("JQuery", "jQuery")
            book_v = book_v.replace("Hands-on", "Hands-On")
            book_v = book_v.replace("Typescript", "TypeScript")
            book_v = book_v.replace("Fastapi", "FastAPI")
            book_v = book_v.replace("Chatgpt", "ChatGPT")
            book_v = book_v.replace("Grpc", "gRPC")
            book_v = book_v.replace("Arcgis", "ArcGIS")
            book_v = book_v.replace("Aws", "AWS")
            book_v = book_v.replace(" Ai ", " AI ")

            book_v = prefix + book_v
            gather_info.append(book_v)

        print(book_k, ":", book_v)


def work_with_isbn_list(isbn_list):
    i = 0
    for isbn in isbn_list:
        i += 1
        print(line_slimm)
        print(i, "isbn: ", isbn)

        valid = validate_isbn(isbn)
        print(f"ISBN {isbn} is valid? {valid}")

        if not valid:
            isbn_list.remove(isbn)
            continue

        if valid:
            try:
                book_info = get_book_info(isbn)
            except Exception as e:
                print(f"Connection aborted: {e}")
                break

            if book_info:
                print_book_info(book_info)
            else:
                print(":( no book info :(")

    return isbn_list


# Iterate through each PDF file in the folder
for file_name in os.listdir(folder):
    if file_name.startswith(name_start) and file_name.endswith(name_end):
        gather_info = []
        print()
        print(line_fatty)
        print("Open:", folder + file_name)
        print(line_fatty)
        if self_controle:
            try:
                input(">>> ")
            except KeyboardInterrupt as e:
                print(e)
                sys.exit()
        print("Wait...")
        print(line_slimm)
        isbn_list = extract_isbn_from_pdf(folder + file_name)

        if isbn_list:
            print("Found ISBN:")
            print(isbn_list)
            isbn_list = work_with_isbn_list(isbn_list)
        else:
            print("ISBN not found.")

        save_data_into_log_file(line_slimm)
        save_data_into_log_file("file_name: "+file_name)
        save_data_into_log_file("isbn_list: "+str(isbn_list))
        for book_name in gather_info:
            save_data_into_log_file(book_name)
