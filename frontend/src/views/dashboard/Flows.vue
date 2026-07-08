<script setup lang="ts">
import { computed, ref, shallowRef } from 'vue'
import { AlertCircle, Plus, RefreshCw, Workflow } from '@lucide/vue'

import AppToast from '@/components/AppToast.vue'
import { useTimedToast } from '@/composables/useTimedToast'
import type { Blave, NewBlave, UpdateBlave } from '@/domains/blaves/contracts'
import {
  useBlaves,
  useCreateBlaveMutation,
  useDeleteBlaveMutation,
  useUpdateBlaveMutation,
} from '@/domains/blaves/queries'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { ApiRequestError } from '@/lib/http/errors'
import { useWorkspaceStore } from '@/stores/workspace'

import BlaveDetailsDrawer from './components/BlaveDetailsDrawer.vue'
import BlaveFlowCard from './components/BlaveFlowCard.vue'
import CreateBlaveDialog from './components/CreateBlaveDialog.vue'
import DeleteBlaveDialog from './components/DeleteBlaveDialog.vue'
import EditBlaveDialog from './components/EditBlaveDialog.vue'

const workspaceStore = useWorkspaceStore()
const selectedBlave = shallowRef<Blave | null>(null)
const editingBlave = shallowRef<Blave | null>(null)
const deletingBlave = shallowRef<Blave | null>(null)
const isCreateDialogOpen = ref(false)
const favoritePendingBlaveId = ref<number | null>(null)
const { hideToast, showErrorToast, showSuccessToast, toast } = useTimedToast()

const organizationId = computed(() => workspaceStore.organizationId)
const blavesQuery = useBlaves(organizationId)
const createBlaveMutation = useCreateBlaveMutation(organizationId)
const editBlaveMutation = useUpdateBlaveMutation(organizationId)
const favoriteBlaveMutation = useUpdateBlaveMutation(organizationId)
const deleteBlaveMutation = useDeleteBlaveMutation(organizationId)

const blaves = computed(() => blavesQuery.data.value ?? [])
const isDrawerOpen = computed(() => selectedBlave.value !== null)
const isEditDialogOpen = computed(() => editingBlave.value !== null)
const isDeleteDialogOpen = computed(() => deletingBlave.value !== null)
const canCreateBlave = computed(
  () => organizationId.value !== null && !createBlaveMutation.isPending.value,
)

const createBlaveErrorMessage = computed(() => {
  const error = createBlaveMutation.error.value

  if (error instanceof ApiRequestError) {
    return error.message
  }

  if (error) {
    return 'Unable to create this flow. Check the details and try again.'
  }

  return ''
})

const editBlaveErrorMessage = computed(() => getMutationErrorMessage(editBlaveMutation.error.value))
const deleteBlaveErrorMessage = computed(() =>
  getMutationErrorMessage(deleteBlaveMutation.error.value),
)

function getMutationErrorMessage(error: unknown) {
  if (error instanceof ApiRequestError) {
    return error.message
  }

  if (error) {
    return 'Unable to save this flow. Check the details and try again.'
  }

  return ''
}

function openCreateDialog() {
  if (!canCreateBlave.value) {
    return
  }

  hideToast()
  createBlaveMutation.reset()
  isCreateDialogOpen.value = true
}

function closeCreateDialog() {
  if (createBlaveMutation.isPending.value) {
    return
  }

  isCreateDialogOpen.value = false
}

function openBlave(blave: Blave) {
  selectedBlave.value = blave
}

function openEditDialog(blave: Blave) {
  editBlaveMutation.reset()
  editingBlave.value = blave
}

function closeEditDialog() {
  if (editBlaveMutation.isPending.value) {
    return
  }

  editingBlave.value = null
}

function openDeleteDialog(blave: Blave) {
  deleteBlaveMutation.reset()
  deletingBlave.value = blave
}

function closeDeleteDialog() {
  if (deleteBlaveMutation.isPending.value) {
    return
  }

  deletingBlave.value = null
}

function closeDrawer() {
  selectedBlave.value = null
}

async function createBlave(payload: NewBlave) {
  hideToast()

  const blave = await createBlaveMutation.mutateAsync(payload).catch(() => null)

  if (!blave) {
    showErrorToast(createBlaveErrorMessage.value || 'Flow could not be created.')
    return
  }

  isCreateDialogOpen.value = false
  showSuccessToast(`Flow "${blave.title}" created.`)
}

async function updateBlave(payload: UpdateBlave) {
  if (!editingBlave.value) {
    return
  }

  hideToast()
  const blave = await editBlaveMutation
    .mutateAsync({ blaveId: editingBlave.value.id, payload })
    .catch(() => null)

  if (!blave) {
    showErrorToast(editBlaveErrorMessage.value || 'Flow could not be updated.')
    return
  }

  if (selectedBlave.value?.id === blave.id) {
    selectedBlave.value = blave
  }

  editingBlave.value = null
  showSuccessToast(`Flow "${blave.title}" updated.`)
}

