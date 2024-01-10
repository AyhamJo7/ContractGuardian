const express = require("express");
const cookieParser = require("cookie-parser");
const analyzeRoute = require("./routes");

require('dotenv').config();

const app = express();

// Body-Parser Middleware, um JSON-Daten zu verarbeiten
app.use(express.json({ limit: "10mb" }));
app.use(cookieParser());

// CORS-Headers einrichten
app.use((req, res, next) => {

  const allowedOrigins = ['http://localhost:3000', 'https://your-heroku-app-name.herokuapp.com']; // Zugriff erlauben
  const origin = req.headers.origin;
  if (allowedOrigins.includes(origin)) {
      res.setHeader('Access-Control-Allow-Origin', origin);
  }
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE"); // Erlaubte Methoden
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization"); // Erlaubte Header
  next();
});

app.use("/api/v1", analyzeRoute);

// Use environment variable for port or default to 4000
const PORT = process.env.PORT || 4000;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
