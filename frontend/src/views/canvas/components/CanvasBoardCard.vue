<script setup lang="ts">
import BoundgroundHierarchy from './BoundgroundHierarchy.vue'
import LaborExecutionMap from './LaborExecutionMap.vue'

export type CanvasBoardCardVariant = 'phase' | 'section'
export type CanvasBoardCardContent = 'boundground' | 'labor'

defineProps<{
  content?: CanvasBoardCardContent
  height: number
  title: string
  variant: CanvasBoardCardVariant
  width: number
}>()
</script>

<template>
  <article
    class="board-card"
    :class="{
      'board-card--phase': variant === 'phase',
      'board-card--section': variant === 'section',
    }"
    :style="{ width: `${width}px`, height: `${height}px` }"
  >
    <header class="board-card__header">{{ title }}</header>

    <div v-if="content" class="board-card__body">
      <BoundgroundHierarchy v-if="content === 'boundground'" />
      <LaborExecutionMap v-else-if="content === 'labor'" />
    </div>
  </article>
</template>

<style scoped>
.board-card {
  overflow: hidden;
  border: 2px solid #3d3d3d;
  background: rgb(255 255 255 / 76%);
  color: #1f1f1f;
  font-family: inherit;
  container-type: inline-size;
  user-select: none;
}

.board-card--phase {
  display: grid;
  place-items: center;
  background: #b3b3b3;
}

.board-card--section {
  display: grid;
  grid-template-rows: 24px 1fr;
}

.board-card__body {
  display: grid;
  min-width: 0;
  min-height: 0;
  place-items: center;
  overflow: hidden;
}

.board-card__header {
  display: grid;
  min-width: 0;
  place-items: center;
  background: #aaa;
  color: #fff;
  font-size: 18px;
  font-weight: 900;
  line-height: 1;
  text-align: center;
  white-space: nowrap;
}

.board-card--phase .board-card__header {
  background: transparent;
  font-size: 18px;
}
</style>
