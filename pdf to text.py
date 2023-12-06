import fitz  # PyMuPDF
import os
import re

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text(self):
        text = ""
        with fitz.open(self.pdf_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text

class TextCleaner:
    @staticmethod
    def clean_text(text):
        if text.startswith('- Wiedergabe '):
            text = TextCleaner.clean_text_2(text)
        elif re.match(r'Handelsregister [A-Z] des', text):
            text = TextCleaner.clean_text_1(text)

        # Apply the different cleaning methods in sequence
        text = TextCleaner.clean_text_1(text)
        text = TextCleaner.clean_text_2(text)
        text = TextCleaner.remove_abruf_vom(text)
        text = TextCleaner.standardize_formatting(text)
        text = TextCleaner.correct_hyphenation(text)
        text = TextCleaner.remove_page_numbers_and_dates(text)
        text = TextCleaner.remove_letzte_eintragung(text)
        return text

    @staticmethod
    def clean_text_1(text):
    # Angepasstes Muster für Handelsregister A bis Z
        pattern = re.compile(
            r'Handelsregister [A-Z] des\s+'
            r'Amtsgerichts .+?\s+'
            r'Abteilung [A-Z]\s+'
            r'Wiedergabe des aktuellen\s+'
            r'Registerinhalts\s+'
            r'Nummer der Firma:\s+'
            r'[A-Z]{2,3} \d+\s+'
            r'Seite \d+ von \d+\s*',
            re.DOTALL)
        return pattern.sub('', text)
    
    @staticmethod
    def clean_text_2(text):
        try:
            # Add a print statement to indicate that the function is called
            print("clean_text_2 called")

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
            
            # Print the input text to see if it matches the expected pattern
            print("Input Text:")
            print(text)

            # Apply the pattern and replace with an empty string
            text = pattern.sub('', text)
            
            # Print the cleaned text
            print("Cleaned Text:")
            print(text)
            
            return text
        except Exception as e:
            # Handle any exceptions and print the error message
            print(f"Error in clean_text_2: {str(e)}")
            return text  # Return the original text if an error occurs



    @staticmethod
    def remove_abruf_vom(text):
        pattern1 = re.compile(r'Abruf vom \d{2}\.\d{2}\.\d{4} \d{2}:\d{2}')
        cleaned_text1 = pattern1.sub('', text)
        return cleaned_text1

    
    @staticmethod
    def standardize_formatting(text):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\r\n|\r|\n', '\n', text)
        return text


    @staticmethod
    def correct_hyphenation(text):
        text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)
        return text

    @staticmethod
    def remove_page_numbers_and_dates(text):
        pattern = re.compile(r'\d{2}\.\d{2}\.\d{4} Seite \d+ von \d+')
        return pattern.sub('', text)

    @staticmethod
    def remove_letzte_eintragung(text):
        pattern = re.compile(
            r'\d+\.\s*(a\)\s*)?Tag der letzten Eintragung:?\s*\d{2}\.\d{2}\.\d{4}\s*',
            re.MULTILINE)
        return pattern.sub('', text)

class ContractParser:
    def __init__(self, text):
        self.text = text

    def parse(self):
        sections = {
            "Anzahl der bisherigen Eintragungen": re.search(r'Anzahl der bisherigen Eintragungen:\s*(\d+)', self.text),
            "Firma": re.search(r'Firma:\s*(.+?)\s*b\)', self.text),
            "Sitz, Niederlassung, Geschäftsanschrift": re.search(r'b\) Sitz, Niederlassung, .+?:\s*(.+?)\s*c\)', self.text),
            "Gegenstand des Unternehmens": re.search(r'c\) Gegenstand des Unternehmens:\s*(.+?)\s*\d+\.', self.text),
            "Grund- oder Stammkapital": re.search(r'Grundoder Stammkapital:\s*(\d+,\d{2}\s*EUR)', self.text),
            "Allgemeine Vertretungsregelung": re.search(r'Allgemeine Vertretungsregelung:\s*(.+?)\s*b\)', self.text),
            "Geschäftsführer und Vertretungsberechtigte": re.search(r'b\) Vorstand, Leitungsorgan, .+?:\s*(.+?)\s*\d+\.\s*Prokura', self.text),
            "Prokura": re.search(r'Prokura:\s*(.+?)\s*\d+\.\s*a\)', self.text),
            "Rechtsform, Beginn, Satzung": re.search(r'a\) Rechtsform, Beginn, .+?:\s*(.+?)\s*b\)', self.text),
            "Tag der letzten Eintragung": re.search(r'Tag der letzten Eintragung:\s*(\d{2}\.\d{2}\.\d{4})', self.text),

            # Add other sections here...
        }
        parsed_data = {key: match.group(1) if match else "" for key, match in sections.items()}
        return parsed_data

class ContractProcessor:
    def __init__(self, pdf_directory, output_directory):
        self.pdf_directory = pdf_directory
        self.output_directory = output_directory
        self.file_counter = 1
        self.file_counter2 = 1

    def process_contracts(self):
        for filename in os.listdir(self.pdf_directory):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(self.pdf_directory, filename)
                extractor = PDFExtractor(pdf_path)
                text = extractor.extract_text()

                cleaner = TextCleaner()
                cleaned_text = cleaner.clean_text(text)
                
                # Save the cleaned text (before parsing)
                self._output_cleaned_text_to_file(cleaned_text)

                parser = ContractParser(cleaned_text)
                parsed_data = parser.parse()

                # Save the parsed data (after parsing)
                self._output_parsed_data_to_file(parsed_data)

    def _output_cleaned_text_to_file(self, cleaned_text):
        output_filename = os.path.join(self.output_directory, f"{self.file_counter}.txt")
        with open(output_filename, 'w', encoding='utf-8') as text_file:
            text_file.write(cleaned_text)
        self.file_counter += 1

    def _output_parsed_data_to_file(self, parsed_data):
        output_filename = os.path.join(self.output_directory, f"{self.file_counter2}p.txt")
        with open(output_filename, 'w', encoding='utf-8') as text_file:
            for section, content in parsed_data.items():
                text_file.write(f"{section}: {content}\n")
        self.file_counter2 += 1
# Main execution
if __name__ == "__main__":
    pdf_directory = 'C:/Users/ayham/Desktop/Projekt/Data/PDFs'
    output_directory = 'C:/Users/ayham/Desktop/txt'
    processor = ContractProcessor(pdf_directory, output_directory)
    processor.process_contracts()
    print("Contract processing completed.")
