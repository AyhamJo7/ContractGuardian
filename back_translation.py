from transformers import pipeline
import os
import json

# Initialize translation pipelines
translator_to_en = pipeline("translation", model="Helsinki-NLP/opus-mt-de-en")
translator_to_de = pipeline("translation", model="Helsinki-NLP/opus-mt-en-de")

1# Load your annotated data
folder_path = "C:/Users/ayham/Desktop/4.anno"
files = os.listdir(folder_path)

data = []
for file in files:
    with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))

chunk_size = 400  # You might reduce this further if needed

# Function to chunk text into smaller segments
def chunk_text(text, chunk_size):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Function for back-translation of chunks
def back_translate_chunks(chunks, translator_to_en, translator_to_de, max_length=512):
    translated_chunks = []
    for chunk in chunks:
        try:
            if len(chunk) > 0:
                translation_en = translator_to_en(chunk, max_length=max_length)[0]['translation_text']
                translation_de = translator_to_de(translation_en, max_length=max_length)[0]['translation_text']
                translated_chunks.append(translation_de)
        except Exception as e:
            print(f"Error in translation: {e}")
            translated_chunks.append(chunk)  # Use original chunk in case of error
    return ''.join(translated_chunks)

# Process each file
output_folder = "C:/Users/ayham/Desktop/5.back_translation"
os.makedirs(output_folder, exist_ok=True)

for i, item in enumerate(data):
    text = item['text']
    chunks = chunk_text(text)
    back_translated_text = back_translate_chunks(chunks, translator_to_en, translator_to_de)
    item['back_translated_text'] = back_translated_text

    # Save the updated item
    with open(os.path.join(output_folder, f'augmented_{i}.json'), 'w', encoding='utf-8') as f:
        json.dump(item, f, ensure_ascii=False, indent=4)
