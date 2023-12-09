import os
import re
from contract_parser import ContractParser  # Ensure this matches the name of your file containing ContractParser

class RedFlagDetector:
    def __init__(self, text):
        self.parser = ContractParser(text)

    def check_red_flags(self):
        """
        Überprüft auf rote Flaggen in Verträgen.
        :return: Ein Dictionary mit den roten Flaggen.
        """
        self.parser.parse()  
        red_flags = {
            "Firma": self.check_if_empty("Firma"),
            "Sitz, Niederlassung, etc.": self.check_if_empty("Sitz, Niederlassung, inländische Geschäftsanschrift, empfangsberechtigte Person, Zweigniederlassungen"),
            "Gegenstand des Unternehmens": self.check_if_empty("Gegenstand des Unternehmens"),
            "Grund- oder Stammkapital": self.check_if_empty("Grund- oder Stammkapital")
        }
        return red_flags

    def check_if_empty(self, section_name):
        """
        Überprüft, ob ein Abschnitt leer oder unzureichend spezifiziert ist.
        :param section_name: Name des Abschnitts, der überprüft werden soll.
        :return: True, wenn der Abschnitt ein Problem darstellt, sonst False.
        """
        parsed_data = self.parser.parsed_data
        if section_name not in parsed_data:
            return True  # Rote Flag, falls Klausel fehlt
        content = parsed_data[section_name]
        return content in ["-", "   ", "---", "--", " ", "  "]  

def process_text_files(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    file_counter = 1
    for filename in os.listdir(input_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                red_flag_detector = RedFlagDetector(text)
                red_flags = red_flag_detector.check_red_flags()

                # Gleiche Name mit "_p_d" am Ende
                output_file_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}_p_d.txt")
                
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    for flag, present in red_flags.items():
                        if present:
                            output_file.write(f"{flag}: FEHLT ODER UNZUREICHEND SPEZIFIZIERT\n")
            file_counter += 1

if __name__ == "__main__":
    input_directory = 'C:/Users/ayham/Desktop/txt'
    output_directory = 'C:/Users/ayham/Desktop/flag_detector'
    process_text_files(input_directory, output_directory)
