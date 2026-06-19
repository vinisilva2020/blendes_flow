<script setup lang="ts">
import { computed, onBeforeUnmount, shallowRef } from 'vue'
import { useRouter } from 'vue-router'
import {
  ArrowRight,
  Blend,
  Building2,
  CheckCircle2,
  Clock3,
  Plus,
  Search,
  UsersRound,
} from '@lucide/vue'

interface Organization {
  id: string
  name: string
  plan: string
  role: string
  members: number
  flows: number
  lastAccess: string
  status: 'Ativo' | 'Revisao'
  initials: string
}

const router = useRouter()

const searchQuery = shallowRef('')
const selectedOrganizationId = shallowRef<string>('blendes-labs')
const selectionFeedback = shallowRef('Blendes Labs selecionada para esta sessao.')
const createdOrganizationsCount = shallowRef(0)

let feedbackTimeout: ReturnType<typeof setTimeout> | undefined

const organizations = shallowRef<Organization[]>([
  {
    id: 'blendes-labs',
    name: 'Blendes Labs',
    plan: 'Growth',
    role: 'Owner',
    members: 18,
    flows: 42,
    lastAccess: 'Hoje, 09:34',
    status: 'Ativo',
    initials: 'BL',
  },
  {
    id: 'nexa-ops',
    name: 'Nexa Operations',
    plan: 'Business',
    role: 'Admin',
    members: 32,
    flows: 76,
    lastAccess: 'Ontem, 17:12',
    status: 'Ativo',
    initials: 'NO',
  },
  {
    id: 'aurora-health',
    name: 'Aurora Health',
    plan: 'Starter',
    role: 'Member',
    members: 9,
    flows: 15,
    lastAccess: 'Segunda, 11:08',
    status: 'Revisao',
    initials: 'AH',
  },
  {
    id: 'orbit-finance',
    name: 'Orbit Finance',
    plan: 'Enterprise',
    role: 'Admin',
    members: 54,
    flows: 118,
    lastAccess: '12 jun, 14:45',
    status: 'Ativo',
    initials: 'OF',
  },
])

const normalizedSearch = computed(() => searchQuery.value.trim().toLocaleLowerCase('pt-BR'))

const filteredOrganizations = computed(() => {
  if (!normalizedSearch.value) {
    return organizations.value
  }

  return organizations.value.filter((organization) => {
    const searchableContent = [
      organization.name,
      organization.plan,
      organization.role,
      organization.status,
      organization.initials,
    ]
      .join(' ')
      .toLocaleLowerCase('pt-BR')

    return searchableContent.includes(normalizedSearch.value)
  })
})

const selectedOrganization = computed<Organization>(
  () =>
    organizations.value.find((organization) => organization.id === selectedOrganizationId.value) ??
    organizations.value[0]!,
)

const activeOrganizations = computed(
  () => organizations.value.filter((organization) => organization.status === 'Ativo').length,
)

const totalMembers = computed(() =>
  organizations.value.reduce((total, organization) => total + organization.members, 0),
)

function selectOrganization(organization: Organization) {
  selectedOrganizationId.value = organization.id
  selectionFeedback.value = `${organization.name} selecionada para esta sessao.`

  if (feedbackTimeout) {
    window.clearTimeout(feedbackTimeout)
  }

  feedbackTimeout = window.setTimeout(() => {
    selectionFeedback.value = `${organization.name} pronta para abrir como workspace.`
  }, 2200)
}

function clearSearch() {
  searchQuery.value = ''
}

function createOrganization() {
  createdOrganizationsCount.value += 1

  const organizationNumber = createdOrganizationsCount.value
  const newOrganization: Organization = {
    id: `nova-organizacao-${organizationNumber}`,
    name: organizationNumber === 1 ? 'Nova organizacao' : `Nova organizacao ${organizationNumber}`,
    plan: 'Starter',
    role: 'Owner',
    members: 1,
    flows: 0,
    lastAccess: 'Criada agora',
    status: 'Revisao',
    initials: organizationNumber === 1 ? 'NO' : `N${organizationNumber}`,
  }

  organizations.value = [newOrganization, ...organizations.value]
  searchQuery.value = ''
  selectedOrganizationId.value = newOrganization.id
  selectionFeedback.value = `${newOrganization.name} criada e selecionada para configuracao.`

  if (feedbackTimeout) {
    window.clearTimeout(feedbackTimeout)
  }

  feedbackTimeout = window.setTimeout(() => {
    selectionFeedback.value = `${newOrganization.name} pronta para configurar como workspace.`
  }, 2200)
}

function goToWorkspace() {
  router.push({
    name: 'canvas',
    query: { organization: selectedOrganization.value.id },
  })
}

