<script setup lang="ts">
import { computed, shallowRef, type Component } from 'vue'
import {
  CheckCircle2,
  CircleDot,
  Crown,
  List,
  Mail,
  MoreHorizontal,
  Search,
  Send,
  Table2,
  UserPlus,
  UsersRound,
  X,
} from '@lucide/vue'

import MembersTable from './components/MembersTable.vue'
import type { OrganizationMember } from './components/members'

type ViewMode = 'table' | 'list'

type InviteCandidate = {
  email: string
  id: number
  initials: string
  name: string
  username: string
}

const viewMode = shallowRef<ViewMode>('table')
const isInviteDialogOpen = shallowRef(false)
const memberSearch = shallowRef('')
const inviteQuery = shallowRef('')
const selectedCandidate = shallowRef<InviteCandidate | null>(null)

const members: OrganizationMember[] = [
  {
    email: 'vinicius@blendes.co',
    id: 1,
    initials: 'VM',
    joinedAt: 'Jun 4, 2026',
    lastActive: 'Now',
    name: 'Vinicius Marques',
    role: 'Admin',
    status: 'active',
    team: 'Operations',
    username: 'vinicius',
  },
  {
    email: 'marina@blendes.co',
    id: 2,
    initials: 'MA',
    joinedAt: 'Jun 8, 2026',
    lastActive: '18 min ago',
    name: 'Marina Alves',
    role: 'Manager',
    status: 'active',
    team: 'Design',
    username: 'marina',
  },
  {
    email: 'rafael@blendes.co',
    id: 3,
    initials: 'RS',
    joinedAt: 'Jun 12, 2026',
    lastActive: 'Yesterday',
    name: 'Rafael Souza',
    role: 'Member',
    status: 'active',
    team: 'Automation',
    username: 'rafael',
  },
  {
    email: 'bianca@blendes.co',
    id: 4,
    initials: 'BL',
    joinedAt: 'Invited Jun 20',
    lastActive: 'Waiting invite',
    name: 'Bianca Lima',
    role: 'Member',
    status: 'pending',
    team: 'Analytics',
    username: 'bianca',
  },
  {
    email: 'thiago@blendes.co',
    id: 5,
    initials: 'TR',
    joinedAt: 'Jun 16, 2026',
    lastActive: '2 hours ago',
    name: 'Thiago Rocha',
    role: 'Manager',
    status: 'active',
    team: 'Customer success',
    username: 'thiago',
  },
]

const inviteCandidates: InviteCandidate[] = [
  {
    email: 'ana.carvalho@blendes.co',
    id: 101,
    initials: 'AC',
    name: 'Ana Carvalho',
    username: 'ana.carvalho',
  },
  {
    email: 'joao.mendes@blendes.co',
    id: 102,
    initials: 'JM',
    name: 'Joao Mendes',
    username: 'joao.mendes',
  },
  {
    email: 'laura.pires@blendes.co',
    id: 103,
    initials: 'LP',
    name: 'Laura Pires',
    username: 'laura.pires',
  },
]

const viewOptions = [
  { icon: Table2, id: 'table', label: 'Table' },
  { icon: List, id: 'list', label: 'List' },
] satisfies Array<{ icon: Component; id: ViewMode; label: string }>

const activeMembers = computed(() => members.filter((member) => member.status === 'active').length)
const pendingMembers = computed(
  () => members.filter((member) => member.status === 'pending').length,
)
const adminMembers = computed(() => members.filter((member) => member.role === 'Admin').length)

const filteredMembers = computed(() => {
  const query = memberSearch.value.trim().toLowerCase()

  return members.filter(
    (member) =>
      !query ||
      [member.name, member.email, member.username, member.team, member.role].some((value) =>
        value.toLowerCase().includes(query),
      ),
  )
})

const visibleCandidates = computed(() => {
  const query = inviteQuery.value.trim().toLowerCase()

  if (!query) {
    return inviteCandidates
  }

  return inviteCandidates.filter((candidate) =>
    [candidate.name, candidate.email, candidate.username].some((value) =>
      value.toLowerCase().includes(query),
    ),
  )
})

const invitePreview = computed(() => {
  if (selectedCandidate.value) {
    return selectedCandidate.value.email
  }

  return inviteQuery.value.trim()
})

