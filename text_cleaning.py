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
        # Remove pagination
        text = self.remove_pagination(text)
        # Remove spaces from titles
        text = self.remove_spaces_from_title(text)


        return text

    def remove_pagination(self, text):
        # Remove 'Seite X von Y' where X and Y are digits
        text = re.sub(r'Seite\s+\d+\s+von\s+\d+', '', text)
        
        # Remove '-Seite X-' where X is a digit
        text = re.sub(r'-Seite\s+\d+-', '', text)

        # Remove '-X-' where X is a digit, surrounded by dashes
        text = re.sub(r'-\d+-', '', text)

        # Remove '- X -' where X is a digit, surrounded by dashes and spaces
        text = re.sub(r'-\s+\d+\s+-', '', text)

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

        return text

    def remove_irrelevant_info(self, text):
        # Remove file paths ending with .docx
        text = re.sub(r'\\\\.*?\.docx', '', text)
        # Remove agreement numbers: 6 or 7 digits followed by up to two capital letters and an optional version number
        text = re.sub(r'\b\d{6,7}[A-Z]{0,2}(v\d)?\b', '', text)
        # Remove pattern like "(StA: year:numbers, Referenz: numbers, Doc: numbers)"
        text = re.sub(r'\(StA:\s+\d{4}:\d+,\s+Referenz:\s*\d*(,\s+Doc:\s*\d*\.?\d*)?\)', '', text)
        # Remove patterns starting with 'tmp' followed by alphanumeric characters
        text = re.sub(r'\btmp[A-Za-z0-9]+\b', '', text)
        # Remove patterns starting with 'cvc' or 'cvd' followed by alphanumeric characters, underscores, or hyphens
        text = re.sub(r'\b(cv[c|d])[A-Za-z0-9_\-]+\b', '', text)
        # Remove the specific phrase "- Ende der Satzung -"        
        text = re.sub(r'-\s*Ende\s*der\s*Satzung\s*-', '', text)
        # Remove the pattern of three stars at the end of the document
        text = re.sub(r'\* \* \*$', '', text)


        return text

    def remove_spaces_from_title(self, text):
        # Patterns to match and correct spaced words
        patterns_to_correct = {
            r'G\s+E\s+S\s+E\s+L\s+L\s+S\s+C\s+H\s+A\s+F\s+T\s+S\s+V\s+E\s+R\s+T\s+R\s+A\s+G': 'GESELLSCHAFTSVERTRAG',
            r'G\s+E\s+S\s+E\s+L\s+L\s+S\s+C\s+H\s+A\s+F\s+T\s+E\s+R\s+V\s+E\s+R\s+T\s+R\s+A\s+G': 'GESELLSCHAFTERVERTRAG',
            r'S\s+A\s+T\s+Z\s+U\s+N\s+G': 'SATZUNG'
        }

        for pattern, replacement in patterns_to_correct.items():
            text = re.sub(pattern, replacement, text)

        return text

    def process_all_texts(self):
        for filename in os.listdir(self.input_directory):
            if filename.lower().endswith('.txt'):
                input_file_path = os.path.join(self.input_directory, filename)
                with open(input_file_path, 'r', encoding='utf-8') as file:
                    text = file.read()

                cleaned_text = self.clean_text(text)

                output_file_path = os.path.join(self.output_directory, 'c_' + filename)
                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(cleaned_text)
                print(f"Processed: {filename} --> c_{filename}")


# Example usage
input_directory = 'C:/Users/ayham/Desktop/1.text'
output_directory = 'C:/Users/ayham/Desktop/2.text'
cleaner = TextCleaning(input_directory, output_directory)
cleaner.process_all_texts()
