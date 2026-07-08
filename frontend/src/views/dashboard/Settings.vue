<script setup lang="ts">
import DashboardLayout from '@/layouts/DashboardLayout.vue'

import SystemPreferencesCard from './components/SystemPreferencesCard.vue'
</script>

<template>
  <DashboardLayout>
    <div class="mx-auto flex w-full max-w-5xl flex-col gap-5">
      <SystemPreferencesCard />
    </div>
  </DashboardLayout>
</template>
