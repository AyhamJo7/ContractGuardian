import json
import os
import pandas as pd
import re  # Regex Modul importieren
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()



# Regex-Muster und entsprechende Flags definieren
regex_flags = {
    r'\b(Firma|Sitz|Gegenstand|Stammkapital|Stammeinlagen|Kapital|Einlagen)\b': 'RED FLAG',
    r'\b(Geschäftsführung|Vertretung|Dauer|Geschäftsjahr|Gesellschafterversammlung)\b': 'Orange Flag',
    r'\b(Veräußerung|Gewinnverteilung|Einziehung|Erbfolge|Kündigung|Abfindung)\b': 'Green Flag'
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

        # Check if annotations are present, if not, apply regex rules
        if 'entities' not in item:
            # Split the section text into words and check each word against regex patterns
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
def batch_process(annotated_data_directory):
    all_data = {}
    for file in os.listdir(annotated_data_directory):
        if file.endswith('.jsonl'):
            file_path = os.path.join(annotated_data_directory, file)
            all_data[file] = compile_data_for_file(file_path)
    return all_data

# Funktion zum Generieren eines Berichts
def generate_report(all_data, annotated_parsed_csv_file):
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
    df.to_csv(annotated_parsed_csv_file, index=False)

# Hauptfunktion
def main():
    annotated_data_directory = os.getenv('ANNOTATED_DATA_DIRECTORY', 'default/path/to/annotated_data_directory')
    annotated_parsed_csv_file = os.getenv('ANNOTATED_PARSED_CSV_FILE', 'default/path/to/annotated_parsed_csv_file')
    all_data = batch_process(annotated_data_directory)
    generate_report(all_data, annotated_parsed_csv_file)

if __name__ == "__main__":
    main()