function openInviteDialog() {
  isInviteDialogOpen.value = true
  inviteQuery.value = ''
  selectedCandidate.value = null
}

function closeInviteDialog() {
  isInviteDialogOpen.value = false
}

function selectCandidate(candidate: InviteCandidate) {
  selectedCandidate.value = candidate
  inviteQuery.value = candidate.email
}

function submitInvite() {
  if (!invitePreview.value) {
    return
  }

  closeInviteDialog()
}
</script>

<template>
  <section class="dashboard-page members-page" aria-labelledby="members-title">
    <div class="members-shell">
      <header class="members-hero">
        <div class="members-title-block">
          <span class="members-emblem" aria-hidden="true">
            <UsersRound :size="24" :stroke-width="2.25" />
          </span>

          <div>
            <p class="members-kicker">Organization members</p>
            <h2 id="members-title">Members</h2>
            <p>
              Review who belongs to this workspace and invite the next collaborator without leaving
              the page.
            </p>
          </div>
        </div>

        <button class="members-primary-button" type="button" @click="openInviteDialog">
          <UserPlus :size="16" :stroke-width="2.45" aria-hidden="true" />
          Add member
        </button>
      </header>

      <div class="members-grid">
        <div class="members-main">
          <section class="members-toolbar" aria-label="Member controls">
            <label class="members-search">
              <Search :size="16" :stroke-width="2.35" aria-hidden="true" />
              <span class="sr-only">Search members</span>
              <input
                v-model="memberSearch"
                type="search"
                placeholder="Search by name, email, role, or team"
              />
            </label>

            <div class="view-switcher" aria-label="Choose member layout">
              <button
                v-for="option in viewOptions"
                :key="option.id"
                type="button"
                :aria-pressed="viewMode === option.id"
                :class="{ 'is-active': viewMode === option.id }"
                @click="viewMode = option.id"
              >
                <component :is="option.icon" :size="15" :stroke-width="2.35" aria-hidden="true" />
                <span>{{ option.label }}</span>
              </button>
            </div>
          </section>

          <section class="members-directory" aria-live="polite">
            <div class="directory-heading">
              <div>
                <p class="members-kicker">Directory</p>
                <h3>{{ filteredMembers.length }} visible members</h3>
              </div>
            </div>

            <MembersTable v-if="viewMode === 'table'" :members="filteredMembers" />

            <div v-else class="members-list">
              <article v-for="member in filteredMembers" :key="member.id" class="member-card">
                <div class="member-card-top">
                  <div class="member-identity">
                    <span class="member-avatar">{{ member.initials }}</span>
                    <span>
                      <strong>{{ member.name }}</strong>
                      <small>@{{ member.username }} - {{ member.email }}</small>
                    </span>
                  </div>

                  <button class="icon-action" type="button" :aria-label="`Manage ${member.name}`">
                    <MoreHorizontal :size="17" :stroke-width="2.4" aria-hidden="true" />
                  </button>
                </div>

                <div class="member-card-meta">
                  <span>{{ member.team }}</span>
                  <span>{{ member.joinedAt }}</span>
                  <span>{{ member.lastActive }}</span>
                </div>

                <div class="member-card-bottom">
                  <span class="role-pill" :class="`is-${member.role.toLowerCase()}`">
                    <Crown
                      v-if="member.role === 'Admin'"
                      :size="13"
                      :stroke-width="2.45"
                      aria-hidden="true"
                    />
                    {{ member.role }}
                  </span>

                  <span class="status-pill" :class="`is-${member.status}`">
                    <CircleDot :size="13" :stroke-width="2.6" aria-hidden="true" />
                    {{ member.status }}
                  </span>
                </div>
              </article>
            </div>
          </section>
        </div>

        <aside class="members-summary-panel" aria-label="Organization member summary">
          <div class="summary-topline"></div>
          <p class="members-kicker">Team roster</p>
          <h3>{{ members.length }} people</h3>
          <p>A compact view of members, roles, teams, and invite status.</p>

          <div class="members-stats">
            <span>
              <CheckCircle2 :size="13" :stroke-width="2.5" aria-hidden="true" />
              <strong>{{ activeMembers }}</strong>
              <small>Active</small>
            </span>
            <span>
              <CircleDot :size="13" :stroke-width="2.6" aria-hidden="true" />
              <strong>{{ pendingMembers }}</strong>
              <small>Pending</small>
            </span>
            <span>
              <Crown :size="13" :stroke-width="2.45" aria-hidden="true" />
              <strong>{{ adminMembers }}</strong>
              <small>Admins</small>
            </span>
          </div>
        </aside>
      </div>
    </div>

    <Teleport to="body">
      <Transition name="members-dialog">
        <div
          v-if="isInviteDialogOpen"
          class="members-dialog-backdrop"
          role="presentation"
          @click.self="closeInviteDialog"
        >
          <section
            class="members-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="invite-member-title"
          >
            <header class="dialog-header">
              <div>
                <p class="members-kicker">New collaborator</p>
                <h2 id="invite-member-title">Add member</h2>
              </div>

              <button
                class="icon-action"
                type="button"
                aria-label="Close dialog"
                @click="closeInviteDialog"
              >
                <X :size="17" :stroke-width="2.45" aria-hidden="true" />
              </button>
            </header>

            <label class="invite-search">
              <Search :size="17" :stroke-width="2.35" aria-hidden="true" />
              <span class="sr-only">Search by email or username</span>
              <input
                v-model="inviteQuery"
                type="search"
                autocomplete="off"
                placeholder="Search email or username"
              />
            </label>

            <div class="candidate-list">
              <button
                v-for="candidate in visibleCandidates"
                :key="candidate.id"
                type="button"
                class="candidate-row"
                :class="{ 'is-selected': selectedCandidate?.id === candidate.id }"
                @click="selectCandidate(candidate)"
              >
                <span class="member-avatar">{{ candidate.initials }}</span>
                <span>
                  <strong>{{ candidate.name }}</strong>
                  <small>@{{ candidate.username }} - {{ candidate.email }}</small>
                </span>
                <CheckCircle2
                  v-if="selectedCandidate?.id === candidate.id"
                  :size="17"
                  :stroke-width="2.45"
                  aria-hidden="true"
                />
              </button>
            </div>

            <div class="invite-preview">
              <Mail :size="17" :stroke-width="2.35" aria-hidden="true" />
              <span>{{
                invitePreview || 'Choose a profile or type an email to prepare the invite.'
              }}</span>
            </div>

            <footer class="dialog-actions">
              <button class="members-secondary-button" type="button" @click="closeInviteDialog">
                Cancel
              </button>
              <button class="members-primary-button" type="button" @click="submitInvite">
                <Send :size="15" :stroke-width="2.45" aria-hidden="true" />
                Send invite
              </button>
            </footer>
          </section>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<style scoped>
