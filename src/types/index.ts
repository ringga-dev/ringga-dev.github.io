/**
 * Global Application Types
 * Emerald Zambrut Portfolio
 */

export interface SiteConfig {
  siteName: string
  tagline: string
  seo: {
    description: string
    keywords: string[]
    author: string
  }
  socials: {
    github: string
    linkedin: string
    instagram: string
    whatsapp: string
    email: string
    telegram: string
  }
}

export interface Project {
  id: string
  slug: string
  title: string
  shortDescription: string
  longDescription: string
  imageUrl: string
  gallery: string[]
  technologies: string[]
  features: string[]
  challenges: string[]
  solutions: string[]
  results: string[]
  role: string
  year: string
  client: string
  status: 'completed' | 'ongoing' | 'planned'
  demoUrl?: string
  githubUrl?: string
  caseStudyUrl?: string
  featured: boolean
  order: number
}

export interface Skill {
  name: string
  slug: string
  level: number
  icon: string
  longDescription: string
  yearsOfUse: string
  proficiency: 'Beginner' | 'Intermediate' | 'Advanced' | 'Expert'
  category: 'frontend' | 'backend' | 'mobile' | 'desktop' | 'devops' | 'tools'
}

export interface Experience {
  id: string
  company: string
  position: string
  location: string
  startDate: string
  endDate: string | null
  current: boolean
  description: string
  achievements: string[]
  technologies: string[]
  logoUrl?: string
}

export interface Education {
  institution: string
  degree: string
  field: string
  location: string
  startDate: string
  endDate: string
  gpa?: string
  achievements?: string[]
}

export interface BlogPost {
  slug: string
  title: string
  excerpt: string
  content: string
  publishedAt: string
  updatedAt: string
  coverImage: string
  tags: string[]
  category: string
  readTime: number
  featured: boolean
  author: {
    name: string
    avatar: string
  }
}

export interface GalleryItem {
  id: string
  title: string
  description: string
  imageUrl: string
  thumbnailUrl: string
  category: string
  width: number
  height: number
  takenAt?: string
}

export interface Service {
  title: string
  description: string
  icon: string
  features: string[]
  priceRange?: string
}

export interface NavItem {
  label: string
  href: string
  icon?: string
  children?: NavItem[]
}

export interface FooterLink {
  label: string
  href: string
  external?: boolean
}

export interface StatItem {
  label: string
  value: string | number
  suffix?: string
  prefix?: string
  icon: string
}
