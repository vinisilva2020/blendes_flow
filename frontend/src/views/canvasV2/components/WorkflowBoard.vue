<script setup lang="ts">
import { shallowRef } from 'vue'
import { VueFlow, type Edge, type Node, type VueFlowStore } from '@vue-flow/core'

import WorkflowBoardCard, {
  type WorkflowCardContent,
  type WorkflowCardVariant,
} from './WorkflowBoardCard.vue'

import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'

type BoardNodeData = {
  content?: WorkflowCardContent
  title: string
  variant: WorkflowCardVariant
}

type BoardNode = Node<BoardNodeData, any, 'board'>

const flowId = 'canvas-v2-workflow-board'
const flowInstance = shallowRef<VueFlowStore | null>(null)

function createBoardNode(
  id: string,
  position: { x: number; y: number },
  size: { width: number; height: number },
  data: BoardNodeData,
): BoardNode {
  return {
    id,
    type: 'board',
    position,
    width: size.width,
    height: size.height,
    data,
    draggable: false,
    connectable: false,
  }
}

const nodes = shallowRef<BoardNode[]>([
  createBoardNode(
    'gathering-phase',
    { x: 0, y: 0 },
    { width: 594, height: 58 },
    { title: 'Gathering', variant: 'phase' },
  ),
  createBoardNode(
    'analysis-phase',
    { x: 604, y: 0 },
    { width: 1350, height: 58 },
    { title: 'Analysis', variant: 'phase' },
  ),
  createBoardNode(
    'boundground',
    { x: 0, y: 78 },
    { width: 212, height: 184 },
    { title: 'B - Boundground', variant: 'section', content: 'boundground' },
  ),
  createBoardNode(
    'labor',
    { x: 0, y: 274 },
    { width: 212, height: 346 },
    { title: 'L - Labor', variant: 'section', content: 'labor' },
  ),
  createBoardNode(
    'echo',
    { x: 222, y: 78 },
    { width: 370, height: 542 },
    { title: 'E - Echo', variant: 'section', content: 'echo' },
  ),
  createBoardNode(
    'noisecatch',
    { x: 604, y: 78 },
    { width: 552, height: 542 },
    { title: 'N - Noisecatch', variant: 'section', content: 'noisecatch' },
  ),
  createBoardNode(
    'drawbridge',
    { x: 1166, y: 78 },
    { width: 194, height: 542 },
    { title: 'D - Drawbridge', variant: 'section', content: 'drawbridge' },
  ),
  createBoardNode(
    'enhance',
    { x: 1370, y: 78 },
    { width: 418, height: 542 },
    { title: 'E - Enhance', variant: 'section', content: 'enhance' },
  ),
  createBoardNode(
    'sightline',
    { x: 1798, y: 78 },
    { width: 156, height: 542 },
    { title: 'S - Sightline', variant: 'section', content: 'sightline' },
  ),
])

const edges = shallowRef<Edge[]>([])

function centerCanvas(duration = 360) {
  return flowInstance.value?.fitView({
    duration,
    maxZoom: 1,
    minZoom: 0.28,
    padding: 0.1,
  })
}

function onInit(flow: VueFlowStore) {
  flowInstance.value = flow
  requestAnimationFrame(() => {
    void centerCanvas(0)
  })
}

defineExpose({
  centerCanvas,
})
</script>

<template>
  <section class="workflow-board" aria-label="Workflow canvas board">
    <VueFlow
      :id="flowId"
      class="workflow-board__flow"
      :nodes="nodes"
      :edges="edges"
      :default-viewport="{ x: 80, y: 40, zoom: 0.8 }"
      :min-zoom="0.22"
      :max-zoom="1.5"
      :pan-on-drag="true"
      :zoom-on-scroll="true"
      :zoom-on-pinch="true"
      :zoom-on-double-click="false"
      :pan-on-scroll="false"
      :prevent-scrolling="true"
      :nodes-draggable="false"
      :nodes-connectable="false"
      :elements-selectable="false"
      :select-nodes-on-drag="false"
      :edges-focusable="false"
      :nodes-focusable="false"
      :disable-keyboard-a11y="true"
      @init="onInit"
    >
      <template #node-board="{ data, dimensions }">
        <WorkflowBoardCard
          :content="data.content"
          :height="dimensions.height"
          :title="data.title"
          :variant="data.variant"
          :width="dimensions.width"
        />
      </template>
    </VueFlow>
  </section>
</template>

<style scoped>
.workflow-board {
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}

.workflow-board__flow {
  width: 100%;
  height: 100%;
  background-color: #f8fafc;
  background-image:
    radial-gradient(circle, rgb(30 41 59 / 18%) 1.15px, transparent 1.15px),
    linear-gradient(180deg, rgb(239 246 255 / 62%) 0%, rgb(255 255 255 / 0%) 280px);
  background-size:
    28px 28px,
    100% 100%;
  cursor: grab;
}

.workflow-board__flow:active {
  cursor: grabbing;
}

.workflow-board__flow :deep(.vue-flow__pane),
.workflow-board__flow :deep(.vue-flow__selectionpane),
.workflow-board__flow :deep(.vue-flow__node) {
  cursor: inherit;
}

.workflow-board__flow :deep(.vue-flow__renderer) {
  width: 100%;
  height: 100%;
}

.workflow-board__flow :deep(.vue-flow__node-board) {
  border: 0;
  background: transparent;
  box-shadow: none;
  padding: 0;
}

.workflow-board__flow :deep(.vue-flow__attribution) {
  display: none;
}
</style>
