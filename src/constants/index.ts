/**
 * Application Constants
 * Emerald Zambrut Portfolio
 */

import type { NavItem, FooterLink } from '~/types'

export const SITE_CONFIG = {
  name: 'Ringga Dev',
  tagline: 'Senior Mobile Developer',
  url: 'https://ringgadev.com',
  description: 'Ringga Septia Pribadi — Senior Mobile Developer di Batam, Indonesia. Kotlin, Jetpack Compose, Kotlin Multiplatform, dan Flutter. Pembuat kmp-printer.',
  keywords: ['Android Developer', 'Mobile Developer', 'Kotlin', 'Jetpack Compose', 'Kotlin Multiplatform', 'Flutter', 'ESC/POS', 'Batam', 'Portfolio'],
  author: 'Ringga Septia Pribadi',
  themeColor: '#F5F0E6'
} as const

export const NAVIGATION_ITEMS: NavItem[] = [
  { label: 'Home', href: '/' },
  { label: 'About', href: '/about' },
  { label: 'Projects', href: '/projects' },
  { label: 'Skills', href: '/skills' },
  { label: 'Experience', href: '/experience' },
  { label: 'Gallery', href: '/gallery' },
  { label: 'Blog', href: '/blog' },
  { label: 'Contact', href: '/contact' }
] as const

export const FOOTER_LINKS: { title: string; links: FooterLink[] }[] = [
  {
    title: 'Navigation',
    links: [
      { label: 'Home', href: '/' },
      { label: 'About', href: '/about' },
      { label: 'Projects', href: '/projects' },
      { label: 'Contact', href: '/contact' }
    ]
  },
  {
    title: 'Social',
    links: [
      { label: 'GitHub', href: 'https://github.com/ringga-dev', external: true },
      { label: 'LinkedIn', href: 'https://linkedin.com/in/ringga-dev', external: true },
      { label: 'Instagram', href: 'https://instagram.com/ringga_dev', external: true }
    ]
  },
  {
    title: 'Resources',
    links: [
      { label: 'Blog', href: '/blog' },
      { label: 'Resume', href: '/resume.pdf', external: true }
    ]
  }
] as const

export const SOCIAL_LINKS = {
  github: 'https://github.com/ringga-dev',
  linkedin: 'https://linkedin.com/in/ringga-dev',
  instagram: 'https://instagram.com/ringga_dev',
  twitter: 'https://twitter.com/ringga_dev',
  email: 'mailto:hello@ringgadev.com',
  whatsapp: 'https://wa.me/6281234567890'
} as const

export const TECH_STACK = {
  frontend: ['Vue', 'Nuxt', 'React', 'TailwindCSS', 'TypeScript'],
  backend: ['Spring Boot', 'Node.js', 'Express', 'PostgreSQL', 'MongoDB'],
  mobile: ['Android', 'Kotlin', 'KMP', 'Jetpack Compose'],
  desktop: ['JavaFX', 'Electron', 'Tauri'],
  devops: ['Docker', 'Git', 'CI/CD', 'AWS', 'Vercel'],
  tools: ['Figma', 'Android Studio', 'IntelliJ', 'VS Code']
} as const

export const ANIMATION_CONSTANTS = {
  durations: {
    fast: 200,
    normal: 400,
    slow: 600
  },
  easing: {
    default: 'cubic-bezier(0.4, 0, 0.2, 1)',
    bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    smooth: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
  }
} as const

export const BREAKPOINTS = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1536
} as const
