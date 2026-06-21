<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ArrowRight, Blend, LogOut, Plus } from '@lucide/vue'

type Workspace = {
  id: string
  name: string
  hint: string
  initials: string
  avatarClass: string
}

const router = useRouter()

const workspaces: Workspace[] = [
  {
    id: 'labise',
    name: 'LabiSe',
    hint: 'Main workspace',
    initials: 'LS',
    avatarClass: 'bg-white text-[#246b78]',
  },
  {
    id: 'operations',
    name: 'North Operations',
    hint: 'Routines and improvement',
    initials: 'ON',
    avatarClass: 'bg-[#dff8f3] text-[#0f5753]',
  },
  {
    id: 'quality',
    name: 'Integrated Quality',
    hint: 'Audits and signals',
    initials: 'QI',
    avatarClass: 'bg-[#e6f8fb] text-[#246b78]',
  },
]

function openWorkspace(_workspaceId: string) {
  router.push({ name: 'dashboard' })
}

function createOrganization() {
  router.push({ name: 'canvas' })
}
</script>

<template>
  <main class="min-h-screen bg-[#f5f8f7] text-[#071113]" aria-labelledby="workspace-title">
    <section class="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-5 py-6 sm:px-8 lg:px-12">
      <header class="flex items-center justify-between">
        <RouterLink
          class="inline-flex items-center gap-2 text-sm font-black text-[#172224] no-underline outline-none transition hover:text-[#246b78] focus-visible:ring-4 focus-visible:ring-[#aeeeff]/50"
          :to="{ name: 'home' }"
          aria-label="Back to Blendes Flow"
        >
          <span class="inline-flex h-11 w-11 items-center justify-center rounded-full border border-[#d8e6e9] bg-white shadow-sm">
            <Blend class="text-[#246b78]" :size="22" :stroke-width="2.4" aria-hidden="true" />
          </span>
          <span class="hidden sm:inline">Blendes Flow</span>
        </RouterLink>

        <RouterLink
          class="inline-flex h-11 w-11 items-center justify-center rounded-full border border-[#d8e6e9] bg-white text-[#62777d] no-underline shadow-sm outline-none transition hover:border-[#aeeeff] hover:text-[#246b78] focus-visible:ring-4 focus-visible:ring-[#aeeeff]/50"
          :to="{ name: 'auth' }"
          aria-label="Sign out"
        >
          <LogOut :size="18" :stroke-width="2.3" aria-hidden="true" />
        </RouterLink>
      </header>

      <div class="flex flex-1 flex-col items-center justify-center py-14 text-center">
        <p class="mb-4 rounded-full bg-[#e6f8fb] px-4 py-2 text-xs font-black uppercase tracking-[0.08em] text-[#246b78]">
          Workspace
        </p>

        <h1
          id="workspace-title"
          class="max-w-3xl text-4xl font-black leading-none tracking-normal text-[#071113] sm:text-5xl lg:text-7xl"
        >
          Choose your workspace
        </h1>

        <p class="mt-5 max-w-xl text-base font-semibold leading-7 text-[#62777d]">
          Your organization sets the workspace, members, and flows you can access.
        </p>

        <div class="mt-12 grid w-full max-w-4xl grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4" aria-label="Available workspaces">
          <button
            v-for="workspace in workspaces"
            :key="workspace.id"
            class="group flex cursor-pointer flex-col items-center gap-4 rounded-lg border border-transparent bg-transparent p-3 text-center outline-none transition hover:-translate-y-1 hover:border-[#d8e6e9] hover:bg-white/70 hover:shadow-[0_18px_44px_rgb(15_44_43_/_10%)] focus-visible:border-[#8adff3] focus-visible:bg-white focus-visible:ring-4 focus-visible:ring-[#aeeeff]/40 motion-reduce:transition-none motion-reduce:hover:translate-y-0"
            type="button"
            @click="openWorkspace(workspace.id)"
          >
            <span
              class="grid h-36 w-36 place-items-center rounded-lg border border-[#d8e6e9] text-4xl font-black shadow-[0_18px_44px_rgb(15_44_43_/_10%)] transition group-hover:border-[#8adff3]"
              :class="workspace.avatarClass"
            >
              {{ workspace.initials }}
            </span>

            <span class="grid gap-2">
              <strong class="text-lg font-black leading-tight text-[#172224] group-hover:text-[#246b78]">
                {{ workspace.name }}
              </strong>
              <span class="text-sm font-extrabold text-[#7a8f94]">
                {{ workspace.hint }}
              </span>
            </span>

            <span class="mt-1 inline-flex items-center gap-2 text-xs font-black text-[#246b78] opacity-0 transition group-hover:opacity-100 group-focus-visible:opacity-100">
              Enter
              <ArrowRight :size="14" :stroke-width="2.5" aria-hidden="true" />
            </span>
          </button>

          <button
            class="group flex cursor-pointer flex-col items-center gap-4 rounded-lg border border-transparent bg-transparent p-3 text-center outline-none transition hover:-translate-y-1 hover:border-[#d8e6e9] hover:bg-white/70 hover:shadow-[0_18px_44px_rgb(15_44_43_/_10%)] focus-visible:border-[#8adff3] focus-visible:bg-white focus-visible:ring-4 focus-visible:ring-[#aeeeff]/40 motion-reduce:transition-none motion-reduce:hover:translate-y-0"
            type="button"
            @click="createOrganization"
          >
            <span
              class="grid h-36 w-36 place-items-center rounded-lg border border-dashed border-[#b9d1d7] bg-white/60 text-[#62777d] shadow-[0_18px_44px_rgb(15_44_43_/_7%)] transition group-hover:border-[#8adff3] group-hover:bg-white group-hover:text-[#246b78]"
            >
              <Plus :size="38" :stroke-width="2.2" aria-hidden="true" />
            </span>

            <span class="grid gap-2">
              <strong class="text-lg font-black leading-tight text-[#172224] group-hover:text-[#246b78]">
                New organization
              </strong>
              <span class="text-sm font-extrabold text-[#7a8f94]">
                Create workspace
              </span>
            </span>

            <span class="mt-1 inline-flex items-center gap-2 text-xs font-black text-[#246b78] opacity-0 transition group-hover:opacity-100 group-focus-visible:opacity-100">
              Create
              <ArrowRight :size="14" :stroke-width="2.5" aria-hidden="true" />
            </span>
          </button>
        </div>
      </div>
    </section>
  </main>
</template>
