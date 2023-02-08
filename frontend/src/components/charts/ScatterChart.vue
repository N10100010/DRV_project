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
.chart-container {
 position: relative;
  margin: auto;
  height: 100%;
  width: 100%;
}
</style>