async function toggleFavorite(blave: Blave) {
  if (favoritePendingBlaveId.value !== null) {
    return
  }

  hideToast()
  favoritePendingBlaveId.value = blave.id
  const updatedBlave = await favoriteBlaveMutation
    .mutateAsync({
      blaveId: blave.id,
      payload: {
        is_favorite: !blave.is_favorite,
      },
    })
    .catch(() => null)
    .finally(() => {
      favoritePendingBlaveId.value = null
    })

  if (!updatedBlave) {
    showErrorToast(
      getMutationErrorMessage(favoriteBlaveMutation.error.value) ||
        'Favorite state could not be saved.',
    )
    return
  }

  if (selectedBlave.value?.id === updatedBlave.id) {
    selectedBlave.value = updatedBlave
  }

  showSuccessToast(
    updatedBlave.is_favorite ? 'Flow added to favorites.' : 'Flow removed from favorites.',
  )
}

async function deleteBlave() {
  if (!deletingBlave.value) {
    return
  }

  hideToast()
  const blave = deletingBlave.value
  const wasDeleted = await deleteBlaveMutation
    .mutateAsync(blave.id)
    .then(() => true)
    .catch(() => false)

  if (!wasDeleted) {
    showErrorToast(deleteBlaveErrorMessage.value || 'Flow could not be removed.')
    return
  }

  if (selectedBlave.value?.id === blave.id) {
    selectedBlave.value = null
  }

  if (editingBlave.value?.id === blave.id) {
    editingBlave.value = null
  }

  deletingBlave.value = null
  showSuccessToast(`Flow "${blave.title}" removed.`)
}
</script>

