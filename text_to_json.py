import json
import os

# Funktion zum Lesen einer Textdatei
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Funktion zum Aufteilen des Textes in Abschnitte anhand eines Trennzeichens (Standardmäßig '§')
def split_into_sections(text, delimiter='§'):
    return text.split(delimiter)[1:]

# Funktion zum Speichern von Daten im JSONL-Format
def save_jsonl(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for entry in data:
            json.dump(entry, file, ensure_ascii=False)
            file.write('\n')

# Funktion zum Verarbeiten eines Verzeichnisses von Textdateien
def process_directory(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_directory, filename)
            text = read_file(file_path)
            sections = split_into_sections(text)
            # Erstellen von JSONL-Datenstrukturen für jede Sektion des Textes
            json_data = [{"text": section.strip()} for section in sections]
            output_file = os.path.join(output_directory, filename.replace('.txt', '.jsonl'))
            # Speichern der JSONL-Daten in einer Ausgabedatei
            save_jsonl(json_data, output_file)
            print(f"Verarbeitet {filename}")



# Angeben der Verzeichnispfade für Eingabe und Ausgabe
input_directory = 'C:/Users/ayham/Desktop/2.text'
output_directory = 'C:/Users/ayham/Desktop/3.jsonl'
#Aufrufen der Funktion zur Verarbeitung des Verzeichnisses
process_directory(input_directory, output_directory)

""" # Angeben der Verzeichnispfade für Eingabe und Ausgabe
input_directory = '/Users/adamj7/Desktop/2.text'
output_directory = '/Users/adamj7/Desktop/3.jsonl'
# Aufrufen der Funktion zur Verarbeitung des Verzeichnisses
process_directory(input_directory, output_directory) """
