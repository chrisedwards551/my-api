async function getUsers() {
    const controller = new AbortController();

    const timeout = setTimeout(() => {
        controller.abort();
    }, 5000);

    try {
        const response = await fetch(`${process.env.FASTAPI_URL}/users/`, {
            signal: controller.signal
        });

        clearTimeout(timeout);

        if (!response.ok) {
            throw new Error(`FastAPI returned status ${response.status}`);
        }

        const users = await response.json();

        return users;

    } catch (error) {
        clearTimeout(timeout);

        throw error;
    }
}

module.exports = {
    getUsers
};