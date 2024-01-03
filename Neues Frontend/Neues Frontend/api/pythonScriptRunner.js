require('dotenv').config();
const { exec } = require('child_process');

function runPythonScript(inputPath, callback) {
    const pythonCommand = 'python'; 
    // Verwende os.getenv() um den Pfad des Python-Skripts aus der .env-Datei zu holen
    const scriptPath = process.env.PYTHON_SCRIPT_PATH;
    const command = `${pythonCommand} ${scriptPath} "${inputPath}"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Ausführungsfehler: ${error}`);
            callback(error, null);
            return;
        }
    
        if (stderr) {
            console.error(`Skriptfehler: ${stderr}`);
            callback(stderr, null);
            return; // Wichtig, um die Ausführung bei einem Fehler zu stoppen
        }
    
        // Trimme die Ausgabe und versuche, sie als JSON zu parsen
        try {
            const trimmedOutput = stdout.trim();
            const results = JSON.parse(trimmedOutput);
            callback(null, results);
        } catch (parseError) {
            console.error(`Fehler beim Parsen des JSON aus dem Python-Skript: ${parseError}`);
            console.error(`Erhaltene stdout: ${stdout}`);
            callback(parseError, null);
        }
    });
}

module.exports = runPythonScript;
