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
    title: 'Modern Web Application',
    description: 'A responsive and high-performance web application built with a focus on user experience and speed.',
    image: '/images/portfolio/pf1.jpg',
    category: 'Web Development',
    tags: ['HTML', 'SCSS', 'JavaScript'],
    github: 'https://github.com/ringga-dev',
    link: '#'
  },
  {
    title: 'Android Development',
    description: 'Beautifully designed Android application with intuitive user interfaces and smooth performance.',
    image: '/images/portfolio/pf2.jpg',
    category: 'Mobile App',
    tags: ['Java', 'Android SDK', 'XML'],
    github: 'https://github.com/ringga-dev',
    link: 'https://youtu.be/DD0b3db2li8'
  },
  {
    title: 'Creative Portfolio',
    description: 'Showcasing digital creativity through video and interactive design elements.',
    image: '/images/portfolio/pf3.jpg',
    category: 'Design',
    tags: ['Video Editing', 'CSS', 'UI/UX'],
    github: 'https://github.com/ringga-dev',
    link: 'https://vimeo.com/115041822'
  }
]
</script>
