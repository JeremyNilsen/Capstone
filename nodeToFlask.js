const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
const PORT = 5500;

// Allow cross-origin requests
app.use(cors());
app.use(express.json());

// Flask server URL
const FLASK_SERVER_URL = 'http://localhost:5000';

// Route to handle requests from the frontend
app.post('/run-python', async (req, res) => {
    const { modelFile, hashValue } = req.body;

    if (!hashValue) {
        return res.status(400).json({ error: 'Missing hashValue' });
    }

    try {
        // Send data to Flask
        const response = await axios.post(`${FLASK_SERVER_URL}/run-python`, { modelFile, hashValue });
        res.json(response.data);
    } catch (error) {
        console.error(`Error calling Flask server: ${error.message}`);
        res.status(500).json({ error: 'Flask server execution failed.' });
    }
});

// Start server
app.listen(PORT, () => {
    console.log(`Node.js server running on http://localhost:${PORT}`);
});
