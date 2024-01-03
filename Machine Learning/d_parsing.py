import json
import os
import pandas as pd
import re  
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()


# Definiere Regex-Muster und entsprechende Flags
regex_flags = {
    r'\b(Firma|Sitz|Gegenstand|Stammkapital|Stammeinlagen|Kapital|Einlagen)\b': 'RED FLAG',
    r'\b(Geschäftsführung|Vertretung|Dauer|Geschäftsjahr|Gesellschafterversammlung|Geschaftsjahr)\b': 'Orange Flag',
    r'\b(Veräußerung|Gewinnverteilung|Einziehung|Erbfolge|Kündigung|Abfindung|Wettbewerb|Schlussbestimmungen|Gesellschafterbeschlüsse|Jahresabschluss|Ergebnisverwendung|Kosten|Gründungskosten|Salvatorische|Auflösung|Sonstige)\b': 'Green Flag'
}

# Funktion zum Parsen von JSONL-Dateien
def parse_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data

# Funktion zur Extraktion von Daten
def extract_data(data):
    extracted_data = {}
    for item in data:
        section_text = item.get('text')
        section_data = {
            'flags': [],
            'clauses': [],
            'subsections': []
        }

        # Überprüfen , ob Annotations vorhanden sind. Wenn nicht, Regex-Regeln anwenden
        if 'entities' not in item:
            #  Abschnittstext in Wörter aufteilen und jedes Wort mit Regex-Mustern vergleichen
            words = re.findall(r'\b\w+\b', section_text, re.IGNORECASE)
            for word in words:
                for regex_pattern, flag in regex_flags.items():
                    if re.search(regex_pattern, word):
                        section_data['flags'].append(flag)

        for entity in item.get('entities', []):
            label = entity.get('label')
            entity_text = entity.get('text', '')

            if label in ['RED FLAG', 'Orange Flag', 'Green Flag']:
                section_data['flags'].append(label)
            elif label == 'Section':
                section_data['section'] = section_text
            elif label == 'Subsection':
                section_data['subsections'].append(entity_text)
            else:
                section_data['clauses'].append(label)

        extracted_data[section_text] = section_data
    return extracted_data

# Funktion zum Kompilieren der Daten für eine Datei
def compile_data_for_file(file_path):
    data = parse_jsonl(file_path)
    return extract_data(data)

# Funktion zum Verarbeiten aller Dateien in einem Verzeichnis
def batch_process(converted_to_json_directory):
    all_data = {}
    for file in os.listdir(converted_to_json_directory):
        if file.endswith('.jsonl'):
            file_path = os.path.join(converted_to_json_directory, file)
            all_data[file] = compile_data_for_file(file_path)
    return all_data

# Funktion zum Generieren eines Berichts
def generate_report(all_data, parsed_csv_file):
    report_data = []
    for file, data in all_data.items():
        for section, details in data.items():
            report_data.append({
                'File': file,
                'Section': section,
                'Flags': ', '.join(details['flags']),
                'Clauses': ', '.join(details['clauses'])
            })
    df = pd.DataFrame(report_data)
    df.to_csv(parsed_csv_file, index=False)

# Hauptfunktion
def main():
    converted_to_json_directory = os.getenv('CONVERTED_TO_JSON_DIRECTORY', 'default/path/to/converted_to_json')
    parsed_csv_file = os.getenv('PARSED_CSV_FILE', 'default/path/to/parsed_csv.csv')
    all_data = batch_process(converted_to_json_directory)
    generate_report(all_data, parsed_csv_file)

if __name__ == "__main__":
    main()
