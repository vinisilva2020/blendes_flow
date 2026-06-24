<script setup lang="ts">
import { BadgeCheck, Clock3, Mail, MapPin } from '@lucide/vue'

import googleIcon from '@/assets/img/google.svg'

const profileForm = {
  company: 'Blendes Studio',
  email: 'vinicius@blendes.co',
  fullName: 'Vinicius Marques',
  language: 'Portuguese (Brazil)',
  phone: '+55 11 98888-2042',
  role: 'Workspace administrator',
  timezone: 'America/Sao_Paulo',
  username: 'vinicius',
}

const accountFields = [
  {
    autocomplete: 'name',
    description: 'Shown on your profile and invites.',
    id: 'profile-full-name',
    label: 'Full name',
    model: profileForm.fullName,
    readonly: false,
    type: 'text',
  },
  {
    autocomplete: 'username',
    description: 'Used in mentions and activity logs.',
    id: 'profile-username',
    label: 'Username',
    model: profileForm.username,
    readonly: false,
    type: 'text',
  },
  {
    autocomplete: 'email',
    description: 'Login, alerts, and recovery.',
    id: 'profile-email',
    label: 'Email',
    model: profileForm.email,
    readonly: false,
    type: 'email',
  },
  {
    autocomplete: 'tel',
    description: 'Contact for critical alerts.',
    id: 'profile-phone',
    label: 'Phone',
    model: profileForm.phone,
    readonly: false,
    type: 'tel',
  },
  {
    autocomplete: 'organization',
    description: 'Managed by the workspace.',
    id: 'profile-company',
    label: 'Company',
    model: profileForm.company,
    readonly: true,
    type: 'text',
  },
  {
    autocomplete: 'organization-title',
    description: 'Managed by workspace admins.',
    id: 'profile-role',
    label: 'Role',
    model: profileForm.role,
    readonly: true,
    type: 'text',
  },
]

const preferenceFields = [
  {
    description: 'Sets the default language for screens, notifications, and system messages.',
    id: 'profile-language',
    label: 'Language',
    model: profileForm.language,
  },
  {
    description: 'Used for session times, audit logs, and activity alerts.',
    id: 'profile-timezone',
    label: 'Time zone',
    model: profileForm.timezone,
  },
]
</script>

<template>
  <div class="profile-grid">
    <form class="profile-stack" @submit.prevent>
      <article class="profile-card account-card">
        <div class="card-heading">
          <div>
            <p>Account information</p>
            <h3>Main details</h3>
          </div>

          <span class="card-badge">
            <BadgeCheck :size="14" :stroke-width="2.4" aria-hidden="true" />
            Verified
          </span>
        </div>

        <div class="field-grid">
          <label
            v-for="field in accountFields"
            :key="field.id"
            class="profile-field"
            :class="{ 'is-readonly': field.readonly }"
          >
            <span class="field-copy">
              <strong>{{ field.label }}</strong>
              <small>{{ field.description }}</small>
            </span>

            <input
              :id="field.id"
              :value="field.model"
              :type="field.type"
              :autocomplete="field.autocomplete"
              :readonly="field.readonly"
              :aria-readonly="field.readonly"
            />
          </label>
        </div>
      </article>

      <article class="profile-card">
        <div class="card-heading">
          <div>
            <p>Social accounts</p>
            <h3>Connected integrations</h3>
          </div>
        </div>

        <div class="social-account-row">
          <span class="social-provider-icon" aria-hidden="true">
            <img :src="googleIcon" alt="" />
          </span>

          <span class="field-copy">
            <strong>Google</strong>
            <small>Use your Google account to make access to Blendes Flow faster.</small>
          </span>

          <button class="secondary-button social-connect-button" type="button">
            Connect Google
          </button>
        </div>
      </article>

      <article class="profile-card">
        <div class="card-heading">
          <div>
            <p>Preferences</p>
            <h3>Location and language</h3>
          </div>
        </div>

        <div class="field-grid is-compact">
          <label v-for="field in preferenceFields" :key="field.id" class="profile-field">
            <span class="field-copy">
              <strong>{{ field.label }}</strong>
              <small>{{ field.description }}</small>
            </span>

            <select :id="field.id" :value="field.model">
              <option>{{ field.model }}</option>
            </select>
          </label>
        </div>
      </article>

      <div class="form-actions">
        <button class="secondary-button" type="button">Discard</button>
        <button class="primary-button" type="submit">Save changes</button>
      </div>
    </form>

    <aside class="profile-side-panel" aria-label="Profile summary">
      <div class="side-panel-topline"></div>
      <p class="side-label">Summary</p>
      <h3>{{ profileForm.fullName }}</h3>
      <p>Workspace administrator with full access to members, flows, and security settings.</p>

      <div class="summary-list">
        <span>
          <Mail :size="15" :stroke-width="2.35" aria-hidden="true" />
          {{ profileForm.email }}
        </span>
        <span>
          <MapPin :size="15" :stroke-width="2.35" aria-hidden="true" />
          {{ profileForm.timezone }}
        </span>
        <span>
          <Clock3 :size="15" :stroke-width="2.35" aria-hidden="true" />
          Member since Jun 2026
        </span>
      </div>
    </aside>
  </div>
</template>