.members-page {
  --members-ink: #172224;
  --members-muted: #667b80;
  --members-soft: #eef8fa;
  --members-line: rgb(18 33 36 / 11%);
  --members-accent: #34cbbf;
  --members-accent-deep: #0f5753;
  --members-amber: #f2b84b;
  --members-rose: #d96666;

  min-width: 0;
  padding: 28px 30px 36px;
  color: var(--members-ink);
}

.members-shell {
  display: grid;
  gap: 18px;
  width: min(100%, 1280px);
}

.members-hero,
.members-summary-panel,
.members-toolbar,
.members-directory {
  border: 1px solid var(--members-line);
  background: rgb(255 255 255 / 88%);
  box-shadow:
    0 18px 42px rgb(18 33 36 / 5%),
    inset 0 1px 0 rgb(255 255 255 / 86%);
}

.members-hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 18px;
  border-radius: 12px;
}

.members-title-block,
.member-identity {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.members-emblem {
  display: inline-grid;
  place-items: center;
  width: 62px;
  height: 62px;
  flex: 0 0 62px;
  color: #ffffff;
  background:
    linear-gradient(135deg, rgb(255 255 255 / 18%), transparent 42%),
    linear-gradient(145deg, #0d5d67, #34cbbf 58%, #f2b84b);
  border: 4px solid #ffffff;
  border-radius: 18px;
  box-shadow:
    0 18px 34px rgb(15 87 83 / 18%),
    0 0 0 1px #dbe8eb;
}

.members-kicker {
  margin: 0;
  color: #246b78;
  font-size: 0.68rem;
  font-weight: 950;
  letter-spacing: 0.1em;
  line-height: 1;
  text-transform: uppercase;
}

.members-title-block h2,
.members-summary-panel h3,
.directory-heading h3,
.dialog-header h2 {
  margin: 6px 0 0;
  color: var(--members-ink);
  font-weight: 950;
  letter-spacing: 0;
  line-height: 1.08;
}

.members-title-block h2 {
  font-size: clamp(1.35rem, 2.1vw, 1.9rem);
}

.members-title-block p:not(.members-kicker),
.members-summary-panel p {
  max-width: 660px;
  margin: 7px 0 0;
  color: var(--members-muted);
  font-size: 0.86rem;
  font-weight: 700;
  line-height: 1.55;
}

.members-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(190px, 220px);
  align-items: start;
  gap: 18px;
}

.members-summary-panel {
  position: sticky;
  top: 88px;
  padding: 14px;
  overflow: hidden;
  border-radius: 12px;
}

.members-summary-panel::before {
  content: none;
}

.summary-topline {
  width: 34px;
  height: 3px;
  margin-bottom: 14px;
  background: var(--members-accent);
  border-radius: 999px;
}

.members-summary-panel h3 {
  font-size: 0.95rem;
}

.members-summary-panel p:not(.members-kicker) {
  font-size: 0.72rem;
  font-weight: 750;
  line-height: 1.45;
}

.members-stats {
  display: grid;
  gap: 7px;
  margin-top: 14px;
}

.members-stats span {
  display: grid;
  grid-template-columns: auto minmax(26px, auto) minmax(0, 1fr);
  align-items: center;
  gap: 8px;
  min-width: 0;
  min-height: 32px;
  padding: 0 9px;
  color: #657c82;
  font-weight: 850;
  background: #f7fcfd;
  border: 1px solid #dce9ec;
  border-radius: 8px;
}

.members-stats svg {
  color: #246b78;
}

.members-stats strong {
  color: var(--members-ink);
  font-size: 0.82rem;
  font-weight: 950;
  line-height: 1;
}

.members-stats small {
  min-width: 0;
  overflow: hidden;
  color: #70868b;
  font-size: 0.64rem;
  font-weight: 850;
  line-height: 1;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.members-main {
  display: grid;
  gap: 16px;
  min-width: 0;
}

.members-toolbar {
  display: grid;
  grid-template-columns: minmax(220px, 1fr) auto;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 12px;
}

.members-search,
.invite-search {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  align-items: center;
  gap: 9px;
  min-width: 0;
  min-height: 40px;
  padding: 0 12px;
  color: #789096;
  background: #fbfeff;
  border: 1px solid #d8e6e9;
  border-radius: 8px;
  box-shadow:
    0 8px 18px rgb(18 33 36 / 4%),
    inset 0 1px 0 rgb(255 255 255 / 92%);
}

.members-search input,
.invite-search input {
  width: 100%;
  min-width: 0;
  color: var(--members-ink);
  font-size: 0.78rem;
  font-weight: 800;
  background: transparent;
  border: 0;
  outline: 0;
}

.members-search input::placeholder,
.invite-search input::placeholder {
  color: #9cafb4;
}

.members-search:focus-within,
.invite-search:focus-within {
  border-color: #8adff3;
  box-shadow:
    0 0 0 4px rgb(174 238 255 / 26%),
    0 10px 24px rgb(18 33 36 / 7%);
}

.view-switcher {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px;
  background: #f3fafb;
  border: 1px solid #dce9ec;
  border-radius: 10px;
}

.view-switcher button,
.members-primary-button,
.members-secondary-button,
.icon-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: 0;
  cursor: pointer;
  transition:
    border-color 180ms ease,
    background 180ms ease,
    box-shadow 180ms ease,
    color 180ms ease,
    transform 180ms ease;
}

.view-switcher button {
  min-height: 30px;
  padding: 0 10px;
  color: #60777d;
  font-size: 0.7rem;
  font-weight: 950;
  background: transparent;
  border-radius: 7px;
}

.view-switcher span {
  line-height: 1;
}

.view-switcher button:hover,
.view-switcher button:focus-visible,
.view-switcher button.is-active {
  color: var(--members-accent-deep);
  background: #ffffff;
  box-shadow:
    0 8px 18px rgb(18 33 36 / 5%),
    inset 0 0 0 1px rgb(52 203 191 / 16%);
}

.members-primary-button,
.members-secondary-button {
  min-height: 38px;
  padding: 0 13px;
  font-size: 0.76rem;
  font-weight: 950;
  line-height: 1;
  border-radius: 8px;
}

.members-primary-button {
  color: #ffffff;
  background: var(--members-accent-deep);
  border: 1px solid #0f5753;
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 22%),
    0 15px 28px rgb(15 87 83 / 18%);
}

