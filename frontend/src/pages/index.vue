<script setup lang="ts">
  import ResultsDisplay from '@/components/Results.vue'
  import Start from '@/components/Start.vue'
  import { useStore } from '@/stores/app'

  const store = useStore()
</script>

<template>
  <ResultsDisplay v-if="store.analysisResult" />
  <Start v-else />
</template>
