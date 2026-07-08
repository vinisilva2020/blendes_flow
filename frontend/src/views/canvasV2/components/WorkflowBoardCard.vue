<script setup lang="ts">
import { computed } from 'vue'

export type WorkflowCardContent =
  | 'boundground'
  | 'labor'
  | 'echo'
  | 'noisecatch'
  | 'drawbridge'
  | 'enhance'
  | 'sightline'

export type WorkflowCardVariant = 'phase' | 'section'

const props = defineProps<{
  content?: WorkflowCardContent
  height: number
  title: string
  variant: WorkflowCardVariant
  width: number
}>()

const toneClass = computed(() => {
  if (props.variant === 'phase') {
    return props.title === 'Gathering' ? 'workflow-card--gathering' : 'workflow-card--analysis'
  }

  return props.content ? `workflow-card--${props.content}` : 'workflow-card--neutral'
})

const echoRows = [
  ['What', 'Name', ''],
  ['Why', 'Goal', 'Obs'],
  ['When', 'Trigger', 'Obs'],
  ['Who', 'Roles', 'Obs'],
  ['With', 'Tools', 'Obs'],
  ['Whereby', 'Techniques', 'Obs'],
  ['In', 'Input', 'Obs'],
  ['Out', 'Output', 'Obs'],
]

const riskRows = Array.from({ length: 7 }, (_, index) => ({
  id: `risk-${index + 1}`,
  prompt: 'What risk this facet rises?',
  tags: ['Operational', 'Tactical', 'Strategic'],
}))

const repeatedRows = Array.from({ length: 7 }, (_, index) => index + 1)
</script>

<template>
  <article
    class="workflow-card"
    :class="[
      toneClass,
      {
        'workflow-card--phase': variant === 'phase',
        'workflow-card--section': variant === 'section',
      },
    ]"
    :style="{ width: `${width}px`, height: `${height}px` }"
  >
    <header class="workflow-card__header">{{ title }}</header>

    <div v-if="content" class="workflow-card__body">
      <div v-if="content === 'boundground'" class="boundground" aria-label="Boundground hierarchy">
        <div class="boundground__boundary boundground__boundary--supra">Supra Boundary</div>
        <div class="boundground__line" aria-hidden="true"></div>
        <div class="boundground__boundary">Boundary</div>
      </div>

      <div v-else-if="content === 'labor'" class="labor-map" aria-label="Labor execution map">
        <div class="labor-map__actor labor-map__actor--role">
          <span class="labor-map__avatar" aria-hidden="true">R</span>
          <span>Role</span>
        </div>
        <div class="labor-map__connector labor-map__connector--one" aria-hidden="true"></div>
        <div class="labor-map__node">Schapter</div>
        <div class="labor-map__connector labor-map__connector--two" aria-hidden="true"></div>
        <div class="labor-map__actor labor-map__actor--group">
          <span class="labor-map__avatar labor-map__avatar--group" aria-hidden="true">G</span>
          <span>Group</span>
        </div>
      </div>

      <div v-else-if="content === 'echo'" class="echo-grid" aria-label="Echo structure">
        <div
          v-for="(row, index) in echoRows"
          :key="`${row[0]}-${index}`"
          class="echo-grid__row"
          :class="{ 'echo-grid__row--compact': index === 0 }"
        >
          <div class="echo-grid__label">{{ row[0] }}</div>
          <div class="echo-grid__field echo-grid__field--primary">{{ row[1] }}</div>
          <div v-if="row[2]" class="echo-grid__field">{{ row[2] }}</div>
        </div>
      </div>

      <div v-else-if="content === 'noisecatch'" class="risk-grid" aria-label="Noisecatch analysis">
        <div v-for="row in riskRows" :key="row.id" class="risk-grid__row">
          <div class="risk-grid__prompt">{{ row.prompt }}</div>
          <div v-for="tag in row.tags" :key="tag" class="risk-grid__tag">{{ tag }}</div>
        </div>
      </div>

      <div v-else-if="content === 'drawbridge'" class="stack-grid" aria-label="Prioritized risks">
        <div v-for="row in repeatedRows" :key="row" class="stack-grid__cell">Prioritized Risk</div>
      </div>

      <div v-else-if="content === 'enhance'" class="enhance-grid" aria-label="Enhancement actions">
        <div v-for="row in repeatedRows" :key="row" class="enhance-grid__row">
          <div class="enhance-grid__practice">Kref practices</div>
          <div class="enhance-grid__action">Concrete Action</div>
        </div>
      </div>

      <div v-else-if="content === 'sightline'" class="stack-grid" aria-label="Sightline outcomes">
        <div
          v-for="row in repeatedRows"
          :key="row"
          class="stack-grid__cell stack-grid__cell--crest"
        >
          Crest
        </div>
      </div>
    </div>
  </article>
