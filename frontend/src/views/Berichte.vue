<script setup>
import ScatterChart from '@/components/charts/ScatterChart.vue';
import BarChart from "@/components/charts/BarChart.vue";
import BerichteFilter from "@/components/filters/berichteFilter.vue";
import 'chartjs-adapter-moment';
import {Chart as ChartJS, LinearScale, PointElement, Tooltip, Legend, TimeScale} from "chart.js";
ChartJS.register(LinearScale, PointElement, Tooltip, Legend, TimeScale);

</script>

<template>
   <v-btn color="blue"
         @click="drawer = !drawer" v-show="!drawer"
         style="position: fixed; z-index: 10; left: 0; border-radius: 0"
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


  <v-container class="pa-10">
    <h1>Berichte</h1>
    <v-divider></v-divider>
    <v-container class="pa-0 mt-8">
      <v-row>
        <v-col cols="12">
          <h2>{{ tableData.boat_class }}</h2>
          <p>Von {{ tableData.start_date }} bis {{ tableData.end_date }}</p>
          <p>{{ tableData.results }} Datensätze gefunden.</p>
            <v-table class="tableStyles">
              <tbody class="nth-grey">
                <tr>
                  <th>Weltbestzeit</th>
                  <td>{{ tableData.world_best_time_boat_class }}</td>
                </tr>
                <tr>
                  <th>Beste im Zeitraum</th>
                  <td>{{ tableData.best_in_period }}</td>
                </tr>
                <tr>
                  <th>Mittelwert</th>
                  <td>
                    <p>
                      {{ tableData["mean"]["mm:ss,00"] }}<br>
                      {{ tableData["mean"]["m/s"] }}[m/s]<br>
                      {{ tableData["mean"]["pace 500m"] }}[500m]<br>
                      {{ tableData["mean"]["pace 1000m"] }}[1000m]
                    </p>
                  </td>
                </tr>
                <tr>
                  <th>Standardabweichung</th>
                  <td>{{ tableData.std_dev }}</td>
                </tr>
                <tr>
                  <th>Median</th>
                  <td>{{ tableData.median }}</td>
                </tr>
                <tr>
                  <th></th><td style="font-style: italic;">Bedingungen</td>
                </tr>
                <tr>
                  <th>Abstufung schnellste</th>
                  <td>(n={{ tableData["gradation_fastest"]["no_of_samples"] }}) {{ tableData["gradation_fastest"]["time"] }}</td>
                </tr>
                <tr>
                  <th>Abstufung mittel</th>
                  <td>(n={{ tableData["gradation_medium"]["no_of_samples"] }}) {{ tableData["gradation_medium"]["time"] }}</td>
                </tr>
                <tr>
                  <th>Abstufung langsam</th>
                  <td>(n={{ tableData["gradation_slow"]["no_of_samples"] }}) {{ tableData["gradation_slow"]["time"] }}</td>
                </tr>
                <tr>
                  <th>Abstufung langsamste</th>
                  <td>(n={{ tableData["gradation_slowest"]["no_of_samples"] }}) {{ tableData["gradation_slowest"]["time"] }}</td>
                </tr>
              </tbody>
            </v-table>
        </v-col>
        <v-col cols="12">
          <v-container>
            <BarChart :height="400" :data="getBarChartData" :chartOptions="barChartOptions"></BarChart>
          </v-container>
          <v-container>
            <ScatterChart :height="400" :data="getScatterChartData" :chartOptions="scatterChartOptions"></ScatterChart>
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
      tableData: "getTableData"
    }),
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
        scales: {
          x: {
            title: {
              display: true,
              text: 'Zeit [mm:ss]'
            }
          },
          y: {
            title: {
              display: true,
              text: 'Anzahl Rennen'
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: "Histogram Men's Single Sculls"
          }
        }
      },
      scatterChartOptions: {
        scales: {
            x: {
                type: 'time',
                time: {
                  unit: 'year',
                  parser: 'yyyy-mm-dd'
                },
                title: {
                display: true,
                text: 'Jahr'
              }
            },
            y: {
              type: 'time',
              time: {
                parser: 'HH:mm:ss',
                    unit: "seconds",
                    tooltipFormat: 'HH:mm:ss',
                    displayFormats: {
                        'seconds': "mm:ss"
                    },
                    unitStepSize: 30
              },
              title: {
                display: true,
                text: 'Zeit [mm:ss]'
              }
            }
        },
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

<style lang="scss" scoped>
.tableStyles {
  border: 1px solid #e0e0e0;

  th {
    border: 1px solid #e0e0e0;
    font-size: 14px !important;
  }

  td {
  text-align: center;
  border: 1px solid #e0e0e0;
  }
}

.nth-grey tr:nth-child(even) {
  background-color: rgba(0, 0, 0, .05);
}
</style>