.members-secondary-button {
  color: #4d6267;
  background: #ffffff;
  border: 1px solid #d8e6e9;
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 92%),
    0 10px 22px rgb(18 33 36 / 5%);
}

.members-primary-button:hover,
.members-primary-button:focus-visible {
  background: #0b4946;
  transform: translateY(-1px);
}

.members-secondary-button:hover,
.members-secondary-button:focus-visible,
.icon-action:hover,
.icon-action:focus-visible {
  color: var(--members-ink);
  background: #f7fcfd;
  border-color: #c8dce0;
}

.members-directory {
  padding: 16px;
  overflow: hidden;
  border-radius: 12px;
}

.directory-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 14px;
}

.directory-heading h3,
.dialog-header h2 {
  font-size: 1.02rem;
}

.role-pill,
.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 28px;
  padding: 0 10px;
  font-size: 0.68rem;
  font-weight: 950;
  line-height: 1;
  white-space: nowrap;
  border-radius: 999px;
}

.member-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  flex: 0 0 42px;
  color: #ffffff;
  font-size: 0.74rem;
  font-weight: 950;
  line-height: 1;
  background: linear-gradient(145deg, #0d5d67, #34cbbf 62%, #f2b84b);
  border: 3px solid #ffffff;
  border-radius: 13px;
  box-shadow:
    0 12px 24px rgb(15 87 83 / 14%),
    0 0 0 1px #dbe8eb;
}

