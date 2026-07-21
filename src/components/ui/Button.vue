<template>
  <button
    @click="handleClick"
    :class="[
      'inline-flex items-center justify-center font-semibold transition-all duration-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-offset-2',
      variantClasses[variant],
      sizeClasses[size],
      disabled ? 'opacity-50 cursor-not-allowed' : 'hover:scale-105 active:scale-95',
      className
    ]"
    :disabled="disabled || loading"
    :type="type"
  >
    <span v-if="loading" class="mr-2">
      <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
      </svg>
    </span>
    
    <slot name="icon-left"></slot>
    
    <span v-if="$slots.default"><slot /></span>
    
    <slot name="icon-right"></slot>
  </button>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  loading?: boolean
  className?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  type: 'button',
  disabled: false,
  loading: false,
  className: ''
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const variantClasses = {
  primary: 'bg-brand text-brand-dark hover:bg-brand/90 shadow-lg shadow-brand/25 focus:ring-brand',
  secondary: 'bg-surface-elevated text-main hover:bg-surface-elevated/80 border border-border focus:ring-brand',
  outline: 'bg-transparent text-main border-2 border-brand hover:bg-brand/10 focus:ring-brand',
  ghost: 'bg-transparent text-main hover:bg-surface-elevated focus:ring-brand',
  danger: 'bg-red-500 text-white hover:bg-red-600 shadow-lg shadow-red-500/25 focus:ring-red-500'
}

const sizeClasses = {
  sm: 'px-4 py-2 text-sm gap-1.5',
  md: 'px-6 py-3 text-base gap-2',
  lg: 'px-8 py-4 text-lg gap-2.5'
}

const handleClick = (event: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>
