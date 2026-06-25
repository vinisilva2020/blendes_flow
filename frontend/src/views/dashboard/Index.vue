<script setup lang="ts">
import { computed } from 'vue'
import {
  Activity,
  AlertTriangle,
  ArrowRight,
  BarChart3,
  CheckCircle2,
  Clock3,
  GitBranch,
  LineChart,
  Sparkles,
  TrendingDown,
  TrendingUp,
  UsersRound,
  Workflow,
  Zap,
  type LucideIcon,
} from '@lucide/vue'

import { useWorkspaceStore } from '@/stores/workspace'

type IndicatorTone = 'good' | 'warning' | 'danger' | 'neutral'

type MetricCard = {
  change: string
  icon: LucideIcon
  label: string
  tone: IndicatorTone
  value: string
}

type WorkflowStatus = {
  id: number
  lastRun: string
  name: string
  owner: string
  progress: number
  status: 'Running' | 'Review' | 'Paused'
  tone: IndicatorTone
}

type WatchedMetric = {
  change: string
  label: string
  trend: 'up' | 'down'
  value: string
}

type MemberActivity = {
  initials: string
  name: string
  role: string
  status: string
  tone: IndicatorTone
}

type QueueItem = {
  due: string
  label: string
  meta: string
  tone: IndicatorTone
}

const workspaceStore = useWorkspaceStore()

const workspaceName = computed(() => workspaceStore.organizationName || 'Blendes workspace')

const metricCards: MetricCard[] = [
  {
    change: '+4 this week',
    icon: Workflow,
    label: 'Running workflows',
    tone: 'good',
    value: '16',
  },
  {
    change: '3 need a human pass',
    icon: AlertTriangle,
    label: 'Attention needed',
    tone: 'warning',
    value: '03',
  },
  {
    change: '+12.6% vs last cycle',
    icon: BarChart3,
    label: 'Tracked metrics',
    tone: 'good',
    value: '42',
  },
  {
    change: '8 active now',
    icon: UsersRound,
    label: 'Organization members',
    tone: 'neutral',
    value: '18',
  },
]

const workflowStatuses: WorkflowStatus[] = [
  {
    id: 1,
    lastRun: '12 min ago',
    name: 'Lead intake briefing',
    owner: 'Sales ops',
    progress: 84,
    status: 'Running',
    tone: 'good',
  },
  {
    id: 2,
    lastRun: '28 min ago',
    name: 'CRM reconciliation',
    owner: 'Automation',
    progress: 62,
    status: 'Review',
    tone: 'warning',
  },
  {
    id: 3,
    lastRun: '1 hour ago',
    name: 'Account health scan',
    owner: 'Customer success',
    progress: 91,
    status: 'Running',
    tone: 'good',
  },
  {
    id: 4,
    lastRun: 'Yesterday',
    name: 'Executive digest sync',
    owner: 'Leadership',
    progress: 38,
    status: 'Paused',
    tone: 'danger',
  },
]

const watchedMetrics: WatchedMetric[] = [
  {
    change: '+8.2%',
    label: 'Qualified conversion',
    trend: 'up',
    value: '37.8%',
  },
  {
    change: '-11 min',
    label: 'Average handoff delay',
    trend: 'down',
    value: '24m',
  },
  {
    change: '+126',
    label: 'Clean records created',
    trend: 'up',
    value: '1.8k',
  },
]

const memberActivity: MemberActivity[] = [
  {
    initials: 'VM',
    name: 'Vinicius Marques',
    role: 'Admin',
    status: 'Reviewing automations',
    tone: 'good',
  },
  {
    initials: 'MA',
    name: 'Marina Alves',
    role: 'Manager',
    status: 'Tuning metric targets',
    tone: 'neutral',
  },
  {
    initials: 'RS',
    name: 'Rafael Souza',
    role: 'Member',
    status: 'Waiting on handoff',
    tone: 'warning',
  },
]

const queueItems: QueueItem[] = [
  {
    due: '09:30',
    label: 'Approve CRM merge rules',
    meta: 'Blocks 2 workflows',
    tone: 'warning',
  },
  {
    due: '11:00',
    label: 'Publish executive digest',
    meta: 'Leadership channel',
    tone: 'good',
  },
  {
    due: '14:15',
    label: 'Refresh account risk model',
    meta: 'Customer success',
    tone: 'neutral',
  },
]

const activeWorkflows = computed(
  () => workflowStatuses.filter((workflow) => workflow.status === 'Running').length,
)

