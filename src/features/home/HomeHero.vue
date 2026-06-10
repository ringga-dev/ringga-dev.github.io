<template>
  <section class="min-h-screen flex items-center justify-center pt-32 pb-24 px-6 relative overflow-hidden bg-surface transition-colors duration-500">
    <!-- Background glow bubbles -->
    <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-brand/5 blur-[150px] pointer-events-none rounded-full animate-pulse-slow"></div>
    <div class="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-brand-light/5 blur-[150px] pointer-events-none rounded-full animate-pulse-slow"></div>

    <!-- Math and Code floating elements -->
    <div class="absolute top-40 left-12 w-20 h-20 border border-brand/5 rounded-full animate-float hidden xl:block"></div>
    <div class="absolute bottom-40 right-16 w-16 h-16 border border-brand-light/5 rounded-2xl rotate-12 animate-float hidden xl:block" style="animation-delay: 2.5s"></div>

    <div class="max-w-6xl mx-auto w-full relative z-10">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
        
        <!-- LEFT COLUMN: Developer Intro & Identity (7 cols on lg) -->
        <div class="lg:col-span-7 text-left space-y-6 md:space-y-8 animate-reveal">
          
          <!-- Avatar + Status badge row -->
          <div class="flex flex-col sm:flex-row sm:items-center gap-6">
            <!-- Glassmorphic Avatar frame -->
            <div class="relative inline-block shrink-0">
              <div class="absolute inset-0 bg-brand rounded-full blur-2xl opacity-20 group-hover:opacity-40 transition-opacity duration-700"></div>
              <div class="p-1 rounded-full bg-gradient-to-tr from-brand to-brand-light shadow-2xl hover:scale-105 transition-transform duration-500">
                <img 
                  src="/images/branding/logo-3d.jpeg" 
                  alt="Ringga Septia Pribadi" 
                  @error="onAvatarError"
                  v-if="!avatarLoadError"
                  class="w-24 h-24 sm:w-28 sm:h-28 rounded-full object-cover border-4 border-surface shadow-inner"
                />
                <div 
                  v-else 
                  class="w-24 h-24 sm:w-28 sm:h-28 rounded-full bg-surface-card border border-border flex items-center justify-center text-brand font-heading text-3xl font-black"
                >
                  RD
                </div>
              </div>
            </div>

            <!-- Meta Title and Availability -->
            <div class="space-y-3">
              <div class="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-brand/10 border border-brand/20 text-brand text-[10px] md:text-xs font-black tracking-widest uppercase shadow-sm">
                <span class="relative flex h-2 w-2">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2 w-2 bg-brand"></span>
                </span>
                {{ homeData.hero.badge }}
              </div>
              <p class="text-xs font-black uppercase tracking-[0.2em] text-muted">
                Ringga Septia Pribadi
              </p>
            </div>
          </div>

          <!-- Main Typography Header -->
          <div class="space-y-4">
            <h1 class="text-4xl sm:text-5xl md:text-6xl font-heading font-black text-main leading-[1.1] tracking-tight">
              {{ homeData.hero.title }} <br />
              <span class="text-gradient">{{ typedRole }}</span><span class="animate-pulse text-brand font-light">|</span>
            </h1>
            
            <p class="text-muted text-base sm:text-lg md:text-xl font-medium max-w-xl leading-relaxed">
              {{ homeData.hero.description }}
            </p>
          </div>

          <!-- CTA Buttons -->
          <div class="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
            <a 
              :href="homeData.hero.primaryCta.url" 
              target="_blank" 
              class="btn-primary flex items-center justify-center gap-3 px-8 py-4 group font-black uppercase tracking-wider text-xs shadow-lg shadow-brand/10"
            >
              {{ homeData.hero.primaryCta.text }}
              <ArrowRightIcon class="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </a>
            <NuxtLink 
              :to="homeData.hero.secondaryCta.url" 
              class="btn-secondary flex items-center justify-center gap-3 px-8 py-4 font-black uppercase tracking-wider text-xs"
            >
              {{ homeData.hero.secondaryCta.text }}
            </NuxtLink>
          </div>
        </div>

        <!-- RIGHT COLUMN: Interactive IDE Console simulator (5 cols on lg) -->
        <div class="lg:col-span-5 w-full animate-reveal" style="animation-delay: 150ms">
          <div class="bg-[#0b0f19] border border-slate-800 rounded-[2rem] overflow-hidden shadow-2xl relative">
            <!-- Window Title bar -->
            <div class="bg-[#070a10] border-b border-slate-800/80 px-5 py-3.5 flex items-center justify-between">
              <!-- Window control dots -->
              <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-red-500/80 block"></span>
                <span class="w-3 h-3 rounded-full bg-yellow-500/80 block"></span>
                <span class="w-3 h-3 rounded-full bg-green-500/80 block"></span>
              </div>
              
              <!-- Tab File indicators -->
              <div class="flex gap-2">
                <button 
                  @click="activeTab = 'kotlin'"
                  class="text-[10px] px-3.5 py-1.5 rounded-lg font-mono font-bold uppercase tracking-wider flex items-center gap-1.5 transition-all"
                  :class="activeTab === 'kotlin' ? 'bg-[#0b0f19] text-brand border border-slate-800' : 'text-slate-400 hover:text-slate-100'"
                >
                  <span class="w-1.5 h-1.5 rounded-full bg-brand"></span>
                  Main.kt
                </button>
                <button 
                  @click="activeTab = 'bash'"
                  class="text-[10px] px-3.5 py-1.5 rounded-lg font-mono font-bold uppercase tracking-wider flex items-center gap-1.5 transition-all"
                  :class="activeTab === 'bash' ? 'bg-[#0b0f19] text-brand-light border border-slate-800' : 'text-slate-400 hover:text-slate-100'"
                >
                  <span class="w-1.5 h-1.5 rounded-full bg-brand-light"></span>
                  System.sh
                </button>
              </div>

              <!-- Compile/Run action -->
              <button 
                @click="runMockCompiler"
                :disabled="isRunning"
                class="flex items-center justify-center w-7 h-7 rounded-lg bg-brand/10 hover:bg-brand text-brand hover:text-slate-950 transition-colors cursor-pointer disabled:opacity-40"
                aria-label="Run Code"
              >
                <span v-if="isRunning" class="w-3 h-3 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></span>
                <span v-else class="text-[10px] font-black">▶</span>
              </button>
            </div>

            <!-- Code Editor Area -->
            <div class="p-6 h-[240px] overflow-y-auto bg-[#03060b]/40 backdrop-blur-sm border-b border-slate-800/60">
              
              <!-- Kotlin file content -->
              <div v-if="activeTab === 'kotlin'" class="font-mono text-xs text-left space-y-1.5 text-slate-300 select-none leading-relaxed">
                <p><span class="text-emerald-400">import</span> <span class="text-cyan-400">com.ringga.pos.printer.*</span></p>
                <p class="text-slate-500 text-[10px]">// KMP & Hardware Integration Expert</p>
                <p><span class="text-emerald-400">class</span> <span class="text-yellow-400">RinggaDeveloper</span> {</p>
                <p class="pl-4"><span class="text-emerald-400">val</span> coreSkills = <span class="text-emerald-400">listOf</span>(</p>
                <p class="pl-8"><span class="text-orange-400">"KMP/Compose"</span>, <span class="text-orange-400">"Android SDK"</span>, <span class="text-orange-400">"ESC/POS Printers"</span></p>
                <p class="pl-4">)</p>
                <p class="pl-4"><span class="text-emerald-400">fun</span> <span class="text-cyan-400">printCapabilities</span>() {</p>
                <p class="pl-8">printer.printHeader(<span class="text-orange-400">"BUILDING HIGH PERF ECOSYSTEM"</span>)</p>
                <p class="pl-8">printer.printDetails(<span class="text-orange-400">"Offline-First Sockets & DB APIs"</span>)</p>
                <p class="pl-4">}</p>
                <p>}</p>
              </div>

              <!-- System.sh file content -->
              <div v-if="activeTab === 'bash'" class="font-mono text-xs text-left space-y-1.5 text-slate-300 select-none leading-relaxed">
                <p><span class="text-brand-light">ringga@portfolio</span>:<span class="text-cyan-400">~</span>$ neofetch</p>
                <p class="text-slate-600">-----------------------------</p>
                <p><span class="text-brand-light">OS</span>: Android SDK / Kotlin Multiplatform</p>
                <p><span class="text-brand-light">Architecture</span>: Clean Modular / SOLID</p>
                <p><span class="text-brand-light">Uptime</span>: 3+ Years Commercial Experience</p>
                <p><span class="text-brand-light">Main Stack</span>: Kotlin, Vue, Room, Spring Boot</p>
                <p><span class="text-brand-light">Hardware API</span>: USB, Bluetooth, TCP ESC/POS</p>
                <p><span class="text-brand-light">Focus</span>: Modular Offline-first Mobile Solutions</p>
              </div>

            </div>

            <!-- Terminal Output console -->
            <div class="bg-[#020408] p-5 min-h-[120px] font-mono text-[10px] text-left text-slate-300 space-y-1 border-t border-slate-800/40 overflow-y-auto">
              <div class="text-slate-500 mb-1 border-b border-slate-800/40 pb-1 flex justify-between items-center select-none">
                <span>TERMINAL CONSOLE OUTPUT</span>
                <span class="text-[8px] px-1.5 py-0.5 rounded bg-brand/10 border border-brand/20 text-brand">ACTIVE</span>
              </div>
              
              <div v-if="consoleLogs.length === 0" class="text-slate-600 italic select-none">
                Click the Play (▶) button in the window header to run compiler simulator...
              </div>

              <div 
                v-for="(log, idx) in consoleLogs" 
                :key="idx" 
                class="leading-relaxed whitespace-pre-wrap font-semibold"
                :class="{ 
                  'text-brand': log.type === 'info', 
                  'text-cyan-400': log.type === 'step', 
                  'text-amber-300': log.type === 'warn',
                  'text-white': log.type === 'receipt'
                }"
              >
                {{ log.text }}
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Core Stack Footer with Brand Color Glows -->
      <div class="scroll-reveal w-full max-w-6xl border-t border-border pt-12 mt-20 animate-reveal" style="animation-delay: 250ms">
        <p class="text-[10px] font-black uppercase tracking-[0.3em] text-muted mb-8 text-center sm:text-left">
          {{ homeData.techStack.badge }}
        </p>
        <div class="flex flex-wrap justify-center sm:justify-start gap-4 md:gap-6">
          <div 
            v-for="tech in homeData.techStack.techs" 
            :key="tech.name" 
            class="flex flex-col items-center gap-3 group cursor-pointer"
            :style="{ '--glow-color': tech.color }"
          >
            <div 
              class="p-4 bg-surface-card rounded-2xl border border-border group-hover:border-[var(--glow-color)] transition-all duration-300 transform group-hover:-translate-y-1 relative"
              :style="{ 
                boxShadow: '0 0 0 transparent', 
              }"
              @mouseenter="onHover(tech.color, $event)"
              @mouseleave="onLeave($event)"
            >
              <component :is="getIcon(tech.icon)" class="w-6 h-6 text-muted group-hover:text-[var(--glow-color)] transition-colors duration-300" />
            </div>
            <span class="text-[9px] font-black text-muted tracking-widest uppercase group-hover:text-main transition-colors duration-300">
              {{ tech.name }}
            </span>
          </div>
        </div>
      </div>

    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
  ArrowRightIcon, 
  SmartphoneIcon, 
  LayersIcon, 
  DatabaseIcon, 
  Code2Icon, 
  CpuIcon, 
  BoxIcon 
} from 'lucide-vue-next'
import homeData from '~/data/home.json'

