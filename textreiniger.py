import fitz  # PyMuPDF
import os
import re

class PDFTextExtractor:
    def __init__(self, pdf_directory, output_directory):
        self.pdf_directory = pdf_directory
        self.output_directory = output_directory if output_directory else pdf_directory

    def extract_text_from_pdf(self, pdf_path):
        with fitz.open(pdf_path) as pdf:
            text = ""
            for page in pdf:
                text += page.get_text()
        return text

    def clean_text(self, text):
        # Angepasstes Muster, um die spezifizierten Sätze zu entfernen
        pattern = re.compile(
            r'Handelsregister [A-Z] des\s+'  # Matches 'Handelsregister' followed by any single uppercase letter
            r'Amtsgerichts .+?\s+'
            r'Abteilung [A-Z]\s+'  # Matches 'Abteilung' followed by any single uppercase letter
            r'Wiedergabe des aktuellen\s+'
            r'Registerinhalts\s+'
            r'Nummer der Firma:\s+'
            r'[A-Z]{2,3} \d+\s+'  # Matches two to three uppercase letters (e.g., HRB, HAR, HRA, HBA) followed by digits
            r'Seite \d+ von \d+\s*',
            re.DOTALL)
        text = pattern.sub('', text)
        return text

    def clean_text_2(self, text):
        pattern = re.compile(
            r'- Wiedergabe des aktuellen Registerinhalts -\s+'
            r'Abruf vom \d{2}\.\d{2}\.\d{4}, \d{2}:\d{2}\s+'
            r'Amtsgericht .+?\s+'
            r'Ausdruck - Handelsregister Abteilung [A-Z] - [A-Z]{2,3} \d{4,8} [A-Z]{0,2}\s+'
            r'Aktueller Ausdruck [A-Z]{2,3} \d{4,8} [A-Z]{0,2}\s+'
            r'Handelsregister Abteilung [A-Z]\s+'
            r'Amtsgericht .+?\s+'
            r'(?=1\. Anzahl der bisherigen Eintragungen|2\.a\) Firma)',
            re.DOTALL)
        text = pattern.sub('\n', text)  # Replace the matched pattern with a newline to separate sections
        return text

    def clean_text_3(self, text):
        pattern = re.compile(
            r'- Wiedergabe des aktuellen Registerinhalts -\s+'
            r'Abruf vom \d{2}\.\d{2}\.\d{4}, \d{2}:\d{2}\s+'
            r'Amtsgericht .+?\s+'
            r'Ausdruck - Handelsregister Abteilung [A-Z] - [A-Z]{2,3} \d{4,8} [A-Z]{0,2}\s+',
            re.DOTALL)
        text = pattern.sub('', text)
        return text


    def remove_seite_von(self, text):
        pattern = re.compile(r'Seite \d+ von \d+\s*')
        text = pattern.sub('', text)
        return text

    def remove_abruf_vom(self, text):
        pattern = re.compile(r'Abruf vom \d{2}\.\d{2}\.\d{4} \d{2}:\d{2}')
        text = pattern.sub('', text)
        return text

    def standardize_formatting(self, text):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\r\n|\r|\n', '\n', text)
        return text

    def correct_hyphenation(self, text):
        text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)
        return text

    def process_pdfs(self):
        file_counter = 1
        for filename in os.listdir(self.pdf_directory):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_directory, filename)
                text = self.extract_text_from_pdf(pdf_path)

                cleaned_text = self.standardize_formatting(text)
                cleaned_text = self.correct_hyphenation(cleaned_text)
                
                if cleaned_text.startswith('- Wiedergabe des aktuellen Registerinhalts -'):
                    cleaned_text = self.clean_text_2(cleaned_text)
                if re.search(r'- Wiedergabe des aktuellen Registerinhalts -', cleaned_text):
                    cleaned_text = self.clean_text_3(cleaned_text)

                if  re.match(r'Handelsregister [A-Z] des', cleaned_text):
                    cleaned_text = self.clean_text(cleaned_text)

                cleaned_text = self.remove_abruf_vom(cleaned_text)
                cleaned_text = self.remove_seite_von(cleaned_text)
                
                phrases_to_check = [
                    "1. Anzahl der bisherigen Eintragungen",
                    "2.a) Firma",
                    "b) Sitz, Niederlassung, inländische Geschäftsanschrift, empfangsberechtigte Person, Zweigniederlassungen",
                    "c) Gegenstand des Unternehmens",
                    "3. Grund- oder Stammkapital",
                    "4.a) Allgemeine Vertretungsregelung",
                    "b) Vorstand, Leitungsorgan, geschäftsführende Direktoren, persönlich haftende Gesellschafter, Geschäftsführer, Vertretungsberechtigte und besondere Vertretungsbefugnis",
                    "5. Prokura",
                    "6.a) Rechtsform, Beginn, Satzung oder Gesellschaftsvertrag",
                    "7. Tag der letzten Eintragung",
                    "3. Grundoder Stammkapital"
                ]

                for phrase in phrases_to_check:
                    if phrase in cleaned_text and f"{phrase}:" not in cleaned_text:
                        cleaned_text = cleaned_text.replace(phrase, f"{phrase}:")

                output_filename = os.path.join(self.output_directory, f"{file_counter}.txt")
                with open(output_filename, 'w', encoding='utf-8') as text_file:
                    text_file.write(cleaned_text)
                file_counter += 1

        print("Text extraction and cleaning completed. Text files saved to directory.")

def main():
    pdf_directory = 'C:/Users/ayham/Desktop/Projekt/Data/PDFs'
    output_directory = 'C:/Users/ayham/Desktop/txt'
    pdf_extractor = PDFTextExtractor(pdf_directory, output_directory)
    pdf_extractor.process_pdfs()

if __name__ == "__main__":
    main()
