const express = require("express");
const app = express();
const cookieParser = require("cookie-parser");
const analyzeRoute = require("./routes");


app.use(express.json({ limit: "10mb" }));
app.use(cookieParser());

// Set up CORS headers
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "http://localhost:3000");
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");
  next();
});

app.use("/api/v1", analyzeRoute);

app.listen(4000, () => {
  console.log(`Server is running on port 4000`);
});
