import json
import os

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def split_into_sections(text, delimiter='§'):
    return text.split(delimiter)[1:]

def save_jsonl(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for entry in data:
            json.dump(entry, file, ensure_ascii=False)
            file.write('\n')

def process_directory(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_directory, filename)
            text = read_file(file_path)
            sections = split_into_sections(text)
            json_data = [{"text": section.strip()} for section in sections]
            output_file = os.path.join(output_directory, filename.replace('.txt', '.jsonl'))
            save_jsonl(json_data, output_file)
            print(f"Processed {filename}")

""" # Specify the input and output directory paths
input_directory = 'C:/Users/ayham/Desktop/2.text'
output_directory = 'C:/Users/ayham/Desktop/3.jsonl'
process_directory(input_directory, output_directory) """


# Specify the input and output directory paths
input_directory = '/Users/adamj7/Desktop/2.text'
output_directory = '/Users/adamj7/Desktop/3.jsonl'
process_directory(input_directory, output_directory)
