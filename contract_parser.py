import os
import re

class ContractParser:
    def __init__(self, text):
        self.text = text

    def parse(self):
        sections = {
            "Anzahl der bisherigen Eintragungen": r'Anzahl der bisherigen Eintragungen:\s*(\d+)',
            "Firma": r'Firma:\s*(.+?)\s*b\)',
            "Sitz, Niederlassung, inländische Geschäftsanschrift, empfangsberechtigte Person, Zweigniederlassungen": r'b\) Sitz, Niederlassung, .+?:\s*(.+?)\s*c\)',
            "Gegenstand des Unternehmens": r'c\) Gegenstand des Unternehmens:\s*(.+?)\s*\d+\.',
            "Grundoder Stammkapital": r'Grundoder Stammkapital:\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*(EUR|DEM)',
            "Allgemeine Vertretungsregelung": r'Allgemeine Vertretungsregelung:\s*(.+?)\s*b\)',
            "Geschäftsführer und Vertretungsberechtigte": r'b\) Vorstand, Leitungsorgan, .+?:\s*(.+?)\s*\d+\.\s*Prokura',
            "Prokura": r'Prokura:\s*(.+?)\s*\d+\.\s*a\)',
            "Rechtsform, Beginn, Satzung": r'a\) Rechtsform, Beginn, .+?:\s*(.+?)\s*b\)',
            "Tag der letzten Eintragung": r'Tag der letzten Eintragung:\s*(\d{2}\.\d{2}\.\d{4})',
        }
        parsed_data = {"Grundoder Stammkapital currency": ""}  # Initialize with a default currency value

        for key, pattern in sections.items():
            try:
                match = re.search(pattern, self.text)
                if match:
                    if key == "Grundoder Stammkapital":
                        parsed_data[key] = match.group(1).strip()
                        parsed_data["Grundoder Stammkapital currency"] = match.group(2).strip()
                    else:
                        parsed_data[key] = match.group(1).strip()
                else:
                    parsed_data[key] = ""
            except Exception as e:
                print(f"Error processing {key}: {e}")
                parsed_data[key] = ""

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
                
                # Write parsed data to the output file, ensuring the 'Grundoder Stammkapital currency' is right after 'Grundoder Stammkapital'
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    for key, value in parsed_data.items():
                        if key == "Grundoder Stammkapital":
                            # Append the currency to the numeric value
                            value_with_currency = f"{value} {parsed_data['Grundoder Stammkapital currency']}"
                            output_file.write(f"{key}: {value_with_currency}\n")
                        elif key != "Grundoder Stammkapital currency":  # Skip writing 'Grundoder Stammkapital currency' again
                            output_file.write(f"{key}: {value}\n")

        file_counter += 1


def main():
    input_directory = 'C:/Users/ayham/Desktop/txt'
    output_directory = 'C:/Users/ayham/Desktop/txt_parsed'
    process_text_files(input_directory, output_directory)

    print("Parsing completed. Output files saved in:", output_directory)

if __name__ == "__main__":
    main()

