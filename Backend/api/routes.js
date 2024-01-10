const express = require('express');
const router = express.Router();
const multer = require('multer');
const runPythonScript = require('./pythonScriptRunner');
const path = require('path');

// Set up storage for multer to use the /tmp directory
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, '/tmp/') // Use the /tmp directory for temporary storage
  },
  filename: function (req, file, cb) {
    // Create a unique filename here
    cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname))
  }
});

const upload = multer({ storage: storage });

router.post('/analyze', upload.single('file'), (req, res) => {
  if (!req.file) {
    return res.status(400).send('No file uploaded.');
  }

  
  const inputPath = req.file.path;

  runPythonScript(inputPath, (error, results) => {
    if (error) {
      console.error(`Error running Python script: ${error}`);
      return res.status(500).send(error.message);
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
