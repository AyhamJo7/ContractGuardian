import re
import os

class TextCleaning:

    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory
        self.output_directory = output_directory
        os.makedirs(self.output_directory, exist_ok=True)

    def clean_text(self, text):
        # Correct hyphenation
        text = self.correct_hyphenation(text)
        # Standardize formatting
        text = self.standardize_formatting(text)
        # Remove irrelevant information
        text = self.remove_irrelevant_info(text)
        return text

    def correct_hyphenation(self, text):
        # Join hyphenated words at the end of a line
        text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
        return text

    def standardize_formatting(self, text):
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)

        # Standardize paragraph breaks
        text = re.sub(r'(\.\s+)([A-Z])', r'\1\n\2', text)

        # Add other formatting rules as needed

        return text

    def remove_irrelevant_info(self, text):
        # Implement regex patterns to remove irrelevant information here
        return text

    def process_all_texts(self):
        for filename in os.listdir(self.input_directory):
            if filename.lower().endswith('.txt'):
                input_file_path = os.path.join(self.input_directory, filename)
                with open(input_file_path, 'r', encoding='utf-8') as file:
                    text = file.read()

                cleaned_text = self.clean_text(text)

                # Modify this line to add 'c_' prefix to the output file name
                output_file_path = os.path.join(self.output_directory, 'c_' + filename)
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(cleaned_text)
                print(f"Processed: {filename} --> c_{filename}")


# Example usage
input_directory = 'C:/Users/ayham/Desktop/1.text'
output_directory = 'C:/Users/ayham/Desktop/2.text'
cleaner = TextCleaning(input_directory, output_directory)
cleaner.process_all_texts()
