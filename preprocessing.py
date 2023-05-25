import io
import os

import requests
import tiktoken
from PyPDF2 import PdfReader


def extract_pdf_by_url(url):
    """
    Loads PDF's text in memory by creating a bytes object and populating it with the text.
    """
    pdf_bytes = requests.get(url).content
    temp = io.BytesIO(pdf_bytes)
    temp.seek(0, os.SEEK_END)

    pdf = PdfReader(temp)

    pdf_text = ""
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        pdf_text += page.extract_text()

    return pdf_text


def break_up_text_to_chunks(
    text, 
    chunk_size=4000, 
    overlap=200,
):
    encoding = tiktoken.get_encoding("gpt2")

    tokens = encoding.encode(text)
    num_tokens = len(tokens)
    
    chunks = []
    for i in range(0, num_tokens, chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        chunks.append(chunk)
    chunks = [encoding.decode(chunk) for chunk in chunks]
    
    return chunks