const healthScore = computed(() => 82)
</script>

<template>
  <section class="dashboard-page overview-page" aria-labelledby="overview-title">
    <div class="overview-shell">
      <header class="overview-hero">
        <div class="overview-title-block">
          <span class="overview-emblem" aria-hidden="true">
            <Sparkles :size="24" :stroke-width="2.35" />
          </span>

          <div>
            <p class="overview-kicker">Workspace pulse</p>
            <h2 id="overview-title">{{ workspaceName }} overview</h2>
            <p>
              A compact operating panel for live workflows, watched indicators, team capacity, and
              decisions waiting for a human pass.
            </p>
          </div>
        </div>

        <div class="overview-health-card" aria-label="Workspace health score">
          <div class="health-ring" :style="{ '--score': `${healthScore}%` }">
            <strong>{{ healthScore }}</strong>
            <span>health</span>
          </div>

          <div>
            <p class="overview-kicker">Live control</p>
            <strong>{{ activeWorkflows }} workflows running</strong>
            <small>Signal quality is stable across the current cycle.</small>
          </div>
        </div>
      </header>

      <div class="overview-metrics" aria-label="Workspace metrics">
        <article
          v-for="metric in metricCards"
          :key="metric.label"
          class="metric-card"
          :data-tone="metric.tone"
        >
          <span class="metric-icon" aria-hidden="true">
            <component :is="metric.icon" :size="18" :stroke-width="2.35" />
          </span>
          <span class="metric-label">{{ metric.label }}</span>
          <strong>{{ metric.value }}</strong>
          <small>{{ metric.change }}</small>
        </article>
      </div>

      <div class="overview-grid">
        <section class="overview-panel workflows-panel" aria-labelledby="workflow-status-title">
          <header class="panel-header">
            <div>
              <p class="overview-kicker">Current project</p>
              <h3 id="workflow-status-title">Workflow status</h3>
            </div>

            <RouterLink class="panel-link" to="/dashboard/workflows">
              See all
              <ArrowRight :size="14" :stroke-width="2.5" aria-hidden="true" />
            </RouterLink>
          </header>

          <div class="blend-track" aria-label="B.L.E.N.D.E.S execution phases">
            <span v-for="phase in ['B', 'L', 'E', 'N', 'D', 'E', 'S']" :key="phase">
              {{ phase }}
            </span>
          </div>

          <div class="workflow-list">
            <article
              v-for="workflow in workflowStatuses"
              :key="workflow.id"
              class="workflow-row"
              :data-tone="workflow.tone"
            >
              <div class="workflow-row-main">
                <span class="workflow-status-dot" aria-hidden="true"></span>
                <div>
                  <h4>{{ workflow.name }}</h4>
                  <p>{{ workflow.owner }} · {{ workflow.lastRun }}</p>
                </div>
              </div>

              <div class="workflow-row-progress">
                <span class="status-pill" :data-tone="workflow.tone">{{ workflow.status }}</span>
                <div class="progress-track" aria-hidden="true">
                  <span :style="{ width: `${workflow.progress}%` }"></span>
                </div>
              </div>
            </article>
          </div>
        </section>

        <section class="overview-panel metrics-panel" aria-labelledby="watched-metrics-title">
          <header class="panel-header">
            <div>
              <p class="overview-kicker">Indicators</p>
              <h3 id="watched-metrics-title">Watched metrics</h3>
            </div>
            <LineChart :size="19" :stroke-width="2.3" aria-hidden="true" />
          </header>

          <div class="metric-sparkline" aria-hidden="true">
            <span
              v-for="bar in [34, 48, 42, 64, 58, 72, 86]"
              :key="bar"
              :style="{ height: `${bar}%` }"
            ></span>
          </div>

          <div class="watched-list">
            <article v-for="metric in watchedMetrics" :key="metric.label" class="watched-row">
              <div>
                <strong>{{ metric.value }}</strong>
                <span>{{ metric.label }}</span>
              </div>

              <small :data-trend="metric.trend">
                <TrendingUp
                  v-if="metric.trend === 'up'"
                  :size="13"
                  :stroke-width="2.7"
                  aria-hidden="true"
                />
                <TrendingDown v-else :size="13" :stroke-width="2.7" aria-hidden="true" />
                {{ metric.change }}
              </small>
            </article>
          </div>
        </section>

        <section class="overview-panel members-panel" aria-labelledby="member-activity-title">
          <header class="panel-header">
            <div>
              <p class="overview-kicker">Team</p>
              <h3 id="member-activity-title">Members online</h3>
            </div>

            <RouterLink class="panel-link" to="/dashboard/members">
              Manage
              <ArrowRight :size="14" :stroke-width="2.5" aria-hidden="true" />
            </RouterLink>
          </header>

          <div class="member-list">
            <article v-for="member in memberActivity" :key="member.name" class="member-row">
              <span class="member-avatar">{{ member.initials }}</span>
              <div>
                <strong>{{ member.name }}</strong>
                <small>{{ member.role }} · {{ member.status }}</small>
              </div>
              <span class="member-presence" :data-tone="member.tone" aria-hidden="true"></span>
            </article>
          </div>
        </section>

        <section class="overview-panel queue-panel" aria-labelledby="queue-title">
          <header class="panel-header">
            <div>
              <p class="overview-kicker">Schedule</p>
              <h3 id="queue-title">Today queue</h3>
            </div>
            <Clock3 :size="19" :stroke-width="2.3" aria-hidden="true" />
          </header>

          <div class="queue-list">
            <article
              v-for="item in queueItems"
              :key="item.label"
              class="queue-row"
              :data-tone="item.tone"
            >
              <time>{{ item.due }}</time>
              <div>
                <strong>{{ item.label }}</strong>
                <span>{{ item.meta }}</span>
              </div>
            </article>
          </div>
        </section>

        <section class="overview-panel automation-panel" aria-labelledby="automation-title">
          <div class="automation-strip" aria-hidden="true">
            <span><GitBranch :size="15" :stroke-width="2.5" /></span>
            <span><Activity :size="15" :stroke-width="2.5" /></span>
            <span><Zap :size="15" :stroke-width="2.5" /></span>
            <span><CheckCircle2 :size="15" :stroke-width="2.5" /></span>
          </div>

          <div>
            <p class="overview-kicker">Signal route</p>
            <h3 id="automation-title">Next automation pass</h3>
            <p>
              Intake, reconciliation, enrichment, and publishing are aligned for the next scheduled
              run at 15:00.
            </p>
          </div>
        </section>
      </div>
    </div>
  </section>
