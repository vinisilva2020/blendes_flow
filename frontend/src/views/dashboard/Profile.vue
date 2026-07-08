<script setup lang="ts">
import { computed, ref } from 'vue'

import { ApiRequestError } from '@/lib/http/errors'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import {
  useCurrentAccount,
  useLinkCurrentGoogleSocialAccountMutation,
  useUnlinkCurrentGoogleSocialAccountMutation,
  useUpdateCurrentAccountPasswordMutation,
  useUpdateCurrentAccountMutation,
} from '@/domains/accounts/queries'
import type {
  AccountGoogleSocialAccountPayload,
  AccountPasswordPayload,
} from '@/domains/accounts/contracts'

import AvatarPickerDialog from './components/AvatarPickerDialog.vue'
import ProfileDetailsForm, {
  type ProfileDetailsFormPayload,
  type ProfileDetailsFormValues,
} from './components/ProfileDetailsForm.vue'
import SecurityPasswordCard from './components/SecurityPasswordCard.vue'

const currentAccount = useCurrentAccount()
const updateAccountMutation = useUpdateCurrentAccountMutation()
const updatePasswordMutation = useUpdateCurrentAccountPasswordMutation()
const linkGoogleMutation = useLinkCurrentGoogleSocialAccountMutation()
const unlinkGoogleMutation = useUnlinkCurrentGoogleSocialAccountMutation()

const profileFormRef = ref<InstanceType<typeof ProfileDetailsForm> | null>(null)
const isAvatarDialogOpen = ref(false)
const avatarDialogSelection = ref<string | null>(null)
const successMessage = ref('')
const passwordSuccessMessage = ref('')

const account = computed(() => currentAccount.data.value ?? null)
const profileInitialValues = computed<ProfileDetailsFormValues>(() => ({
  avatarType: account.value?.avatar_type ?? null,
  email: account.value?.email ?? '',
  username: account.value?.username ?? '',
}))
const resetKey = computed(() => account.value?.id ?? null)
const selectedAvatarType = computed(
  () => avatarDialogSelection.value ?? profileInitialValues.value.avatarType,
)
const socialAccounts = computed(() => account.value?.social_accounts ?? [])
const needsLocalPasswordBeforeGoogleUnlink = computed(() =>
  socialAccounts.value.some(
    (socialAccount) => socialAccount.provider === 'google' && !socialAccount.can_unlink,
  ),
)

const queryErrorMessage = computed(() => {
  const error = currentAccount.error.value

  if (error instanceof ApiRequestError) {
    return error.message
  }

  if (error) {
    return 'Unable to load your profile. Try again in a moment.'
  }

  return ''
})

const updateErrorMessage = computed(() => {
  const error =
    updateAccountMutation.error.value ??
    linkGoogleMutation.error.value ??
    unlinkGoogleMutation.error.value

  if (error instanceof ApiRequestError) {
    return error.message
  }

  if (error) {
    return 'Unable to save profile changes. Review the fields and try again.'
  }

  return ''
})

const passwordSetupErrorMessage = computed(() => {
  const error = updatePasswordMutation.error.value

  if (error instanceof ApiRequestError) {
    return error.message
  }

  if (error) {
    return 'Unable to save this password. Review the fields and try again.'
  }

  return ''
})

async function saveProfile(payload: ProfileDetailsFormPayload) {
  successMessage.value = ''
  passwordSuccessMessage.value = ''
  updateAccountMutation.reset()
  updatePasswordMutation.reset()
  linkGoogleMutation.reset()
  unlinkGoogleMutation.reset()

  const updatedAccount = await updateAccountMutation.mutateAsync(payload).catch(() => null)

  if (!updatedAccount) {
    return
  }

  successMessage.value = 'Profile changes saved.'

  window.setTimeout(() => {
    successMessage.value = ''
  }, 2600)
}

async function setLocalPassword(payload: AccountPasswordPayload) {
  successMessage.value = ''
  passwordSuccessMessage.value = ''
  updateAccountMutation.reset()
  updatePasswordMutation.reset()
  linkGoogleMutation.reset()
  unlinkGoogleMutation.reset()

  await updatePasswordMutation.mutateAsync(payload).catch(() => null)

  if (updatePasswordMutation.isError.value) {
    return
  }

  successMessage.value = 'Local password saved. You can disconnect Google now.'

  window.setTimeout(() => {
    successMessage.value = ''
  }, 3600)
}

