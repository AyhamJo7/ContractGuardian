import fitz  # PyMuPDF
import os
import pytesseract
from pdf2image import convert_from_path
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

class PDFTextExtractor:
    # Konstruktor: Initialisiert die Pfade für PDF-Verzeichnis und Ausgabe-Verzeichnis
    def __init__(self, pdf_directory, extracted_text_directory):
        self.pdf_directory = pdf_directory
        self.extracted_text_directory = extracted_text_directory
        os.makedirs(self.extracted_text_directory, exist_ok=True)

    #pytesseract on HEROKU
    pytesseract.pytesseract.tesseract_cmd = "/app/.apt/usr/bin/tesseract"

    # Text aus einer einzelnen PDF-Seite extrahieren
    def extract_text_from_page(self, page):
        try:
            text = page.get_text()
            return text if text.strip() != "" else None
        except Exception as e:
            logging.error(f"Fehler beim Extrahieren des Textes von der Seite: {e}", exc_info=True)
            return None

    # Text mit PyTesseract extrahieren, falls notwendig
    def extract_text_with_pytesseract(self, pdf_path, page_number):
        try:
            images = convert_from_path(pdf_path, first_page=page_number, last_page=page_number)
            text = pytesseract.image_to_string(images[0])
            return text
        except Exception as e:
            logging.error(f"Fehler mit pytesseract: {e}", exc_info=True)
            return ""

    # Text aus der gesamten PDF extrahieren
    def extract_text_from_pdf(self, pdf_path):
        full_text = ''
        with fitz.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                text = self.extract_text_from_page(page)
                if text is None:
                    text = self.extract_text_with_pytesseract(pdf_path, page_number)
                full_text += text + "\n" if text else "\n"
        return full_text

    # Verarbeitet alle PDFs im angegebenen Verzeichnis
    def process_all_pdfs(self):
        for filename in os.listdir(self.pdf_directory):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_directory, filename)
                full_text = self.extract_text_from_pdf(pdf_path)

                output_file_path = os.path.join(self.extracted_text_directory, filename.replace('.pdf', '.txt'))
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(full_text)
                    
""" # Beispielhafte Verwendung
pdf_directory = os.getenv('PDF_DIRECTORY', 'default/path/to/PDFs')
extracted_text_directory = os.getenv('EXTRACTED_TEXT_DIRECTORY', 'default/path/to/extracted_text')
pytesseract.pytesseract.tesseract_cmd = os.getenv('TESSERACT_CMD', 'default/path/to/tesseract')

extractor = PDFTextExtractor(pdf_directory, extracted_text_directory)
extractor.process_all_pdfs()
 """