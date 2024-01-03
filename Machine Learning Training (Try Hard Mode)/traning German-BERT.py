import os
import json
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, Dataset
from torch.nn import BCEWithLogitsLoss
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Verzeichnispfade mit Umgebungsvariablen
german_bert_checkpoint_directory = os.getenv('GERMAN_BERT_CHECKPOINT_DIRECTORY', 'default/path/to/German_BERT Checkpoint Directory')
annotated_data_directory = os.getenv('ANNOTATED_DATA_DIRECTORY', 'default/path/to/Annotated Data')

checkpoint_filename = 'bert_sequence_classification_checkpoint.pth'
checkpoint_path = os.path.join(german_bert_checkpoint_directory, checkpoint_filename)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Verwende Gerät: {device}")

bce_logits_loss = BCEWithLogitsLoss()
tokenizer = BertTokenizer.from_pretrained('bert-base-german-dbmdz-uncased')

# Flag-Zuordnungen und Label-Mapping
flag_associations = {
    "RED FLAG": ["Firma", "Sitz", "Gegenstand", "Stammkapital", "Stammeinlagen"],
    "Orange Flag": ["Geschäftsjahr", "Dauer", "Geschäftsführung", "Vertretung", "Gesellschafterversammlung"]
}

label_to_flag = {label: flag for flag, labels in flag_associations.items() for label in labels}
label_mapping = {"RED FLAG": 0, "Orange Flag": 1, "Green Flag": 2, "Firma": 3, "Sitz": 4, "Gegenstand": 5, "Stammkapital": 6, "Stammeinlagen": 7, "Geschäftsjahr": 8, "Dauer": 9, "Geschäftsführung": 10, "Vertretung": 11, "Gesellschafterversammlung": 12}
num_labels = len(label_mapping)


# CustomDataset-Klasse
class CustomDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        labels = self.labels[idx]
        encoding = self.tokenizer(text, padding='max_length', truncation=True, return_tensors='pt')
        return {key: val.flatten() for key, val in encoding.items()}, torch.tensor(labels)

def load_data(directory):
    # Lade und verarbeite Daten
    texts, label_sets = [], []
    for filename in os.listdir(directory):
        if filename.endswith('.jsonl'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                for line in file:
                    data = json.loads(line)
                    text = data['text']
                    entities = data['entities']
                    
                    labels = set()
                    for entity in entities:
                        label = entity['label']
                        
                        if label in label_mapping:
                            labels.add(label_mapping[label])
                        
                        if label in label_to_flag:
                            flag_label = label_to_flag[label]
                            labels.add(label_mapping[flag_label])

                    label_list = [0] * num_labels
                    for label in labels:
                        label_list[label] = 1

                    texts.append(text)
                    label_sets.append(label_list)
    return texts, label_sets

# Lade die Daten
texts, labels = load_data(annotated_data_directory)

# Erstelle ein Dataset und DataLoader
dataset = CustomDataset(texts, labels, tokenizer)
data_loader = DataLoader(dataset, batch_size=8, shuffle=True, pin_memory=True)

# Lade das Modell und verschiebe es auf die GPU
model = BertForSequenceClassification.from_pretrained('bert-base-german-dbmdz-uncased', num_labels=num_labels).to(device)

# Initialisiere den Optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

# Lade den Modell-Checkpoint
model.load_state_dict(torch.load(checkpoint_path))
model.to(device)

# Gib die Start-Epoche an (angepasst nach Bedarf)
start_epoch = 0

# Vor der Trainingsschleife
accumulation_steps = 4  # Gradienten über 4 Batches akkumulieren

# Innerhalb der Trainingsschleife
for epoch in range(start_epoch, 4):  # Anzahl der Epochen (angepasst nach Bedarf)
    total_loss = 0.0
    for i, batch in enumerate(data_loader):
        inputs, batch_labels = batch
        inputs = {k: v.to(device) for k, v in inputs.items()}
        batch_labels = batch_labels.to(device)

        optimizer.zero_grad()
        try:
            outputs = model(**inputs)
            logits = outputs.logits
            
            # Berechne den benutzerdefinierten Verlust
            loss = bce_logits_loss(logits, batch_labels.float())  # Stelle sicher, dass Labels float sind
            total_loss += loss

            # Führe eine Gradientenakkumulation durch
            if (i + 1) % accumulation_steps == 0:
                total_loss.backward()
                optimizer.step()
                total_loss = 0.0

            print(f"Epoche: {epoch}, Batch: {i}, Verlust: {loss.item()}")
        except Exception as e:
            print("Ein Fehler ist aufgetreten:", e)

    # Führe eine endgültige Aktualisierung des Gradienten durch, falls erforderlich
    if i % accumulation_steps != 0:
        total_loss.backward()
        optimizer.step()

# Speichere den endgültigen Modell-Checkpoint nach Abschluss des Trainings
torch.save(model.state_dict(), checkpoint_path)

