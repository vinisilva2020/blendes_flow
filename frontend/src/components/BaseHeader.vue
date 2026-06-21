<script setup lang="ts">
import { Bell, CalendarDays, Plus, Search } from '@lucide/vue'

defineOptions({
  name: 'BaseHeader',
})

withDefaults(
  defineProps<{
    avatarLabel?: string
    subtitle?: string
    title?: string
  }>(),
  {
    avatarLabel: 'BF',
    subtitle: 'Track workspace activity and keep flows moving.',
    title: 'Dashboard',
  },
)
</script>

<template>
  <header class="base-header" aria-label="Page header">
    <div class="base-header-profile">
      <slot name="avatar">
        <span class="base-header-avatar" aria-hidden="true">{{ avatarLabel }}</span>
      </slot>

      <div class="base-header-copy">
        <slot name="title">
          <h1>{{ title }}</h1>
        </slot>

        <slot name="subtitle">
          <p>{{ subtitle }}</p>
        </slot>
      </div>
    </div>

    <div v-if="$slots['header-extra']" class="base-header-extra">
      <slot name="header-extra" />
    </div>

    <div class="base-header-actions">
      <slot name="actions">
        <button class="base-header-icon-button" type="button" aria-label="Search">
          <Search :size="16" :stroke-width="2.1" aria-hidden="true" />
        </button>

        <button
          class="base-header-icon-button has-notification"
          type="button"
          aria-label="Notifications"
        >
          <Bell :size="16" :stroke-width="2.1" aria-hidden="true" />
        </button>

        <button class="base-header-secondary-button" type="button">
          <CalendarDays :size="15" :stroke-width="2.1" aria-hidden="true" />
          <span>Schedule</span>
        </button>

        <button class="base-header-primary-button" type="button">
          <Plus :size="16" :stroke-width="2.35" aria-hidden="true" />
          <span>Create request</span>
        </button>
      </slot>
    </div>
  </header>
</template>

<style scoped>
.base-header {
  --header-ink: #172224;
  --header-muted: #6c8085;
  --header-line: rgb(18 33 36 / 10%);
  --header-accent: #34cbbf;
  --header-accent-deep: #0f5753;

  position: sticky;
  top: 0;
  z-index: 10;
  box-sizing: border-box;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto auto;
  align-items: center;
  gap: 14px;
  min-height: 68px;
  padding: 12px 28px;
  color: var(--header-ink);
  background: rgb(255 255 255 / 88%);
  border-bottom: 1px solid var(--header-line);
  backdrop-filter: blur(18px) saturate(132%);
}

.base-header::after {
  position: absolute;
  right: 28px;
  bottom: -1px;
  left: 28px;
  height: 1px;
  pointer-events: none;
  content: '';
  background: linear-gradient(
    90deg,
    transparent,
    rgb(52 203 191 / 26%),
    rgb(18 33 36 / 8%),
    transparent
  );
}

.base-header-profile {
  display: flex;
  align-items: center;
  gap: 11px;
  min-width: 0;
}

.base-header-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  flex: 0 0 38px;
  overflow: hidden;
  color: #ffffff;
  font-size: 0.68rem;
  font-weight: 900;
  line-height: 1;
  background:
    linear-gradient(145deg, rgb(255 255 255 / 18%), transparent 34%),
    radial-gradient(circle at 74% 22%, #aeeeff 0 13%, transparent 14%),
    linear-gradient(145deg, #0d5d67, #34cbbf 54%, #f2b84b);
  border: 3px solid #ffffff;
  border-radius: 999px;
  box-shadow:
    0 0 0 1px #dfeaec,
    0 12px 28px rgb(18 33 36 / 12%);
}

.base-header-copy {
  min-width: 0;
}

.base-header-copy h1,
.base-header-copy p {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.base-header-copy h1 {
  margin: 0;
  color: var(--header-ink);
  font-size: 0.94rem;
  font-weight: 900;
  letter-spacing: 0;
  line-height: 1.25;
}

.base-header-copy p {
  margin: 4px 0 0;
  color: var(--header-muted);
  font-size: 0.72rem;
  font-weight: 750;
  line-height: 1.25;
}

.base-header-extra {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  min-width: 0;
}

.base-header-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}

.base-header-icon-button,
.base-header-secondary-button,
.base-header-primary-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-width: 0;
  height: 36px;
  color: #4d6267;
  font-size: 0.73rem;
  font-weight: 850;
  line-height: 1;
  white-space: nowrap;
  border: 0;
  border-radius: 8px;
  cursor: pointer;
  transition:
    background 180ms ease,
    box-shadow 180ms ease,
    color 180ms ease,
    transform 180ms ease;
}

.base-header-icon-button {
  width: 36px;
  background: transparent;
}

.base-header-icon-button:hover,
.base-header-icon-button:focus-visible {
  color: var(--header-ink);
  background: rgb(238 248 250 / 84%);
}

.base-header-secondary-button {
  padding: 0 12px;
  background: #ffffff;
  box-shadow:
    inset 0 0 0 1px #e1e9eb,
    0 10px 24px rgb(27 40 44 / 4%);
}

.base-header-secondary-button:hover,
.base-header-secondary-button:focus-visible {
  color: var(--header-ink);
  background: #f8fcfd;
  box-shadow:
    inset 0 0 0 1px #d3e0e3,
    0 12px 28px rgb(27 40 44 / 7%);
}

.base-header-primary-button {
  padding: 0 14px;
  color: #ffffff;
  background: var(--header-accent-deep);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 24%),
    0 14px 28px rgb(15 87 83 / 18%);
}

.base-header-primary-button:hover,
.base-header-primary-button:focus-visible {
  background: #0b4946;
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 24%),
    0 16px 32px rgb(15 87 83 / 24%);
}

.base-header-icon-button:active,
.base-header-secondary-button:active,
.base-header-primary-button:active {
  transform: translateY(1px) scale(0.98);
}

.base-header-icon-button:focus-visible,
.base-header-secondary-button:focus-visible,
.base-header-primary-button:focus-visible {
  outline: 3px solid rgb(52 203 191 / 28%);
  outline-offset: 2px;
}

.has-notification::after {
  position: absolute;
  top: 11px;
  right: 10px;
  width: 5px;
  height: 5px;
  content: '';
  background: #ff4f67;
  border: 2px solid #ffffff;
  border-radius: 999px;
}

@media (prefers-reduced-motion: reduce) {
  .base-header-icon-button,
  .base-header-secondary-button,
  .base-header-primary-button {
    transition: none;
  }
}

@media (max-width: 880px) {
  .base-header {
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 14px;
    padding: 10px 18px;
  }

  .base-header::after {
    right: 18px;
    left: 18px;
  }

  .base-header-extra {
    display: none;
  }

  .base-header-actions {
    gap: 7px;
  }

  .base-header-secondary-button,
  .base-header-primary-button {
    width: 36px;
    padding: 0;
  }

  .base-header-secondary-button span,
  .base-header-primary-button span {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    overflow: hidden;
    white-space: nowrap;
    border: 0;
    clip: rect(0, 0, 0, 0);
  }
}

@media (max-width: 520px) {
  .base-header {
    grid-template-columns: minmax(0, 1fr);
    min-height: auto;
    padding: 14px 16px;
  }

  .base-header-actions {
    justify-content: flex-start;
    width: 100%;
  }

  .base-header-icon-button,
  .base-header-secondary-button,
  .base-header-primary-button {
    flex: 0 0 36px;
  }
}
</style>
