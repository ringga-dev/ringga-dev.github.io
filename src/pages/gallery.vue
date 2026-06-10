<template>
  <div class="pt-32 md:pt-44 pb-32 px-6 min-h-screen relative overflow-hidden bg-surface text-main">
    <!-- Nebula bubble glows -->
    <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-brand/5 blur-[150px] pointer-events-none rounded-full"></div>
    <div class="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-brand-light/5 blur-[150px] pointer-events-none rounded-full"></div>

    <div class="max-w-7xl mx-auto relative z-10">
      <!-- Section Header -->
      <SectionHeader 
        badge="Creative Showcase"
        description="A visual showcase of interface designs, product mockups, and custom branding assets built throughout our engineering journey."
        centered
      >
        <template #title>
          Design & UI <span class="text-gradient">Gallery</span>
        </template>
      </SectionHeader>

      <!-- Category Filter Pills -->
      <div class="flex flex-wrap items-center justify-center gap-3 mt-12 relative z-10">
        <button
          v-for="cat in categories"
          :key="cat"
          @click="selectedCategory = cat"
          class="gallery-filter-pill"
          :class="selectedCategory === cat 
            ? 'gallery-filter-pill--active' 
            : 'gallery-filter-pill--inactive'"
        >
          {{ cat }}
          <span 
            v-if="cat !== 'All'" 
            class="ml-1.5 text-[8px] opacity-60"
          >
            {{ getCategoryCount(cat) }}
          </span>
        </button>
      </div>

      <!-- Gallery Grid -->
      <TransitionGroup
        tag="div"
        class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3 sm:gap-5 mt-16"
        enter-active-class="transition-all duration-500 ease-out"
        leave-active-class="transition-all duration-300 ease-in"
        enter-from-class="opacity-0 scale-90 translate-y-4"
        leave-to-class="opacity-0 scale-90 -translate-y-4"
        move-class="transition-all duration-500 ease-out"
      >
        <GalleryCard
          v-for="(item, idx) in filteredItems"
          :key="item.id"
          :item="item"
          :index="idx"
          @select="lightbox.open"
        />
      </TransitionGroup>
      
      <!-- Empty state -->
      <div v-if="filteredItems.length === 0" class="gallery-empty-state">
        <div class="gallery-empty-icon">
          <ImageOffIcon class="w-10 h-10" />
        </div>
        <p class="text-lg font-heading font-bold mt-4">No designs found</p>
        <p class="text-sm text-muted mt-1">Try selecting a different category</p>
      </div>
    </div>

    <!-- Lightbox Modal -->
    <GalleryLightbox
      :items="filteredItems"
      :active-index="lightbox.activeIndex.value"
      :is-open="lightbox.isOpen.value"
      :current-item="lightbox.currentItem.value"
      :total-items="lightbox.totalItems.value"
      :direction="lightbox.direction.value"
      @close="lightbox.close"
      @next="lightbox.next"
      @prev="lightbox.prev"
      @jump-to="lightbox.open"
    />

    <BackToTop />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ImageOffIcon } from 'lucide-vue-next'
import { useLightbox } from '~/composables/useLightbox'
import globalData from '~/data/global.json'

const categories = ["All", "Mobile UI", "Web Design", "SaaS Platform", "UI/UX Design"]
const selectedCategory = ref("All")

