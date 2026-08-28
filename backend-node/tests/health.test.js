const test = require('node:test');
const assert = require('node:assert');
const request = require('supertest');

const app = require('../app');

test('GET /health returns healthy status', async () => {
    const response = await request(app)
        .get('/health')
        .expect(200);

    assert.deepStrictEqual(response.body, {
        status: 'healthy',
        service: 'node-api'
    });
});