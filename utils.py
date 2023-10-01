from docx import Document
import fitz  # PyMuPDF
import os

def write_string_to_word(text, filename):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)

def read_docx(file):
    doc = Document(file)
    text = ' '.join([paragraph.text for paragraph in doc.paragraphs])
    return text

def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = ''
    for page_number in range(doc.page_count):
        page = doc[page_number]
        text += page.get_text()

    return text
