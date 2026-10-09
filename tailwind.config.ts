import type {Config} from 'tailwindcss'

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
                ink: 'hsl(var(--text-main) / <alpha-value>)',
                paper: 'hsl(var(--bg-color) / <alpha-value>)',
                // Second spot ink (riso blue). Complementary to brand.
                'ink-2': {
                    DEFAULT: 'hsl(var(--ink-2) / <alpha-value>)',
                    light: 'hsl(var(--ink-2-light) / <alpha-value>)',
                    dark: 'hsl(var(--ink-2-dark) / <alpha-value>)',
                },
                'accent-1': 'hsl(var(--accent-1) / <alpha-value>)',
                'accent-2': 'hsl(var(--accent-2) / <alpha-value>)',
            },
            fontFamily: {
                // Display serif for headings/hero (Fraunces, loaded in nuxt.config).
                display: ['"Fraunces"', 'Georgia', 'serif'],
                // Readable serif for article body (Newsreader).
                serif: ['"Newsreader"', 'Georgia', 'serif'],
                // System monospace for metadata; no webfont needed.
                mono: ['ui-monospace', '"SF Mono"', '"JetBrains Mono"', 'Menlo', 'Consolas', 'monospace'],
                // Keep legacy names mapped so existing classes do not break.
                sans: ['"Newsreader"', 'Georgia', 'serif'],
                heading: ['"Fraunces"', 'Georgia', 'serif'],
            },
            fontWeight: {
                black: '900',
            },
            boxShadow: {
                // Hard riso offset shadows (no blur), one per spot ink.
                riso: '4px 4px 0 hsl(var(--brand-color) / 0.9)',
                'riso-2': '4px 4px 0 hsl(var(--ink-2) / 0.9)',
                'riso-ink': '4px 4px 0 hsl(var(--text-main) / 0.9)',
                'riso-lg': '6px 6px 0 hsl(var(--brand-color))',
            },
            rotate: {
                // Stamp-style micro-rotations.
                'stamp-l': '-2.5deg',
                'stamp-r': '2.5deg',
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
                        '--tw-prose-bullets': 'hsl(var(--text-muted))',
                        '--tw-prose-hr': 'hsl(var(--border-color))',
                        '--tw-prose-quotes': 'hsl(var(--text-main))',
                        '--tw-prose-quote-borders': 'hsl(var(--brand-color))',
                        '--tw-prose-captions': 'hsl(var(--text-muted))',
                        '--tw-prose-code': 'hsl(var(--text-main))',
                        '--tw-prose-pre-code': 'hsl(var(--text-main))',
                        '--tw-prose-pre-bg': 'hsl(var(--surface-elevated))',
                        '--tw-prose-th-borders': 'hsl(var(--border-color))',
                        '--tw-prose-td-borders': 'hsl(var(--border-color))',

                        '--tw-prose-invert-body': 'hsl(var(--text-muted))',
                        '--tw-prose-invert-headings': 'hsl(var(--text-main))',
                        '--tw-prose-invert-links': 'hsl(var(--brand-color))',
                        '--tw-prose-invert-bold': 'hsl(var(--text-main))',
                        '--tw-prose-invert-bullets': 'hsl(var(--text-muted))',
                        '--tw-prose-invert-quotes': 'hsl(var(--text-main))',
                        '--tw-prose-invert-quote-borders': 'hsl(var(--brand-color))',
                        '--tw-prose-invert-code': 'hsl(var(--text-main))',
                        '--tw-prose-invert-pre-code': 'hsl(var(--text-main))',
                        '--tw-prose-invert-pre-bg': 'hsl(var(--surface-elevated))',

                        maxWidth: '68ch',
                        a: {
                            color: 'hsl(var(--brand-color))',
                            textDecoration: 'underline',
                            textDecorationThickness: '1px',
                            textUnderlineOffset: '3px',
                            textDecorationColor: 'hsl(var(--brand-color) / 0.4)',
                            '&:hover': {
                                textDecorationColor: 'hsl(var(--brand-color))'
                            }
                        },
                        blockquote: {
                            borderLeftWidth: '2px',
                            borderLeftColor: 'hsl(var(--brand-color))',
                            fontStyle: 'normal',
                            paddingLeft: '1.25rem',
                            color: 'hsl(var(--text-muted))'
                        },
                        pre: {
                            border: '1px solid hsl(var(--border-color))',
                            borderRadius: '4px',
                            boxShadow: 'none'
                        },
                        img: {
                            borderRadius: '4px',
                            boxShadow: 'none',
                            border: '1px solid hsl(var(--border-color))'
                        }
                    }
                }
            }),
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}

export default config
