const express = require('express');
const pool = require('../config/database');

const router = express.Router();

router.get('/', async (req, res) => {
    try {
        const result = await pool.query(
            'SELECT id, username, email, created_at FROM users'
        );

        res.json(result.rows);

    } catch (error) {
        console.error(error);

        res.status(500).json({
            message: 'Failed to retrieve users',
            error: error.message
        });
    }
});

module.exports = router;