</template>

<style scoped>
.workflow-card {
  --card-accent: #64748b;
  --card-accent-strong: #475569;
  --card-tint: rgb(248 250 252 / 78%);

  overflow: hidden;
  border-radius: 7px;
  background:
    linear-gradient(180deg, var(--card-tint), rgb(255 255 255 / 88%) 92px), rgb(255 255 255 / 88%);
  box-shadow:
    0 0 0 1px color-mix(in srgb, var(--card-accent) 18%, transparent),
    0 10px 24px rgb(15 23 42 / 8%);
  color: #0f172a;
  container-type: inline-size;
  user-select: none;
}

.workflow-card--phase {
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, var(--card-accent), var(--card-accent-strong));
  color: #ffffff;
}

.workflow-card--section {
  display: grid;
  grid-template-rows: 26px 1fr;
}

.workflow-card__header {
  display: grid;
  min-width: 0;
  place-items: center;
  background: linear-gradient(135deg, var(--card-accent), var(--card-accent-strong));
  color: #ffffff;
  font-size: 14px;
  font-weight: 820;
  line-height: 1;
  letter-spacing: 0.01em;
  text-align: center;
  text-wrap: balance;
}

.workflow-card--phase .workflow-card__header {
  background: transparent;
  font-size: 16px;
}

.workflow-card__body {
  display: grid;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
  padding: 8px;
}

.workflow-card--gathering {
  --card-accent: #14b8a6;
  --card-accent-strong: #0f766e;
  --card-tint: rgb(240 253 250 / 76%);
}

.workflow-card--analysis {
  --card-accent: #2563eb;
  --card-accent-strong: #1e40af;
  --card-tint: rgb(239 246 255 / 78%);
}

.workflow-card--boundground {
  --card-accent: #22c55e;
  --card-accent-strong: #15803d;
  --card-tint: rgb(240 253 244 / 78%);
}

.workflow-card--labor {
  --card-accent: #8b5cf6;
  --card-accent-strong: #6d28d9;
  --card-tint: rgb(245 243 255 / 78%);
}

.workflow-card--echo {
  --card-accent: #0ea5e9;
  --card-accent-strong: #0369a1;
  --card-tint: rgb(240 249 255 / 78%);
}

.workflow-card--noisecatch {
  --card-accent: #f59e0b;
  --card-accent-strong: #b45309;
  --card-tint: rgb(255 251 235 / 82%);
}

.workflow-card--drawbridge {
  --card-accent: #f43f5e;
  --card-accent-strong: #be123c;
  --card-tint: rgb(255 241 242 / 78%);
}

.workflow-card--enhance {
  --card-accent: #06b6d4;
  --card-accent-strong: #0e7490;
  --card-tint: rgb(236 254 255 / 78%);
}

.workflow-card--sightline {
  --card-accent: #6366f1;
  --card-accent-strong: #4338ca;
  --card-tint: rgb(238 242 255 / 78%);
}

.boundground {
  display: grid;
  grid-template-rows: 38px 38px 38px;
  justify-items: center;
  align-content: start;
  padding: 4px 0;
}

