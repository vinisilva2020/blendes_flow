<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowRight, Blend, CheckCircle2, LogOut, Plus } from '@lucide/vue'

import { useSignOutMutation } from '@/domains/auth/queries'
import { useCreateOrganizationMutation, useOrganizations } from '@/domains/organizations/queries'
import type { Organization } from '@/domains/organizations/contracts'
import { ApiRequestError } from '@/lib/http/errors'
import { useAuthenticationStore } from '@/stores/authentication'
import { useWorkspaceStore } from '@/stores/workspace'

import CreateOrganizationDialog from './components/CreateOrganizationDialog.vue'

type WorkspaceColor = {
  activeCardClass: string
  avatarClass: string
  cardClass: string
}

const defaultWorkspaceColor: WorkspaceColor = {
  activeCardClass: 'border-[#8adff3] bg-white shadow-[0_18px_44px_rgb(15_44_43_/_10%)]',
  avatarClass: 'border-[#d8e6e9] bg-white text-[#246b78]',
  cardClass: 'border-transparent bg-transparent hover:border-[#d8e6e9]',
}

const workspaceColors: WorkspaceColor[] = [
  defaultWorkspaceColor,
  {
    activeCardClass: 'border-[#5ed8c6] bg-white shadow-[0_18px_44px_rgb(15_87_83_/_12%)]',
    avatarClass: 'border-[#ccefe8] bg-[#dff8f3] text-[#0f5753]',
    cardClass: 'border-transparent bg-transparent hover:border-[#ccefe8]',
  },
  {
    activeCardClass: 'border-[#8adff3] bg-white shadow-[0_18px_44px_rgb(36_107_120_/_12%)]',
    avatarClass: 'border-[#cbeef6] bg-[#e6f8fb] text-[#246b78]',
    cardClass: 'border-transparent bg-transparent hover:border-[#cbeef6]',
  },
]

const router = useRouter()
const authenticationStore = useAuthenticationStore()
const workspaceStore = useWorkspaceStore()

const organizationsQuery = useOrganizations(authenticationStore.isAuthenticated)
const createOrganizationMutation = useCreateOrganizationMutation()
const signOutMutation = useSignOutMutation()

const isCreateDialogOpen = ref(false)

const organizations = computed(() => organizationsQuery.data.value ?? [])

const errorMessage = computed(() => {
  const error = organizationsQuery.error.value

  if (error instanceof ApiRequestError) {
    return error.message
  }

  if (error) {
    return 'Unable to load organizations. Try again in a moment.'
  }

  return ''
})

const createOrganizationErrorMessage = computed(() => {
  const error = createOrganizationMutation.error.value

  if (error instanceof ApiRequestError) {
    return error.message
  }

  if (error) {
    return 'Unable to create organization. Try again in a moment.'
  }

  return ''
})

function getInitials(name: string) {
  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? '')
    .join('')
}

function isActiveWorkspace(organization: Organization) {
  return workspaceStore.organizationId === organization.id
}

function getWorkspaceColor(index: number) {
  return workspaceColors[index % workspaceColors.length] ?? defaultWorkspaceColor
}

async function openWorkspace(organization: Organization) {
  workspaceStore.selectWorkspace(organization)
  await router.push({ name: 'dashboard' })
}

async function createOrganization(name: string) {
  const organization = await createOrganizationMutation.mutateAsync({ name }).catch(() => null)

  if (!organization) {
    return
  }

  isCreateDialogOpen.value = false
}

async function signOut() {
  try {
    if (authenticationStore.isAuthenticated) {
      await signOutMutation.mutateAsync()
    }
  } finally {
    // Mesmo se o backend recusar a sessao, limpamos a memoria local do cliente.
    authenticationStore.endSession()
    workspaceStore.clearWorkspace()
    await router.push({ name: 'auth' })
  }
}
</script>

