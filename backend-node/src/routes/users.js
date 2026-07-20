const express = require('express');

const router = express.Router();

router.get('/', async (req, res) => {
    const controller = new AbortController();

    const timeout = setTimeout(() => {
        controller.abort();
    }, 5000);

    try {
        const response = await fetch('http://localhost:8000/users/', {
            signal: controller.signal
        });

        clearTimeout(timeout);

        if (!response.ok) {
            return res.status(response.status).json({
                message: 'FastAPI service returned an error',
                status: response.status
            });
        }

        const users = await response.json();

        res.json(users);

    } catch (error) {
        clearTimeout(timeout);

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