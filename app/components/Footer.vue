<template>
  <footer class="py-24 border-t border-slate-800/30 px-6 relative overflow-hidden bg-[#020408]">
    <div class="nuxt-glow bottom-0 left-1/2 -translate-x-1/2 opacity-30"></div>
    
    <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-16 relative z-10">
      <div class="lg:col-span-2">
        <NuxtLink to="/" class="text-3xl font-black tracking-tighter mb-8 block">
          RINGGA <span class="text-[#00DC82]">DEV</span>
        </NuxtLink>
        <p class="text-slate-400 text-lg max-w-sm leading-relaxed font-medium">
          Delivering premium digital solutions across Android and Web platforms. Focused on high-performance architecture and modern design.
        </p>
      </div>
      
      <div class="flex flex-col gap-6">
        <span class="text-xs font-black uppercase tracking-[0.2em] text-[#00DC82]">Social Ecosystem</span>
        <a href="https://github.com/ringga-dev" class="nav-link text-lg">GitHub</a>
        <a href="https://www.facebook.com/ringga.septia/" class="nav-link text-lg">Facebook</a>
        <a href="https://www.instagram.com/ringga_dev/" class="nav-link text-lg">Instagram</a>
      </div>

      <div class="flex flex-col gap-6">
        <span class="text-xs font-black uppercase tracking-[0.2em] text-[#00DC82]">Direct Contact</span>
        <a href="mailto:ringgadev@gmail.com" class="nav-link text-lg">Email Me</a>
        <a href="https://api.whatsapp.com/send?phone=+6282284621151&text=Hallo" class="nav-link text-lg">WhatsApp</a>
        <div class="text-slate-500 text-sm mt-4 font-medium">
          Batam, Indonesia <br/>
          Available Worldwide
        </div>
      </div>
    </div>
    
    <div class="max-w-7xl mx-auto mt-32 pt-8 border-t border-slate-800/30 flex flex-col md:flex-row justify-between items-center gap-6 text-slate-500 text-[11px] font-black uppercase tracking-[0.3em]">
      <div>© {{ new Date().getFullYear() }} RINGGA DEV. CRAFTED WITH PASSION.</div>
      <div class="flex gap-8">
        <span class="text-[#00DC82]">NUXT 4</span>
        <span>TAILWIND CSS</span>
        <span>VITE</span>
      </div>
    </div>
  </footer>
</template>
