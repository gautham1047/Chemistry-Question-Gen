/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg-primary': '#0f172a',
        'bg-secondary': '#1e293b',
        'highlight': '#334155',
        'highlight-alt': '#0891b2',
        'text-primary': '#f8fafc',
        'text-secondary': '#94a3b8',
        'accent': '#06b6d4',
        'accent-hover': '#0891b2',
        'success': '#10b981',
      },
    },
  },
  plugins: [],
}