const avatarLoadError = ref(false)
const onAvatarError = () => {
  avatarLoadError.value = true
}

const getIcon = (name) => {
  switch (name) {
    case 'SmartphoneIcon': return SmartphoneIcon
    case 'LayersIcon': return LayersIcon
    case 'DatabaseIcon': return DatabaseIcon
    case 'Code2Icon': return Code2Icon
    case 'CpuIcon': return CpuIcon
    case 'BoxIcon': return BoxIcon
    default: return Code2Icon
  }
}

// Hover Brand Glow effect helpers
const onHover = (color, event) => {
  event.currentTarget.style.boxShadow = `0 10px 20px -10px ${color}`
  event.currentTarget.style.backgroundColor = `${color}08`
}

const onLeave = (event) => {
  event.currentTarget.style.boxShadow = 'none'
  event.currentTarget.style.backgroundColor = ''
}

// Interactive IDE widget variables and function
const activeTab = ref('kotlin')
const isRunning = ref(false)
const consoleLogs = ref([])

const runMockCompiler = async () => {
  if (isRunning.value) return
  
  isRunning.value = true
  consoleLogs.value = []
  
  // Terminal simulation steps
  const steps = [
    { text: '$ nuxt run-compiler --main RinggaDeveloper', type: 'info', delay: 100 },
    { text: '[SYSTEM] Initializing compilation environment...', type: 'step', delay: 350 },
    { text: '[SYSTEM] Resolving module dependencies (Printer-ESC-POS, Coroutines, Room)...', type: 'step', delay: 700 },
    { text: '[SUCCESS] Modules loaded. Emulating thermal printer connection (Bluetooth/Sockets)...', type: 'step', delay: 1100 },
    { 
      text: `
+------------------------------------+
|       RINGGA SEPTIA PRIBADI        |
|    MULTI-PLATFORM SYSTEMS ENG      |
+------------------------------------+
| Target: Kotlin Multiplatform (KMP) |
| Stack: Compose, Android, Vue, Spring|
| Focus: Hardware & Systems Drivers  |
+------------------------------------+
| Status: AVAILABLE FOR COOPERATION   |
+------------------------------------+
`, 
      type: 'receipt', 
      delay: 1550 
    },
    { text: 'Build successful in 1.58s.', type: 'info', delay: 1750 }
  ]

  for (const step of steps) {
    await new Promise(resolve => setTimeout(resolve, step.delay - (consoleLogs.value.length ? steps[consoleLogs.value.length-1].delay : 0)))
    consoleLogs.value.push({ text: step.text, type: step.type })
  }
  
  isRunning.value = false
}

// Typing Effect for main hero title
const roles = ['Multi-Platform Developer', 'KMP/Compose Expert', 'Systems Architect', 'Fullstack Engineer']
const typedRole = ref('')
let roleIndex = 0
let charIndex = 0
let isDeleting = false

const typeEffect = () => {
  const currentRole = roles[roleIndex]
  
  if (isDeleting) {
    typedRole.value = currentRole.substring(0, charIndex - 1)
    charIndex--
  } else {
    typedRole.value = currentRole.substring(0, charIndex + 1)
    charIndex++
  }

  let typeSpeed = isDeleting ? 45 : 85

  if (!isDeleting && charIndex === currentRole.length) {
    typeSpeed = 2200 // Keep static word longer
    isDeleting = true
  } else if (isDeleting && charIndex === 0) {
    isDeleting = false
    roleIndex = (roleIndex + 1) % roles.length
    typeSpeed = 400
  }

  setTimeout(typeEffect, typeSpeed)
}

onMounted(() => {
  typeEffect()
  // Run mock compile automatically after short delay on initial landing to engage visitors!
  setTimeout(() => {
    runMockCompiler()
  }, 1000)
})
</script>
