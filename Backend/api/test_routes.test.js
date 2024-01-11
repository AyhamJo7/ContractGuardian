const request = require('supertest');
const express = require('express');
const multer = require('multer');
const router = require('./routes'); 
const runPythonScript = require('./pythonScriptRunner');
jest.mock('./pythonScriptRunner');

const app = express();
const upload = multer({ dest: 'uploads/' });
app.use(upload.single('file'));
app.use('/api', router);

describe('/api/analyze endpoint', () => {
  beforeEach(() => {
    runPythonScript.mockReset();
  });

  it('should handle file upload and return analysis result', async () => {
    runPythonScript.mockImplementation((inputPath, callback) => {
      callback(null, JSON.stringify({ analysis: 'success' }));
    });

    const response = await request(app)
      .post('/api/analyze')
      .attach('file', 'C:\\Users\\ayham\\Desktop\\Dummy_GmbH_Gesellschaftervertrag.pdf'); // Replace with path to a test file

    expect(response.statusCode).toBe(200);
    expect(response.body).toEqual({ analysis: 'success' });
  });

  it('should return error if no file is uploaded', async () => {
    const response = await request(app).post('/api/analyze');
    expect(response.statusCode).toBe(400);
    expect(response.text).toBe('No file uploaded.');
  });

});

/* Ergebnisse:
PS C:\Users\ayham\Desktop\Projekt\ContractGuardian\Backend\api> npm test

> api@1.0.0 test
> jest

 PASS  test_routes.test.js
 ✓ Test case 1: should handle file upload and return analysis result (34 ms)
 ✓ Test case 2: should return error if no file is uploaded (4 ms)

Test Suites: 1 passed, 1 total
Tests:       2 passed, 2 total
Snapshots:   0 total
Time:        1.382 s, estimated 3 s

PS C:\Users\ayham\Desktop\Projekt\ContractGuardian\Backend\api> */

