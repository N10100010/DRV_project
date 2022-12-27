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
          labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'],
          datasets: [
              {
                label: 'one',
                backgroundColor: '#f5bd00',
                borderColor: '#f5bd00',
                data: [40, 20, 12, 22, 455, 122, 533, 32]
              }
          ]
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: "Line Plot example title"
            }
          }
        }
      }
  }
}
</script>

<template>
    <div class="chart-container">
      <Line
        id="my-chart-id2"
        :options="chartOptions"
        :data="chartData"
      />
    </div>
</template>

<style scoped src="@/assets/chart.css">
</style>