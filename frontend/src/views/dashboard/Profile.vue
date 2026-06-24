<script setup lang="ts">
import { shallowRef } from 'vue'
import { ShieldCheck, UserRound } from '@lucide/vue'

import ProfileAccountForm from './components/ProfileAccountForm.vue'
import ProfileSecurityForm from './components/ProfileSecurityForm.vue'

type ProfileTab = 'account' | 'security'

const activeTab = shallowRef<ProfileTab>('account')

const tabs = [
  {
    description: 'Personal details and contact preferences.',
    icon: UserRound,
    id: 'account',
    label: 'Account',
  },
  {
    description: 'Password, recovery, sessions, and devices.',
    icon: ShieldCheck,
    id: 'security',
    label: 'Security',
  },
] satisfies Array<{
  description: string
  icon: typeof UserRound
  id: ProfileTab
  label: string
}>

</script>

<template>
  <section class="dashboard-page" aria-labelledby="profile-title">
    <div class="profile-shell">
      <header class="profile-hero">
        <div class="profile-identity">
          <span class="profile-avatar" aria-hidden="true">VM</span>

          <div>
            <p class="profile-kicker">Account center</p>
            <h2 id="profile-title">Profile management</h2>
            <p>
              Review your details, adjust preferences, and check how your account is protected.
            </p>
          </div>
        </div>

        <div class="profile-status-card" aria-label="Account status">
          <span class="status-orbit" aria-hidden="true">
            <ShieldCheck :size="24" :stroke-width="2.25" />
          </span>
          <div>
            <strong>Verified account</strong>
            <small>Last security review 8 days ago</small>
          </div>
        </div>
      </header>

      <div class="profile-tabs" role="tablist" aria-label="Profile sections">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          :id="`profile-tab-${tab.id}`"
          class="profile-tab"
          :class="{ 'is-active': activeTab === tab.id }"
          type="button"
          role="tab"
          :aria-selected="activeTab === tab.id"
          :aria-controls="`profile-panel-${tab.id}`"
          @click="activeTab = tab.id"
        >
          <component :is="tab.icon" :size="17" :stroke-width="2.25" aria-hidden="true" />
          <span>
            <strong>{{ tab.label }}</strong>
            <small>{{ tab.description }}</small>
          </span>
        </button>
      </div>

      <Transition mode="out-in" name="profile-panel">
        <ProfileAccountForm
          v-if="activeTab === 'account'"
          id="profile-panel-account"
          key="account"
          role="tabpanel"
          aria-labelledby="profile-tab-account"
        />

        <ProfileSecurityForm
          v-else
          id="profile-panel-security"
          key="security"
          role="tabpanel"
          aria-labelledby="profile-tab-security"
        />
      </Transition>
    </div>
  </section>
</template>

<style>
.dashboard-page {
  --profile-ink: #172224;
  --profile-muted: #667b80;
  --profile-soft: #eef8fa;
  --profile-line: rgb(18 33 36 / 11%);
  --profile-accent: #34cbbf;
  --profile-accent-deep: #0f5753;
  --profile-amber: #f2b84b;

  min-width: 0;
  padding: 28px 30px 36px;
  color: var(--profile-ink);
}

.profile-shell {
  display: grid;
  gap: 18px;
  width: min(100%, 1280px);
}

.profile-hero,
.profile-tabs,
.profile-card,
.profile-side-panel {
  border: 1px solid var(--profile-line);
  background: rgb(255 255 255 / 88%);
  box-shadow:
    0 18px 42px rgb(18 33 36 / 5%),
    inset 0 1px 0 rgb(255 255 255 / 86%);
}

.profile-hero {
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  gap: 18px;
  padding: 18px;
  overflow: hidden;
  border-radius: 12px;
}

.profile-identity {
  display: flex;
  align-items: center;
  gap: 16px;
  min-width: 0;
}

