module.exports = {
    env: {
        browser: true,
        es2021: true,
        node: true,
    },
    extends: [
        'eslint:recommended',
        'plugin:react/recommended',
        'plugin:@typescript-eslint/recommended',
    ],
    parser: '@typescript-eslint/parser',
    parserOptions: {
        ecmaFeatures: {
            jsx: true,
        },
        ecmaVersion: 12,
        sourceType: 'module',
    },
    plugins: [
        'react',
        '@typescript-eslint',
        'react-hooks',
    ],
    rules: {
        // Possible Errors
        'no-console': 'warn',
        'no-debugger': 'error',

        // Best Practices
        'eqeqeq': ['error', 'always'],
        'no-else-return': 'error',
        'no-unused-vars': 'warn',

        // Style
        'indent': ['error', 4],
        'max-len': ['warn', { code: 88 }],
        'quotes': ['error', 'single'],
        'semi': ['error', 'always'],

        // React Specific
        'react/prop-types': 'off',
        'react-hooks/rules-of-hooks': 'error',
        'react-hooks/exhaustive-deps': 'warn',
    },
    settings: {
        react: {
            version: 'detect',
        },
    },
};