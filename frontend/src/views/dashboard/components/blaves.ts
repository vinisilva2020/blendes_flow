import type { BlaveMovementName, BlaveMovementStatus } from '@/domains/blaves/contracts'

export type MovementMeta = {
  accentClass: string
  description: string
  key: BlaveMovementName
  label: string
  letter: string
}

export const movementOrder: BlaveMovementName[] = [
  'BOUNDGROUND',
  'LABOR',
  'ECHO',
  'NOISECATCH',
  'DRAWBRIDGE',
  'ENHANCE',
  'SIGHTLINE',
]

export const movementMeta: Record<BlaveMovementName, MovementMeta> = {
  BOUNDGROUND: {
    accentClass:
      'border-cyan-200 bg-cyan-50 text-cyan-700 dark:border-cyan-300/30 dark:bg-cyan-400/10 dark:text-cyan-200',
    description: 'Defines the operating boundary and the first usable scope.',
    key: 'BOUNDGROUND',
    label: 'Boundground',
    letter: 'B',
  },
  LABOR: {
    accentClass:
      'border-indigo-200 bg-indigo-50 text-indigo-700 dark:border-indigo-300/30 dark:bg-indigo-400/10 dark:text-indigo-200',
    description: 'Maps the work chapters, actors, and execution context.',
    key: 'LABOR',
    label: 'Labor',
    letter: 'L',
  },
  ECHO: {
    accentClass:
      'border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-300/30 dark:bg-emerald-400/10 dark:text-emerald-200',
    description: 'Turns observations into facet descriptions and risks.',
    key: 'ECHO',
    label: 'Echo',
    letter: 'E',
  },
  NOISECATCH: {
    accentClass:
      'border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-300/30 dark:bg-amber-400/10 dark:text-amber-200',
    description: 'Captures signal loss, weak spots, and operational noise.',
    key: 'NOISECATCH',
    label: 'Noisecatch',
    letter: 'N',
  },
  DRAWBRIDGE: {
    accentClass:
      'border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-300/30 dark:bg-rose-400/10 dark:text-rose-200',
    description: 'Prioritizes risks and decides what must be crossed first.',
    key: 'DRAWBRIDGE',
    label: 'Drawbridge',
    letter: 'D',
  },
  ENHANCE: {
    accentClass:
      'border-violet-200 bg-violet-50 text-violet-700 dark:border-violet-300/30 dark:bg-violet-400/10 dark:text-violet-200',
    description: 'Connects practices and concrete actions to the selected risks.',
    key: 'ENHANCE',
    label: 'Enhance',
    letter: 'E',
  },
  SIGHTLINE: {
    accentClass:
      'border-slate-300 bg-slate-100 text-slate-800 dark:border-slate-600 dark:bg-slate-800 dark:text-slate-200',
    description: 'Tracks mixpoints and the visible signs of change.',
    key: 'SIGHTLINE',
    label: 'Sightline',
    letter: 'S',
  },
}

export const movementStatusLabels: Record<BlaveMovementStatus, string> = {
  ACTIVE: 'Active',
  COMPLETED: 'Completed',
  INVALIDATED: 'Invalidated',
  LOCKED: 'Locked',
}
