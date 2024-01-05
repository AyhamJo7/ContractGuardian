const { exec } = require('child_process');
const db = require('./database');
const dotenv = require('dotenv');

dotenv.config();

// Function to generate a summary based on results
function generateSummary(results) {
    let redCount = results['Red Flags'].length;
    let orangeCount = results['Orange Flags'].length;
    let greenCount = results['Green Flags'].length;
    return `Analysis completed. Red Flags: ${redCount}, Orange Flags: ${orangeCount}, Green Flags: ${greenCount}`;
}

function runPythonScript(inputPath, callback) {
    const pythonCommand = 'python';
    const scriptPath = `"${process.env.PYTHON_SCRIPT_PATH}"`;
    const command = `${pythonCommand} ${scriptPath} "${inputPath}"`;

    exec(command, async (error, stdout, stderr) => {
        if (error) {
            console.error(`Execution error: ${error}`);
            callback(error, null);
            return;
        }
        if (stderr) {
            console.error(`Script error: ${stderr}`);
            callback(stderr, null);
            return;
        }

        try {
            const trimmedOutput = stdout.trim();
            const results = JSON.parse(trimmedOutput);

            const summary = generateSummary(results);
            const sessionResult = await db.query(`
                INSERT INTO AnalysisSessions (SessionDate, ProcessedFileName, ResultSummary) 
                VALUES ($1, $2, $3) RETURNING SessionID;`, 
                [new Date(), inputPath, summary]
            );
            const sessionId = sessionResult.rows[0].SessionID;

            for (const flagType in results) {
                for (const clause of results[flagType]) {
                    try {
                        const clauseResult = await db.query('SELECT ClauseID FROM Clauses WHERE ClauseName = $1', [clause.name]);
                        const clauseId = clauseResult.rows[0]?.ClauseID;

                        if (clauseId) {
                            const analysisResult = await db.query(`
                                INSERT INTO AnalysisResults (ClauseID, AnalysisDate, Status, AdditionalNotes) 
                                VALUES ($1, $2, $3, $4) RETURNING ResultID;`, 
                                [clauseId, new Date(), clause.status === '✓' ? 'OK' : 'Missing', '']
                            );
                            const resultId = analysisResult.rows[0].ResultID;

                            await db.query(`
                                INSERT INTO SessionResults (SessionID, ResultID) 
                                VALUES ($1, $2);`, 
                                [sessionId, resultId]
                            );
                        } else {
                            console.error(`Clause not found in database: ${clause.name}`);
                        }
                    } catch (dbError) {
                        console.error(`Database operation failed: ${dbError}`);
                    }
                }
            }
            callback(null, results);
        } catch (parseError) {
            console.error(`Error parsing JSON from Python script: ${parseError}`);
            console.error(`Received stdout: ${stdout}`);
            callback(parseError, null);
        }
    });
}

module.exports = runPythonScript;
