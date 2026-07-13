<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, shallowRef, watch } from 'vue'
import { ArrowUpRight, Building2, X } from '@lucide/vue'

import OrganizationMapNode from './OrganizationMapNode.vue'
import OrganizationFlowMap from './OrganizationFlowMap.vue'
import { organizationMap, type OrganizationNode } from './organization-map'

const isOpen = shallowRef(false)
const dialog = shallowRef<HTMLElement>()

const previewMap = computed<OrganizationNode>(() => ({
  ...organizationMap,
  children: organizationMap.children?.slice(0, 2).map((department) => ({
    ...department,
    children: department.children?.slice(0, 1),
  })),
}))

function closeDialog() {
  isOpen.value = false
}

function handleKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') closeDialog()
}

watch(isOpen, async (open) => {
  document.body.style.overflow = open ? 'hidden' : ''
  if (open) {
    window.addEventListener('keydown', handleKeydown)
    await nextTick()
    dialog.value?.focus()
  } else {
    window.removeEventListener('keydown', handleKeydown)
  }
})

onBeforeUnmount(() => {
  document.body.style.overflow = ''
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<template>
  <article
    class="group overflow-hidden rounded-2xl bg-white text-slate-950 shadow-[0_1px_2px_rgb(15_23_42_/_0.05),0_14px_38px_rgb(15_23_42_/_0.06)] ring-1 ring-slate-950/6 dark:bg-slate-900 dark:text-slate-50 dark:shadow-[0_18px_42px_rgb(0_0_0_/_24%)] dark:ring-white/10"
    aria-labelledby="organization-map-title"
  >
    <button
      class="block w-full cursor-pointer text-left outline-none focus-visible:ring-4 focus-visible:ring-inset focus-visible:ring-blue-100 active:bg-slate-50/70 dark:focus-visible:ring-blue-950 dark:active:bg-slate-800/50"
      type="button"
      aria-haspopup="dialog"
      @click="isOpen = true"
    >
      <header class="flex items-start justify-between gap-5 px-5 pt-5 sm:px-6 sm:pt-6">
        <div class="flex min-w-0 gap-3.5">
          <span class="grid size-10 shrink-0 place-items-center rounded-xl bg-blue-50 text-blue-700 dark:bg-blue-400/10 dark:text-blue-300">
            <Building2 :size="19" :stroke-width="2.1" aria-hidden="true" />
          </span>
          <div>
            <p class="text-[11px] leading-4 font-bold tracking-[0.1em] text-blue-700 uppercase dark:text-blue-300">Organization map</p>
            <h2 id="organization-map-title" class="mt-0.5 text-lg leading-6 font-semibold tracking-[-0.015em] text-wrap-balance">How your organization flows</h2>
            <p class="mt-1 max-w-xl text-sm leading-5 text-slate-500 text-pretty dark:text-slate-400">Departments and operations connected in Blendes Flow.</p>
          </div>
        </div>
        <span class="inline-flex min-h-10 shrink-0 items-center gap-2 rounded-xl bg-slate-50 px-3 text-xs font-semibold text-slate-600 ring-1 ring-slate-950/5 transition-[background-color,color,transform] duration-150 group-hover:bg-blue-50 group-hover:text-blue-700 group-active:scale-[0.96] motion-reduce:transition-none dark:bg-slate-800 dark:text-slate-300 dark:ring-white/10 dark:group-hover:bg-blue-400/10 dark:group-hover:text-blue-300">
          <span class="hidden sm:inline">View full map</span>
          <ArrowUpRight :size="16" :stroke-width="2.1" aria-hidden="true" />
        </span>
      </header>

      <div class="relative mt-5 h-[255px] overflow-hidden bg-[radial-gradient(circle,rgb(148_163_184_/_0.26)_1px,transparent_1px)] bg-[size:18px_18px] px-5 pt-3 dark:bg-[radial-gradient(circle,rgb(100_116_139_/_0.25)_1px,transparent_1px)]">
        <div class="absolute inset-x-0 bottom-0 z-20 h-20 bg-gradient-to-t from-white to-transparent dark:from-slate-900" aria-hidden="true"></div>
        <div class="flex min-w-max justify-center origin-top scale-[0.82] sm:scale-90">
          <ul><OrganizationMapNode :node="previewMap" compact /></ul>
        </div>
      </div>
    </button>
  </article>

  <Teleport to="body">
    <Transition enter-active-class="transition-opacity duration-200" enter-from-class="opacity-0" leave-active-class="transition-opacity duration-150" leave-to-class="opacity-0">
      <div v-if="isOpen" class="fixed inset-0 z-50 grid place-items-center bg-slate-950/55 p-3 backdrop-blur-[5px] sm:p-6" @click.self="closeDialog">
        <section
          ref="dialog"
          class="flex h-[calc(100dvh-24px)] w-full max-w-7xl flex-col overflow-hidden rounded-2xl bg-slate-50 text-slate-950 shadow-[0_30px_100px_rgb(0_0_0_/_30%)] outline-none ring-1 ring-white/20 sm:h-[min(860px,calc(100dvh-48px))] dark:bg-slate-950 dark:text-slate-50"
          role="dialog"
          aria-modal="true"
          aria-labelledby="full-map-title"
          tabindex="-1"
        >
          <header class="flex items-start justify-between gap-5 bg-white px-5 py-4 shadow-[0_1px_0_rgb(15_23_42_/_0.08)] sm:px-6 dark:bg-slate-900 dark:shadow-[0_1px_0_rgb(255_255_255_/_0.10)]">
            <div>
              <p class="text-[11px] leading-4 font-bold tracking-[0.1em] text-blue-700 uppercase dark:text-blue-300">Organization map</p>
              <h2 id="full-map-title" class="mt-1 text-xl leading-7 font-semibold tracking-[-0.02em] text-wrap-balance">Blendes organizational structure</h2>
              <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">3 departments · 6 mapped operations</p>
            </div>
            <button class="grid size-10 shrink-0 cursor-pointer place-items-center rounded-xl bg-slate-100 text-slate-500 outline-none ring-1 ring-slate-950/5 transition-[background-color,color,transform,box-shadow] duration-150 hover:bg-slate-200 hover:text-slate-900 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.96] motion-reduce:transition-none dark:bg-slate-800 dark:text-slate-400 dark:ring-white/10 dark:hover:bg-slate-700 dark:hover:text-white dark:focus-visible:ring-blue-950" type="button" aria-label="Close organization map" @click="closeDialog">
              <X :size="17" :stroke-width="2.2" aria-hidden="true" />
            </button>
          </header>

          <div class="relative min-h-0 flex-1 overflow-hidden">
            <OrganizationFlowMap />
          </div>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>
