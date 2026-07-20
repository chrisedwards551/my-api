const express = require('express');
const { getUsers } = require('../services/userService');

const router = express.Router();

router.get('/', async (req, res) => {
    try {
        const users = await getUsers();

        res.json(users);

    } catch (error) {
        console.error(error);

        if (error.name === 'AbortError') {
            return res.status(503).json({
                message: 'FastAPI service timeout'
            });
        }

        res.status(503).json({
            message: 'FastAPI service unavailable',
            error: error.message
        });
    }
});

module.exports = router;