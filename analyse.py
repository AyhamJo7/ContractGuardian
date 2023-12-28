import os
import fitz  # PyMuPDF
import spacy

# Define the keywords for each flag category
red_flags = ["Firma", "Sitz", "Gegenstand", "Stammkapital", "Stammeinlagen"]
orange_flags = ["Geschäftsführung", "Vertretung", "Dauer", "Geschäftsjahr", "Gesellschafterversammlung"]
green_flags = ["Veräußerung", "Gewinnverteilung", "Einziehung", "Erbfolge", "Kündigung", 
               "Abfindung", "Wettbewerb", "Schlussbestimmungen", "Gesellschafterbeschlüsse", 
               "Jahresabschluss", "Ergebnisverwendung", "Kosten", "Salvatorische Klausel", "Sonstige_Klauseln"]

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# Function to analyze a text for flag keywords
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

# Function to analyze a PDF for all flags
def analyze_pdf_for_flags(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    missing_red = analyze_text_for_flags(text, red_flags)
    missing_orange = analyze_text_for_flags(text, orange_flags)
    missing_green = analyze_text_for_flags(text, green_flags)

    return missing_red, missing_orange, missing_green

# Example usage
pdf_path = 'C:\\Users\\ayham\\Desktop\\Projekt\\ContractGuardian\\Data\\PDFs\\4Sports GmbH.pdf'
missing_red, missing_orange, missing_green = analyze_pdf_for_flags(pdf_path)

# Print the results
print("Missing Red Flags:", missing_red)
print("Missing Orange Flags:", missing_orange)
print("Missing Green Flags:", missing_green)