.member-identity strong,
.member-identity small,
.candidate-row strong,
.candidate-row small {
  display: block;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.member-identity strong,
.candidate-row strong {
  color: var(--members-ink);
  font-size: 0.8rem;
  font-weight: 950;
  line-height: 1.2;
}

.member-identity small,
.candidate-row small {
  max-width: 320px;
  margin-top: 4px;
  color: #70868b;
  font-size: 0.68rem;
  font-weight: 750;
  line-height: 1.3;
}

.role-pill.is-admin {
  color: #7a5200;
  background: #fff7e4;
  border: 1px solid #f6dfaa;
}

.role-pill.is-manager {
  color: var(--members-accent-deep);
  background: #e9fbf7;
  border: 1px solid #ccefed;
}

.role-pill.is-member {
  color: #4d6267;
  background: #f3fafb;
  border: 1px solid #dce9ec;
}

.status-pill.is-active {
  color: var(--members-accent-deep);
  background: #e9fbf7;
  border: 1px solid #ccefed;
}

.status-pill.is-pending {
  color: #7a5200;
  background: #fff7e4;
  border: 1px solid #f6dfaa;
}

.icon-action {
  width: 34px;
  height: 34px;
  color: #647b80;
  background: #ffffff;
  border: 1px solid #d8e6e9;
  border-radius: 8px;
}

.members-list {
  display: grid;
  gap: 10px;
}

.member-card {
  display: grid;
  gap: 13px;
  padding: 14px;
  background: #fbfeff;
  border: 1px solid #e2ecef;
  border-radius: 10px;
}

.member-card-top,
.member-card-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  min-width: 0;
}

.member-card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.member-card-meta span {
  color: #70868b;
  font-size: 0.69rem;
  font-weight: 800;
  line-height: 1;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  overflow: hidden;
  white-space: nowrap;
  border: 0;
  clip: rect(0, 0, 0, 0);
}

.members-dialog-backdrop {
  --members-ink: #172224;
  --members-muted: #667b80;
  --members-line: rgb(18 33 36 / 11%);
  --members-accent: #34cbbf;
  --members-accent-deep: #0f5753;
  --members-amber: #f2b84b;

  position: fixed;
  inset: 0;
  z-index: 60;
  display: grid;
  place-items: center;
  padding: 22px;
  background: rgb(7 17 19 / 42%);
  backdrop-filter: blur(10px);
}

