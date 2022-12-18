<script>
  import { Bar } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
  
  export default {
    name: 'BarChart',
    components: { Bar },
    data() {
      return {
        chartData: {
          labels: [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'],
          datasets: [ 
            { label: 'one', backgroundColor: '#f87979', data: [40, 20, 12, 22, 455, 122, 533, 32] },
            { label: 'two', backgroundColor: '#855fff', data: [50, 10, 22, 39, 5, 8, 400, 300] }
          ]
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
    <Bar
      id="my-chart-id"
      :options="chartOptions"
      :data="chartData"
    />
  </template>