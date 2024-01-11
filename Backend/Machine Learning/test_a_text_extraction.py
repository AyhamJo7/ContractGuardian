import unittest
import os
from dotenv import load_dotenv
from a_text_extraction import PDFTextExtractor

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

class TestPDFTextExtractor(unittest.TestCase):
    def setUp(self):
        self.pdf_directory = os.getenv('PDF_DIRECTORY') 
        self.extracted_text_directory = os.getenv('EXTRACTED_TEXT_DIRECTORY')

        self.extractor = PDFTextExtractor(self.pdf_directory, self.extracted_text_directory)
        self.test_pdf_path = os.getenv('TEST_PDF_PATH')  

    def test_extract_text_from_valid_pdf(self):
        text = self.extractor.extract_text_from_pdf(self.test_pdf_path)
        self.assertNotEqual(text, '', "Text should not be empty for a valid PDF")

if __name__ == '__main__':
    unittest.main()

#Ergebnisse:
"""
.
----------------------------------------------------------------------
Ran 1 test in 4.650s

OK 
"""
