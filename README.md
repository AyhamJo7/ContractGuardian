
![Contract Guardian Logo](https://github.com/AyhamJo7/ContractGuardian/blob/main/Frontend/public/logo.png)


## Überblick

Contract Guardian ist eine innovative Webanwendung, die darauf abzielt, den Analyseprozess von Verträgen für Gesellschaften mit beschränkter Haftung (GmbH) in Deutschland zu optimieren und zu verbessern. Die Anwendung nutzt modernste Technologien und bietet eine benutzerfreundliche Plattform, auf der Nutzer ihren "GmbH Gesellschaftervertrag" im PDF-Format hochladen können. Nach dem Hochladen des Vertrags werden die Nutzer nahtlos auf eine Analyse-Seite weitergeleitet, auf der der Vertrag in drei Kategorien analysiert wird: Rote Flaggen (PflichtKlauseln), Orange Flaggen (Empfohlene Klauseln) und Grüne Flaggen (Optionale Klauseln).

Die Kernfunktionalität von Contract Guardian beruht auf einer ausgeklügelten Backend-Logik, die jede Klausel im Vertrag bewertet und entsprechend kategorisiert. Die Analyseergebnisse werden übersichtlich dargestellt und zeigen an, ob eine Klausel vorhanden ist oder fehlt, symbolisiert durch ein einfaches [✓] oder [✗]. Diese intuitive Darstellung ermöglicht es den Nutzern, schnell zu identifizieren, welche kritischen, empfohlenen oder optionalen Klauseln in ihrem Vertrag fehlen, um so die rechtliche Konformität und Vollständigkeit sicherzustellen.

Contract Guardian wurde als Full-Stack-Webanwendung entwickelt und verwendet eine robuste Kombination aus React für das Frontend und Node.js, Express, Multer und Python für das Backend. Die gesamte Anwendung ist in einem Monorepo-Ansatz strukturiert, was eine effiziente Entwicklung und Wartung gewährleistet. Die Bereitstellung der Anwendung erfolgt über Heroku, wobei PostgreSQL als zentrale Datenbank dient und zuverlässige und skalierbare Datenspeicherlösungen bietet.

Das Hauptziel von Contract Guardian ist es, ein Werkzeug zur Verfügung zu stellen, das nicht nur den Prozess der Vertragsprüfung vereinfacht, sondern die Nutzer auch über die wesentlichen Elemente eines rechtlich fundierten GmbH-Vertrags aufklärt. Dieses Projekt ist das Ergebnis modernster Webtechnologien und innovativer Softwareentwicklung mit dem Ziel, die Art und Weise, wie rechtliche Dokumente im Geschäftsumfeld analysiert und verstanden werden, zu revolutionisieren.

Dieses Webanwendung wurde von Mhd Ayham Joumran, Sergej Popkow, Sofia Ahmed und Heyjin So entwickelt. Es ist strukturiert, um den Prozess der Vertragsprüfung zu vereinfachen und bietet schnelle und zuverlässige Einblicke durch ein automatisiertes System.

## Funktionen

**Contract Guardian** bietet eine Reihe von Schlüsselfunktionen, die eine umfassende und benutzerfreundliche Vertragsanalyse ermöglichen:

1. **PDF-Vertragsupload:** Einfaches Hochladen des GmbH-Gesellschaftervertrags im PDF-Format.

2. **Automatische Vertragsanalyse:** Detaillierte, automatisierte Analyse des hochgeladenen Vertrags.

3. **Kategorisierung von Klauseln:** 
   - *Rote Flaggen (PflichtKlauseln):* Unverzichtbare Klauseln für die rechtliche Gültigkeit.
   - *Orange Flaggen (Empfohlene Klauseln):* Empfohlene Klauseln für zusätzlichen Vertragsschutz.
   - *Grüne Flaggen (Optionale Klauseln):* Optionale Klauseln für spezifische Bedürfnisse.

4. **Übersichtliche Ergebnisdarstellung:** Klare Darstellung der Analyseergebnisse, inklusive Anzeige der vorhandenen und fehlenden Klauseln.

5. **Intuitive Benutzeroberfläche:** Benutzerfreundliches Frontend, entwickelt mit React.

6. **Robustes Backend:** Zuverlässige Datenverarbeitung durch Node.js, Express und Python.

7. **Datenbankintegration:** Sicherer und effizienter Umgang mit Vertragsdaten dank PostgreSQL.

8. **Heroku-Deployment:** Zuverlässige und skalierbare Bereitstellung über Heroku.

9. **Echtzeit-Feedback:** Sofortige Rückmeldung über den Vertragsstatus.

10. **Datenschutz und Sicherheit:** Hoher Stellenwert von Datenschutz und Sicherheitsmaßnahmen.


## Technologiestapel

**Frontend**: React
**Backend**: Node.js, Express, Python
**Datenbank**: PostgreSQL
**Deployment**: HEROKU


## Verzeichnisstruktur

![Contract Guardian Verzeichnisstruktur](https://github.com/AyhamJo7/ContractGuardian/blob/main/Frontend/public/Verzeichnisstruktur.svg)

Das Projekt ist in mehrere Schlüsselverzeichnisse gegliedert, die jeweils eine spezifische Funktion im Gesamtworkflow erfüllen:

### Frontend
Das Frontend-Verzeichnis beinhaltet die gesamte Benutzeroberfläche der Anwendung. Es ist in React entwickelt und nutzt TailwindCSS für das Styling. Wichtige Unterordner und Dateien umfassen:
- `src`: Enthält die React-Komponenten, Seiten und CSS-Dateien.
- `public`: Beinhaltet öffentliche Assets wie Bilder und Icons.
- `node_modules`: Enthält alle Frontend-Abhängigkeiten.
- `package.json`: Definiert Skripte und Abhängigkeiten für das Frontend.

### Backend
Das Backend-Verzeichnis besteht aus der Server-Logik, API-Endpunkten und der Integration mit der Datenbank. Es ist hauptsächlich in Node.js und Express entwickelt. Wesentliche Bestandteile sind:
- `api`: Beinhaltet die Express-Routen und Middleware.
- `Machine Learning`: Enthält Python-Skripte für die Verarbeitung und Analyse der Verträge.
- `node_modules`: Enthält Backend-Abhängigkeiten.
- `database.js`: Verwaltet die Verbindung zur PostgreSQL-Datenbank.
- `server.js`: Der Haupt-Entry-Point des Servers.

### Data
Das Data-Verzeichnis enthält Daten, die für das maschinelle Lernen und die Vertragsanalyse verwendet werden. Es umfasst:
- Verschiedene Unterordner mit annotierten Daten, Ergebnissen und ursprüngliche Datensatz **PDFs**.
- Skripte und Ergebnisse für das maschinelle Lernen.
- Daten für das Training und die Validierung der Modelle.



## Installation und Einrichtung

### Voraussetzungen
Stellen Sie sicher, dass folgende Software auf Ihrem System installiert ist, bevor Sie mit der Installation und Einrichtung des Projekts beginnen:

- **Node.js:** Für das Backend und das Frontend.
- **Python:** Für die Ausführung der Machine-Learning-Skripte.
- **PostgreSQL:** Für die Datenbankverwaltung.

### Erste Schritte
Befolgen Sie diese Schritte, um das Projekt lokal einzurichten:

1. **Klonen des Repositories:**

git clone https://github.com/AyhamJo7/ContractGuardian.git

2. **Installieren der Backend-Abhängigkeiten:**

cd Backend
npm install

3. **Installieren der Frontend-Abhängigkeiten:**

cd ../Frontend
npm install

4. **Einrichten der Umgebungsvariablen:**
Konfigurieren Sie alle erforderlichen Umgebungsvariablen in `.env`-Dateien im Backend- und Frontend-Verzeichnis.

5. **Vorbereitung der Datenbank:**
Stellen Sie sicher, dass PostgreSQL läuft und die erforderliche Datenbank eingerichtet ist.

### Ausführen der Anwendung
Um die Webanwendung lokal zu starten, folgen Sie diesen Schritten:

1. **Starten des Backends:**

cd Backend
npm start

Der Server läuft nun auf dem angegebenen Port.

2. **Starten des Frontends:**

cd Frontend
npm start

Das Frontend sollte sich automatisch in Ihrem Standardbrowser öffnen.



## Deployment auf Heroku

### Vorbereitungen
Bevor Sie mit dem Deployment auf Heroku beginnen, stellen Sie sicher, dass die Heroku CLI auf Ihrem System installiert ist und Sie sich bei Ihrem Heroku-Konto angemeldet haben. Führen Sie die folgenden Schritte aus:

1. **Heroku CLI installieren:**
   Laden Sie die Heroku CLI herunter und installieren Sie sie. Weitere Informationen finden Sie unter [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

2. **Anmelden bei Heroku:**
   Melden Sie sich mit dem Befehl `heroku login` bei Ihrem Heroku-Konto an und folgen Sie den Anweisungen zur Erstellung eines neuen SSH-Schlüssels.

heroku login



### Klonen des Repositories
Klonen Sie das Repository Ihres Projekts auf Ihren lokalen Computer:

heroku git:clone -a contract-guardian
cd contract-guardian



### Einrichten der Umgebungsvariablen
Konfigurieren Sie die erforderlichen Umgebungsvariablen auf Heroku:

- `DATABASE_URL`: URL Ihrer PostgreSQL-Datenbank.
- `LOAD_FOR_TRAINING_PATH`: Pfad zum Verzeichnis 'Load for Training'.
- `PYTHON_SCRIPT_PATH`: Pfad zum Python-Skript im 'Machine Learning'-Verzeichnis.
- `TESSDATA_PREFIX`: Pfad zum Tesseract-OCR-Datenverzeichnis.

Diese Werte können in der Heroku-App unter 'Settings' -> 'Config Vars' hinzugefügt werden.

### Hinzufügen der Buildpacks
Fügen Sie die notwendigen Buildpacks zu Ihrer Heroku-App hinzu. Diese werden verwendet, um Abhängigkeiten für Ihre App zu installieren und Ihre Umgebung zu konfigurieren. Die erforderlichen Buildpacks sind:

- `heroku/nodejs`
- `heroku/python`
- `heroku-buildpack-apt`
- `heroku-buildpack-poppler`

Diese können unter 'Settings' -> 'Buildpacks' hinzugefügt werden.

### Deployment Ihrer Änderungen
Nehmen Sie Änderungen am Code vor und deployen Sie diese auf Heroku:

git add .
git commit -am "Kommentar"
git push heroku main


Mit diesen Schritten haben Sie das Projekt "Contract Guardian" erfolgreich auf Heroku deployed.

## Datenbankkonfiguration

### Einrichten von PostgreSQL

#### Lokale Einrichtung
1. **Installieren Sie PostgreSQL:** Stellen Sie sicher, dass PostgreSQL auf Ihrem System installiert ist.

2. **Erstellen Sie eine neue Datenbank:** Nutzen Sie das PostgreSQL Management Tool Ihrer Wahl (z.B. pgAdmin oder die Kommandozeile), um eine neue Datenbank zu erstellen.

3. **Konfigurieren Sie die Verbindungsdaten:** Stellen Sie sicher, dass die Verbindungsdaten in den `.env`-Dateien Ihres Projekts korrekt eingestellt sind.

#### Einrichtung auf Heroku
1. **Erstellen Sie eine PostgreSQL-Datenbank auf Heroku:** Nutzen Sie die Heroku Postgres Add-ons, um eine PostgreSQL-Datenbank zu Ihrer App hinzuzufügen.

2. **Konfigurieren Sie die `DATABASE_URL`:** Heroku setzt automatisch die Umgebungsvariable `DATABASE_URL` mit den Verbindungsdaten zur Datenbank.

### Datenbankschema

Die Datenbank besteht aus den folgenden Tabellen:

#### Clauses
- `ClauseID`: Primärschlüssel, Integer, Auto-Increment
- `ClauseName`: Text, Eindeutig (Name oder Titel der Klausel)
- `FlagType`: Text (Werte: 'Red Flag', 'Orange Flag', 'Green Flag')
- `Description`: Text (Optionale Beschreibung oder Anmerkungen zur Klausel)

#### AnalysisResults
- `ResultID`: Primärschlüssel, Integer, Auto-Increment
- `ClauseID`: Fremdschlüssel, Verweist auf Clauses(ClauseID)
- `AnalysisDate`: Timestamp
- `Status`: Text (Werte: 'OK', 'Missing')
- `AdditionalNotes`: Text (Optionale zusätzliche Informationen zum Analyseergebnis)

#### AnalysisSessions
- `SessionID`: Primärschlüssel, Integer, Auto-Increment
- `SessionDate`: Timestamp
- `ProcessedFileName`: Text (Name der verarbeiteten Datei)
- `ResultSummary`: Text (Zusammenfassung oder Gesamtergebnis der Analyse)

#### SessionResults
- `SessionResultID`: Primärschlüssel, Integer, Auto-Increment
- `SessionID`: Fremdschlüssel, Verweist auf AnalysisSessions(SessionID)
- `ResultID`: Fremdschlüssel, Verweist auf AnalysisResults(ResultID)

### Beziehungen
- Jeder Eintrag in `AnalysisResults` ist mit einem Eintrag in `Clauses` verknüpft, der das Ergebnis der Analyse einer spezifischen Klausel in einem Vertrag darstellt.
- Die Tabelle `AnalysisSessions` enthält Informationen über jede Analyse-Session, einschließlich einer Zusammenfassung und des verarbeiteten Dateinamens.
- `SessionResults` verknüpft `AnalysisSessions` mit `AnalysisResults`, um nachzuverfolgen, welche Ergebnisse zu welcher Session gehören.


## Nutzung

Die Webanwendung "Contract Guardian" ermöglicht es Benutzern, ihre GmbH-Gesellschafterverträge hochzuladen und automatisch analysieren zu lassen. Hier ist eine schrittweise Anleitung zur Nutzung der App:

1. **PDF-Upload:**
   Klicken Sie auf das Upload-Symbol auf der Startseite, um Ihr PDF-Dokument hochzuladen. Wählen Sie Ihren GmbH-Gesellschaftervertrag aus Ihrem Dateisystem aus.

   ![Upload-Symbol](https://github.com/AyhamJo7/ContractGuardian/blob/main/Frontend/public/Upload-Symbol.jpg)

2. **Analyse-Seite:**
   Nach dem Hochladen des Dokuments öffnet sich automatisch die Analyse-Seite. Hier können Sie die durchgeführte Analyse Ihres Vertrags einsehen.


3. **Analyse-Details:**
   Klicken Sie auf das Dropdown-Menü „Analyse“, um eine detaillierte Ansicht der Analyseergebnisse zu erhalten. Hier sehen Sie die kategorisierten Klauseln Ihres Vertrags.

   ![Analyse-Details](https://github.com/AyhamJo7/ContractGuardian/blob/main/Frontend/public/Analyse-Details.jpg) 

4. **Weiterer PDF-Upload:**
   Innerhalb der Analyse-Seite haben Sie die Möglichkeit, ein weiteres PDF-Dokument hochzuladen und zu analysieren.

5. **Dark Mode Umschalten:**
   Sie können jederzeit die Hintergrundfarbe der Anwendung ändern, indem Sie oben rechts auf den Dark-Mode-Schalter klicken.

   ![Dark Mode](https://github.com/AyhamJo7/ContractGuardian/blob/main/Frontend/public/Dark-Mode.jpg) 


Mit diesen Schritten können Sie die Hauptfunktionalitäten von "Contract Guardian" einfach und intuitiv nutzen.

## Haftungsausschluss

Dieses Werkzeug dient ausschließlich zu Informationszwecken. Es bietet eine Analyse von GmbH-Verträgen auf mögliche fehlende Klauseln. Es stellt keine Rechtsberatung dar. Wir übernehmen keine Garantie für die Genauigkeit oder Vollständigkeit. Benutzer sollten sich für Beratung an Rechtsprofis wenden. Die Nutzung dieses Werkzeugs erfolgt auf eigenes Risiko, und wir haften nicht für etwaige Folgen. Mit der Nutzung dieses Werkzeugs stimmen Sie diesen Bedingungen zu.

## Beiträge

Dieses Projekt ist eine gemeinschaftliche Anstrengung von Mhd Ayham Joumran, Sofia Ahmed, Sergej und Mia. Für Beiträge oder Anfragen kontaktieren Sie bitte das Team.


