const express = require('express');

const router = express.Router();

router.get('/', async (req, res) => {
    try {
        const response = await fetch('http://localhost:8000/users/');

        if (!response.ok) {
            throw new Error(`FastAPI returned ${response.status}`);
        }

        const users = await response.json();

        res.json(users);

    } catch (error) {
        console.error(error);

        res.status(500).json({
            message: 'Failed to retrieve users from FastAPI',
            error: error.message
        });
    }
});

module.exports = router;