</template>

<style scoped>
.overview-page {
  --overview-ink: #172224;
  --overview-muted: #667b80;
  --overview-soft: #eef8fa;
  --overview-line: rgb(18 33 36 / 11%);
  --overview-accent: #34cbbf;
  --overview-accent-deep: #0f5753;
  --overview-sky: #8adff3;
  --overview-amber: #f2b84b;
  --overview-rose: #d96666;
  --overview-lilac: #7567f2;

  min-width: 0;
  padding: 28px 30px 36px;
  color: var(--overview-ink);
}

.overview-shell {
  display: grid;
  gap: 18px;
  width: min(100%, 1320px);
}

.overview-hero,
.metric-card,
.overview-panel {
  background: rgb(255 255 255 / 88%);
  border: 1px solid var(--overview-line);
  box-shadow:
    0 18px 42px rgb(18 33 36 / 5%),
    inset 0 1px 0 rgb(255 255 255 / 86%);
}

.overview-hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(260px, 330px);
  align-items: stretch;
  gap: 16px;
  padding: 18px;
  border-radius: 12px;
}

.overview-title-block,
.overview-health-card,
.panel-header,
.workflow-row-main,
.member-row,
.automation-strip {
  display: flex;
  align-items: center;
  min-width: 0;
}

.overview-title-block {
  gap: 14px;
}

