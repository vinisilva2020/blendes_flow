<script setup lang="ts">
import { computed, shallowRef } from 'vue'
import {
  Activity,
  ArrowRight,
  CheckCircle2,
  Clock3,
  Layers3,
  Play,
  Plus,
  Workflow,
  X,
} from '@lucide/vue'

type WorkflowPhase = 'B' | 'L' | 'E' | 'N' | 'D' | 'E2' | 'S'

type WorkflowCard = {
  description: string
  id: number
  intent: string
  lastRun: string
  phase: WorkflowPhase
  phaseLabel: string
  preview: string[]
  runLabel: string
  title: string
}

const workflows: WorkflowCard[] = [
  {
    description:
      'Qualifica sinais novos, cruza fonte do lead e prepara o primeiro bloco de contexto comercial.',
    id: 1,
    intent: 'Transformar entradas soltas em oportunidades com contexto suficiente para abordagem.',
    lastRun: '12 min ago',
    phase: 'B',
    phaseLabel: 'Brief',
    preview: ['Coletar origem', 'Normalizar contato', 'Classificar urgencia', 'Criar briefing'],
    runLabel: 'Run brief',
    title: 'Lead intake briefing',
  },
  {
    description:
      'Limpa dados duplicados, padroniza campos e destaca lacunas antes da transferencia para vendas.',
    id: 2,
    intent: 'Reduzir retrabalho entre captacao e validacao usando uma leitura unica dos dados.',
    lastRun: '28 min ago',
    phase: 'L',
    phaseLabel: 'Link',
    preview: ['Buscar duplicatas', 'Vincular empresa', 'Checar proprietario', 'Enviar resumo'],
    runLabel: 'Run link',
    title: 'CRM reconciliation',
  },
  {
    description:
      'Enriquece contas ativas com sinais de produto, tickets recentes e historico de relacionamento.',
    id: 3,
    intent: 'Dar ao time de sucesso uma leitura rapida do estado real de cada conta.',
    lastRun: '1 hour ago',
    phase: 'E',
    phaseLabel: 'Enrich',
    preview: ['Ler uso recente', 'Analisar tickets', 'Marcar risco', 'Atualizar perfil'],
    runLabel: 'Run enrich',
    title: 'Account health scan',
  },
  {
    description:
      'Notifica responsaveis quando uma execucao critica exige revisao humana antes do proximo passo.',
    id: 4,
    intent: 'Manter decisoes sensiveis sob controle sem pausar todo o fluxo operacional.',
    lastRun: '2 hours ago',
    phase: 'N',
    phaseLabel: 'Notify',
    preview: ['Detectar excecao', 'Preparar contexto', 'Notificar dono', 'Aguardar retorno'],
    runLabel: 'Run notify',
    title: 'Approval handoff',
  },
  {
    description:
      'Despacha tarefas aprovadas para os canais internos certos e registra o estado da execucao.',
    id: 5,
    intent: 'Garantir que cada equipe receba apenas o que pode executar agora.',
    lastRun: 'Today, 09:41',
    phase: 'D',
    phaseLabel: 'Dispatch',
    preview: ['Definir canal', 'Enviar payload', 'Gravar evento', 'Confirmar entrega'],
    runLabel: 'Run dispatch',
    title: 'Ops task routing',
  },
  {
    description:
      'Executa atualizacoes finais em documentos, resumos e campos de status depois da conclusao.',
    id: 6,
    intent: 'Fechar a execucao com rastreabilidade, clareza de status e historico consultavel.',
    lastRun: 'Yesterday',
    phase: 'E2',
    phaseLabel: 'Execute',
    preview: ['Aplicar mudancas', 'Validar saida', 'Salvar resumo', 'Emitir auditoria'],
    runLabel: 'Run execute',
    title: 'Closeout writer',
  },
  {
    description:
      'Sincroniza resultados com dashboards, relatorios e alertas para manter a organizacao alinhada.',
    id: 7,
    intent: 'Distribuir o resultado da execucao para leitura, acompanhamento e tomada de decisao.',
    lastRun: 'Jun 23, 2026',
    phase: 'S',
    phaseLabel: 'Sync',
    preview: ['Publicar metricas', 'Atualizar dashboard', 'Enviar digest', 'Arquivar log'],
    runLabel: 'Run sync',
    title: 'Executive digest sync',
  },
]

