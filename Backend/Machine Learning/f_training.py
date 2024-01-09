import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Laden des Datensatzes
dataset_path = os.getenv('DATASET_PATH', 'default/path/to/anno_processed_report.csv')
df = pd.read_csv(dataset_path)

# NaN-Werte in der Spalte "Flags" auffüllen
df['Flags'].fillna('', inplace=True)

# Vektorisierung der 'Flags'-Spalte mit TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X_flags = tfidf_vectorizer.fit_transform(df['Flags'])

# Speichern des TfidfVectorizer
vectorizer_filename = os.path.join(os.getenv('LOAD_FOR_TRAINING_PATH', 'default/path/to/Load for Training'), 'tfidf_vectorizer.joblib')
joblib.dump(tfidf_vectorizer, vectorizer_filename)

# Vorbereitung der Merkmalsmatrix
X = pd.DataFrame(X_flags.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
X['Flags_Code'] = df['Flags_Code'].astype(str)  # 'Flags_Code' in String-Typ umwandeln

# Definition und Aufteilung der Zielvariablen
targets = ['Has_Red_Flag', 'Has_Orange_Flag', 'Has_Green_Flag']
for target in targets:
    y = df[target]

    # Aufteilung der Daten in Trainings- und Testsets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    # Training des Modells
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Vorhersagen und Bewertung
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    print(f"Evaluationsbericht für {target}:\n{report}")

    # Speichern des Modells
    model_filename = os.path.join(os.getenv('LOAD_FOR_TRAINING_PATH', 'default/path/to/Load for Training'), f'trained_model_{target}.joblib')
    joblib.dump(model, model_filename)
    print(f"Modell gespeichert unter: {model_filename}")
