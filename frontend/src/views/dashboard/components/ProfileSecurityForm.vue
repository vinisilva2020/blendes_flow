<script setup lang="ts">
import { shallowRef } from 'vue'
import {
  ArrowRight,
  CheckCircle2,
  ChevronRight,
  KeyRound,
  Laptop,
  LockKeyhole,
  MonitorSmartphone,
  Smartphone,
} from '@lucide/vue'

type SessionDevice = {
  browser: string
  device: string
  icon: typeof Laptop
  id: number
  ipAddress: string
  isCurrent: boolean
  lastSeen: string
  location: string
}

const passwordForm = shallowRef({
  confirmPassword: '',
  currentPassword: '',
  newPassword: '',
})

const activeSessions: SessionDevice[] = [
  {
    browser: 'Chrome 126',
    device: 'Windows desktop',
    icon: Laptop,
    id: 1,
    ipAddress: '189.44.102.18',
    isCurrent: true,
    lastSeen: 'Now',
    location: 'Sao Paulo, BR',
  },
  {
    browser: 'Safari 18',
    device: 'iPhone 15',
    icon: Smartphone,
    id: 2,
    ipAddress: '179.83.18.64',
    isCurrent: false,
    lastSeen: '42 min ago',
    location: 'Campinas, BR',
  },
  {
    browser: 'Edge 126',
    device: 'Windows laptop',
    icon: MonitorSmartphone,
    id: 3,
    ipAddress: '201.17.44.90',
    isCurrent: false,
    lastSeen: 'Yesterday, 18:12',
    location: 'Rio de Janeiro, BR',
  },
]
</script>

<template>
  <div class="profile-grid">
    <form class="profile-stack" @submit.prevent>
      <article class="profile-card">
        <div class="card-heading">
          <div>
            <p>Password change</p>
            <h3>Confirm your current password</h3>
          </div>

          <RouterLink class="inline-link" to="/forgot-password">
            Recover password
            <ArrowRight :size="14" :stroke-width="2.5" aria-hidden="true" />
          </RouterLink>
        </div>

        <div class="field-grid is-single">
          <label class="profile-field">
            <span class="field-copy">
              <strong>Current password</strong>
              <small>Required to confirm this request came from you.</small>
            </span>

            <input
              v-model="passwordForm.currentPassword"
              type="password"
              autocomplete="current-password"
              placeholder="Enter current password"
            />
          </label>

          <label class="profile-field">
            <span class="field-copy">
              <strong>New password</strong>
              <small>Use a unique password with letters, numbers, and symbols.</small>
            </span>

            <input
              v-model="passwordForm.newPassword"
              type="password"
              autocomplete="new-password"
              placeholder="Create new password"
            />
          </label>

          <label class="profile-field">
            <span class="field-copy">
              <strong>Confirm new password</strong>
              <small>Repeat the new password to avoid typing errors.</small>
            </span>

            <input
              v-model="passwordForm.confirmPassword"
              type="password"
              autocomplete="new-password"
              placeholder="Repeat new password"
            />
          </label>
        </div>

        <div class="form-actions">
          <RouterLink class="secondary-button as-link" to="/forgot-password">
            I forgot my password
          </RouterLink>
          <button class="primary-button" type="submit">Request change</button>
        </div>
      </article>

      <article class="profile-card">
        <div class="card-heading">
          <div>
            <p>Active sessions</p>
            <h3>Connected devices</h3>
          </div>
        </div>

        <div class="session-list">
          <article
            v-for="session in activeSessions"
            :key="session.id"
            class="session-card"
            :class="{ 'is-current': session.isCurrent }"
          >
            <span class="session-icon" aria-hidden="true">
              <component :is="session.icon" :size="18" :stroke-width="2.25" />
            </span>

            <div class="session-copy">
              <div>
                <strong>{{ session.device }}</strong>
                <small>{{ session.browser }} - {{ session.ipAddress }}</small>
              </div>
              <span>{{ session.location }}</span>
            </div>

            <div class="session-meta">
              <span v-if="session.isCurrent" class="current-pill">
                <CheckCircle2 :size="13" :stroke-width="2.5" aria-hidden="true" />
                Current
              </span>
              <span v-else>{{ session.lastSeen }}</span>
              <button type="button" :aria-label="`Manage ${session.device}`">
                <ChevronRight :size="16" :stroke-width="2.4" aria-hidden="true" />
              </button>
            </div>
          </article>
        </div>
      </article>
    </form>

    <aside class="profile-side-panel" aria-label="Security summary">
      <div class="side-panel-topline"></div>
      <p class="side-label">Security posture</p>
      <h3>Security</h3>
      <p>
        Your current password protects sensitive changes. If you lose access, use email recovery.
      </p>

      <div class="security-meter" aria-hidden="true">
        <span></span>
        <span></span>
        <span></span>
      </div>

      <div class="summary-list">
        <span>
          <LockKeyhole :size="15" :stroke-width="2.35" aria-hidden="true" />
          Password protected
        </span>
        <span>
          <KeyRound :size="15" :stroke-width="2.35" aria-hidden="true" />
          Recovery available
        </span>
        <span>
          <MonitorSmartphone :size="15" :stroke-width="2.35" aria-hidden="true" />
          {{ activeSessions.length }} active devices
        </span>
      </div>
    </aside>
  </div>
</template>
