const express = require("express");
const path = require("path"); 
const cookieParser = require("cookie-parser");
const analyzeRoute = require("./routes");

require('dotenv').config();

const app = express();

// Body-Parser Middleware, um JSON-Daten zu verarbeiten
app.use(express.json({ limit: "10mb" }));
app.use(cookieParser());

// Statische Dateien vom React-App-Ordner bedienen
app.use(express.static(path.join(__dirname, '../../Frontend/build')));

// CORS-Headers Konfiguration
app.use((req, res, next) => {
  // Erlaubte Quellen
  const allowedOrigins = [
    'http://localhost:3000', 
    'https://<your-heroku-app-name>.herokuapp.com'
  ];
  // Überprüfen, ob die Herkunft der Anfrage erlaubt ist
  const origin = req.headers.origin;
  if (allowedOrigins.includes(origin)) {
      res.setHeader('Access-Control-Allow-Origin', origin);
  }
  // Weitere CORS-Einstellungen
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  next();
});

// API-Routen
app.use("/api/v1", analyzeRoute);

// Alle verbleibenden Anfragen schicken die React-App zurück, damit sie das Routing übernehmen kann.
app.get('*', function(request, response) {
  response.sendFile(path.resolve(__dirname, '../../Frontend/build', 'index.html'));
});

// Port Einstellung von der Umgebungsvariablen oder Standardport 4000
const PORT = process.env.PORT || 4000;

// Server starten
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
