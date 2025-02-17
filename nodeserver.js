const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors');
const app = express();
const PORT = 5500;

app.use(cors()); // Enable cross-origin requests
app.use(express.json()); // Parse incoming JSON requests

// POST route to handle requests
app.post('/run-python', (req, res) => {
    // Extract the modelFile and hashValue from the request body
    const { modelFile, hashValue } = req.body;

    // Check if both fields are provided
    if (!modelFile || !hashValue) {
        return res.status(400).json({ error: 'Missing modelFile or hashValue' });
    }

    // Log the received data for debugging
    console.log(`Model File: ${modelFile}`);
    console.log(`Hash Value: ${hashValue}`);

    // Simulate running the Python script (you can replace this with actual logic)
    const pythonProcess = spawn('python', ['rftest.py', modelFile, hashValue]);

    let output = '';

    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code === 0) {
            res.json({ result: output.trim() });
        } else {
            res.status(500).json({ error: 'Python script execution failed.' });
        }
    });
});

// Start the server on port 5500
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
