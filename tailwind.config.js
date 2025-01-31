/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './Algolyzer/templates/**/*.html', //shared template dir at root level
    './Algolyzer/**/templates/**/*.html', //template dirs at app level
  ],
  theme: {
    extend: {
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'],
        montserrat: ['Montserrat', 'sans-serif'],
        dance: ['Dancing Script', 'sans-serif']
      },
    },
  },
  plugins: [require('daisyui'),],

  // DaisyUI Theme setup
  daisyui: {
    themes: [
      "night",
    ],
  },
}