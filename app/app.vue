<template>
  <div class="min-h-screen relative">
    <!-- Background Effects -->
    <div class="nebula-bg"></div>
    <div class="glow w-[500px] h-[500px] bg-purple-600 top-[-100px] left-[-100px]"></div>
    <div class="glow w-[400px] h-[400px] bg-blue-600 bottom-[-50px] right-[-50px]"></div>
    
    <Navbar />
    
    <main class="relative z-10">
      <NuxtPage />
    </main>

    <Footer />
  </div>
</template>

<script setup>
// No extra logic needed here for now
</script>

<style>
/* Transitions */
.page-enter-active,
.page-leave-active {
  transition: all 0.4s;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
  filter: blur(1rem);
}
</style>
