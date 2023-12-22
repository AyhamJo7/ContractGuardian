import os
import json
import spacy

# Laden des spaCy-Deutsch-Modells
nlp = spacy.load("de_core_news_sm")

class JSONLTextProcessor:
    def __init__(self, input_directory, output_directory):
        """
        Initialisiert die JSONLTextProcessor-Klasse.
        :param input_directory: Verzeichnis mit JSONL-Dateien.
        :param output_directory: Verzeichnis, in dem verarbeitete Textdateien gespeichert werden.
        """
        self.input_directory = input_directory
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def process_file(self, file_path):
        """
        Verarbeitet eine JSONL-Datei und speichert die Ergebnisse.
        :param file_path: Pfad zur JSONL-Datei.
        """
        output_file = os.path.join(
            self.output_directory,
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
        if os.path.isdir(self.input_directory):
            for filename in os.listdir(self.input_directory):
                if filename.endswith(".jsonl"):
                    file_path = os.path.join(self.input_directory, filename)
                    self.process_file(file_path)
                    print(f"Verarbeitet: {filename}")
        else:
            print(f"Eingabepfad {self.input_directory} ist kein Verzeichnis.")

if __name__ == "__main__":
    # Beispielverwendung MacOS
    input_directory = '/Users/adamj7/Desktop/3.jsonl'
    output_directory = '/Users/adamj7/Desktop/4.spacy'
    processor = JSONLTextProcessor(input_directory, output_directory)
    processor.process_all_jsonl_files()
        
