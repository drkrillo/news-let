from PyPDF2 import PdfReader
import io
import os
import requests


def extract_pdf_by_url(url):
    """
    Loads PDF's text in memory by creating a bytes object and populating it with the text.
    """
    pdf_bytes = requests.get(url).content
    temp = io.BytesIO(pdf_bytes)
    temp.seek(0, os.SEEK_END)
    pdf = PdfReader(temp)
    pdf_text = ""
    # For each page we extract the text
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        pdf_text += page.extract_text()
    return pdf_text
