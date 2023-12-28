import sys
from PyPDF2 import PdfReader
import os

class PDFTextExtractor:
    def __init__(self, pdf_directory, output_directory):
        # Initialize with the provided directories
        self.pdf_directory = pdf_directory
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def extract_text_from_pdf(self, pdf_path):
        # Extract text from PDF using PyPDF2
        with open(pdf_path, 'rb') as file:
            pdf = PdfReader(file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text

    def process_all_pdfs(self):
        # Process all PDF files in the input directory and save extracted text in the output directory
        for filename in os.listdir(self.pdf_directory):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_directory, filename)
                text = self.extract_text_from_pdf(pdf_path)
                output_file_path = os.path.join(self.output_directory, filename.replace('.pdf', '.txt'))
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(text)
                print(f"Processed: {filename}")

# Accept input and output directories as command-line arguments
if __name__ == "__main__":
    print("hello py!")
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    
    extractor = PDFTextExtractor(input_directory, output_directory)
    extractor.process_all_pdfs()
