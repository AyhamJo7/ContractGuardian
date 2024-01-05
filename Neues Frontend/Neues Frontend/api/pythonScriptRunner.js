const { exec } = require('child_process');
const dotenv = require('dotenv');

dotenv.config();

function runPythonScript(inputPath, callback) {
    const pythonCommand = 'python'; // or python3 if that's the correct command
    const scriptPath = `"${process.env.PYTHON_SCRIPT_PATH}"`; 

    const command = `${pythonCommand} ${scriptPath} "${inputPath}"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`Execution error: ${error}`);
            callback(error, null);
            return;
        }
    
        if (stderr) {
            console.error(`Script error: ${stderr}`);
            callback(stderr, null);
            return; // This is important to prevent further execution when there's an error
        }
    
        // Trim the output and attempt to parse it as JSON
        try {
            const trimmedOutput = stdout.trim();
            const results = JSON.parse(trimmedOutput);
            callback(null, results);
        } catch (parseError) {
            console.error(`Error parsing JSON from Python script: ${parseError}`);
            console.error(`Received stdout: ${stdout}`);
            callback(parseError, null);
        }
    });
    }

module.exports = runPythonScript;
