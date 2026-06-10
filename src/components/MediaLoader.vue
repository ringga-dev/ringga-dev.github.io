<template>
  <div class="relative w-full h-full overflow-hidden">
    <!-- Shimmer Placeholder -->
    <div v-if="!loaded && !hasError" class="absolute inset-0 shimmer z-10"></div>
    
    <!-- Error Fallback -->
    <div v-if="hasError" class="absolute inset-0 flex flex-col items-center justify-center bg-surface-card text-muted">
      <BoxIcon class="w-12 h-12 mb-2 opacity-25" />
      <span class="text-[10px] font-black uppercase tracking-widest opacity-40">Preview Unavailable</span>
    </div>

    <!-- Image / GIF Loader (or Video Fallback) -->
    <img 
      v-if="mediaType === 'image' || (mediaType === 'video' && hoverPlay && !isHovered) || videoError"
      :src="hoverPlay && !isHovered ? (media.poster || media.src) : (videoError && media.poster ? media.poster : media.src)" 
      :alt="altText"
      loading="lazy"
      @load="onLoad"
      @error="onError"
      class="object-cover w-full h-full transition-all duration-700"
      :class="[loaded && !hasError ? 'opacity-100' : 'opacity-0', zoomOnHover ? 'group-hover:scale-110' : '']"
    />

    <!-- Local HTML5 Video Loader -->
    <video
      v-else-if="mediaType === 'video' && isLocalVideo && !videoError"
      ref="videoRef"
      :src="media.src"
      :poster="media.poster"
      muted
      loop
      playsinline
      preload="auto"
      @loadeddata="onLoad"
      @error="onVideoError"
      class="object-cover w-full h-full transition-opacity duration-500"
      :class="[loaded && !hasError ? 'opacity-100' : 'opacity-0']"
    ></video>

    <!-- Embedded Video URL (YouTube, Vimeo, etc.) -->
    <iframe
      v-else-if="mediaType === 'video' && !isLocalVideo && !videoError"
      :src="embeddedUrl"
      frameborder="0"
      allow="autoplay; encrypted-media"
      allowfullscreen
      @load="onLoad"
      @error="onVideoError"
      class="object-cover w-full h-full transition-opacity duration-500"
      :class="[loaded && !hasError ? 'opacity-100' : 'opacity-0']"
    ></iframe>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { BoxIcon } from 'lucide-vue-next'

const props = defineProps({
  media: {
    type: Object,
    required: true,
    default: () => ({ type: 'image', src: '', poster: '' })
  },
  altText: {
    type: String,
    default: 'Media preview'
  },
  hoverPlay: {
    type: Boolean,
    default: false
  },
  isHovered: {
    type: Boolean,
    default: false
  },
  zoomOnHover: {
    type: Boolean,
    default: true
  }
})

const loaded = ref(false)
const hasError = ref(false)
const videoError = ref(false)
const videoRef = ref(null)

const mediaType = computed(() => {
  return props.media?.type || 'image'
})

const isLocalVideo = computed(() => {
  const src = props.media?.src || ''
  // If it's a relative path or direct mp4/webm link, treat as HTML5 local video
  return src.startsWith('/') || src.endsWith('.mp4') || src.endsWith('.webm') || src.includes('mixkit.co')
})

const embeddedUrl = computed(() => {
  const src = props.media?.src || ''
  let finalUrl = src
  if (src.includes('youtube.com') || src.includes('youtu.be')) {
    const videoId = src.includes('embed') ? src.split('embed/')[1] : src.split('v=')[1]
    finalUrl = `https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1&loop=1&playlist=${videoId}&controls=0&showinfo=0`
  } else if (src.includes('vimeo.com')) {
    const videoId = src.split('vimeo.com/')[1]
    finalUrl = `https://player.vimeo.com/video/${videoId}?autoplay=1&loop=1&muted=1&background=1`
  }
  return finalUrl
})

const onLoad = () => {
  loaded.value = true
}

const onError = () => {
  hasError.value = true
  loaded.value = true // stop shimmer
}

const onVideoError = (err) => {
  console.warn('Video failed to load or play. Falling back to image/poster.', err)
  videoError.value = true
  // If there's a poster, we will show it, which triggers onLoad. 
  // If there's no poster, image loading might fail or load direct src (which might also error out).
  if (!props.media?.poster) {
    hasError.value = true
    loaded.value = true
  }
}

watch(() => props.isHovered, (newVal) => {
  if (mediaType.value === 'video' && isLocalVideo.value && videoRef.value && !videoError.value) {
    if (newVal) {
      videoRef.value.play().catch(err => {
        console.warn('Video play failed:', err)
        videoError.value = true
      })
    } else {
      videoRef.value.pause()
      videoRef.value.currentTime = 0
    }
  }
})

onMounted(() => {
  // If it is a video and we are NOT using hoverPlay, auto trigger play
  if (mediaType.value === 'video' && isLocalVideo.value && !props.hoverPlay && videoRef.value && !videoError.value) {
    videoRef.value.play().catch(err => {
      console.warn('Auto video play failed. Falling back to poster image.', err)
      // Do not treat auto-play failure as block error if we have a poster to show, 
      // but if browser blocked autoplay, the video element is still showing poster.
      // If it's a real loading error, @error triggers onVideoError.
    })
  }
})
</script>
