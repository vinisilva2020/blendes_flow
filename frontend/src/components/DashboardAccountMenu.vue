<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, shallowRef, watch } from 'vue'
import { CircleUserRound, LogOut, UserRound } from '@lucide/vue'
import { useRouter } from 'vue-router'

import { useSignOutMutation } from '@/domains/auth/queries'
import { useAccountAvatar } from '@/domains/accounts/composables/useAccountAvatar'
import { useCurrentAccount } from '@/domains/accounts/queries'
import { useAuthenticationStore } from '@/stores/authentication'
import { useWorkspaceStore } from '@/stores/workspace'

const currentAccount = useCurrentAccount()
const router = useRouter()
const authenticationStore = useAuthenticationStore()
const workspaceStore = useWorkspaceStore()
const signOutMutation = useSignOutMutation()

const account = computed(() => currentAccount.data.value ?? null)
const { avatarUrl: accountAvatarUrl } = useAccountAvatar(() => account.value?.avatar_type)
const accountLabel = computed(
  () => account.value?.username || account.value?.email || 'User profile',
)
const accountEmail = computed(() => account.value?.email || 'No email available')
const accountAvatarAlt = computed(() =>
  account.value?.username ? `${account.value.username} avatar` : 'User avatar',
)
const isAccountMenuOpen = shallowRef(false)
const accountMenuRef = shallowRef<HTMLElement | null>(null)
const accountMenuButtonRef = shallowRef<HTMLButtonElement | null>(null)

function getMenuItems() {
  return Array.from(accountMenuRef.value?.querySelectorAll<HTMLElement>('[role="menuitem"]') ?? [])
}

function focusMenuItem(index: number) {
  const menuItems = getMenuItems()
  const nextItem = menuItems.at(index)

  nextItem?.focus()
}

async function openAccountMenu() {
  isAccountMenuOpen.value = true
  await nextTick()
  focusMenuItem(0)
}

function closeAccountMenu(options: { restoreFocus?: boolean } = {}) {
  if (!isAccountMenuOpen.value) {
    return
  }

  isAccountMenuOpen.value = false

  if (options.restoreFocus) {
    accountMenuButtonRef.value?.focus()
  }
}

async function toggleAccountMenu() {
  if (isAccountMenuOpen.value) {
    closeAccountMenu({ restoreFocus: true })
    return
  }

  await openAccountMenu()
}

function onDocumentPointerDown(event: PointerEvent) {
  const target = event.target

  if (!(target instanceof Node)) {
    return
  }

  if (accountMenuRef.value?.contains(target) || accountMenuButtonRef.value?.contains(target)) {
    return
  }

  closeAccountMenu()
}

function onDocumentKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') {
    event.preventDefault()
    closeAccountMenu({ restoreFocus: true })
  }
}

function onAccountMenuKeydown(event: KeyboardEvent) {
  const menuItems = getMenuItems()
  const currentIndex = menuItems.findIndex((item) => item === document.activeElement)

  if (event.key === 'ArrowDown') {
    event.preventDefault()
    focusMenuItem(currentIndex >= 0 ? (currentIndex + 1) % menuItems.length : 0)
  }

  if (event.key === 'ArrowUp') {
    event.preventDefault()
    focusMenuItem(currentIndex > 0 ? currentIndex - 1 : menuItems.length - 1)
  }

  if (event.key === 'Home') {
    event.preventDefault()
    focusMenuItem(0)
  }

  if (event.key === 'End') {
    event.preventDefault()
    focusMenuItem(menuItems.length - 1)
  }
}

function openProfile() {
  closeAccountMenu()
}

async function signOut() {
  closeAccountMenu()

  try {
    if (authenticationStore.isAuthenticated) {
      await signOutMutation.mutateAsync()
    }
  } finally {
    authenticationStore.endSession()
    workspaceStore.clearWorkspace()
    await router.push({ name: 'auth' })
  }
}

