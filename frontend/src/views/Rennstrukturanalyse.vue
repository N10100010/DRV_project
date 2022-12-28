<template>
  <rennstruktur-filter></rennstruktur-filter>

  <!-- Placeholder for initial page -->
  <v-breadcrumbs style="color: grey" class="pa-0" :items="['Competition', 'Event', 'Race']"></v-breadcrumbs>
  <h1>Rennstrukturanalyse (Platzhalter initiale Seite)</h1>
  <v-divider></v-divider>
  <v-container class="pa-0 mt-8">
    <v-row>
      <v-col cols="12">
        <h2>Results</h2>
        <v-container class="pa-0" style="min-height: 500px">
          <v-col cols="6">
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

  <!-- Placeholder for final site, including data and plots -->
  <h1>Rennstrukturanalyse (Platzhalter für finale Seite)</h1>

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

  <!-- added test for pinia store api response -->
  <p><b>Test-Abfrage für Pinia-State-Management Store:</b></p>
  <p>{{ getData }}</p>

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