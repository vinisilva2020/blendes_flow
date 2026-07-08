<script setup lang="ts">
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { Check, X } from '@lucide/vue'

import { useAccountAvatarOptions } from '@/domains/accounts/composables/useAccountAvatar'

const props = defineProps<{
  isOpen: boolean
  selectedAvatarType: string | null
}>()

const emit = defineEmits<{
  close: []
  select: [avatarType: string]
}>()

const avatarOptions = useAccountAvatarOptions()
const draftAvatarType = ref(props.selectedAvatarType ?? avatarOptions[0]?.type ?? '01')
const dialogPanelRef = ref<HTMLElement | null>(null)

watch(
  () => props.isOpen,
  async (isOpen) => {
    if (!isOpen) {
      document.removeEventListener('keydown', onDocumentKeydown)
      return
    }

    draftAvatarType.value = props.selectedAvatarType ?? avatarOptions[0]?.type ?? '01'
    document.addEventListener('keydown', onDocumentKeydown)
    await nextTick()
    dialogPanelRef.value?.focus()
  },
)

watch(
  () => props.selectedAvatarType,
  (avatarType) => {
    if (!props.isOpen) {
      draftAvatarType.value = avatarType ?? avatarOptions[0]?.type ?? '01'
    }
  },
)

function onDocumentKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') {
    event.preventDefault()
    emit('close')
  }
}

function chooseAvatar(avatarType: string) {
  draftAvatarType.value = avatarType
}

function confirmAvatar() {
  emit('select', draftAvatarType.value)
}

onBeforeUnmount(() => {
  document.removeEventListener('keydown', onDocumentKeydown)
})
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition-[opacity] duration-150 ease-out motion-reduce:transition-none"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-[opacity] duration-100 ease-in motion-reduce:transition-none"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isOpen"
        class="fixed inset-0 z-50 grid place-items-center bg-slate-950/36 p-4 backdrop-blur-sm"
        role="presentation"
        @click.self="emit('close')"
      >
        <section
          ref="dialogPanelRef"
          class="w-full max-w-[520px] rounded-3xl bg-white p-2 text-slate-950 shadow-[0_0_0_1px_rgb(15_23_42_/_6%),0_22px_56px_rgb(15_23_42_/_18%)] outline-none"
          role="dialog"
          aria-modal="true"
          aria-labelledby="avatar-dialog-title"
          aria-describedby="avatar-dialog-description"
          tabindex="-1"
        >
          <div class="rounded-2xl bg-slate-50 p-4 sm:p-5">
            <header class="flex items-start justify-between gap-4">
              <div class="min-w-0">
                <h2
                  id="avatar-dialog-title"
                  class="text-base leading-6 font-semibold text-balance text-slate-950"
                >
                  Choose your avatar
                </h2>
                <p
                  id="avatar-dialog-description"
                  class="mt-1 text-sm leading-5 font-medium text-pretty text-slate-500"
                >
                  Select the image that will represent you across the workspace.
                </p>
              </div>

              <button
                class="grid size-10 shrink-0 cursor-pointer place-items-center rounded-xl border-0 bg-white text-slate-500 outline-none shadow-[0_0_0_1px_rgb(15_23_42_/_7%)] transition-[background-color,color,scale,box-shadow] duration-150 ease-out hover:bg-slate-100 hover:text-slate-950 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none"
                type="button"
                aria-label="Close avatar chooser"
                @click="emit('close')"
              >
                <X :size="17" :stroke-width="2.2" aria-hidden="true" />
              </button>
            </header>

            <div
              class="mt-5 grid grid-cols-5 gap-2 sm:gap-3"
              role="radiogroup"
              aria-label="Avatars"
            >
              <button
                v-for="avatar in avatarOptions"
                :key="avatar.type"
                class="relative grid aspect-square min-h-14 cursor-pointer place-items-center overflow-hidden rounded-2xl bg-white p-1 outline-none shadow-[0_0_0_1px_rgb(15_23_42_/_7%)] transition-[box-shadow,scale,background-color] duration-150 ease-out hover:bg-blue-50 hover:shadow-[0_0_0_1px_rgb(59_130_246_/_28%)] focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none"
                :class="
                  draftAvatarType === avatar.type
                    ? 'shadow-[0_0_0_2px_rgb(37_99_235),0_8px_18px_rgb(37_99_235_/_14%)]'
                    : ''
                "
                type="button"
                role="radio"
                :aria-checked="draftAvatarType === avatar.type"
                :aria-label="`Avatar ${avatar.type}`"
                @click="chooseAvatar(avatar.type)"
              >
                <img
                  class="size-full rounded-xl object-cover outline outline-1 -outline-offset-1 outline-black/10"
                  :src="avatar.src"
                  :alt="`Avatar ${avatar.type}`"
                />
                <span
                  v-if="draftAvatarType === avatar.type"
                  class="absolute right-1.5 bottom-1.5 grid size-6 place-items-center rounded-full bg-blue-600 text-white shadow-sm"
                  aria-hidden="true"
                >
                  <Check :size="14" :stroke-width="2.5" />
                </span>
              </button>
            </div>

            <footer class="mt-5 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
              <button
                class="inline-flex min-h-10 cursor-pointer items-center justify-center rounded-xl border-0 bg-white px-4 text-sm font-semibold text-slate-600 outline-none shadow-[0_0_0_1px_rgb(15_23_42_/_8%)] transition-[background-color,color,scale,box-shadow] duration-150 ease-out hover:bg-slate-100 hover:text-slate-950 focus-visible:ring-4 focus-visible:ring-slate-200 active:scale-[0.96] motion-reduce:transition-none"
                type="button"
                @click="emit('close')"
              >
                Cancel
              </button>
              <button
                class="inline-flex min-h-10 cursor-pointer items-center justify-center rounded-xl border-0 bg-blue-600 px-4 text-sm font-semibold text-white outline-none transition-[background-color,scale,box-shadow] duration-150 ease-out hover:bg-blue-700 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none"
                type="button"
                @click="confirmAvatar"
              >
                Use avatar
              </button>
            </footer>
          </div>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>
