import os
import json
import spacy

# Load spaCy German model
nlp = spacy.load("de_core_news_sm")

# Define the input and output directories
input_directory = '/Users/adamj7/Desktop/3.jsonl'
output_directory = '/Users/adamj7/Desktop/4.spacy'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Function to process each file and save the results
def process_file(file_path, output_directory):
    output_file = os.path.join(output_directory, os.path.basename(file_path).replace('.jsonl', '_processed.txt'))
    
    with open(file_path, 'r', encoding='utf-8') as file, open(output_file, 'w', encoding='utf-8') as out_file:
        for line in file:
            data = json.loads(line)
            doc = nlp(data['text'])
            # Write entities to output file
            for ent in doc.ents:
                out_file.write(f"{ent.text}\t{ent.label_}\n")

# Iterate over files in the input directory
if os.path.isdir(input_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith(".jsonl"):
            file_path = os.path.join(input_directory, filename)
            process_file(file_path, output_directory)
            print(f"Processed {filename}")
else:
    print(f"Input path {input_directory} is not a directory.")
