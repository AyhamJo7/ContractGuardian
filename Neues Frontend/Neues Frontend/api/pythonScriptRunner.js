const { exec } = require('child_process');

function runPythonScript(inputPath, callback) {
    // Ensure the path is enclosed in double quotes
    const scriptPath = '"C:/Users/ayham/Desktop/Projekt/ContractGuardian/Machine Learning/main.py"';
    const command = `python ${scriptPath} "${inputPath}"`;

    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return;
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return;
        }
        callback(stdout); // Process and use the output from your Python script
    });
}


module.exports = runPythonScript;
