<script setup>
import { Scatter } from 'vue-chartjs'
</script>

<template>
  <div class="chart-container">
    <scatter
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

<style>
.chart-container > canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>