.profile-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  flex: 0 0 64px;
  color: #ffffff;
  font-size: 1rem;
  font-weight: 950;
  line-height: 1;
  background:
    radial-gradient(circle at 74% 20%, #aeeeff 0 12%, transparent 13%),
    linear-gradient(145deg, #0d5d67, #34cbbf 54%, #f2b84b);
  border: 4px solid #ffffff;
  border-radius: 18px;
  box-shadow:
    0 18px 34px rgb(15 87 83 / 18%),
    0 0 0 1px #dbe8eb;
}

.profile-kicker,
.card-heading p,
.side-label {
  margin: 0;
  color: #246b78;
  font-size: 0.68rem;
  font-weight: 950;
  letter-spacing: 0.1em;
  line-height: 1;
  text-transform: uppercase;
}

.profile-identity h2,
.profile-side-panel h3 {
  margin: 6px 0 0;
  color: var(--profile-ink);
  font-size: clamp(1.35rem, 2.1vw, 1.9rem);
  font-weight: 950;
  letter-spacing: 0;
  line-height: 1.08;
}

.profile-identity p:not(.profile-kicker),
.profile-side-panel p {
  max-width: 620px;
  margin: 7px 0 0;
  color: var(--profile-muted);
  font-size: 0.86rem;
  font-weight: 700;
  line-height: 1.55;
}

.profile-status-card {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  align-items: center;
  gap: 12px;
  min-width: 260px;
  padding: 12px 14px;
  background: linear-gradient(135deg, #f6fbfc, #ffffff 72%);
  border: 1px solid #dce9ec;
  border-radius: 10px;
}

.status-orbit {
  display: inline-grid;
  place-items: center;
  width: 44px;
  height: 44px;
  color: var(--profile-accent-deep);
  background: #e7fbf8;
  border-radius: 999px;
  box-shadow:
    inset 0 0 0 1px #c9f0eb,
    0 12px 28px rgb(15 87 83 / 10%);
}

.profile-status-card strong,
.profile-status-card small {
  display: block;
}

.profile-status-card strong {
  font-size: 0.84rem;
  font-weight: 950;
  line-height: 1.2;
}

.profile-status-card small {
  margin-top: 4px;
  color: var(--profile-muted);
  font-size: 0.72rem;
  font-weight: 750;
  line-height: 1.35;
}

.profile-tabs {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  padding: 8px;
  border-radius: 12px;
}

.profile-tab {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  align-items: center;
  gap: 10px;
  min-width: 0;
  padding: 11px 12px;
  color: #526970;
  text-align: left;
  background: transparent;
  border: 0;
  border-radius: 8px;
  cursor: pointer;
  transition:
    color 180ms ease,
    background 180ms ease,
    box-shadow 180ms ease,
    transform 180ms ease;
}

.profile-tab strong,
.profile-tab small {
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.profile-tab strong {
  color: inherit;
  font-size: 0.8rem;
  font-weight: 950;
  line-height: 1.15;
}

.profile-tab small {
  margin-top: 3px;
  color: #789096;
  font-size: 0.68rem;
  font-weight: 750;
  line-height: 1.2;
}

.profile-tab:hover,
.profile-tab:focus-visible {
  color: var(--profile-ink);
  background: #f3fafb;
}

.profile-tab.is-active {
  color: var(--profile-accent-deep);
  background: linear-gradient(180deg, #eefafa, #e6f3f5);
  box-shadow:
    inset 0 0 0 1px rgb(52 203 191 / 18%),
    0 12px 24px rgb(18 33 36 / 5%);
}

.profile-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(240px, 284px);
  align-items: start;
  gap: 18px;
}

.profile-stack {
  display: grid;
  gap: 16px;
}

.profile-card,
.profile-side-panel {
  border-radius: 12px;
}

.profile-card {
  padding: 18px;
}

.account-card {
  padding: 22px;
}

.card-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 16px;
}

.card-heading h3 {
  margin: 6px 0 0;
  color: var(--profile-ink);
  font-size: 1.02rem;
  font-weight: 950;
  line-height: 1.2;
}

.card-badge,
.current-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 28px;
  padding: 0 10px;
  color: var(--profile-accent-deep);
  font-size: 0.68rem;
  font-weight: 950;
  line-height: 1;
  white-space: nowrap;
  background: #e9fbf7;
  border: 1px solid #ccefed;
  border-radius: 999px;
}

.inline-link,
.secondary-button,
.primary-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 38px;
  padding: 0 13px;
  font-size: 0.76rem;
  font-weight: 950;
  line-height: 1;
  text-decoration: none;
  border-radius: 8px;
  transition:
    border-color 180ms ease,
    background 180ms ease,
    box-shadow 180ms ease,
    color 180ms ease,
    transform 180ms ease;
}

.inline-link {
  color: #246b78;
  background: #f3fafb;
}

.field-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.field-grid.is-compact,
.field-grid.is-single {
  grid-template-columns: minmax(0, 1fr);
}

.profile-field {
  display: grid;
  grid-template-columns: minmax(150px, 0.78fr) minmax(180px, 1fr);
  align-items: center;
  gap: 16px;
  min-width: 0;
  padding: 14px;
  background: #fbfeff;
  border: 1px solid #e2ecef;
  border-radius: 10px;
}

