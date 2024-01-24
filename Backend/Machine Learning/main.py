import os
import sys
import json
import argparse
import joblib
import pandas as pd
import shutil
import logging
from a_text_extraction import PDFTextExtractor
from b_text_cleaning import TextCleaning
from c_text_to_json import process_directory
from d_parsing import batch_process, generate_report
from e_flags import process_flags
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

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
        process_directory(cleaned_text_directory=temp_dir, converted_to_json_directory=temp_dir)
        all_data = batch_process(converted_to_json_directory=temp_dir)
        parsed_csv_file = os.path.join(temp_dir, 'report.csv')
        generate_report(all_data, parsed_csv_file)
        return parsed_csv_file
    except Exception as e:
        logging.error(f"Fehler bei der Textverarbeitung: {e}", exc_info=True)
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
def interpret_and_print_results(df, predictions):
    results = {
        'Red Flags': [],
        'Orange Flags': [],
        'Green Flags': []
    }

    # Loop through predictions and add to results
    for flag_type in predictions:
        flag_results = predictions[flag_type]
        for i, flag in enumerate(flag_results):
            status = '✓' if flag == 1 else '✗'
            section = df.iloc[i]['Section']
            results[flag_type].append({'Section': section, 'Status': status})

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
        json_results = interpret_and_print_results(df, predictions)
        print(json_results)
        shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        return json_results

# Ausführung des Skripts
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verarbeitet PDF-Dateien und prognostiziert Flags.")
    parser.add_argument("pdf_file_path", type=str, help="Pfad zur PDF-Datei")
    parser.add_argument("--temp_dir", type=str, default="temp", help="Temporäres Verzeichnis für die Verarbeitung")
    args = parser.parse_args()
    main(args.pdf_file_path, args.temp_dir)