<template>
  <main class="min-h-screen bg-[#f5f8f7] text-[#071113]" aria-labelledby="workspace-title">
    <section class="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-5 py-6 sm:px-8 lg:px-12">
      <header class="flex items-center justify-between">
        <RouterLink
          class="inline-flex items-center gap-2 text-sm font-black text-[#172224] no-underline outline-none transition-[color] hover:text-[#246b78] focus-visible:ring-4 focus-visible:ring-[#aeeeff]/50"
          :to="{ name: 'home' }"
          aria-label="Back to Blendes Flow"
        >
          <span
            class="inline-flex h-11 w-11 items-center justify-center rounded-full border border-[#d8e6e9] bg-white shadow-sm"
          >
            <Blend class="text-[#246b78]" :size="22" :stroke-width="2.4" aria-hidden="true" />
          </span>
          <span class="hidden sm:inline">Blendes Flow</span>
        </RouterLink>

        <button
          class="inline-flex h-11 w-11 cursor-pointer items-center justify-center rounded-full border border-[#d8e6e9] bg-white text-[#62777d] shadow-sm outline-none transition-[border-color,color,transform] hover:border-[#aeeeff] hover:text-[#246b78] active:scale-[0.96] focus-visible:ring-4 focus-visible:ring-[#aeeeff]/50"
          type="button"
          aria-label="Sign out"
          :disabled="signOutMutation.isPending.value"
          @click="signOut"
        >
          <LogOut :size="18" :stroke-width="2.3" aria-hidden="true" />
        </button>
      </header>

      <div class="flex flex-1 flex-col items-center justify-center py-14 text-center">
        <p
          class="mb-4 rounded-full bg-[#e6f8fb] px-4 py-2 text-xs font-black uppercase tracking-[0.08em] text-[#246b78]"
        >
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

        <RouterLink
          v-if="!authenticationStore.isAuthenticated"
          class="mt-9 rounded-lg bg-white px-5 py-3 text-sm font-black text-[#246b78] no-underline shadow-[0_18px_44px_rgb(15_44_43_/_10%)] ring-1 ring-[#d8e6e9] transition-[transform,box-shadow] hover:-translate-y-px hover:shadow-[0_22px_50px_rgb(15_44_43_/_14%)] active:scale-[0.96]"
          :to="{ name: 'auth' }"
        >
          Sign in to load workspaces
        </RouterLink>

        <p
          v-else-if="errorMessage"
          class="mt-9 max-w-xl rounded-lg bg-[#fff1f0] px-4 py-3 text-sm font-bold leading-5 text-[#9f2f25] shadow-[inset_0_0_0_1px_rgb(159_47_37_/_14%)]"
          role="alert"
        >
          {{ errorMessage }}
        </p>

        <div
          v-else
          class="mt-12 grid w-full max-w-4xl grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4"
          aria-label="Available workspaces"
        >
          <div
            v-if="organizationsQuery.isLoading.value"
            class="col-span-full grid gap-4 sm:grid-cols-2 lg:grid-cols-3"
            aria-label="Loading workspaces"
          >
            <span
              v-for="item in 3"
              :key="item"
              class="h-60 rounded-lg bg-white/70 shadow-[0_18px_44px_rgb(15_44_43_/_7%)] ring-1 ring-[#d8e6e9]"
            ></span>
          </div>

          <button
            v-for="(organization, index) in organizations"
            v-else
            :key="organization.id"
            class="group relative flex cursor-pointer flex-col items-center gap-4 rounded-lg border p-3 text-center outline-none transition-[transform,border-color,background-color,box-shadow] hover:-translate-y-1 hover:bg-white/70 hover:shadow-[0_18px_44px_rgb(15_44_43_/_10%)] active:scale-[0.96] focus-visible:border-[#8adff3] focus-visible:bg-white focus-visible:ring-4 focus-visible:ring-[#aeeeff]/40 motion-reduce:transition-none motion-reduce:hover:translate-y-0"
            :class="
              isActiveWorkspace(organization)
                ? getWorkspaceColor(index).activeCardClass
                : getWorkspaceColor(index).cardClass
            "
            type="button"
            :aria-pressed="isActiveWorkspace(organization)"
            @click="openWorkspace(organization)"
          >
            <span
              v-if="isActiveWorkspace(organization)"
              class="absolute right-3 top-3 inline-flex items-center gap-1 rounded-full bg-[#0f5753] px-2.5 py-1 text-[0.65rem] font-black leading-none text-white shadow-[0_10px_22px_rgb(15_87_83_/_18%)]"
            >
              <CheckCircle2 :size="12" :stroke-width="2.5" aria-hidden="true" />
              Active
            </span>

            <span
              class="grid h-36 w-36 place-items-center rounded-lg border text-4xl font-black shadow-[0_18px_44px_rgb(15_44_43_/_10%)] transition-[border-color] group-hover:border-[#8adff3]"
              :class="
                isActiveWorkspace(organization)
                  ? `${getWorkspaceColor(index).avatarClass} border-[#8adff3]`
                  : getWorkspaceColor(index).avatarClass
              "
            >
              {{ getInitials(organization.name) }}
            </span>

            <span class="grid gap-2">
              <strong
                class="text-lg font-black leading-tight text-[#172224] group-hover:text-[#246b78]"
              >
                {{ organization.name }}
              </strong>
              <span class="text-sm font-extrabold text-[#7a8f94]">
                {{
                  isActiveWorkspace(organization)
                    ? 'Active workspace'
                    : organization.description || 'Available workspace'
                }}
              </span>
            </span>

            <span
              class="mt-1 inline-flex items-center gap-2 text-xs font-black text-[#246b78] transition-[opacity] group-hover:opacity-100 group-focus-visible:opacity-100"
              :class="isActiveWorkspace(organization) ? 'opacity-100' : 'opacity-0'"
            >
              {{ isActiveWorkspace(organization) ? 'Current' : 'Enter' }}
              <ArrowRight :size="14" :stroke-width="2.5" aria-hidden="true" />
            </span>
          </button>

          <button
            class="group flex cursor-pointer flex-col items-center gap-4 rounded-lg border border-transparent bg-transparent p-3 text-center outline-none transition-[transform,border-color,background-color,box-shadow] hover:-translate-y-1 hover:border-[#d8e6e9] hover:bg-white/70 hover:shadow-[0_18px_44px_rgb(15_44_43_/_10%)] active:scale-[0.96] focus-visible:border-[#8adff3] focus-visible:bg-white focus-visible:ring-4 focus-visible:ring-[#aeeeff]/40 motion-reduce:transition-none motion-reduce:hover:translate-y-0"
            type="button"
            @click="isCreateDialogOpen = true"
          >
            <span
              class="grid h-36 w-36 place-items-center rounded-lg border border-dashed border-[#b9d1d7] bg-white/60 text-[#62777d] shadow-[0_18px_44px_rgb(15_44_43_/_7%)] transition-[border-color,background-color,color] group-hover:border-[#8adff3] group-hover:bg-white group-hover:text-[#246b78]"
            >
              <Plus :size="38" :stroke-width="2.2" aria-hidden="true" />
            </span>

            <span class="grid gap-2">
              <strong
                class="text-lg font-black leading-tight text-[#172224] group-hover:text-[#246b78]"
              >
                New organization
              </strong>
              <span class="text-sm font-extrabold text-[#7a8f94]"> Create workspace </span>
            </span>

            <span
              class="mt-1 inline-flex items-center gap-2 text-xs font-black text-[#246b78] opacity-0 transition-[opacity] group-hover:opacity-100 group-focus-visible:opacity-100"
            >
              Create
              <ArrowRight :size="14" :stroke-width="2.5" aria-hidden="true" />
            </span>
          </button>
        </div>
      </div>
    </section>

    <CreateOrganizationDialog
      :error-message="createOrganizationErrorMessage"
      :is-open="isCreateDialogOpen"
      :is-pending="createOrganizationMutation.isPending.value"
      @close="isCreateDialogOpen = false"
      @create="createOrganization"
    />
  </main>
</template>
