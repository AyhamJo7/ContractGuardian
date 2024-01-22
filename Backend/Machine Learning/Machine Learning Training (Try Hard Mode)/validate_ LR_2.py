import os
import json
import pandas as pd
import joblib
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Pfadvariablen mit os.getenv()
lr_model_l1_load_path = os.getenv('LR_MODEL_L1_SAVE_PATH', 'default/path/to/model_l1.pkl')
lr_model_l2_load_path = os.getenv('LR_MODEL_L2_SAVE_PATH', 'default/path/to/model_l2.pkl')
unannotated_data_path = os.getenv('UNANNOTATED_DATA_PATH', 'default/path/to/Data/PDFs')

# Definiere Label-Kategorien
label_categories = [
    'Section', 'Subsection', 'TITEL', 'Firma', 'Sitz', 'Gegenstand',
    'Stammkapital', 'Stammeinlagen', 'Geschäftsführung', 'Vertretung',
    'Dauer', 'Geschäftsjahr', 'Gesellschafterversammlung', 'Veräußerung',
    'Gewinnverteilung', 'Einziehung', 'Erbfolge', 'Kündigung', 'Abfindung',
    'Wettbewerb', 'Schlussbestimmungen', 'Gesellschafterbeschlüsse',
    'Jahresabschluss', 'Ergebnisverwendung', 'Kosten', 'Salvatorische Klausel',
    'Sonstige_Klauseln', 'RED FLAG', 'Orange Flag', 'Green Flag'
]

# Funktion zum Extrahieren von Merkmalen aus einer JSONL-Datenzeile
def extract_features(json_data): 
    entities = json_data.get('entities', [])
    features = {label: sum(1 for entity in entities if entity['label'] == label) for label in label_categories}
    return features

# Funktion zum Verarbeiten einer einzelnen JSONL-Datei 
def process_jsonl(file_path):
    features_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.strip():
                try:
                    json_data = json.loads(line)
                    features = extract_features(json_data)
                    features_list.append(features)
                except json.JSONDecodeError:
                    print(f"Warnung: Ungültige JSON-Daten in Datei {file_path} übersprungen")
    return features_list

# Geladene Modelle 
model_l1 = joblib.load(lr_model_l1_load_path)
model_l2 = joblib.load(lr_model_l2_load_path)

# Verarbeite die unannotierten Daten 
unannotated_features = []
unannotated_jsonl_files = [os.path.join(unannotated_data_path, file) for file in os.listdir(unannotated_data_path) if file.endswith('.jsonl')]

for file_path in unannotated_jsonl_files:
    file_features = process_jsonl(file_path)
    unannotated_features.extend(file_features)

# Konvertiere die unannotierten Merkmale in einen DataFrame
X_unannotated = pd.DataFrame(unannotated_features)

# Vorhersagen für unannotierte Daten mit den trainierten Modellen treffen
predictions_l1_unannotated = model_l1.predict(X_unannotated)
predictions_l2_unannotated = model_l2.predict(X_unannotated)

# Drucke die Vorhersagen für die unannotierten Daten
print("Vorhersagen mit L1-Regularisierung:")
print(predictions_l1_unannotated)

print("Vorhersagen mit L2-Regularisierung:")
print(predictions_l2_unannotated)
