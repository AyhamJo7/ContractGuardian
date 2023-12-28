import json
import os
import pandas as pd
import re  # Import the regex module

# Define regex patterns and corresponding flags
regex_flags = {
    r'\b(Firma|Sitz|Gegenstand|Stammkapital|Stammeinlagen|Kapital|Einlagen)\b': 'RED FLAG',
    r'\b(Geschäftsführung|Vertretung|Dauer|Geschäftsjahr|Gesellschafterversammlung)\b': 'Orange Flag',
    r'\b(Veräußerung|Gewinnverteilung|Einziehung|Erbfolge|Kündigung|Abfindung)\b': 'Green Flag'
}

def parse_jsonl(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    return data

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

def compile_data_for_file(file_path):
    data = parse_jsonl(file_path)
    return extract_data(data)

def batch_process(directory):
    all_data = {}
    for file in os.listdir(directory):
        if file.endswith('.jsonl'):
            file_path = os.path.join(directory, file)
            all_data[file] = compile_data_for_file(file_path)
    return all_data

def generate_report(all_data, output_file):
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
    df.to_csv(output_file, index=False)

def main():
    directory = r'C:\Users\ayham\Desktop\3.jsonl'  # Directory containing JSONL files
    output_file = r'C:\Users\ayham\Desktop\5\report.csv'  # Output file path
    all_data = batch_process(directory)
    generate_report(all_data, output_file)

if __name__ == "__main__":
    main()