const selectedWorkflow = shallowRef<WorkflowCard | null>(null)
const runningWorkflowId = shallowRef<number | null>(null)

const activeWorkflow = computed<WorkflowCard>(() => selectedWorkflow.value ?? workflows[0]!)

function openWorkflow(workflow: WorkflowCard) {
  selectedWorkflow.value = workflow
}

function closeWorkflow() {
  selectedWorkflow.value = null
}

function runWorkflow(workflow: WorkflowCard) {
  runningWorkflowId.value = workflow.id
  window.setTimeout(() => {
    if (runningWorkflowId.value === workflow.id) {
      runningWorkflowId.value = null
    }
  }, 900)
}
</script>

<template>
  <section class="dashboard-page workflows-page" aria-labelledby="workflows-title">
    <div class="workflows-shell">
      <header class="workflows-hero">
        <div class="workflows-title-block">
          <span class="workflows-emblem" aria-hidden="true">
            <Workflow :size="25" :stroke-width="2.25" />
          </span>

          <div>
            <p class="workflows-kicker">Organization flows</p>
            <h2 id="workflows-title">Active workflows</h2>
            <p>
              Follow each live execution across the B.L.E.N.D.E.S phases and open a preview before
              running the next pass.
            </p>
          </div>
        </div>

        <div class="workflows-phase-strip" aria-label="Workflow phases">
          <span v-for="phase in ['B', 'L', 'E', 'N', 'D', 'E', 'S']" :key="phase">
            {{ phase }}
          </span>
        </div>
      </header>

      <div class="workflow-grid" aria-live="polite">
        <article
          v-for="workflow in workflows"
          :key="workflow.id"
          class="workflow-card"
          :class="{ 'is-selected': selectedWorkflow?.id === workflow.id }"
          tabindex="0"
          role="button"
          :aria-label="`Open preview for ${workflow.title}`"
          @click="openWorkflow(workflow)"
          @keydown.enter.prevent="openWorkflow(workflow)"
          @keydown.space.prevent="openWorkflow(workflow)"
        >
          <div class="workflow-card-body">
            <header class="workflow-card-header">
              <span class="phase-token" :data-phase="workflow.phase">
                {{ workflow.phase === 'E2' ? 'E' : workflow.phase }}
              </span>
              <div>
                <p>{{ workflow.phaseLabel }}</p>
                <h3>{{ workflow.title }}</h3>
              </div>
            </header>

            <p class="workflow-description">{{ workflow.description }}</p>
          </div>

          <footer class="workflow-card-footer">
            <span class="workflow-run-meta">
              <Clock3 :size="14" :stroke-width="2.45" aria-hidden="true" />
              {{ workflow.lastRun }}
            </span>

            <button class="workflow-run-button" type="button" @click.stop="runWorkflow(workflow)">
              <Play :size="14" :stroke-width="2.8" aria-hidden="true" />
              {{ runningWorkflowId === workflow.id ? 'Running' : 'Run' }}
            </button>
          </footer>
        </article>

        <button class="workflow-card workflow-create-card" type="button">
          <span class="workflow-create-mark" aria-hidden="true">
            <Plus :size="34" :stroke-width="2.35" />
          </span>

          <span class="workflow-create-copy">
            <span class="workflows-kicker">New workflow</span>
            <strong>Create execution</strong>
            <small>Start a fresh B.L.E.N.D.E.S flow for a team process or recurring task.</small>
          </span>

          <span class="workflow-create-action">
            Start draft
            <ArrowRight :size="14" :stroke-width="2.5" aria-hidden="true" />
          </span>
        </button>
      </div>
    </div>

    <Teleport to="body">
      <Transition name="workflow-drawer">
        <div
          v-if="selectedWorkflow"
          class="workflow-drawer-backdrop"
          role="presentation"
          @click.self="closeWorkflow"
        >
          <aside
            class="workflow-drawer"
            role="dialog"
            aria-modal="true"
            :aria-labelledby="`workflow-preview-${activeWorkflow.id}`"
          >
            <header class="drawer-header">
              <div class="drawer-title">
                <span class="phase-token is-large" :data-phase="activeWorkflow.phase">
                  {{ activeWorkflow.phase === 'E2' ? 'E' : activeWorkflow.phase }}
                </span>
                <div>
                  <p class="workflows-kicker">{{ activeWorkflow.phaseLabel }} preview</p>
                  <h2 :id="`workflow-preview-${activeWorkflow.id}`">
                    {{ activeWorkflow.title }}
                  </h2>
                </div>
              </div>

              <button
                class="drawer-close-button"
                type="button"
                aria-label="Close preview"
                @click="closeWorkflow"
              >
                <X :size="17" :stroke-width="2.45" aria-hidden="true" />
              </button>
            </header>

            <section class="drawer-intent" aria-label="Execution intent">
              <span>
                <Activity :size="17" :stroke-width="2.35" aria-hidden="true" />
              </span>
              <div>
                <strong>Execution intent</strong>
                <p>{{ activeWorkflow.intent }}</p>
              </div>
            </section>

            <section class="drawer-preview" aria-label="Execution preview">
              <div class="drawer-section-heading">
                <p class="workflows-kicker">Preview path</p>
                <span>{{ activeWorkflow.preview.length }} steps</span>
              </div>

              <ol class="preview-steps">
                <li v-for="(step, index) in activeWorkflow.preview" :key="step">
                  <span>{{ index + 1 }}</span>
                  <strong>{{ step }}</strong>
                  <ArrowRight :size="15" :stroke-width="2.45" aria-hidden="true" />
                </li>
              </ol>
            </section>

            <section class="drawer-signal" aria-label="Workflow signal">
              <div>
                <Layers3 :size="17" :stroke-width="2.35" aria-hidden="true" />
                <span>Ready to run</span>
              </div>
              <div>
                <CheckCircle2 :size="17" :stroke-width="2.35" aria-hidden="true" />
                <span>Inputs validated</span>
              </div>
            </section>

            <footer class="drawer-actions">
              <button class="drawer-secondary-button" type="button" @click="closeWorkflow">
                Close preview
              </button>
              <button
                class="workflow-run-button is-drawer"
                type="button"
                @click="runWorkflow(activeWorkflow)"
              >
                <Play :size="14" :stroke-width="2.8" aria-hidden="true" />
                {{ runningWorkflowId === activeWorkflow.id ? 'Running' : activeWorkflow.runLabel }}
              </button>
            </footer>
          </aside>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<style scoped>
