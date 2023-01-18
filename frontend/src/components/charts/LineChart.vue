<script>
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

export default {
  name: 'App',
  components: {
    Line
  },
  props: ['data', 'chartOptions']
}
</script>

<template>
    <div class="chart-container">
      <Line
        id="my-chart-id2"
        :options="chartOptions"
        :data="data"
      />
    </div>
</template>

<style scoped src="@/assets/chart.css">
</style>