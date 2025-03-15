/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './flyingcracker/templates/**/*.html',
    './flyingcracker/**/templates/**/*.html',
    './flyingcracker/**/*.py',
  ],
  theme: {
    extend: {
      colors: {
        'flyingcracker-blue': {
          DEFAULT: '#3F6A87',
          '50': '#E6EEF3',
          '100': '#C0D5E3',
          '200': '#9BBCD3',
          '300': '#75A2C2',
          '400': '#5089B2',
          '500': '#3F6A87',
          '600': '#35596F',
          '700': '#2A4758',
          '800': '#203540',
          '900': '#152329',
        },
        'cocktail-orange': {
          DEFAULT: '#ccA17A',
          '100': '#F7EFE7',
          '200': '#EBDAC9',
          '300': '#E0C5AA',
          '400': '#D4B08C',
          '500': '#ccA17A',
          '600': '#B98857',
          '700': '#A07048',
          '800': '#7D5738',
          '900': '#5A3F28',
        },
      },
      fontFamily: {
        sans: ['Helvetica', 'Arial', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}