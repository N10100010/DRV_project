<script>
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
import { Line } from 'vue-chartjs'

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
  data() {
    return {
        chartData: {
          labels: [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'],
          datasets: [ { label: 'one', data: [40, 20, 12, 22, 455, 122, 533, 32] } ]
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false
        }
      }
  }
}
</script>

<template>
    <Line
      id="my-chart-id2"
      :options="chartOptions"
      :data="chartData"
    />
  </template>