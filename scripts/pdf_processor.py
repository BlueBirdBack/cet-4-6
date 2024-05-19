"""
This script pulls out the CET4 and CET6 words from the PDF file.
"""

import os
from pypdf import PdfReader
from pypdf.errors import DependencyError


def is_unicode_digit(s):
    """Return True if any character in the string is a digit, False otherwise"""
    return any(char.isdigit() for char in s)


current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
pdf_dir = os.path.join(parent_dir, "pdf")


def write_cet_4_words_to_file(words_to_write):
    """Write CET 4 words to a file"""
    with open(os.path.join(parent_dir, "cet_4_words.txt"), "w", encoding="utf-8") as f:
        for word in words_to_write:
            f.write(word + "\n")


def write_cet_6_words_to_file(words_to_write):
    """Write CET 6 words to a file"""
    with open(os.path.join(parent_dir, "cet_6_words.txt"), "w", encoding="utf-8") as f:
        for word in words_to_write:
            f.write(word + "\n")


pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
if pdf_files:
    pdf_file = pdf_files[0]
    cet_4_words = []
    cet_6_words = []

    try:
        reader = PdfReader(os.path.join(pdf_dir, pdf_file))

        for page_num in range(21, 150):
            try:
                page = reader.pages[
                    page_num - 1
                ]  # subtract 1 because page numbers start at 0
                text = page.extract_text()
                for line in text.split("\n"):
                    words = line.split()
                    # Filter out lines that contain digits before processing them further
                    filtered_words = [
                        word.replace("表", "")
                        for word in words
                        if not is_unicode_digit(word) and word != "词"
                    ]
                    # print("f:", filtered_words)

                    if filtered_words and filtered_words[0].startswith("★"):
                        cet_6_words.extend(
                            [
                                filtered_words[0].replace("★", ""),
                            ]
                            + filtered_words[1:]
                        )
                    # Skip the first word which is '★...'
                    else:
                        cet_4_words.extend(filtered_words)
            except IndexError:
                print(f"Page {page_num} does not exist in the PDF file.")
            except DependencyError as e:
                print(
                    f"Dependency error: {e}. Ensure 'cryptography' library is installed."
                )
            except Exception as e:  # pylint: disable=broad-exception-caught
                print(f"An error occurred: {e}")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"An error occurred: {e}")

    print(len(cet_4_words))
    print(cet_4_words)
    print(len(cet_6_words) + len(cet_4_words))
    print(cet_6_words)

    write_cet_4_words_to_file(cet_4_words)
    write_cet_6_words_to_file(cet_6_words)
else:
    print(f"No PDF files found in the directory '{pdf_dir}'")
