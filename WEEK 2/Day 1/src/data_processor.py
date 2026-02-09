"""Data processor module for podcast generation."""
import re
import requests
from bs4 import BeautifulSoup

def extract_from_url(url):
    """Extract text content from a URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        return f"Error extracting from URL: {str(e)}"

def extract_from_pdf(file_path):
    """Extract text content from a PDF file."""
    try:
        import PyPDF2
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except ImportError:
        return "PDF library not installed. Install with: pip install PyPDF2"
    except Exception as e:
        return f"Error extracting from PDF: {str(e)}"

def process_input(data):
    """Process input data for podcast generation.
    
    Args:
        data: Input text, URL, or file path to process
        
    Returns:
        Cleaned and processed text
    """
    # Check if it's a URL
    if data.startswith('http://') or data.startswith('https://'):
        data = extract_from_url(data)
    
    # Remove extra whitespace and newlines
    cleaned = re.sub(r'\s+', ' ', data).strip()
    
    # Remove special characters but keep punctuation
    cleaned = re.sub(r'[^a-zA-Z0-9\s.,!?-]', '', cleaned)
    
    # Remove excessive punctuation
    cleaned = re.sub(r'[.!?]{2,}', '.', cleaned)
    
    return cleaned
