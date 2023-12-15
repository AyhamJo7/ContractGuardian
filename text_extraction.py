import fitz  # PyMuPDF
import os

class PDFTextExtractor:
    
    def __init__(self, pdf_directory, output_directory):
        """
        Initialisiert die PDFTextExtractor-Klasse.
        :param pdf_directory: Verzeichnis, in dem sich die PDF-Dateien befinden.
        :param output_directory: Verzeichnis, in das die extrahierten Textdateien gespeichert werden.
        """
        self.pdf_directory = pdf_directory
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)  # Erstellt das Ausgabeverzeichnis, falls es nicht existiert.

    def extract_text_from_pdf(self, pdf_path):
        """
        Extrahiert den Text aus einer PDF-Datei.
        :param pdf_path: Pfad zur PDF-Datei.
        :return: Extrahierter Text als String.
        """
        with fitz.open(pdf_path) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()  # Text von jeder Seite extrahieren
        return text

    def process_all_pdfs(self):
        """
        Verarbeitet alle PDF-Dateien im Eingabeverzeichnis und speichert die extrahierten Texte im Ausgabeverzeichnis.
        """
        for filename in os.listdir(self.pdf_directory):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_directory, filename)
                text = self.extract_text_from_pdf(pdf_path)
                output_file_path = os.path.join(self.output_directory, filename.replace('.pdf', '.txt'))
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(text)  # Speichert den extrahierten Text in einer Textdatei
                print(f"Verarbeitet: {filename}")

# Beispielverwendung
pdf_directory = 'C:/Users/ayham/Desktop/Projekt/Data/PDFs'
output_directory = 'C:/Users/ayham/Desktop/1.text'
extractor = PDFTextExtractor(pdf_directory, output_directory)
extractor.process_all_pdfs()

 