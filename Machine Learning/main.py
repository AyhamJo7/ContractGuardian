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
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()


# Text aus einer PDF extrahieren
def extract_text(pdf_file_path, temp_dir):
    pdf_text_extractor = PDFTextExtractor(pdf_directory=temp_dir, extracted_text_directory=temp_dir)
    return pdf_text_extractor.extract_text_from_pdf(pdf_file_path)

# Text bereinigen
def clean_text(text, temp_dir):
    text_cleaner = TextCleaning(extracted_text_directory=temp_dir, cleaned_text_directory=temp_dir)
    return text_cleaner.clean_text(text)

# Textverarbeitung
def process_text(pdf_file_path, temp_dir):
    try:
        pdf_text = extract_text(pdf_file_path, temp_dir)
        txt_file_path = os.path.join(temp_dir, os.path.basename(pdf_file_path).replace('.pdf', '.txt'))
        with open(txt_file_path, 'w', encoding='utf-8') as file:
            file.write(pdf_text)
        cleaned_text = clean_text(pdf_text, temp_dir)
        process_directory(cleaned_text_directory =temp_dir, converted_to_json_directory=temp_dir)
        all_data = batch_process(converted_to_json_directory=temp_dir)
        parsed_csv_file = os.path.join(temp_dir, 'report.csv')
        generate_report(all_data, parsed_csv_file)
        return parsed_csv_file
    except Exception as e:
        print(f"Fehler bei der Textverarbeitung: {str(e)}")
        return None

# Modelle laden
def load_models():
    models = {}
    for target in ['Has_Red_Flag', 'Has_Orange_Flag', 'Has_Green_Flag']:
        model_filename = os.path.join(os.getenv('LOAD_FOR_TRAINING_PATH', 'default/path/to/Load for Training'), f'trained_model_{target}.joblib')
        models[target] = joblib.load(model_filename)
    return models

# Vorhersage der Flags
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
    
# Ergebnisse interpretieren und ausgeben
def interpret_and_print_results(csv_file_path):
    df = pd.read_csv(csv_file_path)
    

    # Define the clauses for each flag type
    red_flag_clauses = ['Firma', 'Sitz', 'Gegenstand']
    red_flag_alternative_clauses = {
        'Stammkapital': ['Stammkapital', 'Kapital'],
        'Stammeinlagen': ['Stammeinlagen', 'Einlagen', 'Geschäftsanteile']
    }
    orange_flag_clauses = ['Dauer']
    orange_flag_alternative_clauses = {
        'Geschäftsführung': ['Geschäftsführung', 'führung', 'Geschäftsführer'],
        'Geschäftsjahr': ['Geschäftsjahr', 'jahr', 'Jahr'],
        'Gesellschafterversammlung': ['Gesellschafterversammlung', 'versammlung'],
        'Vertretung':['Vertretung','vertreten','Einzelvertretungsbefugnis']
    }
    green_flag_clauses = ['Kündigung', 'Jahresabschluss', 'Schlussbestimmungen', 'Veräußerung', 'Einziehung', 'Verfügung über Geschäftsanteile', 'Beirat', 'Schlichtungsvereinbarung']
    green_flag_alternative_clauses = {
        'Gewinn': ['Gewinnverteilung', 'Gewinn', 'Ergebnisverwendung'],
        'Kosten': ['Kosten', 'Gründungskosten', 'Gründungsaufwand'],
        'Salvatorische Klauseln': ['Salvatorische', 'Salvatorische Klauseln'],
        'Erbfolge': ['Erbfolge', 'Tod'],
        'Gesellschafterbeschlüsse': ['Gesellschafterbeschlüsse','Beschlüsse'],
        'Abfindung' : ['Abfindung','Vergütung'],
        'Auflösung ': ['Beendigung','Beendigung der Gesellschaft','Auflösung'],
        'Wettbewerbsverbot': ['Wettbewerbsverbot', 'Wettbewerb']   
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
        'Red Flags': [{'name': clause, 'status': '✓' if clause in red_flags_found else '✗'} for clause in red_flag_clauses + list(red_flag_alternative_clauses.keys())],
        'Orange Flags': [{'name': clause, 'status': '✓' if clause in orange_flags_found else '✗'} for clause in orange_flag_clauses + list(orange_flag_alternative_clauses.keys())],
        'Green Flags': [{'name': clause, 'status': '✓' if clause in green_flags_found else '✗'} for clause in green_flag_clauses + list(green_flag_alternative_clauses.keys())],
    }
    results_json = json.dumps(results)
    return results_json

# Hauptfunktion
def main(pdf_file_path, temp_dir):
    os.makedirs(temp_dir, exist_ok=True)
    report_output_file = process_text(pdf_file_path, temp_dir)
    if report_output_file:
        df = process_flags(report_output_file, os.path.join(temp_dir, 'processed_report.csv'))
        tfidf_vectorizer = joblib.load(os.path.join(os.getenv('LOAD_FOR_TRAINING_PATH', 'default/path/to/Load for Training'), 'tfidf_vectorizer.joblib'))
        models = load_models()
        predictions = predict_flags(df, models, tfidf_vectorizer)

        # Ergebnisse speichern und ausgeben
        processed_csv_path = os.path.join(temp_dir, 'processed_report.csv')
        df.to_csv(processed_csv_path, index=False)
        json_results = interpret_and_print_results(processed_csv_path)
        shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        print(json_results)  # JSON-Ergebnisse zur Debugging-Zwecken ausgeben
        return json_results

# Ausführung des Skripts
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verarbeitet PDF-Dateien und prognostiziert Flags.")
    parser.add_argument("pdf_file_path", type=str, help="Pfad zur PDF-Datei")
    parser.add_argument("--temp_dir", type=str, default="temp", help="Temporäres Verzeichnis für die Verarbeitung")
    args = parser.parse_args()
    main(args.pdf_file_path, args.temp_dir)