async function savePassword(payload: AccountPasswordPayload) {
  successMessage.value = ''
  passwordSuccessMessage.value = ''
  updateAccountMutation.reset()
  updatePasswordMutation.reset()
  linkGoogleMutation.reset()
  unlinkGoogleMutation.reset()

  await updatePasswordMutation.mutateAsync(payload).catch(() => null)

  if (updatePasswordMutation.isError.value) {
    return
  }

  passwordSuccessMessage.value = 'Password saved.'

  window.setTimeout(() => {
    passwordSuccessMessage.value = ''
  }, 3600)
}

async function linkGoogleAccount(payload: AccountGoogleSocialAccountPayload) {
  successMessage.value = ''
  passwordSuccessMessage.value = ''
  updateAccountMutation.reset()
  updatePasswordMutation.reset()
  linkGoogleMutation.reset()
  unlinkGoogleMutation.reset()

  await linkGoogleMutation.mutateAsync(payload).catch(() => null)

  if (linkGoogleMutation.isError.value) {
    return
  }

  successMessage.value = 'Google account connected.'

  window.setTimeout(() => {
    successMessage.value = ''
  }, 2600)
}

async function unlinkGoogleAccount() {
  successMessage.value = ''
  updateAccountMutation.reset()
  linkGoogleMutation.reset()
  unlinkGoogleMutation.reset()

  await unlinkGoogleMutation.mutateAsync().catch(() => null)

  if (unlinkGoogleMutation.isError.value) {
    return
  }

  successMessage.value = 'Google account disconnected.'

  window.setTimeout(() => {
    successMessage.value = ''
  }, 2600)
}

function selectAvatar(avatarType: string) {
  profileFormRef.value?.setAvatarType(avatarType)
  avatarDialogSelection.value = avatarType
  isAvatarDialogOpen.value = false
}

function openAvatarDialog() {
  avatarDialogSelection.value =
    profileFormRef.value?.getAvatarType() ?? profileInitialValues.value.avatarType
  isAvatarDialogOpen.value = true
}
</script>

<template>
  <DashboardLayout>
    <div class="mx-auto flex w-full max-w-5xl flex-col gap-5">
      <p
        v-if="queryErrorMessage"
        class="rounded-2xl border border-red-100 bg-red-50 px-4 py-3 text-sm leading-5 font-medium text-red-700"
        role="alert"
      >
        {{ queryErrorMessage }}
      </p>

      <template v-else>
        <ProfileDetailsForm
          ref="profileFormRef"
          :error-message="updateErrorMessage"
          :initial-values="profileInitialValues"
          :is-loading="currentAccount.isLoading.value"
          :is-linking-google="linkGoogleMutation.isPending.value"
          :is-pending="updateAccountMutation.isPending.value"
          :is-setting-local-password="updatePasswordMutation.isPending.value"
          :is-unlinking-google="unlinkGoogleMutation.isPending.value"
          :password-setup-error-message="passwordSetupErrorMessage"
          :reset-key="resetKey"
          :social-accounts="socialAccounts"
          :success-message="successMessage"
          @link-google-account="linkGoogleAccount"
          @open-avatar-dialog="openAvatarDialog"
          @set-local-password="setLocalPassword"
          @unlink-google-account="unlinkGoogleAccount"
          @submit="saveProfile"
        />

        <SecurityPasswordCard
          :error-message="passwordSetupErrorMessage"
          :is-pending="updatePasswordMutation.isPending.value"
          :requires-current-password="!needsLocalPasswordBeforeGoogleUnlink"
          :success-message="passwordSuccessMessage"
          @submit="savePassword"
        />
      </template>
    </div>

    <AvatarPickerDialog
      :is-open="isAvatarDialogOpen"
      :selected-avatar-type="selectedAvatarType"
      @close="isAvatarDialogOpen = false"
      @select="selectAvatar"
    />
  </DashboardLayout>
</template>
