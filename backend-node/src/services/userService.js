const apiClient = require('../clients/apiClient');

async function getUsers() {
    return await apiClient.get('/users/');
}

module.exports = {
    getUsers
};