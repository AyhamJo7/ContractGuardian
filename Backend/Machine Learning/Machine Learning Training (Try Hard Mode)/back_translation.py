from transformers import pipeline
import os
import json
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei 
load_dotenv()

# Initialisierung der Übersetzungs-Pipelines 
translator_to_en = pipeline("translation", model="Helsinki-NLP/opus-mt-de-en")
translator_to_de = pipeline("translation", model="Helsinki-NLP/opus-mt-en-de")

# Laden der annotierten Daten
annotated_data_directory = os.getenv('ANNOTATED_DATA_DIRECTORY', 'default/path/to/Annotated Data')
files = os.listdir(annotated_data_directory)

data = []
for file in files:
    with open(os.path.join(annotated_data_directory, file), 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))

chunk_size = 400  # Ggf. weiter reduzieren

# Funktion zum Zerlegen des Textes in kleinere Segmente
def chunk_text(text, chunk_size):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Funktion zur Rückübersetzung von Textsegmenten
def back_translate_chunks(chunks, translator_to_en, translator_to_de, max_length=512):
    translated_chunks = []
    for chunk in chunks:
        try:
            if len(chunk) > 0:
                translation_en = translator_to_en(chunk, max_length=max_length)[0]['translation_text']
                translation_de = translator_to_de(translation_en, max_length=max_length)[0]['translation_text']
                translated_chunks.append(translation_de)
        except Exception as e:
            print(f"Fehler bei der Übersetzung: {e}")
            translated_chunks.append(chunk)  # Originalsegment bei Fehler verwenden
    return ''.join(translated_chunks)

# Verarbeitung jeder Datei
back_translated_annotated_data = os.getenv('BACK_TRANSLATED_ANNOTATED_DATA', 'default/path/to/Back Translated Annotated Data')
os.makedirs(back_translated_annotated_data, exist_ok=True)

for i, item in enumerate(data):
    text = item['text']
    chunks = chunk_text(text, chunk_size)
    back_translated_text = back_translate_chunks(chunks, translator_to_en, translator_to_de)
    item['back_translated_text'] = back_translated_text

    # Speichern des aktualisierten Elements
    with open(os.path.join(back_translated_annotated_data, f'augmented_{i}.json'), 'w', encoding='utf-8') as f:
        json.dump(item, f, ensure_ascii=False, indent=4)