.account-card .field-grid {
  grid-template-columns: minmax(0, 1fr);
  gap: 12px;
}

.account-card .profile-field {
  grid-template-columns: minmax(180px, 0.46fr) minmax(280px, 1fr);
  align-items: center;
  padding: 14px;
}

.account-card .field-copy {
  padding-top: 0;
}

.social-account-row {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 14px;
  min-width: 0;
  padding: 14px;
  background: #fbfeff;
  border: 1px solid #e2ecef;
  border-radius: 10px;
}

.social-provider-icon {
  display: inline-grid;
  place-items: center;
  width: 42px;
  height: 42px;
  background: #ffffff;
  border: 1px solid #d8e6e9;
  border-radius: 10px;
  box-shadow:
    0 8px 18px rgb(18 33 36 / 4%),
    inset 0 1px 0 rgb(255 255 255 / 92%);
}

.social-provider-icon img {
  display: block;
  width: 19px;
  height: 19px;
}

.social-connect-button {
  min-width: 138px;
}

.field-copy {
  min-width: 0;
}

.field-copy strong,
.field-copy small {
  display: block;
}

.field-copy strong {
  color: var(--profile-ink);
  font-size: 0.77rem;
  font-weight: 950;
  line-height: 1.2;
}

.field-copy small {
  margin-top: 5px;
  color: #70868b;
  font-size: 0.68rem;
  font-weight: 700;
  line-height: 1.45;
}

.profile-field input,
.profile-field select {
  box-sizing: border-box;
  width: 100%;
  min-width: 0;
  min-height: 38px;
  padding: 0 11px;
  color: var(--profile-ink);
  font-size: 0.78rem;
  font-weight: 800;
  background: #ffffff;
  border: 1px solid #d8e6e9;
  border-radius: 8px;
  outline: 0;
  box-shadow:
    0 8px 18px rgb(18 33 36 / 4%),
    inset 0 1px 0 rgb(255 255 255 / 92%);
  transition:
    border-color 180ms ease,
    box-shadow 180ms ease;
}

.profile-field input::placeholder {
  color: #9cafb4;
}

.profile-field.is-readonly input {
  color: #5f7378;
  cursor: default;
  background:
    linear-gradient(180deg, rgb(246 251 252 / 92%), rgb(239 248 250 / 86%)),
    #f6fbfc;
  border-color: #dce8eb;
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 88%),
    inset 0 0 0 1px rgb(18 33 36 / 2%);
}

.profile-field input:focus,
.profile-field select:focus {
  border-color: #8adff3;
  box-shadow:
    0 0 0 4px rgb(174 238 255 / 26%),
    0 10px 24px rgb(18 33 36 / 7%);
}

.profile-field.is-readonly input:focus {
  border-color: #dce8eb;
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 88%),
    inset 0 0 0 1px rgb(18 33 36 / 2%);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 9px;
}

.secondary-button {
  color: #4d6267;
  background: #ffffff;
  border: 1px solid #d8e6e9;
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 92%),
    0 10px 22px rgb(18 33 36 / 5%);
}

.primary-button {
  color: #ffffff;
  background: var(--profile-accent-deep);
  border: 1px solid #0f5753;
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 22%),
    0 15px 28px rgb(15 87 83 / 18%);
}

.secondary-button:hover,
.secondary-button:focus-visible,
.inline-link:hover,
.inline-link:focus-visible {
  color: var(--profile-ink);
  background: #f7fcfd;
  border-color: #c8dce0;
}

.primary-button:hover,
.primary-button:focus-visible {
  background: #0b4946;
  transform: translateY(-1px);
}

.secondary-button:active,
.primary-button:active,
.profile-tab:active,
.session-meta button:active {
  transform: scale(0.98);
}

.secondary-button:focus-visible,
.primary-button:focus-visible,
.inline-link:focus-visible,
.profile-tab:focus-visible,
.session-meta button:focus-visible {
  outline: 3px solid rgb(52 203 191 / 28%);
  outline-offset: 2px;
}

.as-link {
  box-sizing: border-box;
}

.profile-side-panel {
  position: sticky;
  top: 88px;
  padding: 18px;
  overflow: hidden;
}

.profile-side-panel::before {
  position: absolute;
  right: -34px;
  bottom: -40px;
  width: 146px;
  height: 146px;
  content: '';
  background:
    radial-gradient(circle, rgb(52 203 191 / 22%) 0 34%, transparent 35%),
    conic-gradient(from 120deg, rgb(52 203 191 / 20%), rgb(242 184 75 / 18%), transparent);
  border-radius: 999px;
}

