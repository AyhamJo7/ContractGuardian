import os
import re

class ContractParser:
    def __init__(self, text):
        self.text = text

    def parse(self):
        sections = {
            "Anzahl der bisherigen Eintragungen": re.search(r"Anzahl der bisherigen Eintragungen:\s*(\d+)", self.text),
            "Firma": re.search(r"Firma:\s*([\w\s]+)", self.text),
            "Sitz, Niederlassung, inländische Geschäftsanschrift, empfangsberechtigte Person, Zweigniederlassungen": re.search(r"Sitz, Niederlassung, inländische Geschäftsanschrift, empfangsberechtigte Person, Zweigniederlassungen:\s*([\w\s,]+)", self.text),
            "Geschäftsanschrift": re.search(r"Geschäftsanschrift:\s*([\w\s,.]+)", self.text),
            "Gegenstand des Unternehmens": re.search(r"Gegenstand des Unternehmens:\s*(.*)", self.text),
            "Grund- oder Stammkapital": re.search(r"Grund- oder Stammkapital:\s*([\w\s,.]+)", self.text),
            "Allgemeine Vertretungsregelung": re.search(r"Allgemeine Vertretungsregelung:\s*(.*)", self.text),
            "Geschäftsführer und Vertretungsberechtigte": re.search(r"Geschäftsführer und Vertretungsberechtigte:\s*(.*)", self.text),
            "Prokura": re.search(r"Prokura:\s*(.*)", self.text),
            "Rechtsform, Beginn, Satzung oder Gesellschaftsvertrag": re.search(r"Rechtsform, Beginn, Satzung oder Gesellschaftsvertrag:\s*(.*)", self.text),
            "Tag der letzten Eintragung": re.search(r"Tag der letzten Eintragung:\s*(.*)", self.text)
        }
        parsed_data = {key: match.group(1).strip() if match else "" for key, match in sections.items()}
        return parsed_data





def process_text_files(input_directory, output_directory):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        file_counter = 1
        for filename in os.listdir(input_directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(input_directory, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                    parser = ContractParser(text)
                    parsed_data = parser.parse()

                    # Output file name
                    output_file_path = os.path.join(output_directory, f"{file_counter}_parsed.txt")
                    
                    # Write parsed data to the output file
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        for key, value in parsed_data.items():
                            output_file.write(f"{key}: {value}\n")
                    
                    file_counter += 1

def main():
    input_directory = 'C:/Users/ayham/Desktop/txt'
    output_directory = 'C:/Users/ayham/Desktop/txt_parsed'
    process_text_files(input_directory, output_directory)

    print("Parsing completed. Output files saved in:", output_directory)

if __name__ == "__main__":
    main()

