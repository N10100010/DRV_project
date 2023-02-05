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
         :class="mobile ? 'filterToggleButtonMobile mt-6 pa-0 ma-0' : 'filterToggleButton mt-6 pa-0 ma-0'"
         :height="mobile ? 100: 180"
         size="x-small"
  >
    <p style="writing-mode: vertical-rl; font-size: 16px; transform: rotate(180deg);">
      <v-icon style="transform: rotate(180deg); font-size: 14px; padding-left: 6px; padding-top: 10px;">mdi-filter
      </v-icon>
      FILTER
    </p>
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

      <v-container :class="mobile ? 'px-5 py-0 main-container' : 'px-10 py-0 main-container'">
        <v-col cols="12" class="d-flex flex-row px-0" style="align-items: center">
          <h1>Berichte</h1>
          <v-icon id="tooltip-analyis-icon" color="grey" class="ml-2 v-icon--size-large">mdi-information-outline
          </v-icon>
          <v-tooltip
              activator="#tooltip-analyis-icon"
              location="end"
              open-on-hover
          >In Berichte kannst du Analysen über längere Zeiträume und weitere Filterkriterien erstellen.
          </v-tooltip>
          <v-icon @click="openPrintDialog()" color="grey" class="ml-2 v-icon--size-large">mdi-printer</v-icon>
        </v-col>
        <v-divider></v-divider>
        <v-container class="pa-0 mt-2 pb-8">
          <v-row>
            <v-col :cols="mobile ? 12 : 5">
              <h2>{{ tableData.boat_class }}</h2>
              <v-alert type="success" variant="tonal" class="my-2" v-if="tableData.results || matrixResults">
                <v-row>
                  <v-col cols="12">
                    <p>{{ matrixVisible ? matrixResults : tableData.results }} Datensätze |
                      Von {{ tableData.start_date.slice(0, 4) }} Bis {{ tableData.end_date.slice(0, 4) }}</p>
                  </v-col>
                </v-row>
              </v-alert>
              <v-alert type="error" variant="tonal" class="my-2" v-else>
                <v-row>
                  <v-col cols="12">
                    <p>Leider keine Ergebnisse gefunden.</p>
                  </v-col>
                </v-row>
              </v-alert>

              <v-table class="tableStyles" density="compact" v-if="!matrixVisible">
                <tbody class="nth-grey">
                <tr>
                  <th>Weltbestzeit</th>
                  <td>{{ formatMilliseconds(tableData.world_best_time_boat_class) }}</td>
                </tr>
                <tr>
                  <th>Beste im Zeitraum</th>
                  <td>{{ formatMilliseconds(tableData.best_in_period) }}</td>
                </tr>
                <tr>
                  <th>Ø Geschwindigkeit (m/s)</th>
                  <td>{{ tableData["mean"]["m/s"] }}</td>
                </tr>
                <tr>
                  <th>Ø t über 500m</th>
                  <td>{{ formatMilliseconds(tableData["mean"]["pace 500m"]) }}</td>
                </tr>
                <tr>
                  <th>Ø t über 1000m</th>
                  <td>{{ formatMilliseconds(tableData["mean"]["pace 1000m"]) }}</td>
                </tr>
                <tr>
                  <th>Ø t über 2000m</th>
                  <td>{{ formatMilliseconds(tableData["mean"]["mm:ss,00"]) }}</td>
                </tr>
                <tr>
                  <th>Standardabweichung</th>
                  <td>{{ formatMilliseconds(tableData.std_dev) }}</td>
                </tr>
                <tr>
                  <th>Median</th>
                  <td>{{ formatMilliseconds(tableData.median) }}</td>
                </tr>
                <tr>
                  <th></th>
                  <td style="font-style: italic;">Bedingungen</td>
                </tr>
                <tr>
                  <th>Abstufung schnellste</th>
                  <td>(n={{ tableData["gradation_fastest"]["no_of_samples"] }})
                    {{ formatMilliseconds(tableData["gradation_fastest"]["time"]) }}
                  </td>
                </tr>
                <tr>
                  <th>Abstufung mittel</th>
                  <td>(n={{ tableData["gradation_medium"]["no_of_samples"] }}) {{
                      formatMilliseconds(tableData["gradation_medium"]["time"])
                    }}
                  </td>
                </tr>
                <tr>
                  <th>Abstufung langsam</th>
                  <td>(n={{ tableData["gradation_slow"]["no_of_samples"] }}) {{
                      formatMilliseconds(tableData["gradation_slow"]["time"])
                    }}
                  </td>
                </tr>
                <tr>
                  <th>Abstufung langsamste</th>
                  <td>(n={{ tableData["gradation_slowest"]["no_of_samples"] }})
                    {{ formatMilliseconds(tableData["gradation_slowest"]["time"]) }}
                  </td>
                </tr>
                </tbody>
              </v-table>
              <v-table class="tableStyles" density="compact" v-if="matrixVisible">
                <thead>
                <tr>
                  <th></th>
                  <th>WB [t]</th>
                  <th>Ø [t]</th>
                  <th>Δ [s]</th>
                  <th>n</th>
                </tr>
                </thead>
                <tbody class="nth-grey">
                <template v-for="row in matrixTableData">
                  <tr v-if="(typeof row === 'string')" class="subheader">
                    <th><b>{{ row }}</b></th>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                  </tr>
                  <tr v-else>
                    <td v-for="item in row">
                      {{ item }}
                    </td>
                  </tr>
                </template>
                </tbody>
              </v-table>
            </v-col>
            <v-col :cols="mobile ? 12 : 7" class="pa-0">
              <v-container style="width: 100%" class="pa-2">
                <BarChart :height="'100%'" :width="'100%'" :data="getBarChartData"
                          :chartOptions="barChartOptions" class="chart-bg"></BarChart>
              </v-container>
              <v-container style="width: 100%" class="pa-2">
                <ScatterChart :height="'100%'" :width="'100%'" :data="getScatterChartData"
                              :chartOptions="scatterChartOptions" class="chart-bg"></ScatterChart>
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
      matrixResults: "getMatrixTableResults"
    }),
    ...mapState(useBerichteState, {
      matrixTableData: 'getMatrixTableData'
    }),
    ...mapState(useBerichteState, {
      getBarChartData: "getBarChartData"
    }),
    ...mapState(useBerichteState, {
      getScatterChartData: "getScatterChartData"
    }),
    ...mapState(useBerichteState, {
      filterState: "getFilterState"
    }),
    ...mapState(useBerichteState, {
      matrixVisible: "getSelectedBoatClass"
    })
  },
  methods: {
    openPrintDialog() {
      window.print();
    },
    setFilterState() {
      this.filterOpen = !this.filterOpen;
      const store = useBerichteState()
      store.setFilterState(this.filterState)
    },
    checkScreen() {
      this.windowWidth = window.innerWidth;
      this.mobile = this.windowWidth <= 750
    },
    formatMilliseconds(ms) {
      return new Date(ms).toISOString().slice(14, -2)
    },
  },
  created() {
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();
    let navbarHeight = window.innerWidth < 750 ? '71.25px' : '160px';
    document.documentElement.style.setProperty('--navbar-height', navbarHeight);
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
            ticks: {
              max: 500,
            },
            title: {
              display: true,
              text: 'Anzahl Rennen'
            }
          }
        },
        plugins: {
          legend: {
            display: true
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
                'seconds': "HH:mm:ss"
              },
              unitStepSize: 30
            },
            title: {
              display: true,
              text: 'Zeit [mm:ss.ms]'
            }
          }
        },
        plugins: {
          legend: {
            display: true,
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
    border: 0.5px solid #e0e0e0;
    font-size: 14px !important;
    text-align: left;
  }

  td {
    text-align: left;
    border: 0.5px solid #e0e0e0;
  }
}

.nth-grey tr:nth-child(odd) {
  background-color: rgba(0, 0, 0, .05);
}

/*
.no-border {
  border-left: none !important;
  border-right: none !important;
}
*/

.filterToggleButton {
  position: fixed;
  z-index: 10;
  left: 0;
  border-radius: 0 5px 5px 0;
  color: #1369b0;
}

.filterToggleButtonMobile {
  position: fixed;
  z-index: 10;
  left: 0;
  border-radius: 0 5px 5px 0;
  color: #1369b0;
  bottom: 10px;
}

.chart-bg {
  background-color: #fbfbfb;
  border-radius: 3px;
}

.main-container {
  min-height: calc(100vh - (var(--navbar-height)) - 95px);
}

@media print {
  i, .filterToggleButton, .filterToggleButtonMobile {
    display: none;
  }
}
</style>
