<script setup lang="ts">
import type { Component } from 'vue'
import { Maximize2, ZoomIn, ZoomOut } from '@lucide/vue'
import { useVueFlow } from '@vue-flow/core'

const props = defineProps<{
  flowId: string
}>()

const { fitView, zoomIn, zoomOut } = useVueFlow(props.flowId)

type CanvasAction = {
  icon: Component
  label: string
  run: () => Promise<boolean>
}

const transition = {
  duration: 260,
}

const actions: CanvasAction[] = [
  {
    icon: ZoomOut,
    label: 'Afastar',
    run: () => zoomOut(transition),
  },
  {
    icon: ZoomIn,
    label: 'Aproximar',
    run: () => zoomIn(transition),
  },
  {
    icon: Maximize2,
    label: 'Enquadrar quadro',
    run: () =>
      fitView({
        duration: transition.duration,
        maxZoom: 1,
        minZoom: 0.3,
        padding: 0.12,
      }),
  },
]
</script>

<template>
  <nav class="canvas-actions" aria-label="Acoes do canvas">
    <button
      v-for="action in actions"
      :key="action.label"
      class="canvas-actions__button"
      type="button"
      :aria-label="action.label"
      @click.stop="action.run"
    >
      <component
        :is="action.icon"
        class="canvas-actions__icon"
        :size="19"
        :stroke-width="2.35"
        aria-hidden="true"
      />
      <span class="canvas-actions__label" role="tooltip">{{ action.label }}</span>
    </button>
  </nav>
</template>

<style scoped>
.canvas-actions {
  position: fixed;
  left: 50%;
  bottom: 24px;
  z-index: 20;
  display: inline-flex;
  gap: 4px;
  padding: 6px;
  border: 1px solid rgb(23 34 36 / 12%);
  border-radius: 8px;
  background: rgb(255 255 255 / 88%);
  box-shadow:
    0 18px 48px rgb(15 44 43 / 16%),
    0 2px 8px rgb(15 44 43 / 8%);
  backdrop-filter: blur(18px);
  transform: translateX(-50%);
}

.canvas-actions__button {
  position: relative;
  display: grid;
  width: 40px;
  height: 40px;
  place-items: center;
  border: 0;
  border-radius: 8px;
  background: transparent;
  color: #324145;
  cursor: pointer;
  outline: none;
  transition-property: background-color, color, transform;
  transition-duration: 150ms;
  transition-timing-function: ease;
}

.canvas-actions__button:hover,
.canvas-actions__button:focus-visible {
  background: #172224;
  color: #ffffff;
}

.canvas-actions__button:active {
  transform: scale(0.96);
}

.canvas-actions__button:focus-visible {
  box-shadow: 0 0 0 4px rgb(174 238 255 / 42%);
}

.canvas-actions__icon {
  pointer-events: none;
}

.canvas-actions__label {
  position: absolute;
  left: 50%;
  bottom: calc(100% + 10px);
  width: max-content;
  max-width: 160px;
  padding: 7px 9px;
  border-radius: 7px;
  background: #172224;
  box-shadow: 0 10px 28px rgb(15 44 43 / 16%);
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 900;
  line-height: 1;
  opacity: 0;
  pointer-events: none;
  transform: translate(-50%, 4px);
  transition-property: opacity, transform;
  transition-duration: 150ms;
  transition-timing-function: ease;
  white-space: nowrap;
}

.canvas-actions__label::after {
  position: absolute;
  left: 50%;
  top: 100%;
  width: 8px;
  height: 8px;
  background: inherit;
  content: '';
  transform: translate(-50%, -4px) rotate(45deg);
}

.canvas-actions__button:hover .canvas-actions__label,
.canvas-actions__button:focus-visible .canvas-actions__label {
  opacity: 1;
  transform: translate(-50%, 0);
}
</style>
