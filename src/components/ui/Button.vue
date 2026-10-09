<template>
  <button
    @click="handleClick"
    :class="[
      'inline-flex items-center justify-center font-mono font-bold uppercase tracking-[0.15em] rounded-sm border-[1.5px] transition-[transform,box-shadow,background-color,border-color,color] duration-150 focus:outline-none focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-offset-2 focus-visible:outline-brand active:translate-x-[1px] active:translate-y-[1px]',
      variantClasses[variant],
      sizeClasses[size],
      disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
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
  primary: 'bg-brand text-white border-ink shadow-riso-ink hover:bg-brand-dark hover:shadow-riso-lg hover:-translate-x-px hover:-translate-y-px active:shadow-[1px_1px_0_hsl(var(--text-main))]',
  secondary: 'bg-surface-elevated text-main border-ink/60 hover:border-ink hover:-translate-x-px hover:-translate-y-px hover:shadow-riso-ink active:shadow-[1px_1px_0_hsl(var(--text-main))]',
  outline: 'bg-transparent text-brand border-brand hover:bg-brand hover:text-white hover:shadow-riso-ink hover:-translate-x-px hover:-translate-y-px active:shadow-[1px_1px_0_hsl(var(--text-main))]',
  ghost: 'bg-transparent text-main border-transparent hover:border-ink/60 hover:-translate-x-px hover:-translate-y-px hover:shadow-riso-ink active:shadow-[1px_1px_0_hsl(var(--text-main))]',
  danger: 'bg-red-600 text-white border-ink shadow-riso-ink hover:bg-red-700 hover:-translate-x-px hover:-translate-y-px hover:shadow-riso-lg active:shadow-[1px_1px_0_hsl(var(--text-main))]'
}

const sizeClasses = {
  sm: 'px-4 py-2 text-xs gap-1.5',
  md: 'px-6 py-3 text-sm gap-2',
  lg: 'px-8 py-4 text-base gap-2.5'
}

const handleClick = (event: MouseEvent) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>
