
## Contract Guardian Projekt


## Überblick

Contract Guardian ist eine umfassende Lösung, die darauf abzielt, GmbH-Verträge zu analysieren, um potenzielle Fehler, fehlende Informationen und Risikofaktoren zu identifizieren. Dieses Tool wurde von Mhd Ayham Joumran, Sergej Popkow, Sofia Ahmed und Heyjin So entwickelt. Es ist strukturiert, um den Prozess der Vertragsprüfung zu vereinfachen und bietet schnelle und zuverlässige Einblicke durch ein automatisiertes System.


## Projektstruktur

Das Projekt ist in mehrere Schlüsselverzeichnisse gegliedert, die jeweils eine spezifische Funktion im Gesamtworkflow erfüllen:

1. **Daten**: Beinhaltet den ursprünglichen PDF-Datensatz und verschiedene Ergebnisse der Verarbeitungsstufen.

2. **Machine Learning**: Beherbergt die maschinellen Lernmodelle und Skripte für Textextraktion, -bereinigung und -analyse.

3. **Neues Frontend**: Verwaltet die Integration von Frontend und Backend und bietet eine Benutzeroberfläche für die Anwendung.

4. **Annotierte Daten**: Speichert Daten, die für das Training der maschinellen Lernmodelle annotiert wurden.

5. **__pycache__**: Ein Verzeichnis für die zwischengespeicherten Dateien von Python, um die Ladezeiten der Module zu verbessern.

6. **Sonstige Dateien**: Enthält Umgebungseinstellungen, Git-Attribute und Ignorierdateien sowie andere Konfigurationsskripte.

## Schlüsselkomponenten

- **Textextraktion (`a_text_extraction.py`)**: Extrahiert Text aus PDFs mit PyMuPDF und PyTesseract.
- **Textbereinigung (`b_text_cleaning.py`)**: Reinigt und standardisiert extrahierten Text.
- **Text zu JSON (`c_text_to_json.py`)**: Konvertiert bereinigten Text in JSON-Format für die weitere Verarbeitung.
- **Parsing (`d_parsing.py`)**: Parst JSON-Daten, um spezifische Klauseln im Vertrag zu identifizieren und zu markieren.
- **Flag-Verarbeitung (`e_flags.py`)**: Verarbeitet identifizierte Flags zur Analyse.
- **Modelltraining (`f_training.py`)**: Trainiert maschinelle Lernmodelle basierend auf verarbeiteten Daten.
- **Hauptskript (`main.py`)**: Orchestriert den gesamten Prozess von der Textextraktion bis zur Flag-Vorhersage.


## Machine Learning (Try Hard Mode)

Im Rahmen des Contract Guardian Projekts wurde ein spezieller Abschnitt "Machine Learning (Try Hard Mode)" entwickelt. Dieser Abschnitt enthält fortgeschrittene Ansätze und Techniken zur Verarbeitung und Analyse von Vertragsdaten. Die wichtigsten Skripte und ihre Funktionen sind:

1. **k_annotated_data_flags.py & k_annotated_data_parsing.py**: Diese Skripte sind zuständig für die erweiterte Verarbeitung und das Parsing von annotierten Daten. Sie ermöglichen eine tiefere und detailliertere Analyse der Vertragsinhalte.
2. **zanalyse.py**: Ein Skript zur umfassenden Analyse der Vertragsdaten, das spezifische Muster und Trends in den Daten identifiziert.
3. **z_back_translation.py**: Dieses Skript führt eine Rückübersetzung (Back-Translating) durch, um die Datenmenge zu erhöhen und die Vielfalt im Trainingsdatensatz zu verbessern. Dabei werden Texte vom Deutschen ins Englische und zurück übersetzt.
4. **z_create_copies.py**: Erstellt Dummy-Kopien von JSONL-Dateien. Dies ist nützlich für Experimente und Tests, bei denen Variationen der Originaldaten ohne bestimmte Elemente benötigt werden.Dieses Skript wurde durchgeführt, um die Datenmenge zu erhöhen und die Vielfalt im Trainingsdatensatz zu verbessern.
5. **z_training LogisticRegression.py & z_traning LogisticRegression 2.py**: Diese Dateien enthalten zwei Versuche, ein maschinelles Lernmodell mit der Methode der logistischen Regression zu trainieren. Dabei werden unterschiedliche Ansätze und Parameterkonfigurationen getestet, um die beste Modellleistung zu erzielen.
6. **z_validate.py**: Ein Skript zur Validierung der Modellergebnisse. Es hilft dabei, die Genauigkeit und Zuverlässigkeit der Vorhersagen des Modells zu überprüfen und sicherzustellen.


## Frontend- und Backend-Integration

- **API**: Das Verzeichnis `api` enthält Backend-Skripte, einschließlich `pythonScriptRunner.js`, `routes.js` und `server.js`, die die Interaktion zwischen dem Frontend und den maschinellen Lernmodellen verwalten.
- **Frontend**: Befindet sich im Verzeichnis `src` und umfasst Komponenten wie `Analyze.jsx`, `App.js` und `Home.jsx`, die eine benutzerfreundliche Schnittstelle für das Hochladen und Analysieren von Verträgen bieten.


## Nutzung

1. **Backend-Server starten**: Führen Sie das Skript `server.js` aus, um das Backend zu initiieren.
2. **Frontend-Anwendung ausführen**: Greifen Sie über einen Webbrowser auf das Frontend zu, um GmbH-Verträge hochzuladen und zu analysieren.
3. **Verträge analysieren**: Laden Sie eine PDF-Datei hoch, und das System wird automatisch die Ergebnisse verarbeiten und anzeigen, kategorisiert als rote, orange oder grüne Flags.


## Haftungsausschluss

Dieses Tool dient ausschließlich Informationszwecken und stellt keine Rechtsberatung dar. Obwohl Anstrengungen unternommen werden, um Genauigkeit zu gewährleisten, sind die Entwickler nicht verantwortlich für Ungenauigkeiten oder Auslassungen. Benutzer sollten sich für eine umfassende Vertragsanalyse an Rechtsexperten wenden.


## Beiträge

Dieses Projekt ist eine gemeinschaftliche Anstrengung von Mhd Ayham Joumran, Sofia Ahmed, Sergej und Mia. Für Beiträge oder Anfragen kontaktieren Sie bitte das Team.


---
