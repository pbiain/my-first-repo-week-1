import re
import requests
from bs4 import BeautifulSoup

def extract_from_url(url):
    # ... (keep your existing URL extraction code) ...
    return text

def extract_from_pdf(file_path): # Ensure this is DEFINED here
    """Extract text content from a PDF file."""
    try:
        import PyPDF2
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting from PDF: {str(e)}"

def process_input(data, file_obj=None): # Updated to accept two arguments
    if file_obj is not None:
        # This is where the error was happening
        return extract_from_pdf(file_obj.name) 
    
    if data and (data.startswith('http://') or data.startswith('https://')):
        return extract_from_url(data)
    
    return data