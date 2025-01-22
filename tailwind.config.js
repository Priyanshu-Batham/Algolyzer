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

  // DaisyUI Theme setup
  daisyui: {
    themes: [
      "winter",
      // {
      //   algolyzer2: {
      //     "primary": "#00ffcc",        // Neon teal for primary actions or key highlights
      //     "secondary": "#ff0099",      // Vibrant magenta for secondary elements
      //     "accent": "#00ff66",         // Bright green for accents
      //     "neutral": "#0d1117",        // Deep, dark gray for backgrounds (similar to GitHub's dark mode)
      //     "base-100": "#161b22",       // Slightly lighter gray for base elements
      //     "info": "#00aaff",           // Electric blue for informational components
      //     "success": "#00ff88",        // Fluorescent green for success states
      //     "warning": "#ffbf00",        // Warm gold for warnings
      //     "error": "#ff003c"           // Vivid red for error messages
      //   }
              
      // }
    ],
  },
}

// {
//   algolyzer2: {
//     "primary": "#00d4ff",
//     "primary-focus": "#00b5e3",
//     "primary-content": "#ffffff",
//     "secondary": "#ff00d4",
//     "secondary-focus": "#d400b5",
//     "secondary-content": "#ffffff",
//     "accent": "#00ff6e",
//     "accent-focus": "#00cc5a",
//     "accent-content": "#121212",
//     "neutral": "#1c1f26",
//     "neutral-focus": "#2c303a",
//     "neutral-content": "#ffffff",
//     "base-100": "#121212",
//     "base-200": "#1f1f2e",
//     "base-300": "#2a2a3f",
//     "base-content": "#d1d5db",
//     "info": "#3b82f6",
//     "info-focus": "#2563eb",
//     "info-content": "#ffffff",
//     "success": "#22c55e",
//     "success-focus": "#16a34a",
//     "success-content": "#ffffff",
//     "warning": "#f59e0b",
//     "warning-focus": "#d97706",
//     "warning-content": "#121212",
//     "error": "#ef4444",
//     "error-focus": "#dc2626",
//     "error-content": "#ffffff",
//     "ring": "#00d4ff",
//     "glow": "rgba(0, 212, 255, 0.3)",
//     "shadow": "rgba(0, 0, 0, 0.8)"
//   }        
// },