<template>
  <DashboardLayout>
    <div class="flex min-h-0 w-full flex-col gap-5">
      <section
        class="flex flex-wrap items-end justify-between gap-4 border-b border-slate-200 pb-5 dark:border-slate-800"
        aria-labelledby="flows-page-title"
      >
        <div class="min-w-0">
          <p
            class="text-xs leading-none font-semibold tracking-[0.08em] text-slate-500 uppercase dark:text-slate-400"
          >
            Workflow executions
          </p>
          <h2
            id="flows-page-title"
            class="mt-2 text-2xl leading-tight font-semibold text-slate-950 dark:text-slate-50"
          >
            Your flows
          </h2>
          <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-600 dark:text-slate-400">
            Track each BlendES run by its current movement and open the flow details without leaving
            the workspace.
          </p>
        </div>

        <div class="flex flex-wrap items-center gap-2">
          <button
            class="inline-flex h-10 cursor-pointer items-center gap-2 rounded-lg bg-blue-700 px-3 text-sm leading-none font-semibold text-white outline-none transition-[background-color,box-shadow,transform,opacity] duration-150 ease-out hover:bg-blue-800 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.97] disabled:cursor-not-allowed disabled:opacity-60 motion-reduce:transition-none"
            type="button"
            :disabled="!canCreateBlave"
            @click="openCreateDialog"
          >
            <Plus class="size-4" :stroke-width="2.2" aria-hidden="true" />
            New flow
          </button>

          <button
            class="inline-flex h-10 cursor-pointer items-center gap-2 rounded-lg border border-slate-200 bg-white px-3 text-sm leading-none font-semibold text-slate-700 outline-none transition-[border-color,background-color,color,box-shadow,transform] duration-150 ease-out hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 focus-visible:border-blue-300 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.97] disabled:cursor-not-allowed disabled:opacity-60 motion-reduce:transition-none dark:border-slate-700 dark:bg-slate-900 dark:text-slate-200 dark:hover:border-blue-400/30 dark:hover:bg-blue-400/10 dark:hover:text-blue-200 dark:focus-visible:ring-blue-950"
            type="button"
            :disabled="blavesQuery.isFetching.value"
            @click="blavesQuery.refetch()"
          >
            <RefreshCw
              class="size-4"
              :class="blavesQuery.isFetching.value ? 'animate-spin motion-reduce:animate-none' : ''"
              :stroke-width="2.1"
              aria-hidden="true"
            />
            Refresh
          </button>
        </div>
      </section>

      <AppToast :message="toast?.message" :tone="toast?.tone" @dismiss="hideToast" />

      <section
        v-if="blavesQuery.isLoading.value"
        class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4"
        aria-label="Loading flows"
        aria-busy="true"
      >
        <div
          v-for="index in 8"
          :key="index"
          class="min-h-[156px] animate-pulse rounded-lg border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900"
        >
          <div class="flex gap-3 px-3.5 pt-3.5">
            <div class="size-9 rounded-md bg-slate-200 dark:bg-slate-800"></div>
            <div class="min-w-0 flex-1">
              <div class="h-4 w-2/3 rounded bg-slate-200 dark:bg-slate-800"></div>
              <div class="mt-2 h-3 w-full rounded bg-slate-100 dark:bg-slate-800/70"></div>
              <div class="mt-2 h-3 w-4/5 rounded bg-slate-100 dark:bg-slate-800/70"></div>
            </div>
          </div>
          <div
            class="mt-10 border-t border-slate-200 bg-slate-50 px-3.5 py-2.5 dark:border-slate-800 dark:bg-slate-950"
          >
            <div class="h-8 w-20 rounded-md bg-slate-200 dark:bg-slate-800"></div>
          </div>
        </div>
      </section>

      <section
        v-else-if="blavesQuery.isError.value"
        class="grid min-h-[280px] place-items-center rounded-xl border border-rose-200 bg-rose-50 px-6 py-10 text-center dark:border-rose-500/30 dark:bg-rose-500/10"
        role="alert"
      >
        <div>
          <AlertCircle
            class="mx-auto size-9 text-rose-600"
            :stroke-width="2.1"
            aria-hidden="true"
          />
          <h2 class="mt-4 text-base leading-6 font-semibold text-rose-950 dark:text-rose-100">
            Flows could not be loaded
          </h2>
          <p class="mt-2 max-w-md text-sm leading-6 text-rose-800 dark:text-rose-200">
            Check your connection and try refreshing the list.
          </p>
        </div>
      </section>

      <section
        v-else-if="blaves.length === 0"
        class="grid min-h-[320px] place-items-center rounded-xl border border-dashed border-slate-300 bg-white px-6 py-12 text-center dark:border-slate-700 dark:bg-slate-900"
        aria-label="Empty flows"
      >
        <div>
          <Workflow
            class="mx-auto size-10 text-slate-400 dark:text-slate-500"
            :stroke-width="2.1"
            aria-hidden="true"
          />
          <h2 class="mt-4 text-base leading-6 font-semibold text-slate-950 dark:text-slate-50">
            No flows yet
          </h2>
          <p class="mt-2 max-w-md text-sm leading-6 text-slate-600 dark:text-slate-400">
            Create a BlendES workflow execution to start tracking movement, risk, and change.
          </p>
          <button
            class="mt-5 inline-flex h-10 cursor-pointer items-center gap-2 rounded-lg bg-blue-700 px-3.5 text-sm leading-none font-semibold text-white outline-none transition-[background-color,box-shadow,transform,opacity] duration-150 ease-out hover:bg-blue-800 focus-visible:ring-4 focus-visible:ring-blue-100 active:scale-[0.97] disabled:cursor-not-allowed disabled:opacity-60 motion-reduce:transition-none"
            type="button"
            :disabled="!canCreateBlave"
            @click="openCreateDialog"
          >
            <Plus class="size-4" :stroke-width="2.2" aria-hidden="true" />
            Create first flow
          </button>
        </div>
      </section>

      <section
        v-else
        class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4"
        aria-label="User flows"
      >
        <BlaveFlowCard
          v-for="blave in blaves"
          :key="blave.id"
          :blave="blave"
          :is-favorite-pending="favoritePendingBlaveId === blave.id"
          :is-remove-pending="deleteBlaveMutation.isPending.value && deletingBlave?.id === blave.id"
          @edit="openEditDialog"
          @open="openBlave"
          @remove="openDeleteDialog"
          @toggle-favorite="toggleFavorite"
        />
      </section>
    </div>

    <BlaveDetailsDrawer :blave="selectedBlave" :is-open="isDrawerOpen" @close="closeDrawer" />
    <CreateBlaveDialog
      :error-message="createBlaveErrorMessage"
      :is-open="isCreateDialogOpen"
      :is-pending="createBlaveMutation.isPending.value"
      @close="closeCreateDialog"
      @create="createBlave"
    />
    <EditBlaveDialog
      :blave="editingBlave"
      :error-message="editBlaveErrorMessage"
      :is-open="isEditDialogOpen"
      :is-pending="editBlaveMutation.isPending.value"
      @close="closeEditDialog"
      @update="updateBlave"
    />
    <DeleteBlaveDialog
      :blave="deletingBlave"
      :error-message="deleteBlaveErrorMessage"
      :is-open="isDeleteDialogOpen"
      :is-pending="deleteBlaveMutation.isPending.value"
      @close="closeDeleteDialog"
      @confirm="deleteBlave"
    />
  </DashboardLayout>
</template>
