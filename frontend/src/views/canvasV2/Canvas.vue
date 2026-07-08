<script setup lang="ts">
import { computed, ref } from 'vue'
import { Save } from '@lucide/vue'
import { useRoute } from 'vue-router'

import WorkflowActionsMenu, { type WorkflowTool } from './components/WorkflowActionsMenu.vue'
import WorkflowBoard from './components/WorkflowBoard.vue'

const route = useRoute()
const workflowBoard = ref<InstanceType<typeof WorkflowBoard> | null>(null)
const activeTool = ref<WorkflowTool>('actions')

const blaveId = computed(() => String(route.params.blaveId ?? 'draft'))
const blaveTitle = computed(() => String(route.query.title ?? 'Discovery flow'))
const canvasCode = computed(() => `BLV-${blaveId.value}-${slugify(blaveTitle.value)}`)
const breadcrumbs = computed(() => [blaveTitle.value, 'Canvas', canvasCode.value])

function slugify(value: string) {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
}

function centerWorkflow() {
  void workflowBoard.value?.centerCanvas()
}

function setActiveTool(tool: WorkflowTool) {
  activeTool.value = tool
}

function saveWorkflow() {
  // Persistence will be connected when the canvas data model is available.
}
</script>

<template>
  <main class="canvas-v2" :aria-label="`Canvas workspace for ${blaveTitle}`">
    <header class="canvas-v2__header" aria-label="Canvas header">
      <div class="canvas-v2__context">
        <h1 class="canvas-v2__title">Canvas</h1>
        <nav class="canvas-v2__breadcrumb" aria-label="Breadcrumb">
          <span
            v-for="(item, index) in breadcrumbs"
            :key="`${item}-${index}`"
            class="canvas-v2__breadcrumb-item"
            :class="{ 'canvas-v2__breadcrumb-item--current': index === breadcrumbs.length - 1 }"
            :aria-current="index === breadcrumbs.length - 1 ? 'page' : undefined"
          >
            <span v-if="index > 0" class="canvas-v2__breadcrumb-separator" aria-hidden="true">
              /
            </span>
            {{ item }}
          </span>
        </nav>
      </div>

      <button class="canvas-v2__save" type="button" @click="saveWorkflow">
        <Save :size="16" :stroke-width="2.2" aria-hidden="true" />
        Salvar
      </button>
    </header>

    <div class="canvas-v2__workspace">
      <WorkflowBoard ref="workflowBoard" class="canvas-v2__board" />

      <WorkflowActionsMenu
        :active-tool="activeTool"
        :can-redo="false"
        :can-undo="false"
        @center="centerWorkflow"
        @redo="() => undefined"
        @set-tool="setActiveTool"
        @undo="() => undefined"
      />
    </div>
  </main>
</template>

<style scoped>
.canvas-v2 {
  position: fixed;
  inset: 0;
  display: grid;
  min-width: 0;
  min-height: 0;
  grid-template-rows: auto 1fr;
  overflow: hidden;
  background: #f8fafc;
  color: #0f172a;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.canvas-v2__header {
  z-index: 30;
  display: grid;
  min-height: 56px;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 14px;
  border-bottom: 1px solid #e2e8f0;
  background: rgb(255 255 255 / 88%);
  padding: 8px 18px 8px 20px;
  box-shadow: 0 1px 0 rgb(15 23 42 / 3%);
  backdrop-filter: blur(18px);
}

.canvas-v2__context {
  display: flex;
  min-width: 0;
  align-items: baseline;
  gap: 12px;
}

.canvas-v2__breadcrumb {
  display: flex;
  min-width: 0;
  align-items: center;
  gap: 6px;
  overflow: hidden;
  color: #64748b;
  font-size: 0.74rem;
  font-weight: 650;
  line-height: 1;
  white-space: nowrap;
}

.canvas-v2__breadcrumb-item {
  display: inline-flex;
  min-width: 0;
  align-items: center;
  gap: 6px;
}

.canvas-v2__breadcrumb-item:first-child {
  overflow: hidden;
  text-overflow: ellipsis;
}

.canvas-v2__breadcrumb-item--current {
  max-width: min(38vw, 360px);
  overflow: hidden;
  color: #334155;
  text-overflow: ellipsis;
}

.canvas-v2__breadcrumb-separator {
  color: #cbd5e1;
}

.canvas-v2__title {
  margin: 0;
  overflow: hidden;
  color: #0f172a;
  font-size: 0.98rem;
  font-weight: 780;
  line-height: 1.2;
  text-overflow: ellipsis;
  text-wrap: balance;
  white-space: nowrap;
}

.canvas-v2__save {
  display: inline-flex;
  min-height: 40px;
  cursor: pointer;
  align-items: center;
  gap: 8px;
  border: 0;
  border-radius: 999px;
  background: #111827;
  color: #ffffff;
  font: inherit;
  font-size: 0.875rem;
  font-weight: 750;
  line-height: 1;
  outline: none;
  padding: 0 14px 0 16px;
  transition-property: background-color, box-shadow, scale;
  transition-duration: 150ms;
  transition-timing-function: ease-out;
}

.canvas-v2__save:hover {
  background: #1d4ed8;
}

.canvas-v2__save:focus-visible {
  box-shadow: 0 0 0 4px rgb(219 234 254 / 92%);
}

.canvas-v2__save:active {
  scale: 0.96;
}

.canvas-v2__workspace {
  position: relative;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}

.canvas-v2__board {
  width: 100%;
  height: 100%;
}

@media (max-width: 720px) {
  .canvas-v2__header {
    grid-template-columns: minmax(0, 1fr);
    align-items: start;
    gap: 10px;
    padding: 10px 14px;
  }

  .canvas-v2__context {
    display: grid;
    gap: 6px;
  }

  .canvas-v2__save {
    width: 100%;
    justify-content: center;
  }
}

@media (prefers-reduced-motion: reduce) {
  .canvas-v2__save {
    transition-duration: 0ms;
  }
}
</style>