.members-dialog {
  box-sizing: border-box;
  display: grid;
  gap: 14px;
  width: min(100%, 520px);
  padding: 18px;
  color: var(--members-ink);
  background: #ffffff;
  border: 1px solid rgb(255 255 255 / 68%);
  border-radius: 14px;
  box-shadow:
    0 28px 80px rgb(7 17 19 / 24%),
    inset 0 1px 0 rgb(255 255 255 / 86%);
}

.dialog-header,
.dialog-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.candidate-list {
  display: grid;
  gap: 8px;
  max-height: 250px;
  overflow: auto;
}

.candidate-row {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 12px;
  width: 100%;
  min-width: 0;
  padding: 11px;
  text-align: left;
  background: #fbfeff;
  border: 1px solid #e2ecef;
  border-radius: 10px;
  cursor: pointer;
  transition:
    border-color 180ms ease,
    background 180ms ease,
    box-shadow 180ms ease,
    transform 180ms ease;
}

.candidate-row:hover,
.candidate-row:focus-visible,
.candidate-row.is-selected {
  background: #f3fdfb;
  border-color: #ccefed;
  box-shadow: 0 12px 24px rgb(18 33 36 / 6%);
}

.invite-preview {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  align-items: center;
  gap: 10px;
  padding: 12px;
  color: #60777d;
  font-size: 0.73rem;
  font-weight: 850;
  line-height: 1.4;
  background: #f7fcfd;
  border: 1px solid #dce9ec;
  border-radius: 10px;
}

.members-primary-button:active,
.members-secondary-button:active,
.icon-action:active,
.view-switcher button:active,
.candidate-row:active {
  transform: scale(0.98);
}

.members-primary-button:focus-visible,
.members-secondary-button:focus-visible,
.icon-action:focus-visible,
.view-switcher button:focus-visible,
.candidate-row:focus-visible {
  outline: 3px solid rgb(52 203 191 / 28%);
  outline-offset: 2px;
}

.members-dialog-enter-active,
.members-dialog-leave-active {
  transition: opacity 180ms ease;
}

.members-dialog-enter-active .members-dialog,
.members-dialog-leave-active .members-dialog {
  transition:
    transform 180ms ease,
    opacity 180ms ease;
}

.members-dialog-enter-from,
.members-dialog-leave-to {
  opacity: 0;
}

.members-dialog-enter-from .members-dialog,
.members-dialog-leave-to .members-dialog {
  opacity: 0;
  transform: translateY(8px) scale(0.98);
}

@media (prefers-reduced-motion: reduce) {
  .members-primary-button,
  .members-secondary-button,
  .icon-action,
  .view-switcher button,
  .candidate-row,
  .members-dialog-enter-active,
  .members-dialog-leave-active,
  .members-dialog-enter-active .members-dialog,
  .members-dialog-leave-active .members-dialog {
    transition: none;
  }

  .members-dialog-enter-from .members-dialog,
  .members-dialog-leave-to .members-dialog {
    transform: none;
  }
}

@media (max-width: 1120px) {
  .members-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .members-summary-panel {
    position: relative;
    top: auto;
  }
}

@media (max-width: 920px) {
  .members-hero,
  .directory-heading,
  .dialog-actions {
    align-items: stretch;
    flex-direction: column;
  }

  .members-toolbar {
    grid-template-columns: minmax(0, 1fr);
  }

  .view-switcher {
    justify-content: stretch;
  }

  .view-switcher button {
    flex: 1 1 0;
  }
}

@media (max-width: 760px) {
  .members-page {
    padding: 20px 16px 28px;
  }

  .members-title-block {
    align-items: flex-start;
  }

  .members-emblem {
    width: 52px;
    height: 52px;
    flex-basis: 52px;
    border-radius: 16px;
  }

  .members-stats {
    grid-template-columns: minmax(0, 1fr);
  }

  .members-primary-button,
  .members-secondary-button {
    width: 100%;
  }

  .member-card-top,
  .member-card-bottom {
    align-items: stretch;
    flex-direction: column;
  }
}

@media (max-width: 520px) {
  .members-dialog-backdrop {
    align-items: end;
    padding: 10px;
  }

  .members-dialog {
    border-radius: 14px 14px 10px 10px;
  }

  .candidate-row {
    grid-template-columns: auto minmax(0, 1fr);
  }

  .candidate-row svg {
    display: none;
  }
}
</style>
