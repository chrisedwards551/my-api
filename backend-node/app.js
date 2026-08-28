require('dotenv').config();

const express = require('express');
const pool = require('./src/config/database');
const usersRouter = require('./src/routes/users');

const app = express();

app.use(express.json());

app.use('/users', usersRouter);

app.get('/', (req, res) => {
    res.send('Hello from your Ubuntu VM API!');
});

// Phase 15.13 — Production Environment Hardening
// Health check endpoint for monitoring/deployment tools
app.get('/health', (req, res) => {
    res.json({
        status: 'healthy',
        service: 'node-api'
    });
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

module.exports = app;