watch(isAccountMenuOpen, (isOpen) => {
  if (isOpen) {
    document.addEventListener('pointerdown', onDocumentPointerDown, true)
    document.addEventListener('keydown', onDocumentKeydown)
    return
  }

  document.removeEventListener('pointerdown', onDocumentPointerDown, true)
  document.removeEventListener('keydown', onDocumentKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('pointerdown', onDocumentPointerDown, true)
  document.removeEventListener('keydown', onDocumentKeydown)
})
</script>

<template>
  <div class="relative shrink-0">
    <button
      ref="accountMenuButtonRef"
      class="grid size-10 cursor-pointer place-items-center overflow-hidden rounded-full border border-slate-200 bg-white text-slate-500 outline-none transition-[border-color,background-color,color,transform,box-shadow] duration-150 ease-out hover:border-slate-300 hover:bg-slate-50 hover:text-slate-950 focus-visible:border-slate-300 focus-visible:ring-4 focus-visible:ring-slate-200/80 active:scale-[0.96] motion-reduce:transition-none dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300 dark:hover:border-slate-600 dark:hover:bg-slate-700 dark:hover:text-slate-50 dark:focus-visible:ring-slate-700"
      type="button"
      aria-haspopup="menu"
      :aria-expanded="isAccountMenuOpen"
      aria-controls="account-menu"
      :aria-label="`Open account menu for ${accountLabel}`"
      :title="accountLabel"
      @click="toggleAccountMenu"
    >
      <img
        v-if="accountAvatarUrl"
        class="size-full object-cover outline outline-1 -outline-offset-1 outline-black/10"
        :src="accountAvatarUrl"
        :alt="accountAvatarAlt"
      />
      <UserRound
        v-else
        class="text-slate-500 dark:text-slate-300"
        :size="18"
        :stroke-width="2"
        aria-hidden="true"
      />
    </button>

    <Transition
      enter-active-class="transition duration-150 ease-out motion-reduce:transition-none"
      enter-from-class="-translate-y-1 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition duration-100 ease-in motion-reduce:transition-none"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="-translate-y-1 opacity-0"
    >
      <div
        v-if="isAccountMenuOpen"
        id="account-menu"
        ref="accountMenuRef"
        class="absolute right-0 top-[calc(100%+10px)] z-50 w-64 max-w-[calc(100vw-1rem)] overflow-hidden rounded-xl border border-slate-200 bg-white p-1.5 text-slate-950 shadow-[0_18px_42px_rgb(15_23_42_/_8%)] dark:border-slate-700 dark:bg-slate-900 dark:text-slate-50 dark:shadow-[0_18px_42px_rgb(0_0_0_/_28%)]"
        role="menu"
        aria-label="Account menu"
        @keydown="onAccountMenuKeydown"
      >
        <div class="grid gap-0.5 px-3 py-2.5" aria-label="Signed in account">
          <strong
            class="min-w-0 overflow-hidden text-sm leading-5 font-semibold text-ellipsis whitespace-nowrap text-slate-950 dark:text-slate-50"
          >
            {{ accountLabel }}
          </strong>
          <span
            class="min-w-0 overflow-hidden text-xs leading-4 font-medium text-ellipsis whitespace-nowrap text-slate-500 dark:text-slate-400"
          >
            {{ accountEmail }}
          </span>
        </div>

        <div class="my-1 h-px bg-slate-200/80 dark:bg-slate-700" aria-hidden="true"></div>

        <RouterLink
          class="flex min-h-11 items-center gap-2.5 rounded-lg px-2.5 text-sm font-medium text-slate-600 no-underline outline-none transition-[background-color,color,transform,box-shadow] duration-150 ease-out hover:bg-slate-50 hover:text-slate-950 focus-visible:bg-slate-50 focus-visible:ring-4 focus-visible:ring-slate-200/80 active:scale-[0.96] motion-reduce:transition-none dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-slate-50 dark:focus-visible:bg-slate-800 dark:focus-visible:ring-slate-700"
          :to="{ name: 'profile' }"
          role="menuitem"
          tabindex="-1"
          @click="openProfile"
        >
          <CircleUserRound :size="17" :stroke-width="2.1" aria-hidden="true" />
          <span class="min-w-0 truncate">Profile</span>
        </RouterLink>

        <button
          class="flex min-h-11 w-full cursor-pointer items-center gap-2.5 rounded-lg border-0 bg-transparent px-2.5 text-left text-sm font-medium text-slate-600 outline-none transition-[background-color,color,transform,box-shadow] duration-150 ease-out hover:bg-rose-50 hover:text-rose-700 focus-visible:bg-rose-50 focus-visible:text-rose-700 focus-visible:ring-4 focus-visible:ring-rose-100 active:scale-[0.96] active:bg-rose-100 active:text-rose-800 motion-reduce:transition-none dark:text-slate-300 dark:hover:bg-rose-500/10 dark:hover:text-rose-300 dark:focus-visible:bg-rose-500/10 dark:focus-visible:text-rose-300 dark:focus-visible:ring-rose-950 dark:active:bg-rose-500/15"
          type="button"
          role="menuitem"
          tabindex="-1"
          :disabled="signOutMutation.isPending.value"
          @click="signOut"
        >
          <LogOut :size="17" :stroke-width="2.1" aria-hidden="true" />
          <span class="min-w-0 truncate">Logout</span>
        </button>
      </div>
    </Transition>
  </div>
</template>