onBeforeUnmount(() => {
  if (feedbackTimeout) {
    window.clearTimeout(feedbackTimeout)
  }
})
</script>

<template>
  <main class="min-h-screen bg-[#f7fafb] text-[#172224]" aria-label="Selecionar organizacao">
    <header
      class="border-b border-[#dfeaed] bg-white/88 shadow-[0_1px_2px_rgb(18_33_36_/_3%)] backdrop-blur"
    >
      <div
        class="mx-auto flex min-h-16 w-full max-w-[1180px] items-center justify-between gap-4 px-6 max-[640px]:px-4"
      >
        <RouterLink
          class="inline-flex min-h-10 items-center gap-2 text-sm font-extrabold text-[#172224] no-underline"
          to="/"
          aria-label="Blendes Flow home"
        >
          <span
            class="inline-flex size-9 items-center justify-center rounded-lg bg-[#edf7f9] shadow-[inset_0_0_0_1px_rgb(36_107_120_/_12%)]"
          >
            <Blend class="text-[#246b78]" :size="20" :stroke-width="2.4" aria-hidden="true" />
          </span>
          <span>Blendes Flow</span>
        </RouterLink>

        <RouterLink
          class="inline-flex min-h-10 items-center justify-center rounded-lg px-3 text-xs font-extrabold text-[#62777d] no-underline transition-[background-color,color,transform] duration-150 hover:bg-[#f2f7f8] hover:text-[#172224] active:scale-[0.96] motion-reduce:transition-none"
          to="/auth"
        >
          Trocar conta
        </RouterLink>
      </div>
    </header>

    <section class="mx-auto w-full max-w-[1180px] px-6 py-8 max-[640px]:px-4">
      <div class="mb-7 flex flex-wrap items-end justify-between gap-5">
        <div>
          <h1 class="m-0 text-[clamp(1.55rem,2.6vw,2.25rem)] font-black leading-tight text-[#172224]">
            Organizacoes
          </h1>
          <p class="mt-2 max-w-[560px] text-sm font-semibold leading-6 text-[#62777d] text-pretty">
            Selecione o workspace que sera usado nesta sessao.
          </p>
        </div>

        <div class="flex flex-wrap items-center gap-2">
          <button
            class="inline-flex min-h-10 cursor-pointer items-center justify-center gap-2 rounded-lg bg-[#246b78] pl-3.5 pr-3 text-xs font-black text-white shadow-[0_1px_2px_rgb(18_33_36_/_16%),0_8px_18px_rgb(36_107_120_/_14%)] transition-[background-color,box-shadow,transform] duration-150 hover:bg-[#1f5f6d] hover:shadow-[0_1px_2px_rgb(18_33_36_/_18%),0_10px_22px_rgb(36_107_120_/_18%)] active:scale-[0.96] focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/70 motion-reduce:transition-none"
            type="button"
            @click="createOrganization"
          >
            <Plus :size="16" :stroke-width="2.6" aria-hidden="true" />
            Nova organizacao
          </button>

          <div
            class="flex min-h-10 items-center gap-2 rounded-lg bg-white px-3 text-xs font-bold text-[#62777d] shadow-[0_0_0_1px_rgb(18_33_36_/_7%),0_1px_2px_rgb(18_33_36_/_4%)]"
          >
            <span class="tabular-nums text-[#172224]">{{ activeOrganizations }}</span>
            ativas
            <span class="h-4 w-px bg-[#dfeaed]" aria-hidden="true"></span>
            <span class="tabular-nums text-[#172224]">{{ totalMembers }}</span>
            membros
          </div>
        </div>
      </div>

      <div class="grid grid-cols-[minmax(0,1fr)_320px] gap-5 max-[980px]:grid-cols-1">
        <section
          class="min-w-0 rounded-xl bg-white shadow-[0_0_0_1px_rgb(18_33_36_/_7%),0_10px_30px_rgb(18_33_36_/_5%)]"
        >
          <div class="grid gap-3 border-b border-[#e2ecef] p-4">
            <div class="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h2 class="m-0 text-sm font-black text-[#172224]">Workspaces disponiveis</h2>
                <p class="mt-1 text-xs font-semibold text-[#7a8f94]" aria-live="polite">
                  {{ filteredOrganizations.length }} de {{ organizations.length }} organizacoes
                </p>
              </div>

              <button
                class="inline-flex min-h-10 items-center justify-center rounded-lg px-3 text-xs font-extrabold text-[#62777d] transition-[background-color,color,transform] duration-150 hover:bg-[#f2f7f8] hover:text-[#172224] active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-40 motion-reduce:transition-none"
                type="button"
                :disabled="!searchQuery"
                @click="clearSearch"
              >
                Limpar
              </button>
            </div>

            <label class="relative block" for="organization-search">
              <Search
                class="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 text-[#7a8f94]"
                :size="17"
                :stroke-width="2.3"
                aria-hidden="true"
              />
              <input
                id="organization-search"
                v-model="searchQuery"
                class="min-h-11 w-full rounded-lg bg-[#f7fafb] px-10 text-sm font-bold text-[#172224] outline-none shadow-[inset_0_0_0_1px_rgb(216_230_233_/_92%)] transition-[background-color,box-shadow] duration-150 placeholder:text-[#91a5aa] focus:bg-white focus:shadow-[inset_0_0_0_1px_#8adff3,0_0_0_3px_rgb(174_238_255_/_22%)]"
                type="search"
                autocomplete="off"
                placeholder="Buscar organizacao, plano ou permissao"
              />
            </label>
          </div>

          <div v-if="filteredOrganizations.length" class="divide-y divide-[#e8f0f2]">
            <button
              v-for="organization in filteredOrganizations"
              :key="organization.id"
              class="group relative grid min-h-[92px] w-full cursor-pointer grid-cols-[44px_minmax(0,1fr)_auto] items-center gap-3 bg-white px-4 py-3 text-left transition-[background-color,box-shadow] duration-150 hover:bg-[#f8fbfc] focus-visible:z-10 focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-[-3px] focus-visible:outline-[#aeeeff]/70 max-[720px]:grid-cols-[44px_minmax(0,1fr)]"
              :class="
                selectedOrganizationId === organization.id
                  ? 'bg-[#fbfeff] shadow-[inset_3px_0_0_#246b78]'
                  : ''
              "
              type="button"
              :aria-pressed="selectedOrganizationId === organization.id"
              @click="selectOrganization(organization)"
            >
              <span
                class="flex size-11 shrink-0 items-center justify-center rounded-lg bg-[#eef7f9] text-sm font-black text-[#246b78] shadow-[inset_0_0_0_1px_rgb(36_107_120_/_10%)]"
              >
                {{ organization.initials }}
              </span>

              <span class="min-w-0">
                <span class="flex min-w-0 flex-wrap items-center gap-x-2 gap-y-1">
                  <span class="truncate text-sm font-black text-[#172224]">
                    {{ organization.name }}
                  </span>
                  <span
                    class="inline-flex min-h-5 items-center rounded-md bg-[#f2f7f8] px-2 text-[0.68rem] font-extrabold uppercase text-[#62777d]"
                  >
                    {{ organization.plan }}
                  </span>
                  <span
                    class="inline-flex min-h-5 items-center rounded-md px-2 text-[0.68rem] font-extrabold uppercase"
                    :class="
                      organization.status === 'Ativo'
                        ? 'bg-[#eef9f5] text-[#207258]'
                        : 'bg-[#fff7e8] text-[#8c6116]'
                    "
                  >
                    {{ organization.status }}
                  </span>
                </span>

                <span
                  class="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs font-bold text-[#71868b]"
                >
                  <span class="inline-flex items-center gap-1.5">
                    <UsersRound :size="14" :stroke-width="2.2" aria-hidden="true" />
                    <span class="tabular-nums">{{ organization.members }}</span>
                    membros
                  </span>
                  <span class="inline-flex items-center gap-1.5">
                    <Building2 :size="14" :stroke-width="2.2" aria-hidden="true" />
                    <span class="tabular-nums">{{ organization.flows }}</span>
                    fluxos
                  </span>
                  <span class="inline-flex items-center gap-1.5">
                    <Clock3 :size="14" :stroke-width="2.2" aria-hidden="true" />
                    {{ organization.lastAccess }}
                  </span>
                </span>
              </span>

              <span
                class="flex min-w-[132px] items-center justify-end gap-2 max-[720px]:col-span-2 max-[720px]:justify-between"
              >
                <span class="text-xs font-extrabold text-[#62777d]">{{ organization.role }}</span>
                <span
                  class="inline-flex min-h-9 items-center gap-1.5 rounded-lg px-3 text-xs font-black transition-[background-color,color,transform] duration-150 group-active:scale-[0.96]"
                  :class="
                    selectedOrganizationId === organization.id
                      ? 'bg-[#246b78] text-white'
                      : 'bg-[#eef7f9] text-[#246b78] group-hover:bg-[#dff1f5]'
                  "
                >
                  <CheckCircle2
                    v-if="selectedOrganizationId === organization.id"
                    :size="15"
                    :stroke-width="2.5"
                    aria-hidden="true"
                  />
                  {{ selectedOrganizationId === organization.id ? 'Atual' : 'Usar' }}
                </span>
              </span>
            </button>
          </div>

          <div v-else class="grid min-h-[260px] place-items-center p-8 text-center">
            <div class="max-w-[330px]">
              <span
                class="mx-auto flex size-11 items-center justify-center rounded-lg bg-[#eef7f9] text-[#246b78]"
              >
                <Search :size="21" :stroke-width="2.3" aria-hidden="true" />
              </span>
              <h2 class="m-0 mt-4 text-base font-black text-[#172224]">
                Nenhuma organizacao encontrada
              </h2>
              <p class="mt-2 text-sm font-semibold leading-6 text-[#62777d] text-pretty">
                Revise o termo buscado ou limpe o filtro para voltar para a lista completa.
              </p>
              <button
                class="mt-4 inline-flex min-h-10 items-center justify-center rounded-lg bg-[#246b78] px-4 text-xs font-black text-white shadow-[0_1px_2px_rgb(18_33_36_/_12%)] transition-[background-color,transform] duration-150 hover:bg-[#1f5f6d] active:scale-[0.96] motion-reduce:transition-none"
                type="button"
                @click="clearSearch"
              >
                Mostrar todas
              </button>
            </div>
          </div>
        </section>

        <aside
          class="h-fit rounded-xl bg-white p-4 shadow-[0_0_0_1px_rgb(18_33_36_/_7%),0_10px_30px_rgb(18_33_36_/_5%)]"
        >
          <div class="flex items-start justify-between gap-3">
            <div>
              <p class="m-0 text-xs font-extrabold uppercase tracking-[0.1em] text-[#7a8f94]">
                Workspace atual
              </p>
              <h2 class="m-0 mt-2 text-xl font-black leading-tight text-[#172224]">
                {{ selectedOrganization.name }}
              </h2>
            </div>
            <span
              class="flex size-10 shrink-0 items-center justify-center rounded-lg bg-[#eef7f9] text-sm font-black text-[#246b78]"
            >
              {{ selectedOrganization.initials }}
            </span>
          </div>

          <div
            class="mt-4 rounded-lg bg-[#f7fafb] p-3 shadow-[inset_0_0_0_1px_rgb(216_230_233_/_84%)]"
            aria-live="polite"
          >
            <p class="m-0 flex items-start gap-2 text-sm font-bold leading-5 text-[#446069]">
              <CheckCircle2
                class="mt-0.5 shrink-0 text-[#246b78]"
                :size="16"
                :stroke-width="2.5"
                aria-hidden="true"
              />
              <span>{{ selectionFeedback }}</span>
            </p>
          </div>

          <dl class="mt-4 grid gap-2 text-sm">
            <div class="flex min-h-9 items-center justify-between gap-3">
              <dt class="font-bold text-[#71868b]">Plano</dt>
              <dd class="m-0 font-black text-[#172224]">{{ selectedOrganization.plan }}</dd>
            </div>
            <div class="flex min-h-9 items-center justify-between gap-3">
              <dt class="font-bold text-[#71868b]">Permissao</dt>
              <dd class="m-0 font-black text-[#172224]">{{ selectedOrganization.role }}</dd>
            </div>
            <div class="flex min-h-9 items-center justify-between gap-3">
              <dt class="font-bold text-[#71868b]">Membros</dt>
              <dd class="m-0 font-black tabular-nums text-[#172224]">
                {{ selectedOrganization.members }}
              </dd>
            </div>
            <div class="flex min-h-9 items-center justify-between gap-3">
              <dt class="font-bold text-[#71868b]">Ultimo acesso</dt>
              <dd class="m-0 font-black text-[#172224]">{{ selectedOrganization.lastAccess }}</dd>
            </div>
          </dl>

          <button
            class="mt-5 inline-flex min-h-11 w-full cursor-pointer items-center justify-center gap-2 rounded-lg bg-[#246b78] pl-4 pr-3.5 text-sm font-black text-white shadow-[0_1px_2px_rgb(18_33_36_/_16%),0_10px_22px_rgb(36_107_120_/_16%)] transition-[background-color,box-shadow,transform] duration-150 hover:bg-[#1f5f6d] hover:shadow-[0_1px_2px_rgb(18_33_36_/_18%),0_12px_26px_rgb(36_107_120_/_20%)] active:scale-[0.96] focus-visible:outline focus-visible:outline-3 focus-visible:outline-offset-3 focus-visible:outline-[#aeeeff]/70 motion-reduce:transition-none"
            type="button"
            @click="goToWorkspace"
          >
            Entrar no workspace
            <ArrowRight class="ml-px" :size="17" :stroke-width="2.6" aria-hidden="true" />
          </button>
        </aside>
      </div>
    </section>
  </main>
</template>
