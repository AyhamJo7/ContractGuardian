import os
import json
import spacy
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Laden des spaCy-Deutsch-Modells
nlp = spacy.load("de_core_news_sm")

class JSONLTextProcessor:
    def __init__(self, converted_to_json_directory, spacy_processed_texts):
        """
        Initialisiert die JSONLTextProcessor-Klasse.
        :param converted_to_json_directory: Verzeichnis mit JSONL-Dateien. 
        :param spacy_processed_texts: Verzeichnis, in dem verarbeitete Textdateien gespeichert werden. 
        """
        self.converted_to_json_directory = converted_to_json_directory
        self.spacy_processed_texts = spacy_processed_texts
        os.makedirs(self.spacy_processed_texts, exist_ok=True)

    def process_file(self, file_path):
        """
        Verarbeitet eine JSONL-Datei und speichert die Ergebnisse. 
        :param file_path: Pfad zur JSONL-Datei. 
        """
        output_file = os.path.join(
            self.spacy_processed_texts,
            os.path.basename(file_path).replace('.jsonl', '_processed.txt')
        )

        with open(file_path, 'r', encoding='utf-8') as file, open(output_file, 'w', encoding='utf-8') as out_file:
            for line in file:
                data = json.loads(line)
                doc = nlp(data['text'])
                # Schreibt Entitäten in die Ausgabedatei
                for ent in doc.ents:
                    out_file.write(f"{ent.text}\t{ent.label_}\n")

    def process_all_jsonl_files(self):
        """
        Verarbeitet alle JSONL-Dateien im Eingabeverzeichnis und speichert die verarbeiteten Textdateien im Ausgabeverzeichnis.
        """
        for filename in os.listdir(self.converted_to_json_directory):
            if filename.endswith(".jsonl"):
                file_path = os.path.join(self.converted_to_json_directory, filename)
                self.process_file(file_path)
                print(f"Verarbeitet: {filename}")

if __name__ == "__main__":
    converted_to_json_directory = os.getenv('CONVERTED_TO_JSON_DIRECTORY', 'default/path/to/Converted To JSON Results')
    spacy_processed_texts = os.getenv('SPACY_PROCESSED_TEXTS', 'default/path/to/Spacy Processed Texts')
    processor = JSONLTextProcessor(converted_to_json_directory, spacy_processed_texts)
    processor.process_all_jsonl_files()
