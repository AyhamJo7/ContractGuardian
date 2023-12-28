from pdfminer.high_level import extract_text
import json

# Define the flag check functions
def check_red_flags(pdf_text):
    red_flags = []
    if len(pdf_text.strip()) == 0: # Document has no text
        red_flags.append("Document has no text")
    # Additional red flags can be added here
    return red_flags

def check_orange_flags(pdf_text):
    orange_flags = []
    if "cat" not in pdf_text.lower(): # Document has no mentions of cats
        orange_flags.append("Document has no mentions of cats")
    # Additional orange flags can be added here
    return orange_flags

def check_green_flags(pdf_text):
    green_flags = []
    # If any red or orange flags are present, they are considered green flags in this context
    reds = check_red_flags(pdf_text)
    oranges = check_orange_flags(pdf_text)
    if reds or oranges:
        green_flags = reds + oranges
    return green_flags

# Function to analyze the PDF and output flags in JSON format
def analyze_pdf(pdf_path):
    text = extract_text(pdf_path)
        
    red_flags = check_red_flags(text)
    orange_flags = check_orange_flags(text)
    green_flags = check_green_flags(text)
    
    return {
        "red_flags": red_flags,
        "orange_flags": orange_flags,
        "green_flags": green_flags
    }


pdf_path = './temp/file.pdf'
result = analyze_pdf(pdf_path)

print(json.dumps(result))


