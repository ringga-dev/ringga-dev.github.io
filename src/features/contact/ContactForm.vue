<template>
  <div class="glass-card p-10 rounded-[2.5rem] bg-surface-card border border-border scroll-reveal relative overflow-hidden h-full">
    <div class="absolute -left-10 -top-10 w-40 h-40 bg-brand-light/5 rounded-full blur-3xl pointer-events-none"></div>

    <h3 class="text-2xl font-heading font-black text-main mb-8">
      {{ contactData.form.title }}
    </h3>

    <form @submit.prevent="submitForm" class="space-y-6">
      <!-- Name Field -->
      <div>
        <label for="name" class="block text-[10px] font-black uppercase text-muted tracking-widest mb-2">
          {{ contactData.form.nameLabel }}
        </label>
        <input 
          id="name"
          v-model="form.name" 
          type="text" 
          required
          :placeholder="contactData.form.namePlaceholder"
          class="w-full px-6 py-4 rounded-xl bg-surface-elevated/40 border border-border text-main font-semibold placeholder:text-muted/60 focus:border-brand/50 focus:bg-surface-elevated/80 focus:outline-none transition-all duration-300"
        />
      </div>

      <!-- Email Field -->
      <div>
        <label for="email" class="block text-[10px] font-black uppercase text-muted tracking-widest mb-2">
          {{ contactData.form.emailLabel }}
        </label>
        <input 
          id="email"
          v-model="form.email" 
          type="email" 
          required
          :placeholder="contactData.form.emailPlaceholder"
          class="w-full px-6 py-4 rounded-xl bg-surface-elevated/40 border border-border text-main font-semibold placeholder:text-muted/60 focus:border-brand/50 focus:bg-surface-elevated/80 focus:outline-none transition-all duration-300"
        />
      </div>

      <!-- Message Field -->
      <div>
        <label for="message" class="block text-[10px] font-black uppercase text-muted tracking-widest mb-2">
          {{ contactData.form.messageLabel }}
        </label>
        <textarea 
          id="message"
          v-model="form.message" 
          rows="4"
          required
          :placeholder="contactData.form.messagePlaceholder"
          class="w-full px-6 py-4 rounded-xl bg-surface-elevated/40 border border-border text-main font-semibold placeholder:text-muted/60 focus:border-brand/50 focus:bg-surface-elevated/80 focus:outline-none transition-all duration-300 resize-none"
        ></textarea>
      </div>

      <!-- Submit Button -->
      <button 
        type="submit" 
        :disabled="isSubmitting"
        class="w-full btn-primary flex items-center justify-center gap-3 py-4 font-black uppercase tracking-wider text-xs"
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
