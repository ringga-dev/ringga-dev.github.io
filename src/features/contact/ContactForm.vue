<template>
  <div class="riso-card p-10 bg-surface-card relative overflow-hidden h-full">
    <h3 class="text-2xl font-display font-bold text-main mb-8">
      {{ contactData.form.title }}
    </h3>

    <form @submit.prevent="submitForm" class="space-y-6">
      <!-- Name Field -->
      <div>
        <label for="name" class="block font-mono text-[10px] font-semibold uppercase text-muted tracking-[0.2em] mb-2">
          {{ contactData.form.nameLabel }}
        </label>
        <input
          id="name"
          v-model="form.name"
          type="text"
          required
          :placeholder="contactData.form.namePlaceholder"
          class="w-full px-5 py-4 rounded-sm bg-surface-card border-[1.5px] border-ink/70 text-main font-serif placeholder:text-muted/60 hover:border-ink focus:border-brand focus:shadow-[3px_3px_0_hsl(var(--brand-color)/0.5)] transition-[box-shadow,border-color] duration-150"
        />
      </div>

      <!-- Email Field -->
      <div>
        <label for="email" class="block font-mono text-[10px] font-semibold uppercase text-muted tracking-[0.2em] mb-2">
          {{ contactData.form.emailLabel }}
        </label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          required
          :placeholder="contactData.form.emailPlaceholder"
          class="w-full px-5 py-4 rounded-sm bg-surface-card border-[1.5px] border-ink/70 text-main font-serif placeholder:text-muted/60 hover:border-ink focus:border-brand focus:shadow-[3px_3px_0_hsl(var(--brand-color)/0.5)] transition-[box-shadow,border-color] duration-150"
        />
      </div>

      <!-- Message Field -->
      <div>
        <label for="message" class="block font-mono text-[10px] font-semibold uppercase text-muted tracking-[0.2em] mb-2">
          {{ contactData.form.messageLabel }}
        </label>
        <textarea
          id="message"
          v-model="form.message"
          rows="4"
          required
          :placeholder="contactData.form.messagePlaceholder"
          class="w-full px-5 py-4 rounded-sm bg-surface-card border-[1.5px] border-ink/70 text-main font-serif placeholder:text-muted/60 hover:border-ink focus:border-brand focus:shadow-[3px_3px_0_hsl(var(--brand-color)/0.5)] transition-[box-shadow,border-color] duration-150 resize-none"
        ></textarea>
      </div>

      <!-- Submit Button -->
      <button
        type="submit"
        :disabled="isSubmitting"
        class="w-full btn-primary flex items-center justify-center gap-3 py-4 font-mono font-semibold uppercase tracking-[0.18em] text-xs"
      >
        <SendIcon class="w-5 h-5" v-if="!isSubmitting" />
        <LoaderIcon class="w-5 h-5 animate-spin" v-else />
        {{ isSubmitting ? contactData.form.sendingText : contactData.form.submitText }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { SendIcon, LoaderIcon } from 'lucide-vue-next'
import contactData from '~/data/contact.json'
import globalData from '~/data/global.json'

const isSubmitting = ref(false)
const form = reactive({
  name: '',
  email: '',
  message: ''
})

const submitForm = () => {
  isSubmitting.value = true

  // Format WhatsApp message
  const phone = '6282284621151' // Raw clean phone number
  const intro = `Halo Ringga, nama saya ${form.name} (${form.email}).`
  const text = encodeURIComponent(`${intro}\n\n${form.message}`)

  setTimeout(() => {
    // Open WhatsApp link
    if (process.client) {
      window.open(`https://api.whatsapp.com/send?phone=${phone}&text=${text}`, '_blank')
    }

    // Reset form
    form.name = ''
    form.email = ''
    form.message = ''
    isSubmitting.value = false
  }, 1000)
}
</script>
