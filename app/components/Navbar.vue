<template>
  <nav class="fixed top-6 left-1/2 -translate-x-1/2 z-50 w-[95%] max-w-5xl">
    <div class="glass px-8 py-4 rounded-3xl flex items-center justify-between shadow-2xl">
      <NuxtLink to="/" class="text-2xl font-black tracking-tighter flex items-center gap-2">
        <div class="w-8 h-8 bg-[#00DC82] rounded-lg flex items-center justify-center text-[#020408] text-sm">R</div>
        <span>RINGGA <span class="text-[#00DC82]">DEV</span></span>
      </NuxtLink>
      
      <div class="hidden md:flex items-center gap-10">
        <NuxtLink to="/" class="nav-link" active-class="!text-[#00DC82]">Home</NuxtLink>
        <NuxtLink to="/projects" class="nav-link" active-class="!text-[#00DC82]">Projects</NuxtLink>
        <NuxtLink to="/about" class="nav-link" active-class="!text-[#00DC82]">About</NuxtLink>
      </div>

      <a href="https://api.whatsapp.com/send?phone=+6282284621151&text=Hallo" class="btn-primary text-sm">
        Hire Me
      </a>
    </div>
  </nav>
</template>

<script setup>
</script>
