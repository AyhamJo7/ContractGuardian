import fitz  # PyMuPDF
import os
import pytesseract
from pdf2image import convert_from_path

class PDFTextExtractor:

    def __init__(self, pdf_directory, output_directory):
        self.pdf_directory = pdf_directory
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def extract_text_from_page(self, page):
        try:
            text = page.get_text()
            return text if text.strip() != "" else None
        except Exception as e:
            print(f"Error extracting text from page: {e}")
            return None

    def extract_text_with_pytesseract(self, pdf_path, page_number):
        try:
            images = convert_from_path(pdf_path, first_page=page_number, last_page=page_number)
            text = pytesseract.image_to_string(images[0])
            return text
        except Exception as e:
            print(f"Error with pytesseract: {e}")
            return ""

    def extract_text_from_pdf(self, pdf_path):
        """
        Extracts text from a given PDF file. Uses fitz to extract text from each page,
        and falls back to pytesseract if text extraction fails.
        """
        full_text = ''
        with fitz.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                text = self.extract_text_from_page(page)
                if text is None:
                    text = self.extract_text_with_pytesseract(pdf_path, page_number)
                full_text += text + "\n" if text else "\n"
        return full_text

    def process_all_pdfs(self):
        for filename in os.listdir(self.pdf_directory):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_directory, filename)
                full_text = self.extract_text_from_pdf(pdf_path)

                output_file_path = os.path.join(self.output_directory, filename.replace('.pdf', '.txt'))
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(full_text)

# Example usage
pdf_directory = 'C:/Users/ayham/Desktop/Projekt/ContractGuardian/Data/PDFs'
output_directory = 'C:/Users/ayham/Desktop/Projekt/ContractGuardian/Data/text_extraction_results'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  
extractor = PDFTextExtractor(pdf_directory, output_directory)
extractor.process_all_pdfs()
