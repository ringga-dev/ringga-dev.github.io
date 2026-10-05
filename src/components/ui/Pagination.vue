<template>
  <nav
    v-if="totalPages > 1"
    class="flex items-center justify-center gap-2 mt-12 animate-reveal"
    style="animation-delay: 400ms"
    aria-label="Pagination"
  >
    <button
      type="button"
      @click="goTo(current - 1)"
      :disabled="current === 1"
      :aria-label="`Ke halaman sebelumnya`"
      class="w-11 h-11 rounded-xl border border-border bg-surface-elevated/40 text-muted hover:bg-surface-elevated/80 hover:text-main hover:border-brand/20 transition-all duration-300 cursor-pointer active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-surface-elevated/40 disabled:hover:text-muted"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 18-6-6 6-6"/></svg>
    </button>

    <div class="flex items-center gap-1">
      <template v-for="(page, idx) in visiblePages" :key="`${page}-${idx}`">
        <span v-if="page === '...'" class="w-8 text-center text-muted/60 select-none font-mono">…</span>
        <button
          v-else
          type="button"
          @click="goTo(page)"
          :aria-current="page === current ? 'page' : undefined"
          class="w-11 h-11 rounded-xl text-sm font-black border transition-all duration-300 cursor-pointer active:scale-95"
          :class="page === current
            ? 'bg-brand text-brand-dark border-brand shadow-lg shadow-brand/10'
            : 'bg-surface-elevated/40 hover:bg-surface-elevated/80 border-border text-muted hover:text-main hover:border-brand/20'"
        >
          {{ page }}
        </button>
      </template>
    </div>

    <button
      type="button"
      @click="goTo(current + 1)"
      :disabled="current === totalPages"
      :aria-label="`Ke halaman berikutnya`"
      class="w-11 h-11 rounded-xl border border-border bg-surface-elevated/40 text-muted hover:bg-surface-elevated/80 hover:text-main hover:border-brand/20 transition-all duration-300 cursor-pointer active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-surface-elevated/40 disabled:hover:text-muted"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>
    </button>
  </nav>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const props = defineProps({
  /** Total jumlah item (sudah difilter) */
  totalItems: { type: Number, required: true },
  /** Jumlah item per halaman */
  perPage: { type: Number, required: true },
  /** Halaman aktif (1-based), dipaginate dari parent */
  modelValue: { type: Number, default: 1 },
  /** Parameter query untuk menyinkronkan URL */
  queryKey: { type: String, default: 'page' }
})

const emit = defineEmits(['update:modelValue'])

const route = useRoute()
const router = useRouter()

const current = computed(() => props.modelValue)
const totalPages = computed(() => Math.max(1, Math.ceil(props.totalItems / props.perPage)))

// Halaman di luar jangkauan (mis. user buka /blog?page=99 saat post berkurang)
watch(totalPages, (tp) => {
  if (current.value > tp) goTo(tp)
})

function goTo(page) {
  const target = Math.min(Math.max(1, page), totalPages.value)
  if (target === current.value) return
  emit('update:modelValue', target)
}

const visiblePages = computed(() => {
  const pages = []
  const cur = current.value
  const total = totalPages.value

  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
    return pages
  }

  pages.push(1)
  if (cur > 3) pages.push('...')

  const start = Math.max(2, cur - 1)
  const end = Math.min(total - 1, cur + 1)
  for (let i = start; i <= end; i++) {
    if (i !== 1 && i !== total) pages.push(i)
  }

  if (cur < total - 2) pages.push('...')
  pages.push(total)
  return pages
})

// Sinkronkan URL setiap kali halaman berubah. Ini yang membuat route
// prerender `?page=N` di nuxt.config benar-benar menampilkan isi yang
// benar saat dibangun — sebelumnya paginasi murni client-side sehingga
// setiap page statis me-render halaman 1.
watch(current, (val) => {
  const query = { ...route.query }
  if (val === 1) {
    delete query[props.queryKey]
  } else {
    query[props.queryKey] = String(val)
  }
  router.replace({ path: route.path, query })
}, { immediate: false })
</script>
