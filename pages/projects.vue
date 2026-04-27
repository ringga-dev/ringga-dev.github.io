<template>
  <div class="pt-40 pb-20 px-6">
    <div class="max-w-6xl mx-auto">
      <div class="mb-20 text-center">
        <h1 class="text-5xl md:text-7xl font-bold mb-6">All <span class="text-gradient">Projects</span></h1>
        <p class="text-white/50 max-w-2xl mx-auto">
          A comprehensive list of my digital experiments, client work, and open-source contributions.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <ProjectCard 
          v-for="project in projects" 
          :key="project.title" 
          v-bind="project" 
        />
      </div>
    </div>
  </div>
</template>

<script setup>
const projects = [
  {
    title: 'E-Commerce Platform',
    description: 'A full-featured online store with real-time inventory and AI-powered recommendations.',
    image: 'https://images.unsplash.com/photo-1557821552-17105176677c?auto=format&fit=crop&q=80&w=1600',
    category: 'Web Application',
    tags: ['Nuxt', 'Supabase', 'Tailwind'],
    github: '#',
    link: '#'
  },
  {
    title: 'Fintech Dashboard',
    description: 'Complex data visualization and management system for financial institutions.',
    image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&q=80&w=1600',
    category: 'SaaS Product',
    tags: ['Vue 3', 'Chart.js', 'PostgreSQL'],
    github: '#',
    link: '#'
  },
  {
    title: 'AI Image Generator',
    description: 'Integration with DALL-E and Midjourney APIs to generate high-quality images.',
    image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=1600',
    category: 'AI Tool',
    tags: ['OpenAI', 'Next.js', 'Vercel'],
    github: '#',
    link: '#'
  },
  {
    title: 'Crypto Portfolio Tracker',
    description: 'Real-time tracking of crypto assets across multiple wallets and exchanges.',
    image: 'https://images.unsplash.com/photo-1621761191319-c6fb62004040?auto=format&fit=crop&q=80&w=1600',
    category: 'Finance',
    tags: ['Web3', 'Ethers.js', 'React'],
    github: '#',
    link: '#'
  }
]
</script>
