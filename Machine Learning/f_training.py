import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load the dataset
df = pd.read_csv('C:\\Users\\ayham\\Desktop\\5\\processed_report.csv')

# Fill NaN values in the "Flags" column
df['Flags'].fillna('', inplace=True)

# Vectorize the 'Flags' column using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X_flags = tfidf_vectorizer.fit_transform(df['Flags'])

# Prepare the feature matrix
X = pd.DataFrame(X_flags.toarray(), columns=[f"tfidf_{i}" for i in range(X_flags.shape[1])])
X['Flags_Code'] = df['Flags_Code'].astype(str)  # Convert 'Flags_Code' to string type

# Define and split target variables
targets = ['Has_Red_Flag', 'Has_Orange_Flag', 'Has_Green_Flag']
for target in targets:
    y = df[target]

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Predictions and Evaluation
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    print(f"Evaluation Report for {target}:\n{report}")

    # Save the model
    model_filename = f'trained_model_{target}.joblib'
    joblib.dump(model, model_filename)