import pandas as pd
import os
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

def process_flags(parsed_csv_file, flags_sorted_csv_file):
    # Einlesen der CSV-Datei in einen DataFrame
    df = pd.read_csv(parsed_csv_file)
    
    # Ersetze fehlende Werte in der 'Flags'-Spalte durch 'Green Flag'
    df['Flags'].fillna('Green Flag', inplace=True)
    df['Flags'] = df['Flags'].astype(str)
    df['Flags_Code'] = pd.Categorical(df['Flags']).codes

    # Bestimme die Anwesenheit von Flags
    df['Has_Red_Flag'] = df['Flags'].str.contains('RED FLAG').astype(int)
    df['Has_Orange_Flag'] = df['Flags'].str.contains('Orange Flag').astype(int)
    df['Has_Green_Flag'] = df['Flags'].str.contains('Green Flag').astype(int)

    # Speichern des bearbeiteten DataFrames in eine neue CSV-Datei
    df.to_csv(flags_sorted_csv_file, index=False)

    # Stelle sicher, dass alle Spaltennamen vom Typ String sind
    df.columns = df.columns.astype(str)
    return df

# Beispielhafte Verwendung
""" if __name__ == "__main__":
    parsed_csv_file = os.getenv('PARSED_CSV_FILE', 'default/path/to/parsed_csv.csv')
    flags_sorted_csv_file = os.getenv('FLAGS_SORTED_CSV_FILE', 'default/path/to/flags_sorted_csv.csv')
    processed_df = process_flags(parsed_csv_file, flags_sorted_csv_file)
 """