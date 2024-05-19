import os
from pypdf import PdfReader
from pypdf.errors import DependencyError

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
pdf_dir = os.path.join(parent_dir, "pdf")

pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
if pdf_files:
    pdf_file = pdf_files[0]
    try:
        reader = PdfReader(os.path.join(pdf_dir, pdf_file))
        print(reader)
        page = reader.pages[19]
        text = page.extract_text()
        print(text)
    except IndexError:
        print(f"The PDF file '{pdf_file}' does not have 22 pages.")
    except DependencyError as e:
        print(f"Dependency error: {e}. Ensure 'cryptography' library is installed.")
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"An error occurred: {e}")
else:
    print(f"No PDF files found in the directory '{pdf_dir}'")
