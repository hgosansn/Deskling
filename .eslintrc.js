module.exports = {
  extends: [
    'eslint:recommended',
    'react-app'
  ],
  parserOptions: {
    ecmaVersion: 2021,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true
    }
  },
  env: {
    browser: true,
    node: true,
    es6: true
  },
  settings: {
    react: {
      pragma: 'React', // Use Preact in this project
      version: 'detect',
    },
  },
  rules: {
    // Add custom rules here
    'no-unused-vars': 'warn',
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'warn',
  }
};
