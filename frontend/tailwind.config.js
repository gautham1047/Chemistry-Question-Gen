/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg-primary': '#545f66',
        'bg-secondary': '#2f0a28',
        'highlight': '#829399',
        'highlight-alt': '#92b5b2',
        'text-primary': '#d5cbcd',
        'text-secondary': '#2f0a28',
      },
      fontFamily: {
        sans: ['Verdana', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
