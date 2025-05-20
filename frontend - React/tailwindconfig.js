/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      animation: {
        'typing': 'typing 3.5s steps(30, end), blink .75s step-end infinite',
        'float': 'float 12s ease-in-out infinite',
        'float-delay-1': 'float 12s ease-in-out 2s infinite',
        'float-delay-2': 'float 14s ease-in-out 4s infinite',
        'float-delay-3': 'float 16s ease-in-out 6s infinite',
        'float-delay-4': 'float 18s ease-in-out 8s infinite',
        'float-delay-5': 'float 20s ease-in-out 10s infinite',
        'multilingual': 'multilingual 8s linear infinite',
        'slide': 'slide 8s linear infinite',
        'fade-out': 'fadeOut 0.5s forwards',
      },
      keyframes: {
        typing: {
          'from': { width: '0' },
          'to': { width: '100%' }
        },
        blink: {
          'from, to': { borderColor: 'transparent' },
          '50%': { borderColor: 'currentColor' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0) rotate(0deg)' },
          '25%': { transform: 'translateY(-10px) rotate(1deg)' },
          '50%': { transform: 'translateY(5px) rotate(-1deg)' },
          '75%': { transform: 'translateY(-5px) rotate(1deg)' },
        },
        multilingual: {
          '0%, 25%': { transform: 'translateY(0)' },
          '26%, 50%': { transform: 'translateY(-100%)' },
          '51%, 75%': { transform: 'translateY(-200%)' },
          '76%, 100%': { transform: 'translateY(-300%)' },
        },
        slide: {
          '0%, 16.66%': { transform: 'translateY(0)', opacity: 1 },
          '16.67%': { transform: 'translateY(-25%)', opacity: 0 },
          '33.33%': { transform: 'translateY(25%)', opacity: 0 },
          '33.34%, 50%': { transform: 'translateY(0)', opacity: 1 },
          '50.01%': { transform: 'translateY(-25%)', opacity: 0 },
          '66.67%': { transform: 'translateY(25%)', opacity: 0 },
          '66.68%, 83.33%': { transform: 'translateY(0)', opacity: 1 },
          '83.34%': { transform: 'translateY(-25%)', opacity: 0 },
          '99.99%': { transform: 'translateY(25%)', opacity: 0 },
          '100%': { transform: 'translateY(0)', opacity: 1 },
        },
        fadeOut: {
          '0%': { opacity: 1 },
          '100%': { opacity: 0, pointerEvents: 'none' }
        }
      },
    },
  },
  plugins: [],
}