.overview-emblem {
  display: inline-grid;
  place-items: center;
  width: 62px;
  height: 62px;
  flex: 0 0 62px;
  color: #ffffff;
  background:
    linear-gradient(135deg, rgb(255 255 255 / 18%), transparent 42%),
    linear-gradient(145deg, #0d5d67, #34cbbf 58%, #f2b84b);
  border: 4px solid #ffffff;
  border-radius: 18px;
  box-shadow:
    0 18px 34px rgb(15 87 83 / 18%),
    0 0 0 1px #dbe8eb;
}

.overview-kicker {
  margin: 0;
  color: #246b78;
  font-size: 0.68rem;
  font-weight: 950;
  letter-spacing: 0.1em;
  line-height: 1;
  text-transform: uppercase;
}

.overview-title-block h2,
.overview-panel h3 {
  margin: 6px 0 0;
  color: var(--overview-ink);
  font-weight: 950;
  letter-spacing: 0;
  line-height: 1.08;
}

.overview-title-block h2 {
  font-size: clamp(1.35rem, 2.1vw, 1.9rem);
}

.overview-title-block p:not(.overview-kicker),
.automation-panel p {
  max-width: 690px;
  margin: 7px 0 0;
  color: var(--overview-muted);
  font-size: 0.86rem;
  font-weight: 700;
  line-height: 1.55;
}

.overview-health-card {
  justify-content: space-between;
  gap: 16px;
  padding: 14px;
  background: linear-gradient(135deg, rgb(238 248 250 / 92%), rgb(255 255 255 / 88%)), #ffffff;
  border: 1px solid #dce9ec;
  border-radius: 12px;
}

.overview-health-card strong {
  display: block;
  color: var(--overview-ink);
  font-size: 0.88rem;
  font-weight: 950;
  line-height: 1.2;
}

.overview-health-card small {
  display: block;
  margin-top: 5px;
  color: #70868b;
  font-size: 0.7rem;
  font-weight: 800;
  line-height: 1.4;
}

.health-ring {
  --score: 82%;

  display: grid;
  place-items: center;
  width: 92px;
  height: 92px;
  flex: 0 0 92px;
  color: var(--overview-accent-deep);
  background:
    radial-gradient(circle, #ffffff 0 56%, transparent 57%),
    conic-gradient(var(--overview-accent) var(--score), #e3edf0 0);
  border-radius: 999px;
  box-shadow: inset 0 0 0 1px #dce9ec;
}

.health-ring strong,
.health-ring span {
  grid-area: 1 / 1;
}

.health-ring strong {
  margin-top: -12px;
  font-size: 1.45rem;
  line-height: 1;
}

.health-ring span {
  margin-top: 30px;
  color: #789096;
  font-size: 0.62rem;
  font-weight: 950;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.overview-metrics {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
}

.metric-card {
  position: relative;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 7px 10px;
  min-height: 132px;
  padding: 14px;
  overflow: hidden;
  border-radius: 12px;
}

.metric-card::after {
  position: absolute;
  right: -24px;
  bottom: -34px;
  width: 96px;
  height: 96px;
  content: '';
  background: rgb(52 203 191 / 12%);
  border-radius: 999px;
}

.metric-card[data-tone='warning']::after {
  background: rgb(242 184 75 / 18%);
}

.metric-card[data-tone='danger']::after {
  background: rgb(217 102 102 / 14%);
}

.metric-icon {
  display: inline-grid;
  grid-row: span 2;
  place-items: center;
  width: 38px;
  height: 38px;
  color: var(--overview-accent-deep);
  background: #e9fbf7;
  border: 1px solid #ccefed;
  border-radius: 10px;
}

.metric-card[data-tone='warning'] .metric-icon {
  color: #8a5a04;
  background: #fff7e4;
  border-color: #f6dfaa;
}

.metric-card[data-tone='danger'] .metric-icon {
  color: #a93d3d;
  background: #fff0ef;
  border-color: #f3cfcc;
}

.metric-card[data-tone='neutral'] .metric-icon {
  color: #3e6472;
  background: #eef8fa;
  border-color: #d6e8ec;
}

.metric-label {
  align-self: end;
  min-width: 0;
  overflow: hidden;
  color: #70868b;
  font-size: 0.68rem;
  font-weight: 900;
  line-height: 1.1;
  text-overflow: ellipsis;
  text-transform: uppercase;
  white-space: nowrap;
}

.metric-card strong {
  z-index: 1;
  grid-column: 1 / -1;
  margin-top: 8px;
  color: var(--overview-ink);
  font-size: clamp(1.8rem, 3vw, 2.45rem);
  font-weight: 950;
  line-height: 0.95;
}

.metric-card small {
  z-index: 1;
  grid-column: 1 / -1;
  color: #70868b;
  font-size: 0.72rem;
  font-weight: 800;
  line-height: 1.3;
}

.overview-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) minmax(260px, 0.8fr) minmax(240px, 0.72fr);
  align-items: start;
  gap: 18px;
}

.overview-panel {
  min-width: 0;
  padding: 16px;
  border-radius: 12px;
}

.workflows-panel {
  grid-row: span 2;
}

.automation-panel {
  grid-column: 2 / -1;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  align-items: center;
  gap: 16px;
  overflow: hidden;
  background: linear-gradient(135deg, rgb(15 87 83 / 96%), rgb(13 93 103 / 92%)), #0f5753;
}

.automation-panel .overview-kicker,
.automation-panel h3,
.automation-panel p {
  color: #ffffff;
}

.automation-panel p {
  opacity: 0.74;
}

.automation-strip {
  gap: 8px;
}

.automation-strip span {
  display: inline-grid;
  place-items: center;
  width: 36px;
  height: 36px;
  color: #0f5753;
  background: rgb(255 255 255 / 92%);
  border-radius: 10px;
}

.panel-header {
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 14px;
}

.panel-header h3 {
  font-size: 1.02rem;
}

.panel-header > svg {
  color: #246b78;
}

.panel-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 32px;
  padding: 0 10px;
  color: #4d6267;
  font-size: 0.7rem;
  font-weight: 950;
  line-height: 1;
  text-decoration: none;
  white-space: nowrap;
  background: #ffffff;
  border: 1px solid #d8e6e9;
  border-radius: 8px;
  box-shadow: 0 10px 22px rgb(18 33 36 / 5%);
  transition:
    background 180ms ease,
    border-color 180ms ease,
    color 180ms ease,
    transform 180ms ease;
}

.panel-link:hover,
.panel-link:focus-visible {
  color: var(--overview-ink);
  background: #f7fcfd;
  border-color: #c8dce0;
}

.blend-track {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 6px;
  margin-bottom: 14px;
  padding: 6px;
  background: #f3fafb;
  border: 1px solid #dce9ec;
  border-radius: 10px;
}

.blend-track span {
  display: grid;
  place-items: center;
  min-height: 34px;
  color: #60777d;
  font-size: 0.7rem;
  font-weight: 950;
  background: #ffffff;
  border: 1px solid #e0ecef;
  border-radius: 8px;
}

.blend-track span:nth-child(-n + 5) {
  color: #ffffff;
  background: var(--overview-accent-deep);
  border-color: var(--overview-accent-deep);
}

.workflow-list,
.watched-list,
.member-list,
.queue-list {
  display: grid;
  gap: 10px;
}

.workflow-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(140px, 190px);
  align-items: center;
  gap: 14px;
  padding: 12px;
  background: #fbfeff;
  border: 1px solid #e2ecef;
  border-radius: 10px;
}

