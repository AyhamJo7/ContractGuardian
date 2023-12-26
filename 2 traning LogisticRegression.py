import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
from collections import Counter

# Definiere deine Label-Kategorien
label_categories = [
    'Section', 'Subsection', 'TITEL', 'Firma', 'Sitz', 'Gegenstand',
    'Stammkapital', 'Stammeinlagen', 'Geschäftsführung', 'Vertretung',
    'Dauer', 'Geschäftsjahr', 'Gesellschafterversammlung', 'Veräußerung',
    'Gewinnverteilung', 'Einziehung', 'Erbfolge', 'Kündigung', 'Abfindung',
    'Wettbewerb', 'Schlussbestimmungen', 'Gesellschafterbeschlüsse',
    'Jahresabschluss', 'Ergebnisverwendung', 'Kosten', 'Salvatorische Klausel',
    'Sonstige_Klauseln', 'RED FLAG', 'Orange Flag', 'Green Flag'
]

# Funktion zum Zählen des Auftretens von Labels in einer JSONL-Zeile
def count_label_occurrences(entities, label):
    return sum(1 for entity in entities if entity['label'] == label)

# Funktion zum Extrahieren von Merkmalen aus einer JSONL-Zeile
def extract_features(json_data):
    entities = json_data.get('entities', [])
    features = {label: count_label_occurrences(entities, label) for label in label_categories}
    return features

# Funktion zum Verarbeiten einer einzelnen JSONL-Datei
def process_jsonl(file_path):
    features_list = []
    labels_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line:
                json_data = json.loads(line)
                features = extract_features(json_data)
                
                # Annahme: 'RED FLAG', 'Orange Flag' und 'Green Flag' sind exklusiv
                # und geben die allgemeine Bedeutung der Klausel an
                label = 'None'
                if features['RED FLAG'] > 0:
                    label = 'Red'
                elif features['Orange Flag'] > 0:
                    label = 'Orange'
                elif features['Green Flag'] > 0:
                    label = 'Green'

                features_list.append(features)
                labels_list.append(label)
    return features_list, labels_list

# Verzeichnis, in dem deine JSONL-Dateien gespeichert sind
directory_path = 'C:/Users/ayham/Desktop/dummy data'

# Funktion zum Auflisten aller JSONL-Dateien im Verzeichnis
def list_jsonl_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.jsonl')]

# Liste aller JSONL-Dateien im Verzeichnis abrufen
jsonl_files = list_jsonl_files(directory_path)

# Merkmale und Labels aus allen Dateien sammeln
all_features = []
all_labels = []
for file_path in jsonl_files:
    file_features, file_labels = process_jsonl(file_path)
    all_features.extend(file_features)
    all_labels.extend(file_labels)

# In DataFrame konvertieren
X = pd.DataFrame(all_features)
y = pd.Series(all_labels)

# Überprüfen der Label-Verteilung
label_distribution = Counter(y)
print("Label Distribution:", label_distribution)

if len(label_distribution) < 2:
    print("Nicht genügend Klassen für das Modelltraining. Beende das Programm.")
    exit()


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)


model_l1 = LogisticRegression(penalty='l1', solver='liblinear', C=1.0, max_iter=1000)
model_l2 = LogisticRegression(penalty='l2', C=1.0, max_iter=1000)


model_l1.fit(X_train, y_train)
model_l2.fit(X_train, y_train)

predictions_l1 = model_l1.predict(X_test)
predictions_l2 = model_l2.predict(X_test)

print("L1 Regularization Model Evaluation")
print(classification_report(y_test, predictions_l1))

print("L2 Regularization Model Evaluation")
print(classification_report(y_test, predictions_l2))




""" # Anwenden von SMOTE, um das Klassenungleichgewicht zu beheben
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Daten aufteilen
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.5, random_state=42)

# L1-Regularisierung (Lasso)
model_l1 = LogisticRegression(penalty='l1', solver='liblinear', C=1.0, max_iter=1000)
model_l1.fit(X_train, y_train)

# L2-Regularisierung (Ridge)
model_l2 = LogisticRegression(penalty='l2', C=1.0, max_iter=1000)
model_l2.fit(X_train, y_train)

# Auswertung des L1-Regularisierten Modells
print("Auswertung des L1-Regularisierten Modells")
print(cross_val_score(model_l1, X_test, y_test, cv=5))

# Auswertung des L2-Regularisierten Modells
print("Auswertung des L2-Regularisierten Modells")
print(cross_val_score(model_l2, X_test, y_test, cv=5))


#OVERFITTINGGGGGGGGGGG
 """
""" Label Distribution: Counter({'Green': 3338, 'Red': 1352, 'Orange': 1350, 'None': 556})
L1 Regularization Model Evaluation
[1. 1. 1. 1. 1.]
L2 Regularization Model Evaluation
[1. 1. 1. 1. 1.] """