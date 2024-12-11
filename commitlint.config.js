module.exports = {
    extends: ['@commitlint/config-conventional'],
    rules: {
        'type-enum': [2, 'always', [
            'build',     // Changes to build system or external dependencies
            'chore',     // Maintenance tasks
            'ci',        // CI configuration files and scripts
            'docs',      // Documentation changes
            'feat',      // New features
            'fix',       // Bug fixes
            'perf',      // Performance improvements
            'refactor',  // Code refactoring
            'revert',    // Reverting previous commits
            'style',     // Code style changes (formatting, etc.)
            'test'       // Adding or modifying tests
        ]],
        'type-case': [2, 'always', 'lower-case'],
        'type-empty': [2, 'never'],
        'scope-case': [2, 'always', 'lower-case'],
        'subject-empty': [2, 'never'],
        'subject-max-length': [2, 'always', 72]
    }
};