const runPythonScript = require('./pythonScriptRunner');

runPythonScript('C:\\Users\\ayham\\Desktop\\Erweiterter_Dummy_GmbH_Gesellschaftervertrag.pdf', (error, results) => {
    if (error) {
        console.error("Error:", error);
    } else {
        console.log("Results:", results);
    }
});