.boundground__boundary {
  display: grid;
  width: min(132px, 100%);
  place-items: center;
  border-radius: 4px;
  background: #ffffff;
  box-shadow: inset 0 0 0 1.5px color-mix(in srgb, var(--card-accent) 58%, #334155);
  color: #64748b;
  font-size: 12px;
  font-weight: 800;
}

.boundground__boundary--supra {
  border-radius: 0;
  border: 1.5px dashed color-mix(in srgb, var(--card-accent) 68%, #334155);
  box-shadow: none;
}

.boundground__line {
  width: 2px;
  background: color-mix(in srgb, var(--card-accent) 68%, #334155);
}

.labor-map {
  position: relative;
  overflow: hidden;
  border-radius: 5px;
  background:
    linear-gradient(color-mix(in srgb, var(--card-accent) 16%, transparent) 1px, transparent 1px),
    linear-gradient(
      90deg,
      color-mix(in srgb, var(--card-accent) 16%, transparent) 1px,
      transparent 1px
    ),
    #f8fafc;
  background-size: 52px 52px;
}

.labor-map__actor {
  position: absolute;
  display: grid;
  gap: 5px;
  justify-items: center;
  color: #334155;
  font-size: 11px;
  line-height: 1;
}

.labor-map__actor--role {
  top: 26px;
  left: 46px;
}

.labor-map__actor--group {
  right: 14px;
  bottom: 22px;
}

.labor-map__avatar {
  display: grid;
  width: 24px;
  height: 24px;
  place-items: center;
  border-radius: 999px;
  background: #ede9fe;
  color: var(--card-accent-strong);
  font-size: 11px;
  font-weight: 900;
}

.labor-map__avatar--group {
  background: #dbeafe;
  color: #1d4ed8;
}

.labor-map__node {
  position: absolute;
  top: 132px;
  left: 36px;
  display: grid;
  width: 108px;
  height: 38px;
  place-items: center;
  border-radius: 999px;
  background: #ffffff;
  box-shadow:
    0 0 0 1.5px color-mix(in srgb, var(--card-accent) 62%, #334155),
    0 8px 18px rgb(15 23 42 / 8%);
  color: #94a3b8;
  font-size: 12px;
  font-weight: 850;
}

.labor-map__connector {
  position: absolute;
  width: 58px;
  border-top: 2px solid color-mix(in srgb, var(--card-accent) 62%, #334155);
  transform-origin: left center;
}

.labor-map__connector--one {
  top: 92px;
  left: 72px;
  transform: rotate(58deg);
}

.labor-map__connector--two {
  right: 45px;
  bottom: 86px;
  border-top-style: dashed;
  transform: rotate(-104deg);
}

.echo-grid,
.risk-grid,
.stack-grid,
.enhance-grid {
  display: grid;
  min-height: 0;
  gap: 7px;
}

.echo-grid {
  grid-template-rows: 22px repeat(7, minmax(0, 1fr));
}

.echo-grid__row {
  display: grid;
  min-height: 0;
  grid-template-columns: 54px minmax(0, 1fr) 86px;
  gap: 8px;
}

.echo-grid__row--compact {
  grid-template-columns: 54px minmax(0, 1fr);
}

.echo-grid__label,
.echo-grid__field,
.risk-grid__prompt,
.risk-grid__tag,
.stack-grid__cell,
.enhance-grid__practice,
.enhance-grid__action {
  display: grid;
  min-width: 0;
  min-height: 0;
  place-items: center;
  border-radius: 4px;
  background: #ffffff;
  box-shadow: inset 0 0 0 1.5px color-mix(in srgb, var(--card-accent) 34%, rgb(51 65 85 / 48%));
  color: #94a3b8;
  font-weight: 800;
  line-height: 1.08;
  text-align: center;
}

.echo-grid__label {
  color: #334155;
  font-size: 10px;
}

.echo-grid__field {
  font-size: 11px;
}

.echo-grid__field--primary {
  font-size: clamp(13px, 6cqw, 17px);
}

.risk-grid {
  grid-template-rows: repeat(7, minmax(0, 1fr));
}

.risk-grid__row {
  display: grid;
  min-height: 0;
  grid-template-columns: minmax(0, 1.9fr) repeat(3, minmax(74px, 1fr));
  gap: 8px;
}

.risk-grid__prompt,
.risk-grid__tag {
  font-size: 10px;
}

.stack-grid {
  grid-template-rows: repeat(7, minmax(0, 1fr));
}

.stack-grid__cell {
  font-size: 12px;
}

.stack-grid__cell--crest {
  font-size: 22px;
}

.enhance-grid {
  grid-template-rows: repeat(7, minmax(0, 1fr));
}

.enhance-grid__row {
  display: grid;
  min-height: 0;
  grid-template-columns: minmax(0, 1.7fr) minmax(96px, 1fr);
  gap: 8px;
}

.enhance-grid__practice {
  justify-items: start;
  padding-inline: 10px;
  color: #94a3b8;
  font-size: 22px;
  text-align: left;
}

.enhance-grid__action {
  color: #94a3b8;
  font-size: 13px;
}
</style>
