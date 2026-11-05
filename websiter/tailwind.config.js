/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./frontend/**/*.{html,js}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        studio: {
          black: '#090B0E',
          dark: '#0F1316',
          surface: '#161B1F',
          card: '#12161A',
          lime: '#CCFF00',
          limeHover: '#B8E600',
          cyan: '#00F0FF',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Space Grotesk', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      }
    }
  },
  plugins: []
};
