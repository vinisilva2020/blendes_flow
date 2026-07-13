<script setup lang="ts">
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import OrganizationMapCard from './components/OrganizationMapCard.vue'
</script>

<template>
  <DashboardLayout>
    <div class="flex min-h-0 w-full flex-col gap-6">
      <OrganizationMapCard />
      <section
        class="grid grid-cols-1 gap-4 lg:grid-cols-2"
        aria-label="Dashboard content sections"
      >
        <article
          class="rounded-xl border border-slate-200/70 bg-white px-4 py-4 text-slate-950 shadow-[0_10px_28px_rgb(15_23_42_/_0.04)] transition-[background-color,border-color,color,box-shadow] duration-200 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-50 dark:shadow-[0_18px_42px_rgb(0_0_0_/_24%)]"
          aria-labelledby="facet-risk-heat-map-title"
        >
          <header class="mb-3">
            <h2
              id="facet-risk-heat-map-title"
              class="text-sm leading-none font-semibold text-slate-950 dark:text-slate-50"
            >
              Facet Mapping by Risk
            </h2>
          </header>

          <div class="mt-4 h-px bg-slate-200/70 dark:bg-slate-800" aria-hidden="true"></div>
        </article>

        <article
          class="rounded-xl border border-slate-200/70 bg-white px-4 py-4 text-slate-950 shadow-[0_10px_28px_rgb(15_23_42_/_0.04)] transition-[background-color,border-color,color,box-shadow] duration-200 dark:border-slate-800 dark:bg-slate-900 dark:text-slate-50 dark:shadow-[0_18px_42px_rgb(0_0_0_/_24%)]"
          aria-labelledby="change-signals-title"
        >
          <header class="mb-3">
            <h2
              id="change-signals-title"
              class="text-sm leading-none font-semibold text-slate-950 dark:text-slate-50"
            >
              Mixpoints - signs of change
            </h2>
          </header>

          <div class="mt-4 h-px bg-slate-200/70 dark:bg-slate-800" aria-hidden="true"></div>

          <div class="mt-5"></div>
        </article>
      </section>
    </div>
  </DashboardLayout>
</template>
