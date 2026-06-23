<script setup lang="ts">
import googleLogo from '@/assets/img/google.svg'

const props = defineProps<{
  isPending?: boolean
}>()

const emit = defineEmits<{
  credential: [credential: string]
  error: [message: string]
}>()

const googleScriptUrl = 'https://accounts.google.com/gsi/client'
let googleScriptPromise: Promise<void> | null = null
let isGoogleInitialized = false

type GoogleCredentialResponse = {
  credential?: string
}

type GooglePromptMomentNotification = {
  getNotDisplayedReason: () => string
  getSkippedReason: () => string
  isDismissedMoment: () => boolean
  isNotDisplayed: () => boolean
  isSkippedMoment: () => boolean
}

type GoogleIdentityServices = {
  accounts: {
    id: {
      initialize: (options: {
        callback: (response: GoogleCredentialResponse) => void
        client_id: string
      }) => void
      prompt: (callback: (notification: GooglePromptMomentNotification) => void) => void
    }
  }
}

declare global {
  interface Window {
    google?: GoogleIdentityServices
  }
}

async function requestGoogleCredential() {
  if (props.isPending) {
    return
  }

  const clientId = import.meta.env.VITE_GOOGLE_OAUTH_CLIENT_ID

  if (!clientId) {
    emit('error', 'Google sign in is not configured.')
    return
  }

  try {
    await loadGoogleScript()
    const credential = await promptGoogleCredential(clientId)
    emit('credential', credential)
  } catch (error) {
    emit(
      'error',
      error instanceof Error ? error.message : 'Unable to sign in with Google.',
    )
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
    script.onerror = () => reject(new Error('Unable to load Google sign in.'))
    document.head.appendChild(script)
  })

  return googleScriptPromise
}

function promptGoogleCredential(clientId: string) {
  return new Promise<string>((resolve, reject) => {
    if (!window.google?.accounts.id) {
      reject(new Error('Google sign in is unavailable.'))
      return
    }

    let settled = false

    if (!isGoogleInitialized) {
      window.google.accounts.id.initialize({
        client_id: clientId,
        callback: (response) => {
          if (settled) {
            return
          }

          settled = true

          if (response.credential) {
            resolve(response.credential)
            return
          }

          reject(new Error('Google did not return a credential.'))
        },
      })
      isGoogleInitialized = true
    }

    window.google.accounts.id.prompt((notification) => {
      if (settled) {
        return
      }

      if (notification.isNotDisplayed()) {
        settled = true
        reject(
          new Error(
            `Google sign in was not displayed: ${notification.getNotDisplayedReason()}.`,
          ),
        )
        return
      }

      if (notification.isSkippedMoment()) {
        settled = true
        reject(
          new Error(`Google sign in was skipped: ${notification.getSkippedReason()}.`),
        )
        return
      }

      if (notification.isDismissedMoment()) {
        settled = true
        reject(new Error('Google sign in was dismissed.'))
      }
    })
  })
}
</script>
<template>
  <button
    class="inline-flex min-h-11 w-full cursor-pointer items-center justify-center gap-2.5 rounded-lg border border-[#d8e6e9] bg-white px-4 text-sm font-extrabold leading-none text-[#172224] shadow-[0_12px_26px_rgb(18_33_36_/_7%),inset_0_1px_0_rgb(255_255_255_/_90%)] transition duration-180 hover:-translate-y-px hover:border-[#b5d2d8] hover:shadow-[0_16px_34px_rgb(18_33_36_/_11%),0_0_20px_rgb(174_238_255_/_14%),inset_0_1px_0_#fff] focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/60 motion-reduce:transition-none motion-reduce:hover:translate-y-0"
    type="button"
    :disabled="isPending"
    @click="requestGoogleCredential"
  >
    <img class="block size-5" :src="googleLogo" alt="" aria-hidden="true" />
    <span>Entrar com Google</span>
  </button>
</template>
