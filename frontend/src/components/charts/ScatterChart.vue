<script setup>
import { Scatter } from 'vue-chartjs'
</script>

<template>
  <div class="chart-container">
    <scatter
      id="scatter-chart-id"
      :options="chartOptions"
      :data="data"
    />
  </div>
</template>

<script>
export default {
  components: {
    Scatter
  },
  props: ['data', 'chartOptions']
}
</script>

<style scoped src="@/assets/chart.css">
</style>
