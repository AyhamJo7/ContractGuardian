
## Contract Guardian Projekt

![Contract Guardian Logo](https://github.com/AyhamJo7/ContractGuardian/blob/main/Frontend/public/logo.png)


## Überblick

Contract Guardian ist eine Webanwendung zur Analyse von "GmbH Gesellschafterverträgen". Die App kategorisiert Vertragsklauseln in "Rote Flaggen" (Pflichtklauseln), "Orange Flaggen" (Empfohlene Klauseln) und "Grüne Flaggen" (Optionale Klauseln) und bietet eine AI-gestützte Analyse der Ergebnisse.

 Dieses Webanwendung wurde von Mhd Ayham Joumran, Sergej Popkow, Sofia Ahmed und Heyjin So entwickelt. Es ist strukturiert, um den Prozess der Vertragsprüfung zu vereinfachen und bietet schnelle und zuverlässige Einblicke durch ein automatisiertes System.

## Funktionen
Upload-Funktion für PDF-Dateien.
Automatisierte Kategorisierung von Vertragsklauseln.
Analyse-Seite, die Ergebnisse mit visuellen Indikatoren anzeigt (✓ für vorhandene Klauseln, ✗ für fehlende Klauseln).
AI-basierte Analyse und Vorschläge zur Modifikation von Verträgen.

## Technologiestapel
Frontend: React
Backend: Node.js, Python
Datenbank: PostgreSQL
Deployment: Lokales Hosting ODER HEROKU



## Verzeichnisstruktur

Das Projekt ist in mehrere Schlüsselverzeichnisse gegliedert, die jeweils eine spezifische Funktion im Gesamtworkflow erfüllen:

1. **Data**: Beinhaltet den ursprünglichen PDF-Datensatz und verschiedene Ergebnisse der Verarbeitungsstufen.

2. **Machine Learning**: Beherbergt die maschinellen Lernmodelle und Skripte für Textextraktion, -bereinigung und -analyse.

3. **Machine Learning Training (Try Hard Mode)**: Beherbergt alle maschinellen Lernmodelle, die wir probiert haben, sowie Augmentationsmethoden, die wir damit unsere Daten vermehrt haben.

4. **Neues Frontend**: Verwaltet die Integration von Frontend, Backend, Database und bietet eine Benutzeroberfläche für die Anwendung.

5. **Annotated Data**: Speichert Daten, die für das Training der maschinellen Lernmodelle annotiert wurden.

6. **Augmented Annotated Data**: Speichert Daten, die für das Training der maschinellen Lernmodelle annotiert und mithilfe von "augmentation.py" augmentiert wurden.

7. **Back Translated Annotated Data**: Speichert Daten, die für das Training der maschinellen Lernmodelle annotiert und mithilfe von "back_translation.py" augmentiert wurden.

8. **Load for Training**: Speichert trainerte Modelle sowie csv Dateien (Ergebnisse von "d_parsing.py", "e_flags.py" & "f_training.py") 

9. **__pycache__**: Ein Verzeichnis für die zwischengespeicherten Dateien von Python, um die Ladezeiten der Module zu verbessern.

10. **Sonstige Dateien**: Enthält Umgebungseinstellungen, Git-Attribute und Ignorierdateien sowie andere Konfigurationsskripte.



## Schlüsselkomponenten und Installation

## 1- MACHINE LEARNING 

- **Textextraktion (`a_text_extraction.py`)** Das Skript a_text_extraction.py ist für die Textextraktion aus PDF-Dateien konzipiert. Es nutzt fitz (PyMuPDF) zur direkten Textextraktion und pytesseract für die Fälle, in denen der Text als Bild vorliegt. Das Skript lädt Einstellungen aus einer .env-Datei und ermöglicht das automatische Durchsuchen eines Verzeichnisses nach PDFs, um den Text daraus zu extrahieren und in Textdateien zu speichern. Es bietet auch die Funktionalität, Pfade dynamisch zu handhaben und erstellt notwendige Verzeichnisse bei Bedarf.

Für dieses Skript sind folgende Bibliotheken erforderlich, die in der requirements.txt Datei aufgeführt werden sollten:

PyMuPDF
pytesseract
pdf2image
python-dotenv


- **Textbereinigung (`b_text_cleaning.py`)**: Das Skript b_text_cleaning.py kümmert sich um die Bereinigung von Texten, die zuvor aus PDF-Dokumenten extrahiert wurden. Es verwendet reguläre Ausdrücke (Regex), um verschiedene Arten von Störungen und Unregelmäßigkeiten im Text zu identifizieren und zu bereinigen. Dazu gehören das Korrigieren von Silbentrennungen, das Standardisieren der Formatierung, das Entfernen von irrelevanten Informationen wie Dateipfaden und spezifischen Ausdrücken sowie das Entfernen von Seitenzahlen. Das Skript ist so konzipiert, dass es ein Verzeichnis mit extrahierten Texten durchläuft und die bereinigten Texte in einem separaten Verzeichnis speichert. Die Pfade zu diesen Verzeichnissen werden über Umgebungsvariablen geladen, die in einer .env-Datei definiert sind.

Für die Ausführung dieses Skripts sollten die folgenden Bibliotheken in der requirements.txt Datei aufgeführt werden:

regex
python-dotenv


- **Text zu JSON (`c_text_to_json.py`)**: Das Skript c_text_to_json.py ist ein wichtiger Bestandteil des Projekts. Es hat die Aufgabe, bereinigte Texte in strukturierte Daten umzuwandeln, genauer gesagt in das JSONL-Format. Dieses Format eignet sich besonders gut für die weitere Verarbeitung und Analyse der Textdaten. 
Das Skript liest Textdateien aus einem angegebenen Verzeichnis. --> 
Der Text wird anhand bestimmter Schlüsselwörter in Abschnitte unterteilt. Diese Funktion ist besonders nützlich, um die Struktur der Vertragstexte zu erhalten und sie für die weitere Analyse vorzubereiten. --> 
Jeder Abschnitt wird als separates JSON-Objekt gespeichert, wodurch eine Datei im JSONL-Format entsteht. Dieses Format ist besonders für maschinelles Lernen und Datenanalyse geeignet. --> 
Das Skript kann ein ganzes Verzeichnis von Textdateien automatisch verarbeiten und die Ergebnisse in einem Zielverzeichnis speichern.

Für die Ausführung dieses Skripts sollten folgende Bibliotheken in der requirements.txt Datei aufgeführt werden:

python-dotenv


- **Parsing (`d_parsing.py`)**: Das Skript d_parsing.py ist verantwortlich für das Parsen und Kategorisieren von Textabschnitten. Es verwendet reguläre Ausdrücke (Regex) zur Identifikation und Zuordnung von Schlüsselwörtern zu verschiedenen Kategorien (Red Flags, Orange Flags, Green Flags). Das Skript verarbeitet JSONL-Dateien, extrahiert relevante Daten und erzeugt einen strukturierten Bericht in Form einer CSV-Datei. 

Für die Ausführung dieses Skripts sind folgende Bibliotheken in der requirements.txt Datei aufzuführen:

regex
pandas
python-dotenv


- **Flag-Verarbeitung (`e_flags.py`)**: Es spezialisiert sich auf die Verarbeitung und Analyse von Daten, die zuvor extrahiert und in eine CSV-Datei gespeichert wurden. Das Hauptziel des Skripts ist es, die Flag-Kategorien (Red, Orange, Green) zu verarbeiten und zu organisieren.
Das Skript lädt eine CSV-Datei in einen Pandas DataFrame, um die Daten zu verarbeiten -->
Es ersetzt fehlende Werte in der Spalte 'Flags' durch 'Green Flag', um sicherzustellen, dass alle Datensätze kategorisiert werden. -->
Um die Analyse zu erleichtern, ordnet das Skript jeder Flag-Kategorie einen numerischen Code zu. -->
Es ermittelt, ob in jedem Abschnitt bestimmte Flags vorhanden sind, und markiert dies entsprechend in neuen Spalten des DataFrames. -->
Nach der Verarbeitung speichert das Skript die Ergebnisse in einer neuen CSV-Datei.

Zur Ausführung dieses Skripts sind folgende Bibliotheken in der requirements.txt Datei erforderlich:

pandas
python-dotenv


- **Modelltraining (`f_training.py`)**: Das Skript f_training.py bildet den Abschluss des maschinellen Lernprozesses im Rahmen des "Contract Guardian" Projekts. Es konzentriert sich auf das Training von Klassifikationsmodellen, die darauf abzielen, Textabschnitte in die Kategorien Red, Orange und Green Flags einzuordnen. Hier sind die Hauptfunktionen des Skripts:

-Datenverarbeitung: Das Skript lädt einen zuvor vorbereiteten Datensatz, bereinigt ihn und füllt fehlende Werte auf.
-Vektorisierung: Es verwendet TF-IDF (Term Frequency-Inverse Document Frequency) zur Vektorisierung der Textdaten, um sie für das maschinelle Lernen nutzbar zu machen.
-Training und Validierung: Das Skript teilt die Daten in Trainings- und Testsets auf und trainiert für jede Flag-Kategorie (Red, Orange, Green) ein eigenes RandomForestClassifier-Modell.
-Modellbewertung: Nach dem Training wird jedes Modell anhand von Testdaten evaluiert und ein Klassifizierungsbericht erstellt.
-Speichern von Modellen und Vektorisierern: Sowohl die trainierten Modelle als auch der TF-IDF Vektorisierer werden für spätere Verwendungen gespeichert.

Zur Ausführung dieses Skripts sind folgende Bibliotheken in der requirements.txt Datei erforderlich:

pandas
scikit-learn
joblib
python-dotenv

- **Augmentation (`augmentation.py`)**: Das Skript augmentation.py ist ein Hilfsprogramm im Rahmen des "Contract Guardian" Projekts, das speziell für die Datenaufbereitung und -erweiterung zuständig ist. Es liest annotierte Daten aus JSONL-Dateien und erstellt davon modifizierte Kopien. Diese Kopien sind nützlich, um die Robustheit und Vielfältigkeit der für das maschinelle Lernen verwendeten Datensätze zu erhöhen.

Dieses Skript ist besonders nützlich, um die Diversität der Trainingsdaten zu erhöhen und potenzielle Überanpassungen (Overfitting) der Modelle zu vermeiden. Es trägt dazu bei, die Robustheit des maschinellen Lernprozesses zu verbessern.

Für die Ausführung dieses Skripts sind folgende Bibliotheken in der requirements.txt Datei erforderlich:

json
os
python-dotenv


- **Augmentation (`back_translating.py`)**: Das Skript back_translation.py ist ein wesentlicher Teil des Datenaufbereitungsprozesses im "Contract Guardian" Projekt. Es nutzt die Technik der Rückübersetzung (Back-Translation), um die Qualität und Vielfalt der Trainingsdaten für maschinelles Lernen zu verbessern. Hier sind die Hauptfunktionen des Skripts:
 Das Skript nutzt zwei Übersetzungs-Pipelines (Helsinki-NLP/opus-mt-de-en und Helsinki-NLP/opus-mt-en-de) für die Übersetzung von Deutsch nach Englisch und zurück. --> 
 Das Skript lädt annotierte Daten aus einem Verzeichnis und bereitet sie für die Rückübersetzung vor. --> 
 Texte werden in kleinere Segmente aufgeteilt und durch Übersetzung ins Englische und Rückübersetzung ins Deutsche bearbeitet. Dieser Prozess erzeugt Variationen im Text, die die Diversität der Trainingsdaten erhöhen. -->
 Die rückübersetzten Texte werden zusammen mit den ursprünglichen Daten als JSON-Dateien gespeichert.

 Dieser Ansatz kann dazu beitragen, die Sprachmodelle robuster zu machen, da die Variationen in den Texten das Modell auf unterschiedliche Formulierungen desselben Inhalts trainieren.

Zur Ausführung dieses Skripts sind folgende Bibliotheken in der requirements.txt Datei erforderlich:

transformers
os
json
python-dotenv



- **Hauptskript (`main.py`)**: Das Skript main.py ist das Herzstück des "Contract Guardian" Projekts. Es Orchestriert die verschiedenen Module und Funktionen, die zuvor entwickelt wurden, in einen einzigen, kohärenten Prozess. Die Hauptfunktionen und Abläufe des Skripts umfassen:

-PDF-Textextraktion: Zunächst extrahiert es den Text aus einer PDF-Datei mittels der PDFTextExtractor-Klasse aus a_text_extraction.py.

-Textbereinigung: Der extrahierte Text wird dann mittels der TextCleaning-Klasse aus b_text_cleaning.py bereinigt.

-Textverarbeitung: Der bereinigte Text wird weiterverarbeitet, in JSON konvertiert (c_text_to_json.py), analysiert (d_parsing.py) und schließlich werden die Flags verarbeitet (e_flags.py).

-Modellvorhersagen: Es lädt trainierte maschinelle Lernmodelle und verwendet diese, um Vorhersagen über die Kategorisierung der Textabschnitte in verschiedene Flag-Kategorien zu treffen.

-Ergebnisinterpretation: Das Skript interpretiert die Ergebnisse und gibt sie in einem strukturierten Format (JSON) aus.

-Automatisierung und Benutzerinteraktion: Mittels argparse ermöglicht das Skript die Eingabe von Benutzerargumenten und automatisiert den Prozess von der Textextraktion bis zur Ausgabe der Ergebnisse.

Dieses Hauptskript fasst somit die verschiedenen Stufen des Projekts – von der Datenaufbereitung bis hin zur Analyse und Prognose – in einem umfassenden Prozess zusammen. Es demonstriert die Anwendung der entwickelten Modelle und Methoden in einer realen Anwendungssituation.

Für die Ausführung des main.py Skripts im Rahmen des "Contract Guardian" Projekts werden verschiedene Bibliotheken benötigt, die in der requirements.txt Datei aufgeführt werden sollten. Hier sind die erforderlichen Bibliotheken basierend auf den verschiedenen importierten Modulen und deren Funktionen:

PyMuPDF (fitz): Für die PDF-Textextraktion.
PyTesseract: Für die Textextraktion aus Bildern in PDFs.
pdf2image: Wird zusammen mit PyTesseract für die Bildextraktion verwendet.
python-dotenv: Zum Laden von Umgebungsvariablen aus einer .env-Datei.
Pandas: Für Datenmanipulation und -analyse.
Scikit-learn: Für maschinelles Lernen, insbesondere das RandomForestClassifier-Modell und andere Funktionen wie train_test_split.
Joblib: Zum Laden und Speichern von trainierten Modellen.
argparse: Zur Verarbeitung von Befehlszeilenargumenten.
shutil: Für Dateioperationen, insbesondere zum Löschen und Erstellen von Verzeichnissen.

PyMuPDF
pytesseract
pdf2image
python-dotenv
pandas
scikit-learn
joblib
argparse
shutil



## 2- NEUES FRONTEND 

1- **API**: Das Verzeichnis `api` enthält Backend-Skripte, einschließlich `pythonScriptRunner.js`, `routes.js` und `server.js`, die die Interaktion zwischen dem Frontend und den maschinellen Lernmodellen verwalten.


- **Database (`database.js`)**: Das database.js Skript ist ein Teil des "Contract Guardian" Projekts und stellt die Verbindung zur PostgreSQL-Datenbank her. Es nutzt das pg Modul von Node.js, um einen Pool von Verbindungen zu verwalten, und verwendet Umgebungsvariablen, um die Datenbank-URL zu konfigurieren

Um dieses Skript auszuführen, sollten Sie sicherstellen, dass die folgenden Abhängigkeiten in Ihrer package.json Datei aufgeführt sind:

pg: Für die PostgreSQL-Verbindungsverwaltung.
dotenv: Zum Laden von Umgebungsvariablen.

- **Express.js-Server (`server.js`)**: Das Skript server.js ist der Kern des Back-Ends im "Contract Guardian" Projekt und setzt einen Express.js-Server auf. Es verwendet verschiedene Middleware und Routen, um die Funktionalität der Webanwendung zu ermöglichen.
Das Skript verwendet Express.js, ein populäres Node.js-Framework, um einen Webserver zu erstellen.

`express.json`: Diese Middleware wird verwendet, um eingehende Anfragen mit JSON-Inhalten zu verarbeiten.
`cookieParser`: Eine Middleware zum Parsen von Cookies in eingehenden Anfragen.
`CORS-Konfiguration`: Das Skript konfiguriert Cross-Origin Resource Sharing (CORS), um Anfragen von der Front-End-Anwendung, die auf einem anderen Port (hier `localhost:3000`) läuft, zu akzeptieren. Dies ist wichtig, um sicherzustellen, dass der Browser Anfragen zwischen dem Front-End und dem Back-End zulässt.
Das Skript bindet die Route analyzeRoute unter dem Pfad /api/v1. Diese Route wird wahrscheinlich für die Verarbeitung spezifischer Anfragen, z.B. zur Analyse von Vertragsdaten, verwendet.
Der Server wird so konfiguriert, dass er auf Port 4000 hört, und eine Nachricht wird ausgegeben, wenn der Server erfolgreich gestartet ist.

Zur Ausführung dieses Servers sind die folgenden Node.js-Module erforderlich, die in Ihrer package.json-Datei aufgeführt sein sollten:

`express`: Für den Webserver und die Middleware.
`cookie-parser`: Zum Parsen von Cookies in HTTP-Anfragen.
Weitere Module, die in den importierten Dateien (./routes) verwendet werden, und alle spezifischen Abhängigkeiten, die in diesen Dateien erforderlich sind.

- **Express.js-Server-Route (`routes.js`)**: Das Skript routes.js im "Contract Guardian" Projekt definiert eine Route für den Express.js-Server, die speziell für die Analyse von hochgeladenen Dateien zuständig ist. Hier sind die wichtigsten Funktionen des Skripts:

- Einrichtung des Routers: Es nutzt den Express.js-Router, um eine spezifische HTTP-Route zu definieren.

- Datei-Upload mit Multer:

`Multer-Konfiguration`: Multer wird als Middleware für das Handling von Datei-Uploads eingesetzt. Hier wird es so konfiguriert, dass hochgeladene Dateien im `temp/`-Verzeichnis gespeichert werden, wobei der ursprüngliche Dateiname beibehalten wird.
`Upload-Route`: Die Route /analyze akzeptiert POST-Anfragen mit einer einzelnen Datei (`upload.single('file')`). Diese Route wird vermutlich für die Analyse von PDF-Dateien oder ähnlichen Dokumenten verwendet.

- Analyseprozess:

o Überprüfung des Datei-Uploads: Zunächst wird überprüft, ob eine Datei erfolgreich hochgeladen wurde.
o Ausführung eines Python-Skripts: Das hochgeladene Dokument wird an ein Python-Skript (runPythonScript) weitergegeben, das die eigentliche Analyse durchführt.
o Fehlerbehandlung: Das Skript enthält Fehlerbehandlung für den Fall, dass beim Ausführen des Python-Skripts oder beim Parsen der Ergebnisse Fehler auftreten.
o Rückgabe der Ergebnisse:
Die Ergebnisse der Python-Skriptausführung werden als JSON an den Client zurückgesendet.

Um diese Route in einem Express.js-Server zu nutzen, müssen folgende Module in der package.json-Datei des Projekts aufgeführt sein:

`express`: Für den Router und das Server-Framework.
`multer`: Für das Handling von Datei-Uploads.





2- **src**: Die beiden React-Komponenten `Home.jsx` und `Analyze.jsx` sind Teile des Frontends. Hier sind die Hauptfunktionen und Elemente jeder Komponente:

`Home.jsx`
Diese Komponente bildet die Startseite der Webanwendung.

Upload-Funktionalität: Nutzer können PDF-Dateien hochladen, entweder durch Klicken.

Navigationsfunktion: Bei erfolgreichem Hochladen einer Datei wird der Nutzer zur Analyse-Seite weitergeleitet.

Styling und Animationen: Die Seite nutzt Icons (FaPlus, BsCloudUpload, IoIosSearch, FaCircleCheck) für visuelle Elemente und framer-motion für Animationen.


`Analyze.jsx`
Diese Komponente ist für die Darstellung und Verarbeitung der Analyseergebnisse zuständig.

Datei-Verarbeitung: Die hochgeladene PDF-Datei wird an den Backend-Server gesendet und dort analysiert.

Anzeige der Analyseergebnisse: Die Ergebnisse (Red, Orange, Green Flags) der Vertragsanalyse werden in einer übersichtlichen Struktur angezeigt.

Ladestatus: Ein Lade-Overlay wird angezeigt, während die Datei verarbeitet wird.

Interaktive Elemente: Die Ergebnisse werden in aufklappbaren Akkordeon-Elementen präsentiert, um die Übersichtlichkeit zu erhöhen.


Beide Komponenten sind darauf ausgelegt, eine benutzerfreundliche und interaktive Schnittstelle für die Vertragsanalyse zu bieten, wobei der Fokus auf einer einfachen Bedienung und klaren Darstellung der Ergebnisse liegt.

Für die Implementierung dieser Komponenten sind folgende Pakete und Bibliotheken erforderlich:

React und React-Router-DOM für die UI-Komponenten und Navigation.
Axios für HTTP-Anfragen an den Server.
Icons von react-icons.
framer-motion für Animationen.
Styling-Techniken, wie CSS oder eine CSS-in-JS-Bibliothek.




## Nutzung

1. **Backend-Server starten**: Führen Sie das Skript `server.js` aus, um das Backend zu initiieren.
2. **Frontend-Anwendung ausführen**: Greifen Sie über einen Webbrowser auf das Frontend zu, um GmbH-Verträge hochzuladen und zu analysieren.
3. **Verträge analysieren**: Laden Sie eine PDF-Datei hoch, und das System wird automatisch die Ergebnisse verarbeiten und anzeigen, kategorisiert als rote, orange oder grüne Flags.


## Haftungsausschluss

Dieses Werkzeug dient ausschließlich zu Informationszwecken. Es bietet eine Analyse von GmbH-Verträgen auf mögliche fehlende Klauseln. Es stellt keine Rechtsberatung dar. Wir übernehmen keine Garantie für die Genauigkeit oder Vollständigkeit. Benutzer sollten sich für Beratung an Rechtsprofis wenden. Die Nutzung dieses Werkzeugs erfolgt auf eigenes Risiko, und wir haften nicht für etwaige Folgen. Mit der Nutzung dieses Werkzeugs stimmen Sie diesen Bedingungen zu.

## Beiträge

Dieses Projekt ist eine gemeinschaftliche Anstrengung von Mhd Ayham Joumran, Sofia Ahmed, Sergej und Mia. Für Beiträge oder Anfragen kontaktieren Sie bitte das Team.


