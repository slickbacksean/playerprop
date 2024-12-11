module.exports = {
    // Consistent code formatting
    semi: true,
    trailingComma: 'es5',
    singleQuote: true,
    printWidth: 88,
    tabWidth: 4,
    useTabs: false,
    
    // Language-specific configurations
    overrides: [
        {
            files: '*.py',
            options: {
                parser: 'python',
                tabWidth: 4,
            },
        },
        {
            files: ['*.js', '*.jsx', '*.ts', '*.tsx'],
            options: {
                parser: 'typescript',
                tabWidth: 4,
            },
        },
    ],
    
    // Plugin configurations
    plugins: [
        'prettier-plugin-toml',
        'prettier-plugin-sort-imports',
    ],
};