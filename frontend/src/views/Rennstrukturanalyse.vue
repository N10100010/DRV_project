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
    <rennstruktur-filter/>
  </v-navigation-drawer>
  <v-container class="pa-10" style="max-width: 1024px">
  <v-breadcrumbs style="color: grey" class="pa-0" :items="['Competition', 'Event', 'Race']"></v-breadcrumbs>
  <h1>Rennstrukturanalyse</h1>
  <v-divider></v-divider>
  <v-container class="pa-0 mt-8">
    <v-row>
      <v-col cols="12">
        <h2>Results</h2>
        <v-container class="pa-0" style="min-height: 500px">
          <v-col cols="6" class="pa-0">
            <v-list density="compact">
              <v-list-item
                  style="background-color: whitesmoke; border-radius: 5px"
                  class="pa-2 my-2"
                  v-for="item in 6"
                  :key="item"
                  title="Competition DisplayName"
                  subtitle="2020"
                  href="/rennstrukturanalyse"
              ></v-list-item>
            </v-list>
          </v-col>
        </v-container>
      </v-col>
    </v-row>
  </v-container>

  <h1>Rennstrukturanalyse</h1>
  <v-container class="pa-0">
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
          <LineChart :data="chartData" :chartOptions="chartOptions"></LineChart>
        </v-container>
        <v-container>
          <LineChart :data="chartData" :chartOptions="chartOptions"></LineChart>
        </v-container>
        <v-container>
          <LineChart :data="chartData" :chartOptions="chartOptions"></LineChart>
        </v-container>
      </v-col>
    </v-row>
  </v-container>

  <p><b>Test-Abfrage für Pinia-State-Management Store:</b></p>
  <p>{{ getData }}</p>

    </v-container>
      </v-layout>
</v-card>
</template>


<script setup>
import RennstrukturFilter from "@/components/filters/rennstrukturFilter.vue";
import LineChart from "@/components/charts/LineChart.vue";
import { useTestState } from "@/stores/baseStore";
const store = useTestState();
import {computed, onMounted} from "vue";

const getData = computed(() => {
  return store.getTestData;
});

onMounted(() => {
  store.fetchData();
});
</script>

<script>
export default {
  data() {
    return {
      drawer: true,
      mobile: false,
        chartData: {
          labels: ['500m', '1000m', '1500m', '2000m'],
          datasets: [
              {
                label: 'DEU',
                backgroundColor: '#f5bd00',
                borderColor: '#f5bd00',
                data: [140, 134, 146, 143]
              },
              {
                label: 'FRA',
                backgroundColor: '#000033',
                borderColor: '#000033',
                data: [138, 143, 153, 142]
              },
              {
                label: 'GBR',
                backgroundColor: '#440000',
                borderColor: '#440000',
                data: [134, 141, 140, 142]
              }
          ]
        },
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: "Intermediate Times"
            }
          }
        }
      }
  }
}
</script>