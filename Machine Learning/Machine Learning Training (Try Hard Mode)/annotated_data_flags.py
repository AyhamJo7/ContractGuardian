import pandas as pd
import os
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

def process_flags(annotated_parsed_csv_file, dataset_path):
    # Einlesen der CSV-Datei
    df = pd.read_csv(annotated_parsed_csv_file)
    # Anwendung von ffill() gemäß der Warnungsvorschläge
    df.ffill(inplace=True)
    df['Flags'] = df['Flags'].astype(str)
    df['Flags_Code'] = pd.Categorical(df['Flags']).codes

    # Flag-Berechnungen
    df['Has_Red_Flag'] = df['Flags'].str.contains('RED FLAG').astype(int)
    df['Has_Orange_Flag'] = df['Flags'].str.contains('Orange Flag').astype(int)
    df['Has_Green_Flag'] = df['Flags'].str.contains('Green Flag').astype(int)

    # Speichern der bearbeiteten DataFrame in eine CSV-Datei
    df.to_csv(dataset_path, index=False)

    # Stellen Sie sicher, dass alle Spaltennamen vom Typ String sind
    df.columns = df.columns.astype(str)
    return df

# Beispielhafte Verwendung
if __name__ == "__main__":
    annotated_parsed_csv_file = os.getenv('ANNOTATED_PARSED_CSV_FILE', 'default/path/to/anno_report.csv')
    dataset_path = os.getenv('DATASET_PATH', 'default/path/to/anno_processed_report.csv')
    processed_df = process_flags(annotated_parsed_csv_file, dataset_path)
