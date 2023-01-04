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
        <v-col cols="12">
          <h2>Tabellen</h2>
          <v-container style="background-color: whitesmoke; min-height: 200px;">
            <p>Placeholder for Table(s)</p>
          </v-container>
        </v-col>
        <v-col cols="12">
          <h2>Plots</h2>
          <v-container>
            <BarChart :data="getBarChartData" :chartOptions="barChartOptions"></BarChart>
          </v-container>
          <v-container>
            <ScatterChart :data="getScatterChartData" :chartOptions="scatterChartOptions"></ScatterChart>
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
import { mapState } from "pinia";
import { useBerichteState } from "@/stores/berichteStore";

export default {
  computed: {
    ...mapState(useBerichteState, {
      getBarChartData: "getBarChartData"
    }),
    ...mapState(useBerichteState, {
      getScatterChartData: "getScatterChartData"
    }),
  },
  data() {
    return {
      drawer: false,
      barChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: "Histogram Men's Single Sculls"
          }
        }
      },
      scatterChartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: "Men's Single Sculls"
          }
        }
      }
    }
  }
}
</script>
