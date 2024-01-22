import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from collections import Counter
from imblearn.over_sampling import SMOTE
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei 
load_dotenv()

# Definiere deine Label-Kategorien 
red_flags = ['Firma', 'Sitz', 'Gegenstand', 'Stammkapital', 'Stammeinlagen']
orange_flags = ['Geschäftsführung', 'Vertretung', 'Dauer', 'Geschäftsjahr', 'Gesellschafterversammlung']
green_flags = ['Veräußerung', 'Gewinnverteilung', 'Einziehung', 'Erbfolge', 'Kündigung', 
               'Abfindung', 'Wettbewerb', 'Schlussbestimmungen', 'Gesellschafterbeschlüsse',  
               'Jahresabschluss', 'Ergebnisverwendung', 'Kosten', 'Salvatorische Klausel', 'Sonstige_Klauseln']

# Verzeichnis, in dem deine JSONL-Dateien gespeichert sind 
augmented_annotated_data = os.getenv('AUGMENTED_ANNOTATED_DATA', 'default/path/to/Augmented Annotated Data')
#back_translated_annotated_data = os.getenv('BACK_TRANSLATED_ANNOTATED_DATA', 'default/path/to/Back Translated Annotated Data') 
#annotated_data_directory = os.getenv('ANNOTATED_DATA_DIRECTORY', 'default/path/to/Annotated Data') 


# Funktion zum Auflisten aller JSONL-Dateien im Verzeichnis
def list_jsonl_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.jsonl')]

# Funktion zum Verarbeiten einer einzelnen JSONL-Datei
def process_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        json_lines = content.split('\n')
        red_flag_labels, orange_flag_labels, green_flag_labels = set(red_flags), set(orange_flags), set(green_flags)

        for line in json_lines:
            if line:
                json_data = json.loads(line)
                for entity in json_data.get('entities', []):
                    if entity['label'] in red_flag_labels:
                        red_flag_labels.remove(entity['label'])
                    elif entity['label'] in orange_flag_labels:
                        orange_flag_labels.remove(entity['label'])
                    elif entity['label'] in green_flag_labels:
                        green_flag_labels.remove(entity['label'])
        
        # Bestimme den Flag-Status basierend auf dem Fehlen erforderlicher Flags
        if red_flag_labels:
            return 'Red'
        elif orange_flag_labels:
            return 'Orange'
        elif green_flag_labels:
            return 'Green'
        else:
            return 'None'

# Liste aller JSONL-Dateien im Verzeichnis abrufen
jsonl_files = list_jsonl_files(augmented_annotated_data)

# Verarbeite jede Datei und speichere die Ergebnisse
y = []
for file_path in jsonl_files:
    flag_status = process_jsonl(file_path)
    y.append(flag_status)

# Überprüfen, ob y nur eine Klasse enthält
class_distribution = Counter(y)

if len(class_distribution) < 2:
    print("Nicht genügend Klassen für das Modelltraining. Beende das Programm.")
    exit()

# Dummy-Feature-Matrix (da der Fokus auf dem Flag-Status liegt, nicht auf individuellen Features)
X = pd.DataFrame({'Dummy-Feature': [1]*len(y)})

# Anwenden von SMOTE zur Ausbalancierung des Datensatzes
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Aufteilen der resamplten Daten
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Initialisieren und Trainieren des Modells auf den resamplten Daten
model = LogisticRegression()
model.fit(X_train, y_train)

# Vorhersagen auf dem Testset
predictions = model.predict(X_test)

# Fehleranalyse
print(classification_report(y_test, predictions))




""" Counter({'Orange': 227, 'Red': 173, 'Green': 80})
              precision    recall  f1-score   support

       Green       0.26      1.00      0.41        35
      Orange       0.00      0.00      0.00        45
         Red       0.00      0.00      0.00        57

    accuracy       0.11      0.12      0.26       137
   macro avg       0.09      0.33      0.14       137
weighted avg       0.07      0.26      0.10       137 """


