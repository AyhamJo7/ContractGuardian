import os
import json
import pandas as pd
import joblib
from sklearn.metrics import classification_report

# Define your label categories
label_categories = [
    'Section', 'Subsection', 'TITEL', 'Firma', 'Sitz', 'Gegenstand',
    'Stammkapital', 'Stammeinlagen', 'Geschäftsführung', 'Vertretung',
    'Dauer', 'Geschäftsjahr', 'Gesellschafterversammlung', 'Veräußerung',
    'Gewinnverteilung', 'Einziehung', 'Erbfolge', 'Kündigung', 'Abfindung',
    'Wettbewerb', 'Schlussbestimmungen', 'Gesellschafterbeschlüsse',
    'Jahresabschluss', 'Ergebnisverwendung', 'Kosten', 'Salvatorische Klausel',
    'Sonstige_Klauseln', 'RED FLAG', 'Orange Flag', 'Green Flag'
]

# Define the function to extract features from a JSONL data line
def extract_features(json_data):
    entities = json_data.get('entities', [])
    features = {label: sum(1 for entity in entities if entity['label'] == label) for label in label_categories}
    return features

# Define the function to process a single JSONL file
# Define the function to process a single JSONL file
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
                    print(f"Warning: Skipping invalid JSON data in file {file_path}")
    return features_list

# Load the trained models
desktop_model_l1_load_path = 'C:/Users/ayham/Desktop/model_l1.pkl'
desktop_model_l2_load_path = 'C:/Users/ayham/Desktop/model_l2.pkl'

model_l1 = joblib.load(desktop_model_l1_load_path)
model_l2 = joblib.load(desktop_model_l2_load_path)

# Define the directory path for your unannotated dataset
unannotated_data_path = 'C:/Users/ayham/Desktop/hehe'

# Process the unannotated data
unannotated_features = []
unannotated_jsonl_files = [os.path.join(unannotated_data_path, file) for file in os.listdir(unannotated_data_path) if file.endswith('.jsonl')]

for file_path in unannotated_jsonl_files:
    file_features = process_jsonl(file_path)
    unannotated_features.extend(file_features)

# Convert the unannotated features into a DataFrame
X_unannotated = pd.DataFrame(unannotated_features)

# Make predictions on the unannotated dataset using the trained models
predictions_l1_unannotated = model_l1.predict(X_unannotated)
predictions_l2_unannotated = model_l2.predict(X_unannotated)

# Print the predictions for the unannotated dataset
print("Predictions using L1 Regularization:")
print(predictions_l1_unannotated)

print("Predictions using L2 Regularization:")
print(predictions_l2_unannotated)
