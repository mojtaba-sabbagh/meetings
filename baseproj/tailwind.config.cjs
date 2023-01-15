/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./node_modules/flowbite/**/*.js",
    './src/**/*.{html,js}', 
    './node_modules/tw-elements/dist/js/**/*.js'
  ],
  theme: {
    extend: {
       // Some useful comment
       fontFamily: {
        'farsi': ['Yekan'],
      },
    },
  },
  plugins: [
    require('tailwindcss-rtl'),
    require('flowbite/plugin'),
    require('tw-elements/dist/plugin'),
  ],
}
