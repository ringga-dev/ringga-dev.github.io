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
      typography: (theme) => ({
        brand: {
          css: {
            '--tw-prose-body': 'hsl(var(--text-main))',
            '--tw-prose-headings': 'hsl(var(--text-main))',
            '--tw-prose-lead': 'hsl(var(--text-muted))',
            '--tw-prose-links': 'hsl(var(--brand-color))',
            '--tw-prose-bold': 'hsl(var(--text-main))',
            '--tw-prose-counters': 'hsl(var(--text-muted))',
            '--tw-prose-bullets': 'hsl(var(--brand-dark))',
            '--tw-prose-hr': 'hsl(var(--border-color))',
            '--tw-prose-quotes': 'hsl(var(--text-main))',
            '--tw-prose-quote-borders': 'hsl(var(--brand-color))',
            '--tw-prose-captions': 'hsl(var(--text-muted))',
            '--tw-prose-code': 'hsl(var(--brand-light))',
            '--tw-prose-pre-code': 'hsl(var(--text-main))',
            '--tw-prose-pre-bg': '#0b0f19',
            '--tw-prose-th-borders': 'hsl(var(--border-color))',
            '--tw-prose-td-borders': 'hsl(var(--border-color))',
            
            '--tw-prose-invert-body': 'hsl(var(--text-muted))',
            '--tw-prose-invert-headings': 'hsl(var(--text-main))',
            '--tw-prose-invert-links': 'hsl(var(--brand-color))',
            '--tw-prose-invert-bold': 'hsl(var(--text-main))',
            '--tw-prose-invert-bullets': 'hsl(var(--brand-dark))',
            '--tw-prose-invert-quotes': 'hsl(var(--text-main))',
            '--tw-prose-invert-quote-borders': 'hsl(var(--brand-color))',
            '--tw-prose-invert-code': 'hsl(var(--brand-light))',
            '--tw-prose-invert-pre-code': 'hsl(var(--text-main))',
            '--tw-prose-invert-pre-bg': '#0b0f19',
            
            a: {
              textDecoration: 'none',
              borderBottom: '1px solid hsl(var(--brand-color) / 0.3)',
              transition: 'all 0.3s',
              '&:hover': {
                color: 'hsl(var(--brand-light))',
                borderBottomColor: 'hsl(var(--brand-light))'
              }
            },
            blockquote: {
              backgroundColor: 'hsl(var(--surface-elevated) / 0.3)',
              borderRadius: '0.5rem',
              padding: '0.5rem 1rem',
              fontStyle: 'normal'
            },
            pre: {
              border: '1px solid hsl(var(--border-color) / 0.5)',
              borderRadius: '1rem',
              boxShadow: '0 10px 30px -10px rgba(0,0,0,0.5)'
            },
            img: {
              borderRadius: '1.5rem',
              boxShadow: '0 10px 40px -10px rgba(0,0,0,0.5)',
              border: '1px solid hsl(var(--border-color) / 0.3)'
            }
          }
        }
      }),
      backgroundImage: {
        'grid-slate': "url(\"data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32' width='32' height='32' fill='none' stroke='rgb(99 102 241 / 0.04)'%3e%3cpath d='M0 .5H31.5V32'/%3e%3c/svg%3e\")",
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}

export default config
