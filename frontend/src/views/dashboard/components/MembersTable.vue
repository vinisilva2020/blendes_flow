<script setup lang="ts">
import { CircleDot, Crown, MoreHorizontal } from '@lucide/vue'

import type { OrganizationMember } from './members'

defineProps<{
  members: OrganizationMember[]
}>()
</script>

<template>
  <div class="members-table-wrap">
    <table class="members-table">
      <thead>
        <tr>
          <th scope="col">Member</th>
          <th scope="col">Role</th>
          <th scope="col">Team</th>
          <th scope="col">Last active</th>
          <th scope="col">Status</th>
          <th scope="col"><span class="sr-only">Actions</span></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="member in members" :key="member.id">
          <td>
            <div class="member-identity">
              <span class="member-avatar">{{ member.initials }}</span>
              <span>
                <strong>{{ member.name }}</strong>
                <small>{{ member.email }}</small>
              </span>
            </div>
          </td>
          <td>
            <span class="role-pill" :class="`is-${member.role.toLowerCase()}`">
              <Crown
                v-if="member.role === 'Admin'"
                :size="13"
                :stroke-width="2.45"
                aria-hidden="true"
              />
              {{ member.role }}
            </span>
          </td>
          <td>{{ member.team }}</td>
          <td>{{ member.lastActive }}</td>
          <td>
            <span class="status-pill" :class="`is-${member.status}`">
              <CircleDot :size="13" :stroke-width="2.6" aria-hidden="true" />
              {{ member.status }}
            </span>
          </td>
          <td>
            <button class="icon-action" type="button" :aria-label="`Manage ${member.name}`">
              <MoreHorizontal :size="17" :stroke-width="2.4" aria-hidden="true" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.members-table-wrap {
  overflow-x: auto;
  border: 1px solid #e2ecef;
  border-radius: 10px;
}

.members-table {
  width: 100%;
  min-width: 760px;
  border-spacing: 0;
}

.members-table th,
.members-table td {
  padding: 12px 13px;
  text-align: left;
  border-bottom: 1px solid #e8f0f2;
}

.members-table th {
  color: #70868b;
  font-size: 0.64rem;
  font-weight: 950;
  letter-spacing: 0.09em;
  line-height: 1;
  text-transform: uppercase;
  background: #f7fcfd;
}

.members-table td {
  color: #566d72;
  font-size: 0.74rem;
  font-weight: 800;
  line-height: 1.35;
  background: #ffffff;
}

.members-table tr:last-child td {
  border-bottom: 0;
}

.member-identity {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
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
.member-identity small {
  display: block;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.member-identity strong {
  color: #172224;
  font-size: 0.8rem;
  font-weight: 950;
  line-height: 1.2;
}

.member-identity small {
  max-width: 320px;
  margin-top: 4px;
  color: #70868b;
  font-size: 0.68rem;
  font-weight: 750;
  line-height: 1.3;
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

.role-pill.is-admin {
  color: #7a5200;
  background: #fff7e4;
  border: 1px solid #f6dfaa;
}

.role-pill.is-manager {
  color: #0f5753;
  background: #e9fbf7;
  border: 1px solid #ccefed;
}

.role-pill.is-member {
  color: #4d6267;
  background: #f3fafb;
  border: 1px solid #dce9ec;
}

.status-pill.is-active {
  color: #0f5753;
  background: #e9fbf7;
  border: 1px solid #ccefed;
}

.status-pill.is-pending {
  color: #7a5200;
  background: #fff7e4;
  border: 1px solid #f6dfaa;
}

.icon-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 34px;
  height: 34px;
  color: #647b80;
  background: #ffffff;
  border: 1px solid #d8e6e9;
  border-radius: 8px;
  cursor: pointer;
  transition:
    border-color 180ms ease,
    background 180ms ease,
    color 180ms ease,
    transform 180ms ease;
}

.icon-action:hover,
.icon-action:focus-visible {
  color: #172224;
  background: #f7fcfd;
  border-color: #c8dce0;
}

.icon-action:active {
  transform: scale(0.98);
}

.icon-action:focus-visible {
  outline: 3px solid rgb(52 203 191 / 28%);
  outline-offset: 2px;
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

@media (prefers-reduced-motion: reduce) {
  .icon-action {
    transition: none;
  }
}
</style>
