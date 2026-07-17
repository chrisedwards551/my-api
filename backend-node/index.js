const express = require('express');
const pool = require('./src/config/database');

const app = express();

app.get('/', (req, res) => {
    res.send('Hello from your Ubuntu VM API!');
});

app.get('/db-test', async (req, res) => {
    try {
        const result = await pool.query('SELECT NOW()');
        
        res.json({
            message: 'Database connected!',
            time: result.rows[0]
        });

    } catch (error) {
        console.error(error);
        res.status(500).json({
            message: 'Database connection failed',
            error: error.message
        });
    }
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});