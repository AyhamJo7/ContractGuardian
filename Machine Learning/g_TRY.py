import os
import joblib
import pandas as pd
from a_text_extraction import PDFTextExtractor
from b_text_cleaning import TextCleaning
from c_text_to_json import process_directory
from parsing import batch_process, generate_report
from flags import process_flags
from sklearn.feature_extraction.text import TfidfVectorizer


def main():
    # Step 1: Define paths and directories
    pdf_file_path = 'C:\\Users\\ayham\\Desktop\\Projekt\\ContractGuardian\\Data\\PDFs\\4Sports GmbH.pdf'
    temp_dir = 'temp'

    # Create a temporary directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)

    # Step 2: Extract and save text from the PDF
    pdf_text_extractor = PDFTextExtractor(pdf_directory=temp_dir, output_directory=temp_dir)
    pdf_text = pdf_text_extractor.extract_text_from_pdf(pdf_file_path)
    txt_file_path = os.path.join(temp_dir, os.path.basename(pdf_file_path).replace('.pdf', '.txt'))
    with open(txt_file_path, 'w', encoding='utf-8') as file:
        file.write(pdf_text)

    # Step 3: Clean the extracted text
    text_cleaner = TextCleaning(input_directory=temp_dir, output_directory=temp_dir)
    cleaned_text = text_cleaner.clean_text(pdf_text)

    # Step 4: Convert cleaned text to JSONL format
    process_directory(input_directory=temp_dir, output_directory=temp_dir)

    # Step 5: Parse the JSONL files and generate a report
    all_data = batch_process(directory=temp_dir)
    report_output_file = os.path.join(temp_dir, 'report.csv')
    generate_report(all_data, report_output_file)

    # Step 6: Process the flags in the report
    processed_report_file = os.path.join(temp_dir, 'processed_report.csv')
    df = process_flags(report_output_file, processed_report_file)

    # Step 7: Load the trained model
    model_filename = 'trained_model.joblib'
    loaded_model = joblib.load(model_filename)

    # Step 8: Prepare the input data for model prediction
    try:
        # Convert column names to strings
        df.columns = df.columns.astype(str)

        # Text Vectorization using TF-IDF
        tfidf_vectorizer = TfidfVectorizer()
        X_flags = tfidf_vectorizer.fit_transform(df['Flags'])

        # Create a DataFrame from the TF-IDF matrix
        X_flags_df = pd.DataFrame(X_flags.toarray())
        X_flags_df.columns = X_flags_df.columns.astype(str)  # Convert feature names to strings
        X = pd.concat([X_flags_df, df[['Flags_Code']]], axis=1)
        X.columns = X.columns.astype(str)  # Ensure all column names are of type string

        # Make predictions on the input data using the loaded model
        y_pred = loaded_model.predict(X)
        print(y_pred)

    except Exception as e:
        print(f"Error in model prediction: {str(e)}")



if __name__ == "__main__":
    main()