.workflows-page {
  --workflow-ink: #172224;
  --workflow-muted: #667b80;
  --workflow-line: rgb(18 33 36 / 11%);
  --workflow-accent: #34cbbf;
  --workflow-accent-deep: #0f5753;
  --workflow-amber: #f2b84b;
  --workflow-blue: #8adff3;
  --workflow-lilac: #7567f2;

  min-width: 0;
  padding: 28px 30px 36px;
  color: var(--workflow-ink);
}

.workflows-shell {
  display: grid;
  gap: 18px;
  width: min(100%, 1280px);
}

.workflows-hero,
.workflow-card {
  border: 1px solid var(--workflow-line);
  background: rgb(255 255 255 / 88%);
  box-shadow:
    0 18px 42px rgb(18 33 36 / 5%),
    inset 0 1px 0 rgb(255 255 255 / 86%);
}

.workflows-hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  padding: 18px;
  overflow: hidden;
  border-radius: 12px;
}

.workflows-title-block,
.workflow-card-header,
.drawer-title {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.workflows-emblem {
  display: inline-grid;
  place-items: center;
  width: 62px;
  height: 62px;
  flex: 0 0 62px;
  color: #ffffff;
  background:
    radial-gradient(circle at 74% 22%, #aeeeff 0 12%, transparent 13%),
    linear-gradient(145deg, #0d5d67, #34cbbf 58%, #f2b84b);
  border: 4px solid #ffffff;
  border-radius: 18px;
  box-shadow:
    0 18px 34px rgb(15 87 83 / 18%),
    0 0 0 1px #dbe8eb;
}

.workflows-kicker,
.workflow-card-header p {
  margin: 0;
  color: #246b78;
  font-size: 0.68rem;
  font-weight: 950;
  letter-spacing: 0.1em;
  line-height: 1;
  text-transform: uppercase;
}

.workflows-title-block h2,
.workflow-card-header h3,
.drawer-header h2 {
  margin: 6px 0 0;
  color: var(--workflow-ink);
  font-weight: 950;
  letter-spacing: 0;
  line-height: 1.08;
}

.workflows-title-block h2 {
  font-size: clamp(1.35rem, 2.1vw, 1.9rem);
}

.workflows-title-block p:not(.workflows-kicker) {
  max-width: 680px;
  margin: 7px 0 0;
  color: var(--workflow-muted);
  font-size: 0.86rem;
  font-weight: 700;
  line-height: 1.55;
}

.workflows-phase-strip {
  display: grid;
  grid-template-columns: repeat(7, 28px);
  gap: 5px;
  padding: 6px;
  background: #f3fafb;
  border: 1px solid #dce9ec;
  border-radius: 10px;
}

.workflows-phase-strip span {
  display: inline-grid;
  place-items: center;
  width: 28px;
  height: 28px;
  color: #246b78;
  font-size: 0.72rem;
  font-weight: 950;
  background: #ffffff;
  border: 1px solid #d8e6e9;
  border-radius: 7px;
}

.workflow-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.workflow-card {
  display: grid;
  grid-template-rows: minmax(0, 1fr) auto;
  min-height: 218px;
  overflow: hidden;
  border-radius: 12px;
  cursor: pointer;
  transition:
    border-color 180ms ease,
    box-shadow 180ms ease,
    transform 180ms ease;
}

.workflow-card:hover,
.workflow-card:focus-visible,
.workflow-card.is-selected {
  border-color: #c7e7e9;
  outline: 0;
}

.workflow-create-card {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  min-height: 218px;
  padding: 16px;
  color: var(--workflow-ink);
  text-align: center;
  background: linear-gradient(135deg, rgb(243 250 251 / 76%), rgb(255 255 255 / 88%)), #ffffff;
  border-style: dashed;
}

.workflow-create-card:hover,
.workflow-create-card:focus-visible {
  background: linear-gradient(135deg, rgb(235 250 248 / 92%), rgb(255 255 255 / 92%)), #ffffff;
}

.workflow-create-mark {
  display: inline-grid;
  place-items: center;
  width: 84px;
  height: 84px;
  flex: 0 0 84px;
  color: #62777d;
  background: rgb(255 255 255 / 72%);
  border: 1px dashed #b9d1d7;
  border-radius: 16px;
  box-shadow:
    0 14px 32px rgb(15 44 43 / 7%),
    inset 0 1px 0 rgb(255 255 255 / 86%);
  transition:
    background 180ms ease,
    border-color 180ms ease,
    color 180ms ease;
}

.workflow-create-card:hover .workflow-create-mark,
.workflow-create-card:focus-visible .workflow-create-mark {
  color: #246b78;
  background: #ffffff;
  border-color: #8adff3;
}

.workflow-create-copy {
  display: grid;
  justify-items: center;
  gap: 7px;
  min-width: 0;
}

.workflow-create-copy strong,
.workflow-create-copy small,
.workflow-create-action {
  display: block;
}

.workflow-create-copy strong {
  color: var(--workflow-ink);
  font-size: 1rem;
  font-weight: 950;
  line-height: 1.15;
}

.workflow-create-copy small {
  max-width: 250px;
  color: #7a8f94;
  font-size: 0.76rem;
  font-weight: 800;
  line-height: 1.45;
}

.workflow-create-action {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  color: #246b78;
  font-size: 0.7rem;
  font-weight: 950;
  line-height: 1;
  opacity: 0;
  transition: opacity 180ms ease;
}

.workflow-create-card:hover .workflow-create-action,
.workflow-create-card:focus-visible .workflow-create-action {
  opacity: 1;
}

.workflow-card-body {
  display: grid;
  align-content: start;
  gap: 18px;
  padding: 16px 16px 14px;
}

.workflow-card-header {
  align-items: flex-start;
}

.workflow-card-header h3 {
  display: -webkit-box;
  overflow: hidden;
  font-size: 0.96rem;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.phase-token {
  display: inline-grid;
  place-items: center;
  width: 42px;
  height: 42px;
  flex: 0 0 42px;
  color: #ffffff;
  font-size: 1rem;
  font-weight: 950;
  line-height: 1;
  background: linear-gradient(145deg, #0d5d67, #34cbbf 58%, #f2b84b);
  border: 3px solid #ffffff;
  border-radius: 13px;
  box-shadow:
    0 12px 24px rgb(15 87 83 / 14%),
    0 0 0 1px #dbe8eb;
}

.phase-token[data-phase='L'],
.phase-token[data-phase='D'] {
  background: linear-gradient(145deg, #194d72, #8adff3 62%, #34cbbf);
}

.phase-token[data-phase='N'],
.phase-token[data-phase='S'] {
  background: linear-gradient(145deg, #463e90, #7567f2 54%, #f2b84b);
}

.phase-token.is-large {
  width: 54px;
  height: 54px;
  flex-basis: 54px;
  border-radius: 16px;
}

.workflow-description {
  display: -webkit-box;
  margin: 0;
  overflow: hidden;
  color: var(--workflow-muted);
  font-size: 0.78rem;
  font-weight: 750;
  line-height: 1.55;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 4;
}

.workflow-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 14px;
  background: linear-gradient(180deg, #fbfeff, #f5fbfc);
  border-top: 1px solid #e2ecef;
}

.workflow-run-meta {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-width: 0;
  overflow: hidden;
  color: #70868b;
  font-size: 0.68rem;
  font-weight: 850;
  line-height: 1;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.workflow-run-button,
.drawer-secondary-button,
.drawer-close-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: 0;
  cursor: pointer;
  transition:
    border-color 180ms ease,
    background 180ms ease,
    box-shadow 180ms ease,
    color 180ms ease,
    transform 180ms ease;
}

.workflow-run-button {
  min-height: 34px;
  padding: 0 12px;
  color: #ffffff;
  font-size: 0.72rem;
  font-weight: 950;
  line-height: 1;
  background: var(--workflow-accent-deep);
  border: 1px solid #0f5753;
  border-radius: 8px;
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 22%),
    0 12px 22px rgb(15 87 83 / 16%);
}

.workflow-run-button:hover,
.workflow-run-button:focus-visible {
  background: #0b4946;
}

.workflow-run-button.is-drawer {
  min-height: 38px;
}

.workflow-drawer-backdrop {
  --workflow-ink: #172224;
  --workflow-muted: #667b80;
  --workflow-line: rgb(18 33 36 / 11%);
  --workflow-accent: #34cbbf;
  --workflow-accent-deep: #0f5753;
  --workflow-amber: #f2b84b;

  position: fixed;
  inset: 0;
  z-index: 60;
  display: flex;
  justify-content: flex-end;
  padding: 14px;
  background: rgb(7 17 19 / 34%);
  backdrop-filter: blur(10px);
}

.workflow-drawer {
  box-sizing: border-box;
  display: grid;
  grid-template-rows: auto auto minmax(0, 1fr) auto auto;
  gap: 16px;
  width: min(100%, 460px);
  height: 100%;
  padding: 18px;
  overflow: auto;
  color: var(--workflow-ink);
  background: #ffffff;
  border: 1px solid rgb(255 255 255 / 68%);
  border-radius: 14px;
  box-shadow:
    0 28px 80px rgb(7 17 19 / 24%),
    inset 0 1px 0 rgb(255 255 255 / 86%);
}

.drawer-header,
.drawer-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.drawer-header h2 {
  font-size: 1.15rem;
}

.drawer-close-button {
  width: 34px;
  height: 34px;
  flex: 0 0 34px;
  color: #647b80;
  background: #ffffff;
  border: 1px solid #d8e6e9;
  border-radius: 8px;
}

.drawer-close-button:hover,
.drawer-close-button:focus-visible,
.drawer-secondary-button:hover,
.drawer-secondary-button:focus-visible {
  color: var(--workflow-ink);
  background: #f7fcfd;
  border-color: #c8dce0;
}

.drawer-intent {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr);
  gap: 12px;
  padding: 14px;
  background: linear-gradient(135deg, #f4fcfc, #ffffff 74%);
  border: 1px solid #dce9ec;
  border-radius: 12px;
}

.drawer-intent > span {
  display: inline-grid;
  place-items: center;
  width: 38px;
  height: 38px;
  color: var(--workflow-accent-deep);
  background: #e7fbf8;
  border-radius: 10px;
  box-shadow: inset 0 0 0 1px #c9f0eb;
}

.drawer-intent strong {
  display: block;
  color: var(--workflow-ink);
  font-size: 0.8rem;
  font-weight: 950;
  line-height: 1.2;
}

.drawer-intent p {
  margin: 5px 0 0;
  color: var(--workflow-muted);
  font-size: 0.75rem;
  font-weight: 750;
  line-height: 1.5;
}

.drawer-preview {
  display: grid;
  align-content: start;
  gap: 12px;
  min-height: 0;
}

.drawer-section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.drawer-section-heading span {
  color: #70868b;
  font-size: 0.68rem;
  font-weight: 900;
}

.preview-steps {
  display: grid;
  gap: 9px;
  padding: 0;
  margin: 0;
  list-style: none;
}

.preview-steps li {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 10px;
  min-height: 44px;
  padding: 0 12px;
  color: #4f666c;
  background: #fbfeff;
  border: 1px solid #e2ecef;
  border-radius: 10px;
}

.preview-steps li > span {
  display: inline-grid;
  place-items: center;
  width: 24px;
  height: 24px;
  color: var(--workflow-accent-deep);
  font-size: 0.66rem;
  font-weight: 950;
  background: #e9fbf7;
  border: 1px solid #ccefed;
  border-radius: 7px;
}

.preview-steps strong {
  overflow: hidden;
  color: var(--workflow-ink);
  font-size: 0.75rem;
  font-weight: 900;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.preview-steps svg {
  color: #789096;
}

.drawer-signal {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 9px;
}

.drawer-signal div {
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 38px;
  padding: 0 11px;
  color: #246b78;
  font-size: 0.7rem;
  font-weight: 900;
  background: #f3fafb;
  border: 1px solid #dce9ec;
  border-radius: 9px;
}

.drawer-secondary-button {
  min-height: 38px;
  padding: 0 13px;
  color: #4d6267;
  font-size: 0.76rem;
  font-weight: 950;
  line-height: 1;
  background: #ffffff;
  border: 1px solid #d8e6e9;
  border-radius: 8px;
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / 92%),
    0 10px 22px rgb(18 33 36 / 5%);
}

.workflow-run-button:active,
.drawer-secondary-button:active,
.drawer-close-button:active,
.workflow-card:active {
  transform: scale(0.98);
}

.workflow-run-button:focus-visible,
.drawer-secondary-button:focus-visible,
.drawer-close-button:focus-visible {
  outline: 3px solid rgb(52 203 191 / 28%);
  outline-offset: 2px;
}

.workflow-drawer-enter-active,
.workflow-drawer-leave-active {
  transition: opacity 180ms ease;
}

.workflow-drawer-enter-active .workflow-drawer,
.workflow-drawer-leave-active .workflow-drawer {
  transition:
    transform 210ms ease,
    opacity 180ms ease;
}

.workflow-drawer-enter-from,
.workflow-drawer-leave-to {
  opacity: 0;
}

.workflow-drawer-enter-from .workflow-drawer,
.workflow-drawer-leave-to .workflow-drawer {
  opacity: 0;
  transform: translateX(18px);
}

@media (prefers-reduced-motion: reduce) {
  .workflow-card,
  .workflow-run-button,
  .drawer-secondary-button,
  .drawer-close-button,
  .workflow-drawer-enter-active,
  .workflow-drawer-leave-active,
  .workflow-drawer-enter-active .workflow-drawer,
  .workflow-drawer-leave-active .workflow-drawer {
    transition: none;
  }

  .workflow-card:hover,
  .workflow-card:focus-visible,
  .workflow-card.is-selected,
  .workflow-drawer-enter-from .workflow-drawer,
  .workflow-drawer-leave-to .workflow-drawer {
    transform: none;
  }
}

@media (max-width: 1120px) {
  .workflow-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 920px) {
  .workflows-hero {
    align-items: stretch;
    flex-direction: column;
  }

  .workflows-phase-strip {
    width: max-content;
  }
}

@media (max-width: 760px) {
  .workflows-page {
    padding: 20px 16px 28px;
  }

  .workflow-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .workflows-title-block {
    align-items: flex-start;
  }

  .workflows-emblem {
    width: 52px;
    height: 52px;
    flex-basis: 52px;
    border-radius: 16px;
  }
}

@media (max-width: 560px) {
  .workflow-drawer-backdrop {
    align-items: end;
    padding: 10px;
  }

  .workflow-drawer {
    width: 100%;
    height: min(92vh, 760px);
    border-radius: 14px 14px 10px 10px;
  }

  .drawer-header,
  .drawer-actions,
  .workflow-card-footer {
    align-items: stretch;
    flex-direction: column;
  }

  .drawer-signal {
    grid-template-columns: minmax(0, 1fr);
  }

  .workflow-run-button,
  .drawer-secondary-button {
    width: 100%;
  }
}
</style>