.side-panel-topline {
  width: 52px;
  height: 4px;
  margin-bottom: 18px;
  background: linear-gradient(90deg, var(--profile-accent), var(--profile-amber));
  border-radius: 999px;
}

.summary-list {
  display: grid;
  gap: 10px;
  margin-top: 18px;
}

.summary-list span {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  align-items: center;
  gap: 9px;
  min-width: 0;
  color: #4f666c;
  font-size: 0.72rem;
  font-weight: 850;
  line-height: 1.35;
}

.summary-list svg {
  color: #246b78;
}

.security-meter {
  display: grid;
  grid-template-columns: 1.1fr 1fr 0.72fr;
  gap: 6px;
  margin-top: 18px;
}

.security-meter span {
  height: 8px;
  background: var(--profile-accent);
  border-radius: 999px;
  box-shadow: 0 0 18px rgb(52 203 191 / 22%);
}

.security-meter span:nth-child(2) {
  background: #8adff3;
}

.security-meter span:nth-child(3) {
  background: var(--profile-amber);
}

.session-list {
  display: grid;
  gap: 10px;
}

.session-card {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 12px;
  padding: 13px;
  background: #fbfeff;
  border: 1px solid #e2ecef;
  border-radius: 10px;
}

.session-card.is-current {
  background: linear-gradient(180deg, #f3fdfb, #ffffff);
  border-color: #ccefed;
}

.session-icon {
  display: inline-grid;
  place-items: center;
  width: 38px;
  height: 38px;
  color: #246b78;
  background: #eef8fa;
  border: 1px solid #d8e6e9;
  border-radius: 10px;
}

.session-copy {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.session-copy strong,
.session-copy small,
.session-copy span {
  display: block;
}

.session-copy strong {
  color: var(--profile-ink);
  font-size: 0.8rem;
  font-weight: 950;
  line-height: 1.2;
}

.session-copy small,
.session-copy span,
.session-meta > span {
  color: #70868b;
  font-size: 0.69rem;
  font-weight: 800;
  line-height: 1.35;
}

.session-copy small {
  margin-top: 4px;
}

.session-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.session-meta button {
  display: inline-grid;
  place-items: center;
  width: 32px;
  height: 32px;
  color: #647b80;
  background: #ffffff;
  border: 1px solid #d8e6e9;
  border-radius: 8px;
  cursor: pointer;
  transition:
    color 180ms ease,
    border-color 180ms ease,
    transform 180ms ease;
}

.session-meta button:hover {
  color: var(--profile-ink);
  border-color: #bad7dc;
}

.profile-panel-enter-active,
.profile-panel-leave-active {
  transition:
    opacity 180ms ease,
    transform 180ms ease;
}

.profile-panel-enter-from,
.profile-panel-leave-to {
  opacity: 0;
  transform: translateY(6px);
}

@media (prefers-reduced-motion: reduce) {
  .profile-tab,
  .inline-link,
  .secondary-button,
  .primary-button,
  .session-meta button,
  .profile-panel-enter-active,
  .profile-panel-leave-active {
    transition: none;
  }

  .profile-panel-enter-from,
  .profile-panel-leave-to {
    transform: none;
  }
}

@media (max-width: 1120px) {
  .profile-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .profile-side-panel {
    position: relative;
    top: auto;
  }
}

@media (max-width: 920px) {
  .profile-hero {
    flex-direction: column;
  }

  .profile-status-card {
    min-width: 0;
  }

  .field-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .account-card .field-grid {
    grid-template-columns: minmax(0, 1fr);
  }
}

@media (max-width: 760px) {
  .dashboard-page {
    padding: 20px 16px 28px;
  }

  .profile-tabs {
    grid-template-columns: minmax(0, 1fr);
  }

  .profile-field,
  .account-card .profile-field,
  .social-account-row,
  .session-card,
  .session-copy {
    grid-template-columns: minmax(0, 1fr);
  }

  .social-connect-button {
    width: 100%;
  }

  .account-card .field-copy {
    padding-top: 0;
  }

  .session-meta {
    justify-content: space-between;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .secondary-button,
  .primary-button {
    width: 100%;
  }
}

@media (max-width: 520px) {
  .profile-identity {
    align-items: flex-start;
  }

  .profile-avatar {
    width: 52px;
    height: 52px;
    flex-basis: 52px;
    border-radius: 16px;
  }

  .card-heading {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
