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
    cb(null, file.fieldname + '-' + Date.now() + '.pdf')
  }
});

const upload = multer({ storage: storage });

router.post('/analyze', upload.single('file'), (req, res) => {
  // Make sure the file is received
  if (!req.file) {
    return res.status(400).send('No file uploaded.');
  }

  // Path of the uploaded file
  const inputPath = req.file.path;

  // Run your Python script here
  runPythonScript(inputPath, (output) => {
    // Send the result back to client
    res.send(output);
  });
});

module.exports = router;
