// eslint.config.cjs
const pluginJs = require("@eslint/js");

module.exports = [
  pluginJs.configs.recommended,
  {
    rules: {
      "no-unused-vars": "warn",
      "no-undef": "warn",
      "semi": ["error", "always"],
      "quotes": ["error", "single"],
      "eqeqeq": "warn",
      "curly": "error",
      "no-console": "warn",
      "no-eval": "error",
      "no-debugger": "error",
      "indent": ["error", 2],
      "comma-dangle": ["error", "never"],
      "camelcase": ["error", { "properties": "always", "ignoreDestructuring": false }],
      "new-cap": ["error", { "newIsCap": true, "capIsNew": true }],
      "max-len": ["warn", { "code": 100, "ignoreUrls": true }],
      "space-infix-ops": "error",
      "keyword-spacing": "error",
      "space-before-blocks": "error",
      "space-unary-ops": "error",
      "prefer-const": "error",
      "no-var": "error",
      "no-implicit-globals": "error",
      "no-restricted-syntax": [
        "error",
        { "selector": "CallExpression[callee.name='eval']", "message": "Avoid eval()." },
        { "selector": "Identifier[name='cur_frm']", "message": "Deprecated API cur_frm is not allowed." },
        { "selector": "CallExpression[callee.name='get_query']", "message": "Deprecated API get_query()." },
        { "selector": "CallExpression[callee.name='add_fetch']", "message": "Deprecated API add_fetch()." }
      ]
    }
  }
];