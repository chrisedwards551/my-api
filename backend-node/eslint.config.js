const js = require('@eslint/js');

module.exports = [
    {
        files: ['**/*.js'],
        languageOptions: {
            ecmaVersion: 'latest',
            sourceType: 'commonjs',
            globals: {
                AbortController: 'readonly',
                clearTimeout: 'readonly',
                console: 'readonly',
                fetch: 'readonly',
                module: 'readonly',
                process: 'readonly',
                require: 'readonly',
                setTimeout: 'readonly'
            }
        },
        rules: {
            ...js.configs.recommended.rules
        }
    }
];