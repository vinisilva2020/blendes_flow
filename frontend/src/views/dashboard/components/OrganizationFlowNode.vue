<script setup lang="ts">
import { Building2, CircleDot, Network } from '@lucide/vue'
import { Handle, Position } from '@vue-flow/core'

import type { OrganizationNodeKind } from './organization-map'

type OrganizationFlowNodeData = {
  kind: OrganizationNodeKind
  label: string
  owner?: string
}

defineProps<{
  data: OrganizationFlowNodeData
}>()

const kindLabels = {
  organization: 'Organization',
  department: 'Department',
  operation: 'Operation',
} as const

const kindIcons = {
  organization: Building2,
  department: Network,
  operation: CircleDot,
}
</script>

<template>
  <article class="organization-flow-node" :class="`organization-flow-node--${data.kind}`">
    <Handle
      v-if="data.kind !== 'organization'"
      type="target"
      :position="Position.Top"
      class="organization-flow-node__handle"
    />

    <span class="organization-flow-node__icon">
      <component :is="kindIcons[data.kind]" :size="18" :stroke-width="2.1" aria-hidden="true" />
    </span>
    <span class="min-w-0">
      <span class="organization-flow-node__kind">{{ kindLabels[data.kind] }}</span>
      <strong class="organization-flow-node__label">{{ data.label }}</strong>
      <span v-if="data.owner" class="organization-flow-node__owner">{{ data.owner }}</span>
    </span>

    <Handle
      v-if="data.kind !== 'operation'"
      type="source"
      :position="Position.Bottom"
      class="organization-flow-node__handle"
    />
  </article>
</template>

<style scoped>
.organization-flow-node {
  display: flex;
  width: 224px;
  min-height: 76px;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 16px;
  background: rgb(255 255 255 / 96%);
  box-shadow:
    0 1px 2px rgb(15 23 42 / 7%),
    0 12px 28px rgb(15 23 42 / 9%);
  outline: 1px solid rgb(15 23 42 / 7%);
  color: #0f172a;
}

.organization-flow-node--organization {
  outline-color: rgb(29 78 216 / 22%);
  box-shadow:
    0 1px 2px rgb(29 78 216 / 10%),
    0 14px 34px rgb(29 78 216 / 16%);
}

.organization-flow-node__icon {
  display: grid;
  width: 40px;
  height: 40px;
  flex: 0 0 auto;
  place-items: center;
  border-radius: 12px;
  background: #eff6ff;
  color: #1d4ed8;
}

.organization-flow-node--department .organization-flow-node__icon {
  background: #ecfeff;
  color: #0e7490;
}

.organization-flow-node--operation .organization-flow-node__icon {
  background: #f5f3ff;
  color: #6d28d9;
}

.organization-flow-node__kind,
.organization-flow-node__label,
.organization-flow-node__owner {
  display: block;
  max-width: 148px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.organization-flow-node__kind {
  color: #94a3b8;
  font-size: 10px;
  font-weight: 750;
  letter-spacing: 0.09em;
  line-height: 14px;
  text-transform: uppercase;
}

.organization-flow-node__label {
  color: inherit;
  font-size: 14px;
  font-weight: 650;
  line-height: 20px;
}

.organization-flow-node__owner {
  color: #64748b;
  font-size: 11px;
  line-height: 16px;
}

.organization-flow-node__handle {
  width: 8px;
  height: 8px;
  border: 2px solid white;
  background: #64748b;
  opacity: 0;
}

:global(.dark) .organization-flow-node {
  background: rgb(15 23 42 / 96%);
  outline-color: rgb(255 255 255 / 11%);
  color: #f8fafc;
  box-shadow: 0 14px 34px rgb(0 0 0 / 28%);
}

:global(.dark) .organization-flow-node__owner {
  color: #94a3b8;
}

:global(.dark) .organization-flow-node__icon {
  background: rgb(59 130 246 / 12%);
  color: #93c5fd;
}

:global(.dark) .organization-flow-node--department .organization-flow-node__icon {
  background: rgb(34 211 238 / 10%);
  color: #67e8f9;
}

:global(.dark) .organization-flow-node--operation .organization-flow-node__icon {
  background: rgb(167 139 250 / 10%);
  color: #c4b5fd;
}
</style>
