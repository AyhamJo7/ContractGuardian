import os
import sys
import argparse
import joblib
import pandas as pd
from a_text_extraction import PDFTextExtractor
from b_text_cleaning import TextCleaning
from c_text_to_json import process_directory
from d_parsing import batch_process, generate_report
from e_flags import process_flags

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

def main(pdf_file_path, temp_dir):
    os.makedirs(temp_dir, exist_ok=True)
    report_output_file = process_text(pdf_file_path, temp_dir)
    if report_output_file:
        df = process_flags(report_output_file, os.path.join(temp_dir, 'processed_report.csv'))
        tfidf_vectorizer = joblib.load('C:\\Users\\ayham\\Desktop\\Projekt\\ContractGuardian\\tfidf_vectorizer.joblib')
        models = load_models()
        predictions = predict_flags(df, models, tfidf_vectorizer)
        print(predictions)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process PDF files and predict flags.")
    parser.add_argument("pdf_file_path", type=str, help="Path to the PDF file")
    parser.add_argument("--temp_dir", type=str, default="temp", help="Temporary directory for processing")
    args = parser.parse_args()

    main(args.pdf_file_path, args.temp_dir)
