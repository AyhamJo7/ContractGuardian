const { exec } = require('child_process');
const db = require('./database');
const dotenv = require('dotenv');

dotenv.config();

let clauseIdMap = {};

async function loadClauseIdMap() {
    try {
        const allClauses = await db.query('SELECT clauseid, clausename FROM Clauses');
        allClauses.rows.forEach(row => {
            let clausename = row.clausename ? row.clausename.toLowerCase().trim() : '';
            if (clausename) {
                clauseIdMap[clausename] = row.clauseid; 
            } else {
                console.error(`Invalid or empty clause name for row: ${JSON.stringify(row)}`);
            }
        });
    } catch (error) {
        console.error('Error initializing Clause ID Map:', error);
    }
}

loadClauseIdMap();

function generateSummary(results) {
    let redCount = results['Red Flags'].length;
    let orangeCount = results['Orange Flags'].length;
    let greenCount = results['Green Flags'].length;
    return `Analysis completed. Red Flags: ${redCount}, Orange Flags: ${orangeCount}, Green Flags: ${greenCount}`;
}

async function runPythonScript(inputPath, callback) {
    await loadClauseIdMap(); 

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
                VALUES ($1, $2, $3) RETURNING sessionid;`, 
                [new Date(), inputPath, summary]
            );
            const sessionId = sessionResult.rows[0].sessionid;

            for (const flagType in results) {
                for (const clause of results[flagType]) {
                    const clauseKey = clause.name.toLowerCase().trim();
                    const clauseid = clauseIdMap[clauseKey];

                    if (clauseid) {
                        const analysisResult = await db.query(`
                            INSERT INTO AnalysisResults (clauseid, AnalysisDate, Status, AdditionalNotes) 
                            VALUES ($1, $2, $3, $4) RETURNING resultid;`, 
                            [clauseid, new Date(), clause.status === '✓' ? 'OK' : 'Missing', '']
                        );
                        const resultId = analysisResult.rows[0].resultid;

                        await db.query(`
                            INSERT INTO SessionResults (SessionID, ResultID) 
                            VALUES ($1, $2);`, 
                            [sessionId, resultId]
                        );
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
