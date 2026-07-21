async function get(endpoint) {
    const controller = new AbortController();

    const timeout = setTimeout(() => {
        controller.abort();
    }, 5000);

    try {
        const response = await fetch(
            `${process.env.FASTAPI_URL}${endpoint}`,
            {
                signal: controller.signal
            }
        );

        clearTimeout(timeout);

        if (!response.ok) {
            throw new Error(`FastAPI returned status ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        clearTimeout(timeout);
        throw error;
    }
}

module.exports = {
    get
};