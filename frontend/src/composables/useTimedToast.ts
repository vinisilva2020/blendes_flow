import { computed, onUnmounted, shallowRef } from 'vue'

type ToastTone = 'success' | 'error'

type ToastState = {
  id: number
  message: string
  tone: ToastTone
}

const DEFAULT_SUCCESS_DURATION = 3600

export function useTimedToast() {
  const toast = shallowRef<ToastState | null>(null)
  let hideTimer: ReturnType<typeof window.setTimeout> | null = null

  function clearHideTimer() {
    if (hideTimer === null) {
      return
    }

    window.clearTimeout(hideTimer)
    hideTimer = null
  }

  function hideToast() {
    clearHideTimer()
    toast.value = null
  }

  function showToast(
    message: string,
    tone: ToastTone = 'success',
    duration = DEFAULT_SUCCESS_DURATION,
  ) {
    clearHideTimer()
    toast.value = {
      id: Date.now(),
      message,
      tone,
    }

    if (duration > 0) {
      hideTimer = window.setTimeout(() => {
        toast.value = null
        hideTimer = null
      }, duration)
    }
  }

  onUnmounted(clearHideTimer)

  return {
    hideToast,
    showErrorToast: (message: string) => showToast(message, 'error', 5200),
    showSuccessToast: (message: string) => showToast(message, 'success'),
    toast: computed(() => toast.value),
  }
}
