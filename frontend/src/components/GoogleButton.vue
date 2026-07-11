<script setup lang="ts">
import { onMounted, ref } from 'vue'

const props = defineProps<{
  isPending?: boolean
  label?: string
}>()

const emit = defineEmits<{
  credential: [credential: string]
  error: [message: string]
}>()

const googleScriptUrl = 'https://accounts.google.com/gsi/client'
let googleScriptPromise: Promise<void> | null = null
const buttonContainer = ref<HTMLElement | null>(null)
const isInitializing = ref(true)

type GoogleCredentialResponse = {
  credential?: string
}

type GoogleIdentityServices = {
  accounts: {
    id: {
      initialize: (options: {
        callback: (response: GoogleCredentialResponse) => void
        client_id: string
      }) => void
      renderButton: (
        parent: HTMLElement,
        options: {
          locale: string
          shape: 'rectangular'
          size: 'large'
          text: 'continue_with' | 'signin_with'
          theme: 'outline'
          type: 'standard'
          width: number
        },
      ) => void
    }
  }
}

declare global {
  interface Window {
    google?: GoogleIdentityServices
  }
}

function loadGoogleScript() {
  if (window.google?.accounts.id) {
    return Promise.resolve()
  }

  if (googleScriptPromise) {
    return googleScriptPromise
  }

  googleScriptPromise = new Promise((resolve, reject) => {
    const script = document.createElement('script')
    script.src = googleScriptUrl
    script.async = true
    script.defer = true
    script.onload = () => resolve()
    script.onerror = () => {
      googleScriptPromise = null
      script.remove()
      reject(new Error('Unable to load Google sign in.'))
    }
    document.head.appendChild(script)
  })

  return googleScriptPromise
}

function handleCredential(response: GoogleCredentialResponse) {
  if (response.credential) {
    emit('credential', response.credential)
    return
  }

  emit('error', 'Google did not return a credential.')
}

onMounted(async () => {
  const clientId = import.meta.env.VITE_GOOGLE_OAUTH_CLIENT_ID

  if (!clientId) {
    isInitializing.value = false
    emit('error', 'Google sign in is not configured.')
    return
  }

  try {
    await loadGoogleScript()

    const googleIdentity = window.google?.accounts.id
    const container = buttonContainer.value

    if (!googleIdentity || !container) {
      throw new Error('Google sign in is unavailable.')
    }

    googleIdentity.initialize({
      client_id: clientId,
      callback: handleCredential,
    })
    googleIdentity.renderButton(container, {
      type: 'standard',
      theme: 'outline',
      size: 'large',
      text: props.label ? 'continue_with' : 'signin_with',
      shape: 'rectangular',
      locale: 'pt_BR',
      width: Math.max(120, Math.floor(container.getBoundingClientRect().width)),
    })
  } catch (error) {
    emit('error', error instanceof Error ? error.message : 'Unable to sign in with Google.')
  } finally {
    isInitializing.value = false
  }
})
</script>

<template>
  <div
    class="relative min-h-11 w-full overflow-hidden rounded-lg"
    :class="{ 'pointer-events-none opacity-65': isPending }"
    :aria-busy="isInitializing || isPending"
  >
    <div ref="buttonContainer" class="min-h-11 w-full"></div>

    <div
      v-if="isInitializing"
      class="absolute inset-0 flex items-center justify-center gap-2.5 border border-[#d8e6e9] bg-white text-sm font-extrabold text-[#172224]"
    >
      <svg class="size-5 animate-spin" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        />
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 0 1 8-8v4a4 4 0 0 0-4 4H4Z"
        />
      </svg>
      <span>Carregando Google…</span>
    </div>
  </div>
</template>
