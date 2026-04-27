<template>
  <footer class="pt-32 pb-12 border-t border-slate-800/50 px-6 relative overflow-hidden">
    <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-16 relative z-10">
      <div class="lg:col-span-2 scroll-reveal">
        <NuxtLink to="/" class="group flex items-center gap-4 mb-8">
          <RdLogo size="md" />
          <span class="text-3xl font-heading font-black tracking-tighter">
            RINGGA <span class="text-brand">DEV</span>
          </span>
        </NuxtLink>
        <p class="text-slate-400 text-lg max-w-sm leading-relaxed font-medium">
          Delivering premium digital solutions across Android and Web platforms. Focused on high-performance architecture and modern design.
        </p>
        
        <div class="flex gap-4 mt-10">
          <a v-for="social in socials" :key="social.name" :href="social.url" target="_blank" 
             class="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-400 hover:text-brand hover:border-brand/30 hover:-translate-y-1 transition-all duration-300">
            <component :is="social.icon" class="w-5 h-5" />
          </a>
        </div>
      </div>
      
      <div class="flex flex-col gap-6 scroll-reveal" style="transition-delay: 200ms">
        <span class="text-xs font-black uppercase tracking-[0.2em] text-brand">Quick Links</span>
        <NuxtLink v-for="link in links" :key="link.path" :to="link.path" class="nav-link text-lg">{{ link.name }}</NuxtLink>
      </div>

      <div class="flex flex-col gap-6 scroll-reveal" style="transition-delay: 400ms">
        <span class="text-xs font-black uppercase tracking-[0.2em] text-brand">Contact Info</span>
        <a href="mailto:ringgadev@gmail.com" class="nav-link text-lg flex items-center gap-3">
          <MailIcon class="w-5 h-5" />
          Email Me
        </a>
        <a href="https://api.whatsapp.com/send?phone=+6282284621151&text=Hallo" class="nav-link text-lg flex items-center gap-3">
          <PhoneIcon class="w-5 h-5" />
          WhatsApp
        </a>
        <div class="text-slate-500 text-sm mt-4 font-medium flex items-center gap-3">
          <MapPinIcon class="w-5 h-5" />
          Batam, Indonesia
        </div>
      </div>
    </div>
    
    <div class="max-w-7xl mx-auto mt-24 pt-8 border-t border-slate-800/30 flex flex-col md:flex-row justify-between items-center gap-6 text-slate-500 text-[10px] font-black uppercase tracking-[0.3em]">
      <div>© {{ new Date().getFullYear() }} RINGGA DEV. ALL RIGHTS RESERVED.</div>
      <div class="flex gap-8 items-center">
        <span class="text-brand">Built with Nuxt 4</span>
        <div class="w-1 h-1 rounded-full bg-slate-800"></div>
        <span>Tailwind CSS</span>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { 
  GithubIcon, 
  FacebookIcon, 
  InstagramIcon, 
  LinkedinIcon,
  MailIcon,
  PhoneIcon,
  MapPinIcon
} from 'lucide-vue-next'

const links = [
  { name: 'Home', path: '/' },
  { name: 'Projects', path: '/projects' },
  { name: 'About', path: '/about' }
]

const socials = [
  { name: 'GitHub', icon: GithubIcon, url: 'https://github.com/ringga-dev' },
  { name: 'Facebook', icon: FacebookIcon, url: 'https://www.facebook.com/ringga.septia/' },
  { name: 'Instagram', icon: InstagramIcon, url: 'https://www.instagram.com/ringga_dev/' },
  { name: 'LinkedIn', icon: LinkedinIcon, url: '#' }
]
</script>

