import { computed, shallowRef } from 'vue'
import { defineStore } from 'pinia'

import type { Organization } from '@/domains/organizations/contracts'

const workspaceStorageKey = 'blendes.workspace'

export const useWorkspaceStore = defineStore('workspace', () => {
  const currentOrganization = shallowRef<Organization | null>(restoreWorkspace())

  const hasWorkspace = computed(() => currentOrganization.value !== null)
  const organizationId = computed(() => currentOrganization.value?.id ?? null)
  const organizationName = computed(() => currentOrganization.value?.name ?? '')

  function selectWorkspace(organization: Organization) {
    currentOrganization.value = organization
    saveWorkspace(organization)
  }

  function clearWorkspace() {
    currentOrganization.value = null
    clearStoredWorkspace()
  }

  return {
    clearWorkspace,
    currentOrganization,
    hasWorkspace,
    organizationId,
    organizationName,
    selectWorkspace,
  }
})

function restoreWorkspace() {
  try {
    const value = sessionStorage.getItem(workspaceStorageKey)

    if (!value) {
      return null
    }

    return JSON.parse(value) as Organization
  } catch {
    clearStoredWorkspace()
    return null
  }
}

function saveWorkspace(organization: Organization) {
  try {
    sessionStorage.setItem(workspaceStorageKey, JSON.stringify(organization))
  } catch {
    // Workspace restore is best-effort. The selected workspace remains in memory.
  }
}

function clearStoredWorkspace() {
  try {
    sessionStorage.removeItem(workspaceStorageKey)
  } catch {
    // Nothing to clear when browser storage is unavailable.
  }
}
