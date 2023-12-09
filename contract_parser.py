import os
import re

class ContractParser:
    def __init__(self, text):
        """
        Initialisiert den ContractParser mit dem zu analysierenden Text.
        :param text: Der Text des Vertrages oder Dokumentes.
        """
        self.text = text

    def parse(self):
        """
        Analysiert den Text und extrahiert spezifische Informationen basierend auf definierten Mustern.
        Verwendet reguläre Ausdrücke, um definierte Abschnitte aus dem Text zu extrahieren.
        :return: Ein Dictionary mit den extrahierten Informationen.
        """        
        # Definieren von Abschnitten, die analysiert werden sollen
        sections = {
            "Firma": r'Firma:\s*(.+?)\s*b\)',
            "Sitz, Niederlassung, inländische Geschäftsanschrift, empfangsberechtigte Person, Zweigniederlassungen": r'b\) Sitz, Niederlassung, .+?:\s*(.+?)\s*c\)',
            "Gegenstand des Unternehmens": r'c\) Gegenstand des Unternehmens:\s*(.+?)\s*\d+\.',
            "Grund- oder Stammkapital": r'Grundoder Stammkapital:\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*(EUR|DEM)',
            "Allgemeine Vertretungsregelung": r'Allgemeine Vertretungsregelung:\s*(.+?)\s*b\)',
            "Geschäftsführer und Vertretungsberechtigte": r'b\) Vorstand, Leitungsorgan, .+?:\s*(.+?)\s*\d+\.\s*Prokura',
            "Prokura": r'Prokura:\s*(.+?)\s*\d+\.\s*a\)',
            "Rechtsform, Beginn, Satzung": r'a\) Rechtsform, Beginn, .+?:\s*(.+?)\s*b\)',
        }
        parsed_data = {"Grundoder Stammkapital currency": ""}  # Initialisierung mit einer Standardwährung

        for key, pattern in sections.items():
            try:
                match = re.search(pattern, self.text)
                if match:  # Spezielle Behandlung für 'Grund- oder Stammkapital', um Währung separat zu speichern
                    if key == "Grund- oder Stammkapital":
                        parsed_data[key] = match.group(1).strip()
                        parsed_data["Grundoder Stammkapital currency"] = match.group(2).strip()
                    else:
                        parsed_data[key] = match.group(1).strip()
                else:
                    parsed_data[key] = ""
            except Exception as e:
                print(f"Fehler bei der Verarbeitung von {key}: {e}")
                parsed_data[key] = ""

        return parsed_data

def process_text_files(input_directory, output_directory):
    """
    Verarbeitet Textdateien aus einem Eingabeverzeichnis, extrahiert Informationen und speichert die Ergebnisse in einem Ausgabeverzeichnis.
    :param input_directory: Verzeichnis mit Eingabetextdateien.
    :param output_directory: Verzeichnis für die gespeicherten Ausgabedateien.
    """
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

                # Dateinamen für die Ausgabe definieren
                output_file_path = os.path.join(output_directory, f"{file_counter}_parsed.txt")
                
                # Analysedaten in die Ausgabedatei schreiben, sicherstellen, dass 'Grund- oder Stammkapital Währung' direkt nach 'Grund- oder Stammkapital' steht
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    for key, value in parsed_data.items():
                        if key == "Grund- oder Stammkapital":
                            # Die Währung zum numerischen Wert hinzufügen
                            value_with_currency = f"{value} {parsed_data['Grundoder Stammkapital currency']}"
                            output_file.write(f"{key}: {value_with_currency}\n")
                        elif key != "Grundoder Stammkapital currency":  # 'Grund- oder Stammkapital currency' nicht erneut schreiben
                            output_file.write(f"{key}: {value}\n")

            # Inkrementiere den Dateizähler innerhalb der Schleife
            file_counter += 1

def main():
    input_directory = 'C:/Users/ayham/Desktop/txt'
    output_directory = 'C:/Users/ayham/Desktop/txt_parsed'
    process_text_files(input_directory, output_directory)

    print("Analyse abgeschlossen. Ausgabedateien wurden gespeichert in:", output_directory)

if __name__ == "__main__":
    main()
