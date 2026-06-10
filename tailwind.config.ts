import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    "./src/components/**/*.{js,vue,ts}",
    "./src/features/**/*.{js,vue,ts}",
    "./src/layouts/**/*.vue",
    "./src/pages/**/*.vue",
    "./src/plugins/**/*.{js,ts}",
    "./src/app.vue",
    "./src/error.vue",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: 'hsl(var(--brand-color) / <alpha-value>)',
          light: 'hsl(var(--brand-light) / <alpha-value>)',
          dark: 'hsl(var(--brand-dark) / <alpha-value>)',
        },
        surface: {
          DEFAULT: 'hsl(var(--bg-color) / <alpha-value>)',
          card: 'hsl(var(--surface-card) / <alpha-value>)',
          elevated: 'hsl(var(--surface-elevated) / <alpha-value>)',
        },
        main: 'hsl(var(--text-main) / <alpha-value>)',
        muted: 'hsl(var(--text-muted) / <alpha-value>)',
        border: 'hsl(var(--border-color) / <alpha-value>)',
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
        heading: ['"Space Grotesk"', 'sans-serif'],
      },
      animation: {
        'gradient-x': 'gradient-x 15s ease infinite',
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        'gradient-x': {
          '0%, 100%': {
            'background-size': '200% 200%',
            'background-position': 'left center'
          },
          '50%': {
            'background-size': '200% 200%',
            'background-position': 'right center'
          }
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' },
        }
      },
      backgroundImage: {
        'grid-slate': "url(\"data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32' width='32' height='32' fill='none' stroke='rgb(99 102 241 / 0.04)'%3e%3cpath d='M0 .5H31.5V32'/%3e%3c/svg%3e\")",
      }
    },
  },
  plugins: [],
}

export default config
