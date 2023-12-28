const express = require("express");
const router = express.Router();
const multer = require("multer");
const { exec } = require("child_process");
const fs = require("fs");

// Set up multer storage
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

const tempFilePath = "./temp/file.pdf";

router.post("/post", upload.single("pdfFile"), async (req, res, next) => {
  if (!req.file) {
    return res.status(400).json({ message: "No file uploaded" });
  }
  const fileData = req.file.buffer;

  fs.writeFileSync(tempFilePath, fileData);
// Change Python Path here if needed
  exec(`python example.py`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      return res.status(500).json({ message: "Error processing the PDF" });
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
      return res.status(500).json({ message: "Error processing the PDF" });
    }

    try {
      const result = JSON.parse(stdout.trim());
      // console.log("Python script result: ", result);

      res.status(200).json({ result });
    } catch (err) {
      console.error("Error parsing JSON:", err);
      res.status(500).json({ message: "Error parsing JSON" });
    }
  });
});

module.exports = router;
