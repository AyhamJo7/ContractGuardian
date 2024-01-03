import os
import fitz  # PyMuPDF
import spacy
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Pfadvariable mit os.getenv()
pdf_example = os.getenv('PDF_EXAMPLE_PATH', 'default/path/to/pdf')

# Definiere die Schlüsselwörter für jede Flag-Kategorie
red_flags = ["Firma", "Sitz", "Gegenstand", "Stammkapital", "Stammeinlagen"]
orange_flags = ["Geschäftsführung", "Vertretung", "Dauer", "Geschäftsjahr", "Gesellschafterversammlung"]
green_flags = ["Veräußerung", "Gewinnverteilung", "Einziehung", "Erbfolge", "Kündigung", 
               "Abfindung", "Wettbewerb", "Schlussbestimmungen", "Gesellschafterbeschlüsse", 
               "Jahresabschluss", "Ergebnisverwendung", "Kosten", "Salvatorische Klausel", "Sonstige_Klauseln"]

# Funktion, um Text aus einer PDF-Datei zu extrahieren
def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# Funktion, um einen Text auf Flag-Schlüsselwörter zu analysieren
def analyze_text_for_flags(text, flag_keywords):
    nlp = spacy.load("de_core_news_sm")
    doc = nlp(text)
    found_keywords = set()

    for token in doc:
        for keyword in flag_keywords:
            if keyword in token.text:
                found_keywords.add(keyword)
    
    missing_keywords = set(flag_keywords) - found_keywords
    return missing_keywords


# Funktion zur Analyse einer PDF auf alle Flags
def analyze_pdf_for_flags(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    missing_red = analyze_text_for_flags(text, red_flags)
    missing_orange = analyze_text_for_flags(text, orange_flags)
    missing_green = analyze_text_for_flags(text, green_flags)

    return missing_red, missing_orange, missing_green

# Beispielverwendung
missing_red, missing_orange, missing_green = analyze_pdf_for_flags(pdf_example)

# Drucke die Ergebnisse
print("Fehlende Rote Flags:", missing_red)
print("Fehlende Orange Flags:", missing_orange)
print("Fehlende Grüne Flags:", missing_green)
