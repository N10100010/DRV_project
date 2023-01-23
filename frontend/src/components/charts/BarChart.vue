<script setup>
import {Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import { Bar } from 'vue-chartjs'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
</script>

<template>
  <div class="chart-container">
    <Bar
      :options="chartOptions"
      :data="data"
    />
  </div>
</template>

<script>
export default {
  props: ['data', 'chartOptions']
}
</script>