const items = [
  { id: 1, title: "Smart IoT Dashboard", category: "UI/UX Design", image: "/images/gallery/gallery-1.png" },
  { id: 2, title: "Fintech Mobile App", category: "Mobile UI", image: "/images/gallery/gallery-2.png" },
  { id: 3, title: "Creative Agency Landing", category: "Web Design", image: "/images/gallery/gallery-3.png" },
  { id: 4, title: "Crypto Portfolio Tracker", category: "UI/UX Design", image: "/images/gallery/gallery-4.png" },
  { id: 5, title: "E-Commerce Checkout", category: "Web Design", image: "/images/gallery/gallery-5.png" },
  { id: 6, title: "Healthcare SaaS Dashboard", category: "SaaS Platform", image: "/images/gallery/gallery-6.png" },
  { id: 7, title: "Fitness Tracking Mobile", category: "Mobile UI", image: "/images/gallery/gallery-7.png" },
  { id: 8, title: "Music Streaming Client", category: "Mobile UI", image: "/images/gallery/gallery-8.png" },
  { id: 9, title: "SaaS Analytics Dashboard", category: "SaaS Platform", image: "/images/gallery/gallery-9.png" },
  { id: 10, title: "Real Estate Portal", category: "Web Design", image: "/images/gallery/gallery-10.png" },
  { id: 11, title: "Travel Booking App", category: "Mobile UI", image: "/images/gallery/gallery-11.png" },
  { id: 12, title: "Cybersecurity Ops Center", category: "SaaS Platform", image: "/images/gallery/gallery-12.png" },
  { id: 13, title: "Food Delivery Interface", category: "Mobile UI", image: "/images/gallery/gallery-13.png" },
  { id: 14, title: "AI Image Editor", category: "UI/UX Design", image: "/images/gallery/gallery-14.png" },
  { id: 15, title: "Project Management Workspace", category: "SaaS Platform", image: "/images/gallery/gallery-15.png" },
  { id: 16, title: "Minimalist Portfolios", category: "Web Design", image: "/images/gallery/gallery-16.png" },
  { id: 17, title: "Task Planner Interface", category: "Mobile UI", image: "/images/gallery/gallery-17.png" },
  { id: 18, title: "Digital Wallet Dashboard", category: "Mobile UI", image: "/images/gallery/gallery-18.png" },
  { id: 19, title: "Blog & Article Layout", category: "Web Design", image: "/images/gallery/gallery-19.png" },
  { id: 20, title: "LMS Learning Portal", category: "SaaS Platform", image: "/images/gallery/gallery-20.png" },
  { id: 21, title: "Fashion Store Frontend", category: "Web Design", image: "/images/gallery/gallery-21.png" },
  { id: 22, title: "CRM Sales Pipeline", category: "SaaS Platform", image: "/images/gallery/gallery-22.png" },
  { id: 23, title: "Recipe & Cooking App", category: "Mobile UI", image: "/images/gallery/gallery-23.png" },
  { id: 24, title: "Kanban Productivity Board", category: "UI/UX Design", image: "/images/gallery/gallery-24.png" },
  { id: 25, title: "E-Learning Homepage", category: "Web Design", image: "/images/gallery/gallery-25.png" },
  { id: 26, title: "Stock Brokerage App", category: "Mobile UI", image: "/images/gallery/gallery-26.png" },
  { id: 27, title: "Event Organizer Calendar", category: "SaaS Platform", image: "/images/gallery/gallery-27.png" },
  { id: 28, title: "Social Platform Feed", category: "Mobile UI", image: "/images/gallery/gallery-28.png" }
]

const filteredItems = computed(() => {
  if (selectedCategory.value === "All") return items
  return items.filter(item => item.category === selectedCategory.value)
})

const getCategoryCount = (cat: string) => {
  return items.filter(item => item.category === cat).length
}

// Use the Nuxt 4 SSR-safe lightbox composable
const lightbox = useLightbox(() => filteredItems.value)

useHead({
  title: `Gallery | ${globalData.siteName}`,
  meta: [
    { name: 'description', content: `Explore the creative UI/UX layouts, branding mockups, and mobile graphics crafted by ${globalData.siteName}.` }
  ]
})
</script>

<style scoped>
.gallery-filter-pill {
  @apply px-5 py-2.5 rounded-xl border text-xs font-black uppercase tracking-wider transition-all duration-300 active:scale-95 cursor-pointer flex items-center;
}

.gallery-filter-pill--active {
  color: hsl(var(--brand-color));
  background: hsl(var(--brand-color) / 0.1);
  border-color: hsl(var(--brand-color) / 0.5);
  box-shadow: 0 0 20px hsl(var(--brand-color) / 0.12), inset 0 0 15px hsl(var(--brand-color) / 0.05);
}

.gallery-filter-pill--inactive {
  color: hsl(var(--text-muted));
  background: hsl(var(--surface-card) / 0.45);
  border-color: hsl(var(--border-color));
}

.gallery-filter-pill--inactive:hover {
  color: hsl(var(--text-main));
  border-color: hsl(var(--brand-color) / 0.3);
}

.gallery-empty-state {
  @apply text-center py-24 flex flex-col items-center;
  color: hsl(var(--text-muted));
}

.gallery-empty-icon {
  @apply w-20 h-20 rounded-2xl flex items-center justify-center;
  background: hsl(var(--surface-card) / 0.5);
  border: 1px solid hsl(var(--border-color) / 0.5);
  color: hsl(var(--text-muted) / 0.5);
}
</style>
