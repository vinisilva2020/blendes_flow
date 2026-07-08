<script setup lang="ts">
import { computed, type Component } from 'vue'
import { Hand, LocateFixed, MousePointer2, Redo2, Undo2 } from '@lucide/vue'

export type WorkflowTool = 'freehand' | 'actions'

const props = defineProps<{
  activeTool: WorkflowTool
  canRedo?: boolean
  canUndo?: boolean
}>()

const emit = defineEmits<{
  center: []
  redo: []
  setTool: [tool: WorkflowTool]
  undo: []
}>()

type ToolAction = {
  icon: Component
  id: WorkflowTool
  label: string
}

type CommandAction = {
  disabled?: boolean
  icon: Component
  label: string
  run: () => void
}

const toolActions: ToolAction[] = [
  {
    icon: Hand,
    id: 'freehand',
    label: 'Mao livre',
  },
  {
    icon: MousePointer2,
    id: 'actions',
    label: 'Mao com acoes',
  },
]

const commandActions = computed<CommandAction[]>(() => [
  {
    disabled: !props.canUndo,
    icon: Undo2,
    label: 'Voltar',
    run: () => emit('undo'),
  },
  {
    disabled: !props.canRedo,
    icon: Redo2,
    label: 'Ir para frente',
    run: () => emit('redo'),
  },
  {
    icon: LocateFixed,
    label: 'Centralizar',
    run: () => emit('center'),
  },
])
</script>

<template>
  <nav class="workflow-actions" aria-label="Acoes do workflow">
    <div class="workflow-actions__group" role="group" aria-label="Modo de interacao">
      <button
        v-for="action in toolActions"
        :key="action.id"
        class="workflow-actions__button"
        :class="{ 'workflow-actions__button--active': activeTool === action.id }"
        type="button"
        :aria-label="action.label"
        :aria-pressed="activeTool === action.id"
        :title="action.label"
        @click="emit('setTool', action.id)"
      >
        <component
          :is="action.icon"
          class="workflow-actions__icon"
          :size="17"
          :stroke-width="2.2"
          aria-hidden="true"
        />
        <span class="workflow-actions__label">{{ action.label }}</span>
      </button>
    </div>

    <div class="workflow-actions__group" role="group" aria-label="Historico e enquadramento">
      <button
        v-for="action in commandActions"
        :key="action.label"
        class="workflow-actions__button"
        type="button"
        :aria-label="action.label"
        :disabled="action.disabled"
        :title="action.label"
        @click="action.run"
      >
        <component
          :is="action.icon"
          class="workflow-actions__icon"
          :size="17"
          :stroke-width="2.2"
          aria-hidden="true"
        />
        <span class="workflow-actions__label">{{ action.label }}</span>
      </button>
    </div>
  </nav>
</template>

<style scoped>
.workflow-actions {
  position: absolute;
  top: 22px;
  left: 24px;
  z-index: 20;
  display: grid;
  gap: 6px;
  width: 56px;
  padding: 6px;
  border-radius: 14px;
  background: rgb(255 255 255 / 94%);
  box-shadow:
    0 0 0 1px rgb(15 23 42 / 8%),
    0 18px 40px rgb(15 23 42 / 14%),
    0 4px 10px rgb(15 23 42 / 7%);
  backdrop-filter: blur(20px);
}

.workflow-actions__group {
  display: grid;
  gap: 3px;
}

.workflow-actions__group + .workflow-actions__group {
  padding-top: 6px;
  border-top: 1px solid rgb(226 232 240 / 96%);
}

.workflow-actions__button {
  position: relative;
  display: grid;
  width: 44px;
  height: 44px;
  cursor: pointer;
  place-items: center;
  border: 0;
  border-radius: 10px;
  background: transparent;
  color: #475569;
  font: inherit;
  outline: none;
  padding: 0;
  transition-property: background-color, color, box-shadow, scale, transform;
  transition-duration: 150ms;
  transition-timing-function: cubic-bezier(0.2, 0, 0, 1);
}

.workflow-actions__button:hover,
.workflow-actions__button:focus-visible {
  background: #f1f5f9;
  color: #1d4ed8;
}

.workflow-actions__button:focus-visible {
  box-shadow: 0 0 0 4px rgb(219 234 254 / 92%);
}

.workflow-actions__button:active {
  scale: 0.96;
}

.workflow-actions__button:disabled {
  cursor: not-allowed;
  color: #cbd5e1;
  opacity: 0.68;
}

.workflow-actions__button--active {
  background: #111827;
  color: #ffffff;
  box-shadow:
    0 10px 22px rgb(15 23 42 / 24%),
    inset 0 0 0 1px rgb(255 255 255 / 18%);
}

.workflow-actions__button--active:hover,
.workflow-actions__button--active:focus-visible {
  background: #111827;
  color: #ffffff;
}

.workflow-actions__icon {
  pointer-events: none;
}

.workflow-actions__label {
  position: absolute;
  left: calc(100% + 10px);
  top: 50%;
  width: max-content;
  max-width: 164px;
  padding: 7px 9px;
  border-radius: 8px;
  background: #111827;
  box-shadow: 0 12px 26px rgb(15 23 42 / 18%);
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 750;
  line-height: 1;
  opacity: 0;
  pointer-events: none;
  text-align: left;
  text-wrap: pretty;
  transform: translate(-4px, -50%) scale(0.98);
  transition-property: opacity, transform;
  transition-duration: 150ms;
  transition-timing-function: cubic-bezier(0.2, 0, 0, 1);
  white-space: nowrap;
}

.workflow-actions__label::before {
  position: absolute;
  top: 50%;
  right: 100%;
  width: 8px;
  height: 8px;
  background: inherit;
  content: '';
  transform: translate(4px, -50%) rotate(45deg);
}

.workflow-actions__button:hover .workflow-actions__label,
.workflow-actions__button:focus-visible .workflow-actions__label {
  opacity: 1;
  transform: translate(0, -50%) scale(1);
}

@media (max-width: 720px) {
  .workflow-actions {
    top: auto;
    right: 50%;
    bottom: 14px;
    left: auto;
    width: auto;
    grid-template-columns: auto auto;
    justify-content: center;
    overflow-x: auto;
    border-radius: 16px;
    transform: translateX(50%);
  }

  .workflow-actions__group {
    display: flex;
    min-width: max-content;
  }

  .workflow-actions__group + .workflow-actions__group {
    padding-top: 0;
    padding-left: 8px;
    border-top: 0;
    border-left: 1px solid rgb(226 232 240 / 92%);
  }

  .workflow-actions__button {
    width: 44px;
    min-height: 44px;
  }

  .workflow-actions__label {
    top: auto;
    bottom: calc(100% + 10px);
    left: 50%;
    transform: translate(-50%, 4px) scale(0.98);
  }

  .workflow-actions__label::before {
    top: 100%;
    right: auto;
    left: 50%;
    transform: translate(-50%, -4px) rotate(45deg);
  }

  .workflow-actions__button:hover .workflow-actions__label,
  .workflow-actions__button:focus-visible .workflow-actions__label {
    transform: translate(-50%, 0) scale(1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .workflow-actions__button {
    transition-duration: 0ms;
  }
}
</style>
