const express = require('express');
const router = express.Router();
const multer = require('multer');
const runPythonScript = require('./pythonScriptRunner');

// Set up storage for multer
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'temp/') // make sure this directory exists
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname) // Use the original file name
  }
});

const upload = multer({ storage: storage });

router.post('/analyze', upload.single('file'), (req, res) => {
  // Make sure the file is received
  if (!req.file) {
    return res.status(400).send('No file uploaded.');
  }

  const inputPath = req.file.path;

  runPythonScript(inputPath, (error, results) => {
    if (error) {
      console.error(`Error running Python script: ${error}`);
      return res.status(500).send(error.message); // Make sure to return here
    }
    
    if (typeof results === 'string') {
      // If results is a string, parse it as JSON
      try {
        const resultsJSON = JSON.parse(results);
        res.json(resultsJSON);
      } catch (parseError) {
        console.error(`Error parsing JSON from Python script: ${parseError}`);
        res.status(500).send(`Error parsing JSON from Python script: ${parseError}`);
      }
    } else {
      // If results is already an object, send it as is
      res.json(results);
    }
  });
});

module.exports = router;
