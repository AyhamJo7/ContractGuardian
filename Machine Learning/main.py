import os
import sys
import json
import argparse
import joblib
import pandas as pd
from a_text_extraction import PDFTextExtractor
from b_text_cleaning import TextCleaning
from c_text_to_json import process_directory
from d_parsing import batch_process, generate_report
from e_flags import process_flags
import shutil


def extract_text(pdf_file_path, temp_dir):
    pdf_text_extractor = PDFTextExtractor(pdf_directory=temp_dir, output_directory=temp_dir)
    return pdf_text_extractor.extract_text_from_pdf(pdf_file_path)

def clean_text(text, temp_dir):
    text_cleaner = TextCleaning(input_directory=temp_dir, output_directory=temp_dir)
    return text_cleaner.clean_text(text)

def process_text(pdf_file_path, temp_dir):
    try:
        pdf_text = extract_text(pdf_file_path, temp_dir)
        txt_file_path = os.path.join(temp_dir, os.path.basename(pdf_file_path).replace('.pdf', '.txt'))
        with open(txt_file_path, 'w', encoding='utf-8') as file:
            file.write(pdf_text)
        cleaned_text = clean_text(pdf_text, temp_dir)
        process_directory(input_directory=temp_dir, output_directory=temp_dir)
        all_data = batch_process(directory=temp_dir)
        report_output_file = os.path.join(temp_dir, 'report.csv')
        generate_report(all_data, report_output_file)
        return report_output_file
    except Exception as e:
        print(f"Error during text processing: {str(e)}")
        return None

def load_models():
    models = {}
    for target in ['Has_Red_Flag', 'Has_Orange_Flag', 'Has_Green_Flag']:
        model_filename = f'C:\\Users\\ayham\\Desktop\\Projekt\\ContractGuardian\\trained_model_{target}.joblib'
        models[target] = joblib.load(model_filename)
    return models

def predict_flags(df, models, tfidf_vectorizer):
    try:
        df.columns = df.columns.astype(str)
        X_flags = tfidf_vectorizer.transform(df['Flags'])
        X_flags_df = pd.DataFrame(X_flags.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
        X_flags_df.columns = X_flags_df.columns.astype(str)
        X = pd.concat([X_flags_df, df[['Flags_Code']].astype(str)], axis=1)
        predictions = {}
        for target in models:
            predictions[target] = models[target].predict(X)
        return predictions
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return None
    
def interpret_and_print_results(csv_file_path):
    df = pd.read_csv(csv_file_path)
    


    # Define the clauses for each flag type
    red_flag_clauses = ['Firma', 'Sitz', 'Gegenstand']
    red_flag_alternative_clauses = {
        'Stammkapital': ['Stammkapital', 'Kapital'],
        'Stammeinlagen': ['Stammeinlagen', 'Einlagen', 'Geschäftsanteile']
    }
    orange_flag_clauses = ['Dauer', 'Vertretung']
    orange_flag_alternative_clauses = {
        'Geschäftsführung': ['Geschäftsführung', 'führung'],
        'Geschäftsjahr': ['Geschäftsjahr', 'jahr'],
        'Gesellschafterversammlung': ['Gesellschafterversammlung', 'versammlung']
    }
    green_flag_clauses = ['Kündigung', 'Abfindung', 'Wettbewerb', 'Jahresabschluss', 'Schlussbestimmungen', 'Veräußerung', 'Einziehung', 'Gesellschafterbeschlüsse', 'Auflösung']
    green_flag_alternative_clauses = {
        'Gewinn': ['Gewinnverteilung', 'Gewinn', 'Ergebnisverwendung'],
        'Kosten': ['Kosten', 'Gründungskosten'],
        'Salvatorische Klauseln': ['Salvatorische', 'Salvatorische Klauseln'],
        'Erbfolge': ['Erbfolge', 'Tod']
    }

    # Function to check if clauses or their alternatives are present in the text
    def check_clauses_in_text(clauses, alternative_clauses, text):
        found_clauses = []
        for clause, alternatives in alternative_clauses.items():
            if any(alt in text for alt in alternatives):
                found_clauses.append(clause)
        found_clauses.extend([clause for clause in clauses if clause in text])
        return found_clauses

    # Concatenate all text to search for clauses
    all_text = ' '.join(df['Section'].tolist())

    # Check for each clause in the text
    red_flags_found = check_clauses_in_text(red_flag_clauses, red_flag_alternative_clauses, all_text)
    orange_flags_found = check_clauses_in_text(orange_flag_clauses, orange_flag_alternative_clauses, all_text)
    green_flags_found = check_clauses_in_text(green_flag_clauses, green_flag_alternative_clauses, all_text)

    results = {
        'Red Flags': [{'name': clause, 'status': '[OK]' if clause in red_flags_found else '[X]'} for clause in red_flag_clauses + list(red_flag_alternative_clauses.keys())],
        'Orange Flags': [{'name': clause, 'status': '[OK]' if clause in orange_flags_found else '[X]'} for clause in orange_flag_clauses + list(orange_flag_alternative_clauses.keys())],
        'Green Flags': [{'name': clause, 'status': '[OK]' if clause in green_flags_found else '[X]'} for clause in green_flag_clauses + list(green_flag_alternative_clauses.keys())],
    }
    results_json = json.dumps(results)
    return results_json



def main(pdf_file_path, temp_dir):
    os.makedirs(temp_dir, exist_ok=True)
    report_output_file = process_text(pdf_file_path, temp_dir)
    if report_output_file:
        df = process_flags(report_output_file, os.path.join(temp_dir, 'processed_report.csv'))
        tfidf_vectorizer = joblib.load('C:\\Users\\ayham\\Desktop\\Projekt\\ContractGuardian\\tfidf_vectorizer.joblib')
        models = load_models()
        predictions = predict_flags(df, models, tfidf_vectorizer)

        # Save the DataFrame to a CSV file and then interpret and print the results
        processed_csv_path = os.path.join(temp_dir, 'processed_report.csv')
        df.to_csv(processed_csv_path, index=False)
        json_results = interpret_and_print_results(processed_csv_path)
        shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        print(json_results)  # Print the JSON for debugging purposes
        return json_results
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process PDF files and predict flags.")
    parser.add_argument("pdf_file_path", type=str, help="Path to the PDF file")
    parser.add_argument("--temp_dir", type=str, default="temp", help="Temporary directory for processing")
    args = parser.parse_args()
    main(args.pdf_file_path, args.temp_dir)