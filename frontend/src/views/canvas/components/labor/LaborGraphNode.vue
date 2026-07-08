<script setup lang="ts">
import { BriefcaseBusiness, UsersRound } from '@lucide/vue'
import { Handle, Position } from '@vue-flow/core'

import type { LaborNodeData } from './types'

defineProps<{
  data: LaborNodeData
  selected?: boolean
}>()
</script>

<template>
  <div
    class="labor-graph-node"
    :class="[
      `labor-graph-node--${data.kind}`,
      {
        'labor-graph-node--selected': selected,
      },
    ]"
  >
    <template v-if="data.kind === 'schapter'">
      <Handle
        id="schapter-target-top"
        class="labor-graph-node__handle"
        type="target"
        :position="Position.Top"
      />
      <Handle
        id="schapter-target-bottom"
        class="labor-graph-node__handle"
        type="target"
        :position="Position.Bottom"
      />

      <span class="labor-graph-node__schapter-label">{{ data.label }}</span>
    </template>

    <template v-else>
      <Handle
        id="executor-source-top"
        class="labor-graph-node__handle"
        type="source"
        :position="Position.Top"
      />
      <Handle
        id="executor-source-bottom"
        class="labor-graph-node__handle"
        type="source"
        :position="Position.Bottom"
      />

      <BriefcaseBusiness
        v-if="data.kind === 'role'"
        class="labor-graph-node__icon"
        :size="32"
        :stroke-width="2.1"
        aria-hidden="true"
      />
      <UsersRound
        v-else
        class="labor-graph-node__icon"
        :size="34"
        :stroke-width="2.1"
        aria-hidden="true"
      />

      <span class="labor-graph-node__note">{{ data.label }}</span>
    </template>
  </div>
</template>

<style scoped>
.labor-graph-node {
  --labor-node-text: #1f1f1f;
  --labor-node-muted: #3d3d3d;
  --labor-note-bg: #fff4a8;
  --labor-note-border: #e3d77a;
  --labor-schapter-bg: #fff7ad;
  --labor-schapter-shadow: 0 7px 16px rgb(0 0 0 / 12%);
  --labor-selection: #333;

  display: grid;
  width: 100%;
  height: 100%;
  min-width: 0;
  color: var(--labor-node-text);
  font-family: inherit;
  text-align: center;
}

.labor-graph-node--role,
.labor-graph-node--group {
  align-content: center;
  justify-items: center;
  gap: 6px;
}

.labor-graph-node--schapter {
  align-items: center;
  justify-items: center;
  padding: 16px 20px;
  border: 1px solid rgb(0 0 0 / 7%);
  background: var(--labor-schapter-bg);
  border-radius: 4px 18px 4px 18px;
  box-shadow: var(--labor-schapter-shadow);
}

.labor-graph-node--selected {
  outline: 2px solid var(--labor-selection);
  outline-offset: 4px;
}

.labor-graph-node__icon {
  color: var(--labor-node-muted);
}

.labor-graph-node__note {
  display: grid;
  width: min(100%, 108px);
  min-height: 38px;
  place-items: center;
  padding: 6px 8px;
  border: 1px solid var(--labor-note-border);
  background: var(--labor-note-bg);
  box-shadow: 0 4px 10px rgb(0 0 0 / 10%);
  color: var(--labor-node-text);
  font-size: 0.88rem;
  font-weight: 650;
  letter-spacing: 0;
  line-height: 1.16;
  overflow-wrap: anywhere;
}

.labor-graph-node__schapter-label {
  display: block;
  max-width: 100%;
  color: var(--labor-node-text);
  font-size: 1.36rem;
  font-weight: 780;
  letter-spacing: 0;
  line-height: 1.18;
  overflow-wrap: anywhere;
  text-wrap: balance;
}

.labor-graph-node__handle {
  width: 10px;
  height: 10px;
  border: 2px solid #fff;
  background: #2f2f2f;
  opacity: 0;
  transition:
    opacity 140ms ease,
    transform 140ms ease;
}

.labor-graph-node:hover .labor-graph-node__handle,
.labor-graph-node--selected .labor-graph-node__handle {
  opacity: 0.8;
}

.labor-graph-node__handle:hover {
  transform: scale(1.14);
}
</style>
