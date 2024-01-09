import json
import os
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()


# Funktion zum Lesen einer Textdatei
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Funktion zum Aufteilen des Textes in Abschnitte, wobei bestimmte Wörter berücksichtigt werden
def split_into_sections(text, delimiter='§'):
    parts = text.split(delimiter)
    sections = []
    i = 0

    while i < len(parts):
        section = delimiter + parts[i].strip()
        while i + 1 < len(parts) and any(section.endswith(word) for word in ["in Verbindung mit", "i.V.m.", "iVm.", "gelten","gilt","entsprechend","entspre­ chend","entspre­ chend §","insbesondere","nach", "gemäß","gemaß","gemaß §","gemaf5","gemaB","gemafs","gemaf3.","gemäß §","gem.","gem. §","gema/1","iSv.","gern.","sondern","vorbehaltlich","soweit er","Verffigungen sind","dieser","wegen,","gegen","des", "der", "von","van","vor","aus","nach §","der §", "(", "in", "und", "d.", "S.","i.S.d.", "i.S.d. §","in Verbindung mit §"]):
            i += 1
            section += ' ' + delimiter + parts[i].strip()

        # Füge den Abschnitt hinzu, wenn er nicht leer ist (nach Entfernen von Leerzeichen)
        if section.strip() and not section.strip() == delimiter:
            sections.append(section)
        i += 1

    return sections

# Funktion zum Speichern von Daten im JSONL-Format
def save_jsonl(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for entry in data:
            json.dump(entry, file, ensure_ascii=False)
            file.write('\n')

# Funktion zum Verarbeiten eines Verzeichnisses von Textdateien
def process_directory(cleaned_text_directory, converted_to_json_directory):
    os.makedirs(converted_to_json_directory, exist_ok=True)

    for filename in os.listdir(cleaned_text_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(cleaned_text_directory, filename)
            text = read_file(file_path)
            sections = split_into_sections(text)
            json_data = [{"text": section.strip()} for section in sections]
            output_file = os.path.join(converted_to_json_directory, filename.replace('.txt', '.jsonl'))
            save_jsonl(json_data, output_file)

# Verzeichnispfade für Eingabe und Ausgabe mittels Umgebungsvariablen definieren
cleaned_text_directory = os.getenv('CLEANED_TEXT_DIRECTORY', 'default/path/to/cleaned_text')
converted_to_json_directory = os.getenv('CONVERTED_TO_JSON_DIRECTORY', 'default/path/to/converted_to_json')
process_directory(cleaned_text_directory, converted_to_json_directory)
