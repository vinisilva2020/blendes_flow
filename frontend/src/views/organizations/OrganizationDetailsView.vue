<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Trash2 } from '@lucide/vue'

import { ApiRequestError } from '@/lib/http/errors'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import {
  useDeleteOrganizationMutation,
  useOrganization,
  useUpdateOrganizationMutation,
} from '@/domains/organizations/queries'
import { useWorkspaceStore } from '@/stores/workspace'

import DeleteOrganizationDialog from './components/DeleteOrganizationDialog.vue'
import OrganizationDetailsForm, {
  type OrganizationDetailsFormPayload,
} from './components/OrganizationDetailsForm.vue'

const router = useRouter()
const workspaceStore = useWorkspaceStore()

const organizationId = computed(() => workspaceStore.organizationId)
const hasSelectedOrganization = computed(() => organizationId.value !== null)

const organizationQuery = useOrganization(organizationId, hasSelectedOrganization)
const updateOrganizationMutation = useUpdateOrganizationMutation()
const deleteOrganizationMutation = useDeleteOrganizationMutation()

const successMessage = ref('')
const isDeleteDialogOpen = ref(false)

const organization = computed(() => organizationQuery.data.value)
const organizationName = computed(
  () => organization.value?.name || workspaceStore.organizationName || 'Organization',
)
const organizationFormValues = computed(() => ({
  description: organization.value?.description ?? '',
  name: organization.value?.name ?? workspaceStore.organizationName,
}))
const organizationStatusLabel = computed(() =>
  organization.value?.is_active === false ? 'Inactive' : 'Active',
)
const isOrganizationActive = computed(() => organization.value?.is_active !== false)

const queryErrorMessage = computed(() => {
  const error = organizationQuery.error.value

  if (error instanceof ApiRequestError) {
    return error.message
  }

  if (error) {
    return 'Unable to load this organization. Try again in a moment.'
  }

  if (!hasSelectedOrganization.value) {
    return 'Select an organization workspace to manage company details.'
  }

  return ''
})

const updateErrorMessage = computed(() => {
  const error = updateOrganizationMutation.error.value

  if (error instanceof ApiRequestError) {
    return error.message
  }

  if (error) {
    return 'Unable to save changes. Review the details and try again.'
  }

  return ''
})

const deleteErrorMessage = computed(() => {
  const error = deleteOrganizationMutation.error.value

  if (error instanceof ApiRequestError) {
    return error.message
  }

  if (error) {
    return 'Unable to delete this organization. Try again in a moment.'
  }

  return ''
})

async function saveChanges(payload: OrganizationDetailsFormPayload) {
  successMessage.value = ''
  updateOrganizationMutation.reset()
  const currentOrganizationId = organizationId.value

  if (currentOrganizationId === null) {
    return
  }

  const updatedOrganization = await updateOrganizationMutation
    .mutateAsync({
      data: payload,
      organizationId: currentOrganizationId,
    })
    .catch(() => null)

  if (!updatedOrganization) {
    return
  }

  successMessage.value = 'Organization changes saved.'

  if (workspaceStore.organizationId === updatedOrganization.id) {
    workspaceStore.selectWorkspace(updatedOrganization)
  }

  window.setTimeout(() => {
    successMessage.value = ''
  }, 2600)
}

async function deleteOrganization() {
  deleteOrganizationMutation.reset()
  const currentOrganizationId = organizationId.value

  if (currentOrganizationId === null) {
    return
  }

  await deleteOrganizationMutation.mutateAsync(currentOrganizationId).catch(() => null)

  if (deleteOrganizationMutation.isError.value) {
    return
  }

  if (workspaceStore.organizationId === currentOrganizationId) {
    workspaceStore.clearWorkspace()
  }

  isDeleteDialogOpen.value = false
  await router.push({ name: 'organizations' })
}
</script>

<template>
  <DashboardLayout>
    <div class="mx-auto flex w-full max-w-5xl flex-col gap-5">
      <p
        v-if="queryErrorMessage"
        class="rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm leading-5 font-medium text-red-700 dark:border-red-400/30 dark:bg-red-500/10 dark:text-red-200"
        role="alert"
      >
        {{ queryErrorMessage }}
      </p>

      <template v-else>
        <OrganizationDetailsForm
          :error-message="updateErrorMessage"
          :initial-values="organizationFormValues"
          :is-loading="organizationQuery.isLoading.value"
          :is-pending="updateOrganizationMutation.isPending.value"
          :is-status-active="isOrganizationActive"
          :reset-key="organization?.updated_at ?? null"
          :status-label="organizationStatusLabel"
          :success-message="successMessage"
          @submit="saveChanges"
        />

        <section
          class="rounded-3xl bg-white p-2 shadow-[0_0_0_1px_rgb(15_23_42_/_6%),0_10px_28px_rgb(15_23_42_/_5%)] dark:bg-slate-900 dark:shadow-[0_0_0_1px_rgb(51_65_85_/_70%),0_18px_42px_rgb(0_0_0_/_24%)]"
          aria-labelledby="delete-organization-heading"
        >
          <div class="rounded-2xl bg-slate-50/80 p-4 sm:p-5 md:p-6 dark:bg-slate-950/70">
            <div class="grid gap-4 md:grid-cols-[minmax(0,1fr)_auto] md:items-center">
              <div>
                <p class="text-xs leading-4 font-semibold tracking-[0.12em] text-red-600 uppercase">
                  Danger zone
                </p>
                <h2
                  id="delete-organization-heading"
                  class="mt-1 text-lg leading-6 font-semibold text-balance text-slate-950 dark:text-slate-50"
                >
                  Delete company
                </h2>
                <p
                  class="mt-1 max-w-2xl text-sm leading-6 font-medium text-pretty text-slate-500 dark:text-slate-400"
                >
                  Permanently remove this workspace and its company context.
                </p>
              </div>

              <button
                class="inline-flex min-h-10 w-full cursor-pointer items-center justify-center gap-2 rounded-xl bg-white px-4 text-sm font-semibold text-red-700 outline-none shadow-[0_0_0_1px_rgb(254_202_202_/_95%)] transition-[background-color,color,scale,opacity,box-shadow] duration-150 ease-out hover:bg-red-50 hover:text-red-800 hover:shadow-[0_0_0_1px_rgb(248_113_113),0_8px_18px_rgb(220_38_38_/_10%)] focus-visible:ring-4 focus-visible:ring-red-100 active:scale-[0.96] disabled:cursor-not-allowed disabled:opacity-60 md:w-auto dark:bg-slate-900 dark:text-red-300 dark:shadow-[0_0_0_1px_rgb(248_113_113_/_28%)] dark:hover:bg-red-500/10 dark:hover:text-red-200 dark:hover:shadow-[0_0_0_1px_rgb(248_113_113_/_40%)] dark:focus-visible:ring-red-950"
                type="button"
                :disabled="!organization"
                @click="isDeleteDialogOpen = true"
              >
                <Trash2 :size="15" :stroke-width="2.2" aria-hidden="true" />
                Delete company
              </button>
            </div>
          </div>
        </section>
      </template>
    </div>

    <DeleteOrganizationDialog
      :error-message="deleteErrorMessage"
      :is-open="isDeleteDialogOpen"
      :is-pending="deleteOrganizationMutation.isPending.value"
      :organization-name="organizationName"
      @close="isDeleteDialogOpen = false"
      @confirm="deleteOrganization"
    />
  </DashboardLayout>
</template>
