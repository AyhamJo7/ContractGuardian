import re
import os

class TextCleaning:

    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def clean_text(self, text):
        # Korrigiere Silbentrennung
        text = self.correct_hyphenation(text)
        # Standardisiere das Format
        text = self.standardize_formatting(text)
        # Entferne irrelevante Informationen
        text = self.remove_irrelevant_info(text)
        # Entferne Seitenzahlen
        text = self.remove_pagination(text)
        # Entferne Leerzeichen aus Titeln
        text = self.remove_spaces_from_title(text)

        return text

    def remove_pagination(self, text):
        # Entferne 'Seite X von Y', wobei X und Y Zahlen sind
        text = re.sub(r'Seite\s+\d+\s+von\s+\d+', '', text)
        
        # Entferne '-Seite X-', wobei X eine Zahl ist
        text = re.sub(r'-Seite\s+\d+-', '', text)

        # Entferne '-X-', wobei X eine Zahl ist, umgeben von Bindestrichen
        text = re.sub(r'-\d+-', '', text)

        # Entferne '- X -', wobei X eine Zahl ist, umgeben von Bindestrichen und Leerzeichen
        text = re.sub(r'-\s+\d+\s+-', '', text)

        return text
    
    def correct_hyphenation(self, text):
        # Verbinde Silbentrennungen am Ende einer Zeile
        text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
        return text

    def standardize_formatting(self, text):
        # Ersetze mehrere Leerzeichen durch ein einzelnes Leerzeichen
        text = re.sub(r'\s+', ' ', text)

        # Standardisiere Absatzumbrüche
        text = re.sub(r'(\.\s+)([A-Z])', r'\1\n\2', text)

        return text

    def remove_irrelevant_info(self, text):
        # Entferne Dateipfade, die mit .docx enden
        text = re.sub(r'\\\\.*?\.docx', '', text)
        # Entferne Vertragsnummern: 6 oder 7 Ziffern, gefolgt von bis zu zwei Großbuchstaben und optionaler Versionsnummer
        text = re.sub(r'\b\d{6,7}[A-Z]{0,2}(v\d)?\b', '', text)
        # Entferne Muster wie "(StA: Jahr:Zahlen, Referenz: Zahlen, Doc: Zahlen)"
        text = re.sub(r'\(StA:\s+\d{4}:\d+,\s+Referenz:\s*\d*(,\s+Doc:\s*\d*\.?\d*)?\)', '', text)
        # Entferne Muster, die mit 'tmp' beginnen, gefolgt von alphanumerischen Zeichen
        text = re.sub(r'\btmp[A-Za-z0-9]+\b', '', text)
        # Entferne Muster, die mit 'cvc' oder 'cvd' beginnen, gefolgt von alphanumerischen Zeichen, Unterstrichen oder Bindestrichen
        text = re.sub(r'\b(cv[c|d])[A-Za-z0-9_\-]+\b', '', text)
        # Entferne den spezifischen Ausdruck "- Ende der Satzung -"
        text = re.sub(r'-\s*Ende\s*der\s*Satzung\s*-', '', text)
        # Entferne den spezifischen Ausdruck "- Ende der Satzung -"
        text = re.sub(r'-\s*Ende\s*der\s*Anlage\s*-', '', text)

        # Entferne das Muster von drei Sternen am Ende des Dokuments
        text = re.sub(r'\* \* \*$', '', text)

        return text

    def remove_spaces_from_title(self, text):
        # Muster zum Erkennen und Korrigieren von Worten mit Leerzeichen
        patterns_to_correct = {
            r'G\s+E\s+S\s+E\s+L\s+L\s+S\s+C\s+H\s+A\s+F\s+T\s+S\s+V\s+E\s+R\s+T\s+R\s+A\s+G': 'GESELLSCHAFTSVERTRAG',
            r'G\s+E\s+S\s+E\s+L\s+L\s+S\s+C\s+H\s+A\s+F\s+T\s+E\s+R\s+V\s+E\s+R\s+T\s+R\s+A\s+G': 'GESELLSCHAFTERVERTRAG',
            r'S\s+A\s+T\s+Z\s+U\s+N\s+G': 'SATZUNG'
        }

        for pattern, replacement in patterns_to_correct.items():
            text = re.sub(pattern, replacement, text)

        return text

    def process_all_texts(self):
        for filename in os.listdir(self.input_directory):
            if filename.lower().endswith('.txt'):
                input_file_path = os.path.join(self.input_directory, filename)
                with open(input_file_path, 'r', encoding='utf-8') as file:
                    text = file.read()

                cleaned_text = self.clean_text(text)

                output_file_path = os.path.join(self.output_directory, 'c_' + filename)
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(cleaned_text)
                print(f"Verarbeitet: {filename} --> c_{filename}")


# Example usage Win
input_directory = 'C:/Users/ayham/Desktop/1.text'
output_directory = 'C:/Users/ayham/Desktop/2.text'
cleaner = TextCleaning(input_directory, output_directory)
cleaner.process_all_texts()


""" # Beispielverwendung Mac
input_directory = '/Users/adamj7/Desktop/1.text'
output_directory = '/Users/adamj7/Desktop/2.text'
cleaner = TextCleaning(input_directory, output_directory)
cleaner.process_all_texts()
 """
 
 
	
