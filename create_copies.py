import json
import os

def read_jsonl_file(file_path):
    # JSON-Lines-Datei lesen und in eine Liste von Python-Dictionaries umwandeln
    with open(file_path, 'r', encoding='utf-8') as file:  # Stelle sicher, dass UTF-8-Codierung beim Lesen verwendet wird
        return [json.loads(line) for line in file]

def create_dummy_copies(file_path):
    original_data = read_jsonl_file(file_path)
    
    dummy_copies = []
    for i in range(len(original_data)):
        # Erstelle eine Kopie der Originaldaten, ohne das i-te Element
        kopie = original_data.copy()
        del kopie[i]
        dummy_copies.append(kopie)
    
    return dummy_copies

def main():
    input_directory = "C:\\Users\\ayham\\Desktop\\4.anno"
    output_directory = "C:\\Users\\ayham\\Desktop\\dummy data"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for file_name in os.listdir(input_directory):
        if file_name.endswith('.jsonl'):
            input_file_path = os.path.join(input_directory, file_name)
            dummy_copies = create_dummy_copies(input_file_path)
            
            for i, dummy in enumerate(dummy_copies):
                # Erstelle einen Dateinamen für die Ausgabedatei, die die Originaldatei widerspiegelt
                output_file_name = f"{os.path.splitext(file_name)[0]}_dummy_{i+1}.jsonl"
                output_file_path = os.path.join(output_directory, output_file_name)
                
                with open(output_file_path, 'w', encoding='utf-8') as file:  # Verwende UTF-8-Codierung beim Schreiben
                    for eintrag in dummy:
                        json.dump(eintrag, file, ensure_ascii=False)
                        file.write('\n')

if __name__ == "__main__":
    main()
