<script setup>
import ScatterChart from '@/components/charts/ScatterChart.vue';
import BarChart from "@/components/charts/BarChart.vue";
import BerichteFilter from "@/components/filters/berichteFilter.vue";
</script>

<template>
   <v-btn color="blue"
         @click="drawer = !drawer" v-show="!drawer"
         style="position: fixed; z-index: 999; left: 0; border-radius: 0"
         class="mt-8"
  >
    <v-icon>mdi-filter</v-icon>
  </v-btn>
  <v-card style="box-shadow: none; z-index: 1">
      <v-layout>
        <v-navigation-drawer
      v-model="drawer"
      temporary
      style="margin-top: 160px; background-color: white; border: none"
      width="500">
    <berichte-filter/>
  </v-navigation-drawer>


  <v-container class="pa-10" style="max-width: 1024px">
    <h1>Berichte</h1>
    <v-divider></v-divider>
    <v-container class="pa-0 mt-8">
      <v-row>
        <v-col cols="6">
          <h2>Tabellen</h2>
          <v-container style="background-color: whitesmoke; height: 80%">
            <p>Placeholder for Table(s)</p>
          </v-container>
        </v-col>
        <v-col cols="6">
          <h2>Plots</h2>
          <v-container>
            <BarChart :data="barChartData" :chartOptions="barChartOptions"></BarChart>
          </v-container>
          <v-container>
            <ScatterChart :data="scatterChartData" :chartOptions="scatterChartOptions"></ScatterChart>
          </v-container>
          <v-container>
          </v-container>
          <v-container>
          </v-container>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
      </v-layout>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      drawer: false,
      barChartData: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'],
        datasets: [
          {label: 'one', backgroundColor: '#f87979', data: [40, 20, 12, 22, 455, 122, 533, 32]},
          {label: 'two', backgroundColor: '#855fff', data: [50, 10, 22, 39, 5, 8, 400, 300]}
        ]
      },
      barChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: "Bar Plot example title"
          }
        }
      },
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