.workflow-row-main {
  gap: 10px;
}

.workflow-status-dot,
.member-presence {
  display: inline-block;
  width: 9px;
  height: 9px;
  flex: 0 0 9px;
  background: var(--overview-accent);
  border-radius: 999px;
  box-shadow: 0 0 0 4px rgb(52 203 191 / 14%);
}

.workflow-row[data-tone='warning'] .workflow-status-dot,
.member-presence[data-tone='warning'] {
  background: var(--overview-amber);
  box-shadow: 0 0 0 4px rgb(242 184 75 / 18%);
}

.workflow-row[data-tone='danger'] .workflow-status-dot {
  background: var(--overview-rose);
  box-shadow: 0 0 0 4px rgb(217 102 102 / 16%);
}

.workflow-row h4,
.workflow-row p,
.member-row strong,
.member-row small,
.queue-row strong,
.queue-row span {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.workflow-row h4 {
  margin: 0;
  color: var(--overview-ink);
  font-size: 0.82rem;
  font-weight: 950;
  line-height: 1.2;
}

.workflow-row p {
  margin: 4px 0 0;
  color: #70868b;
  font-size: 0.68rem;
  font-weight: 800;
  line-height: 1.3;
}

.workflow-row-progress {
  display: grid;
  gap: 8px;
}

.status-pill {
  justify-self: end;
  min-height: 24px;
  padding: 0 8px;
  color: var(--overview-accent-deep);
  font-size: 0.64rem;
  font-weight: 950;
  line-height: 24px;
  background: #e9fbf7;
  border: 1px solid #ccefed;
  border-radius: 999px;
}

.status-pill[data-tone='warning'] {
  color: #8a5a04;
  background: #fff7e4;
  border-color: #f6dfaa;
}

.status-pill[data-tone='danger'] {
  color: #a93d3d;
  background: #fff0ef;
  border-color: #f3cfcc;
}

.progress-track {
  height: 7px;
  overflow: hidden;
  background: #edf4f6;
  border-radius: 999px;
}

.progress-track span {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, var(--overview-accent-deep), var(--overview-accent));
  border-radius: inherit;
}

