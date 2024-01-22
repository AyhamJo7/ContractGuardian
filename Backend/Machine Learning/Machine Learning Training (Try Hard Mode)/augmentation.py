import json
import os
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei 
load_dotenv()


def read_jsonl_file(file_path):
    # JSONL-Datei lesen und in eine Liste von Python-Objekten umwandeln 
    with open(file_path, 'r', encoding='utf-8') as file:
        return [json.loads(line) for line in file]

def create_dummy_copies(file_path):
    # Erstellen von Dummy-Kopien der ursprünglichen Daten 
    original_data = read_jsonl_file(file_path)
    dummy_copies = []
    for i in range(len(original_data)):
        kopie = original_data.copy()
        del kopie[i]
        dummy_copies.append(kopie)
    return dummy_copies


def main():
    # Festlegen der Verzeichnispfade
    annotated_data_directory = os.getenv('ANNOTATED_DATA_DIRECTORY', 'default/path/to/Annotated Data')
    augmented_annotated_data = os.getenv('AUGMENTED_ANNOTATED_DATA', 'default/path/to/Augmented Annotated Data')

    # Erstellen des Ausgabeverzeichnisses, falls es nicht existiert
    if not os.path.exists(augmented_annotated_data):
        os.makedirs(augmented_annotated_data)

    # Verarbeitung jeder Datei im Verzeichnis
    for file_name in os.listdir(annotated_data_directory):
        if file_name.endswith('.jsonl'):
            input_file_path = os.path.join(annotated_data_directory, file_name)
            dummy_copies = create_dummy_copies(input_file_path)
            
            # Speichern der Dummy-Kopien
            for i, dummy in enumerate(dummy_copies):
                output_file_name = f"{os.path.splitext(file_name)[0]}_dummy_{i+1}.jsonl"
                output_file_path = os.path.join(augmented_annotated_data, output_file_name)
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    for eintrag in dummy:
                        json.dump(eintrag, file, ensure_ascii=False)
                        file.write('\n')

if __name__ == "__main__":
    main()
