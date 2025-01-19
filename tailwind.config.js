/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './Algolyzer/templates/**/*.html', //shared template dir at root level
    './Algolyzer/**/templates/**/*.html', //template dirs at app level
  ],
  theme: {
    extend: {},
  },
  plugins: [require('daisyui'),],
}