.metric-sparkline {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  align-items: end;
  gap: 7px;
  height: 108px;
  padding: 10px;
  background: linear-gradient(180deg, rgb(226 232 236 / 40%) 0 1px, transparent 1px 50%), #f7fcfd;
  border: 1px solid #dce9ec;
  border-radius: 10px;
}

.metric-sparkline span {
  min-height: 16px;
  background: linear-gradient(180deg, var(--overview-sky), var(--overview-accent-deep));
  border-radius: 999px 999px 4px 4px;
}

.watched-row,
.member-row,
.queue-row {
  min-width: 0;
  padding: 10px;
  background: #fbfeff;
  border: 1px solid #e2ecef;
  border-radius: 10px;
}

.watched-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.watched-row strong {
  display: block;
  color: var(--overview-ink);
  font-size: 0.92rem;
  font-weight: 950;
  line-height: 1.1;
}

.watched-row span {
  display: block;
  margin-top: 4px;
  color: #70868b;
  font-size: 0.68rem;
  font-weight: 800;
  line-height: 1.3;
}

.watched-row small {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--overview-accent-deep);
  font-size: 0.68rem;
  font-weight: 950;
  white-space: nowrap;
}

.watched-row small[data-trend='down'] {
  color: #7a5200;
}

.member-row {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  gap: 10px;
}

.member-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  flex: 0 0 40px;
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 950;
  line-height: 1;
  background: linear-gradient(145deg, #0d5d67, #34cbbf 62%, #f2b84b);
  border: 3px solid #ffffff;
  border-radius: 13px;
  box-shadow:
    0 12px 24px rgb(15 87 83 / 14%),
    0 0 0 1px #dbe8eb;
}

.member-row strong {
  display: block;
  color: var(--overview-ink);
  font-size: 0.78rem;
  font-weight: 950;
  line-height: 1.2;
}

.member-row small {
  display: block;
  margin-top: 4px;
  color: #70868b;
  font-size: 0.67rem;
  font-weight: 800;
  line-height: 1.3;
}

.member-presence[data-tone='neutral'] {
  background: #8aa0a5;
  box-shadow: 0 0 0 4px rgb(138 160 165 / 14%);
}

.queue-row {
  display: grid;
  grid-template-columns: 48px minmax(0, 1fr);
  gap: 10px;
}

.queue-row time {
  color: var(--overview-accent-deep);
  font-size: 0.7rem;
  font-weight: 950;
  line-height: 1.25;
}

.queue-row strong {
  display: block;
  color: var(--overview-ink);
  font-size: 0.78rem;
  font-weight: 950;
  line-height: 1.2;
}

.queue-row span {
  display: block;
  margin-top: 4px;
  color: #70868b;
  font-size: 0.67rem;
  font-weight: 800;
  line-height: 1.3;
}

.queue-row[data-tone='warning'] time {
  color: #8a5a04;
}

.panel-link:active {
  transform: scale(0.98);
}

.panel-link:focus-visible {
  outline: 3px solid rgb(52 203 191 / 28%);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  .panel-link {
    transition: none;
  }
}

@media (max-width: 1180px) {
  .overview-metrics {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .overview-grid {
    grid-template-columns: minmax(0, 1fr) minmax(260px, 0.82fr);
  }

  .automation-panel {
    grid-column: 1 / -1;
  }
}

@media (max-width: 900px) {
  .overview-hero,
  .overview-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .workflows-panel {
    grid-row: auto;
  }
}

@media (max-width: 760px) {
  .overview-page {
    padding: 20px 16px 28px;
  }

  .overview-title-block {
    align-items: flex-start;
  }

  .overview-emblem {
    width: 52px;
    height: 52px;
    flex-basis: 52px;
    border-radius: 16px;
  }

  .overview-metrics {
    grid-template-columns: minmax(0, 1fr);
  }

  .workflow-row {
    grid-template-columns: minmax(0, 1fr);
  }

  .workflow-row-progress {
    grid-template-columns: auto minmax(0, 1fr);
    align-items: center;
  }

  .status-pill {
    justify-self: start;
  }

  .automation-panel {
    grid-template-columns: minmax(0, 1fr);
  }
}

@media (max-width: 520px) {
  .overview-health-card,
  .panel-header,
  .watched-row {
    align-items: stretch;
    flex-direction: column;
  }

  .overview-health-card {
    display: grid;
  }

  .panel-link {
    width: fit-content;
  }

  .blend-track {
    gap: 4px;
  }
}
</style>
