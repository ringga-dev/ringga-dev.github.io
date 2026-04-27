<template>
  <footer class="py-20 border-t border-white/5 px-6">
    <div class="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-10">
      <div>
        <div class="text-xl font-bold tracking-tighter mb-4">
          RINGGA<span class="text-purple-500">DEV</span>
        </div>
        <p class="text-white/40 text-sm max-w-xs">
          Built with Nuxt 4 and Tailwind CSS. Designed for maximum performance and premium aesthetics.
        </p>
      </div>
      
      <div class="flex gap-10">
        <div class="flex flex-col gap-3">
          <span class="text-xs font-bold uppercase tracking-widest text-white/20">Socials</span>
          <a href="#" class="text-sm text-white/60 hover:text-white transition-colors">GitHub</a>
          <a href="#" class="text-sm text-white/60 hover:text-white transition-colors">LinkedIn</a>
          <a href="#" class="text-sm text-white/60 hover:text-white transition-colors">Instagram</a>
        </div>
        <div class="flex flex-col gap-3">
          <span class="text-xs font-bold uppercase tracking-widest text-white/20">Contact</span>
          <a href="mailto:contact@ringga.dev" class="text-sm text-white/60 hover:text-white transition-colors">Email</a>
          <a href="#" class="text-sm text-white/60 hover:text-white transition-colors">Telegram</a>
        </div>
      </div>
    </div>
    
    <div class="max-w-6xl mx-auto mt-20 text-center text-white/20 text-[10px] uppercase tracking-[0.2em]">
      © {{ new Date().getFullYear() }} RINGGA DEV. ALL RIGHTS RESERVED.
    </div>
  </footer>
</template>
