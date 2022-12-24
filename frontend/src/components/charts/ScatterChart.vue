<script>
import { Scatter } from 'vue-chartjs'

export default {
  components: {
    Scatter
  },
  data() {
    return {
      scatterChartData: {
        datasets: [
          {
            type: 'scatter',
            label: 'Scatter Dataset',
            data: [
              { x: 1, y: 10 },
              { x: 2, y: 20 },
              { x: 3, y: 30 },
              { x: 2.3, y: 15 },
              { x: 4.4, y: 12 },
              { x: 6.4, y: 24 },
              { x: 5.2, y: 18 }
            ],
            backgroundColor: 'blue',
            borderColor: 'blue'
          },
          {
            type: 'line',
            label: 'Line Dataset',
            data: [
              { x: 1, y: 10 },
              { x: 7, y: 28 }
            ],
            backgroundColor: 'green',
            borderColor: 'green'
          }
        ]
      },
      scatterChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: "Scatter Plot example title"
          }
        }
      }
    }
  }
}
</script>

<template>
  <div class="chart-container">
    <scatter
      id="scatter-chart-id"
      :options="scatterChartOptions"
      :data="scatterChartData"
    />
  </div>
</template>

<style scoped src="@/assets/chart.css">
</style>
