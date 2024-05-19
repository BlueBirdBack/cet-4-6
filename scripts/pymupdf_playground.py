import os
import fitz  # PyMuPDF

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
pdf_dir = os.path.join(parent_dir, "pdf")

pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
if pdf_files:
    pdf_file = pdf_files[0]
    doc = fitz.open(os.path.join(pdf_dir, pdf_file))
    print(doc)
    page = doc.load_page(21)
    text = page.get_text()
    print(text)
else:
    print(f"No PDF files found in the directory '{pdf_dir}'")
