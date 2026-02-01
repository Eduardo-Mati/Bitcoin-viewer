/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      boxShadow: {
        glow: "0 0 30px rgba(59, 130, 246, 0.25)"
      }
    }
  },
  plugins: []
};
