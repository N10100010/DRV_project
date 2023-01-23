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
         @click="setFilterState()" v-show="!filterOpen"
         class="filterToggleButton mt-6 pa-0 ma-0"
         height="180"
         size="x-small"
  >
    <v-icon>mdi-filter</v-icon>
  </v-btn>
  <v-card style="box-shadow: none; z-index: 1">
    <v-layout>
      <v-navigation-drawer
          v-model="filterOpen"
          temporary
          v-bind:style='{"margin-top" : (mobile? "71.25px" : "158px" )}'
          style="background-color: white; border: none"
          width="600">
        <berichte-filter/>
      </v-navigation-drawer>

      <v-container class="px-10 py-0">
        <v-col cols="12" class="d-flex flex-row px-0" style="align-items: center">
          <h1>Berichte</h1>
          <v-icon id="tooltip-analyis-icon" color="grey" class="ml-2 v-icon--size-large">mdi-information-outline
          </v-icon>
          <v-tooltip
              activator="#tooltip-analyis-icon"
              location="end"
              open-on-hover
          >In Berichte können Analysen über längere Zeiträume und weitere Filterkriterien erstellt werden.
          </v-tooltip>
        </v-col>
        <v-divider></v-divider>
        <v-container class="pa-0 mt-2">
          <v-row>
            <v-col cols="5">
              <h2>{{ tableData.boat_class }}</h2>
              <v-alert type="success" variant="tonal" class="my-2">
            <v-row>
              <v-col cols="12">
                <p>{{ tableData.results }} Datensätze |
                  Von {{ tableData.start_date.slice(0, 4) }} Bis {{ tableData.end_date.slice(0, 4) }}</p>
              </v-col>
            </v-row>
          </v-alert>
              <v-table class="tableStyles" density="compact">
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
                      {{ tableData["mean"]["m/s"] }} <i>[m/s]</i><br>
                      {{ tableData["mean"]["pace 500m"] }} [500m]<br>
                      {{ tableData["mean"]["pace 1000m"] }} [1000m]
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
                  <th></th>
                  <td style="font-style: italic;">Bedingungen</td>
                </tr>
                <tr>
                  <th>Abstufung schnellste</th>
                  <td>(n={{ tableData["gradation_fastest"]["no_of_samples"] }})
                    {{ tableData["gradation_fastest"]["time"] }}
                  </td>
                </tr>
                <tr>
                  <th>Abstufung mittel</th>
                  <td>(n={{ tableData["gradation_medium"]["no_of_samples"] }}) {{
                      tableData["gradation_medium"]["time"]
                    }}
                  </td>
                </tr>
                <tr>
                  <th>Abstufung langsam</th>
                  <td>(n={{ tableData["gradation_slow"]["no_of_samples"] }}) {{
                      tableData["gradation_slow"]["time"]
                    }}
                  </td>
                </tr>
                <tr>
                  <th>Abstufung langsamste</th>
                  <td>(n={{ tableData["gradation_slowest"]["no_of_samples"] }})
                    {{ tableData["gradation_slowest"]["time"] }}
                  </td>
                </tr>
                </tbody>
              </v-table>
            </v-col>
            <v-col cols="7">
              <v-container style="width: 100%">
                <BarChart :height="'100%'" :width="'100%'" :data="getBarChartData"
                          :chartOptions="barChartOptions"></BarChart>
              </v-container>
              <v-divider></v-divider>
              <v-container style="width: 100%">
                <ScatterChart :height="'100%'" :width="'100%'" :data="getScatterChartData"
                              :chartOptions="scatterChartOptions"></ScatterChart>
              </v-container>
            </v-col>
          </v-row>
        </v-container>
      </v-container>
    </v-layout>
  </v-card>
</template>

<script>
import {mapState} from "pinia";
import {useBerichteState} from "@/stores/berichteStore";

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
    ...mapState(useBerichteState, {
      filterState: "getFilterState"
    })
  },
  methods: {
    setFilterState() {
      this.filterOpen = !this.filterOpen;
      const store = useBerichteState()
      store.setFilterState(this.filterState)
    },
    checkScreen() {
      this.windowWidth = window.innerWidth;
      this.mobile = this.windowWidth <= 750
    }
  },
  created() {
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();
  },
  data() {
    return {
      mobile: false,
      filterOpen: false,
      barChartOptions: {
        responsive: true,
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
          legend: {
            display: false
          },
          title: {
            display: true,
            text: "Histogram Men's Single Sculls"
          }
        }
      },
      scatterChartOptions: {
        responsive: true,
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
          legend: {
            display: false
          },
          title: {
            display: true,
            text: "Men's Single Sculls"
          }
        }
      }
    }
  },
  watch: {
    filterState(newValue) {
      this.filterOpen = newValue;
    },
    filterOpen: function (newVal, oldVal) {
      if (oldVal === true && newVal === false && this.filterState === true) {
        const store = useBerichteState()
        store.setFilterState(oldVal)
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
    text-align: left;
  }

  td {
    text-align: left;
    border: 1px solid #e0e0e0;
  }
}

.nth-grey tr:nth-child(even) {
  background-color: rgba(0, 0, 0, .05);
}

.filterToggleButton {
  position: fixed;
  z-index: 10;
  left: 0;
  border-radius: 0 5px 5px 0;
  color: #1369b0;
}
</style>