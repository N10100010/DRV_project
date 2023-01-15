<template>
  <v-btn color="blue"
         @click="drawer = !drawer" v-show="!drawer"
         class="filterToggleButton mt-6 pa-0 ma-0 bg-light-blue"
         height="180"
         size="x-small"
  >
    <v-icon>mdi-filter</v-icon>
  </v-btn>
  <v-card style="box-shadow: none; z-index: 1">
    <v-layout>
      <v-navigation-drawer
          v-model="drawer"
          temporary
          v-bind:style='{"margin-top" : (mobile? "71.25px" : "158px" )}'
          width="500">
        <rennstruktur-filter/>
      </v-navigation-drawer>
      <v-container class="pa-10">
        <h1>Rennstrukturanalyse</h1>
        <v-divider></v-divider>
        <v-breadcrumbs style="color: grey; height: 22px" class="pa-0 mt-4" :items="breadCrumbs"></v-breadcrumbs>
        <v-container class="pa-0 mt-8" v-if="!displayRaceDataAnalysis">
          <v-row>
            <v-col cols="12">
              <h2>Suchergebnisse</h2>
              <v-container class="pa-0" style="min-height: 500px">
                <v-col cols="6" class="pa-0">
                  <!-- competition list -->
                  <v-list density="compact" v-show="displayCompetitions">
                    <v-list-item
                        min-height="80"
                        style="background-color: whitesmoke; border-radius: 5px"
                        class="pa-2 my-2"
                        v-for="competition in getAnalysis"
                        :key="competition"
                        :title="competition.display_name"
                        :subtitle="competition.start_date+' | '+competition.venue"
                        @click="getEvents(competition.events)"
                    ></v-list-item>
                  </v-list>
                  <!-- events list -->
                  <v-list density="compact" v-show="displayEvents">
                    <v-list-item
                        style="background-color: whitesmoke; border-radius: 5px"
                        class="pa-2 my-2"
                        v-for="event in events"
                        :key="event"
                        :title="event.display_name"
                        @click="getRaces(event.races)"
                    ></v-list-item>
                  </v-list>
                  <!-- races list -->
                  <v-list density="compact" v-show="displayRaces">
                    <v-list-item
                        style="background-color: whitesmoke; border-radius: 5px"
                        class="pa-2 my-2"
                        v-for="race in races"
                        :key="race"
                        :title="race.display_name"
                        @click="loadRaceAnalysis(race.display_name)"
                    ></v-list-item>
                  </v-list>
                </v-col>
              </v-container>
            </v-col>
          </v-row>
        </v-container>

        <v-container v-if="displayRaceDataAnalysis" class="pa-0 mt-8">
          <v-row no-gutters>
            <v-col>
              <v-table>
                <tbody>
                <tr>
                  <td><b>Wettkampf:</b></td>
                  <td>{{ competitionData.displayName }}</td>
                </tr>
                <tr>
                  <td><b>Austragungsort:</b></td>
                  <td>{{ competitionData.venue }}</td>
                </tr>
                <tr>
                  <td><b>Datum & Startzeit:</b></td>
                  <td>{{ competitionData.startDate }}</td>
                </tr>
                </tbody>
              </v-table>
            </v-col>
            <v-col>
              <v-table>
                <tbody>
                <tr>
                  <td><b>Bootsklasse:</b></td>
                  <td>{{ competitionData.boatClass }}</td>
                </tr>
                <tr>
                  <td><b>Weltbestzeit Bootsklasse:</b></td>
                  <td>{{ competitionData.worldBestTimeBoatClass }}</td>
                </tr>
                <tr>
                  <td><b>Bestzeit Bootsklasse laufender OZ/Jahr:</b></td>
                  <td>{{ competitionData.bestTimeBoatClassCurrentOZ }}</td>
                </tr>
                </tbody>
              </v-table>
            </v-col>
          </v-row>

          <v-container class="pa-0 d-flex">
            <v-col cols="6" class="pa-0">
            </v-col>
            <v-col cols="6" class="pa-0 text-right">
            </v-col>
          </v-container>

          <v-row>
            <v-col cols="12">
              <v-table class="tableStyles">
                <thead>
                <tr>
                  <th v-for="tableHead in tableData[0]">{{ tableHead }}</th>
                  <th>Prog.<br>Code</th>
                </tr>
                </thead>
                <tbody class="nth-grey">
                <tr v-for="country, idx in tableData.slice(1)">
                  <td v-for="item in country">
                    <template v-if="Array.isArray(item)">
                      <p v-for="element in item" class="py-1">
                        {{ element }}
                      </p>
                    </template>
                    <template v-else>
                      <p>
                        {{ item }}
                      </p>
                    </template>
                  </td>
                  <td>
                    {{ competitionData.data[idx].progressionCode }}
                  </td>
                </tr>
                </tbody>
              </v-table>
            </v-col>
            <v-divider class="mt-8"></v-divider>
            <v-col cols="6">
              <v-container v-for="(data, idx) in getGPsData">
                <LineChart :data="data" :chartOptions="gpsChartOptions[idx]"></LineChart>
              </v-container>
            </v-col>
            <v-col cols="6">
              <v-container v-for="(data, idx) in getIntermediateData">
                <LineChart :data="data" :chartOptions="intermediateChartOptions[idx]"></LineChart>
              </v-container>
            </v-col>
          </v-row>
        </v-container>
      </v-container>
    </v-layout>
  </v-card>
</template>

<script setup>
import RennstrukturFilter from "@/components/filters/rennstrukturFilter.vue";
import LineChart from "@/components/charts/LineChart.vue";
import '@/assets/base.css';
import 'chartjs-adapter-moment';
import {Chart as ChartJS, Tooltip, Legend, TimeScale} from "chart.js";

ChartJS.register(Tooltip, Legend, TimeScale);
</script>

<script>
import {useRennstrukturAnalyseState} from "@/stores/baseStore";
import {mapState} from "pinia";

export default {
  computed: {
    ...mapState(useRennstrukturAnalyseState, {
      getAnalysis: "getAnalysisData"
    }),
    ...mapState(useRennstrukturAnalyseState, {
      competitionData: 'getCompetitionData'
    }),
    ...mapState(useRennstrukturAnalyseState, {
      oldTableData: "getOldTableData"
    }),
    ...mapState(useRennstrukturAnalyseState, {
      tableData: "getTableData"
    }),
    ...mapState(useRennstrukturAnalyseState, {
      getGPsData: "getGPSChartData"
    }),
    ...mapState(useRennstrukturAnalyseState, {
      getIntermediateData: "getIntermediateChartData"
    })
  },
  data() {
    return {
      drawer: true,
      breadCrumbs: [],
      mobile: false,
      displayRaceDataAnalysis: false,
      displayCompetitions: true,
      displayEvents: false,
      displayRaces: false,
      events: {},
      races: {},
      gpsChartOptions: [{
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Strecke [m]'
            }
          },
          y: {
            title: {
              display: true,
              text: 'Geschwindigkeit [m/sek]'
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: "Geschwindigkeit über Distanz"
          }
        }
      },
        {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: {
                display: true,
                text: 'Strecke [m]'
              }
            },
            y: {
              title: {
                display: true,
                text: 'Schlagfrequenz [1/min]'
              }
            }
          },
          plugins: {
            title: {
              display: true,
              text: "Schlagfrequenz über Distanz"
            }
          }
        }, {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: {
                display: true,
                text: 'Strecke [m]'
              }
            },
            y: {
              title: {
                display: true,
                text: 'Vortrieb [m/Schlag]'
              }
            }
          },
          plugins: {
            title: {
              display: true,
              text: "Vortrieb über Distanz "
            }
          }
        }
      ],
      intermediateChartOptions: [{
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            title: {
              display: true,
              text: 'Strecke [m]'
            }
          },
          y: {
            title: {
              display: true,
              text: 'Platzierung'
            }
          }
        },
        plugins: {
          title: {
            display: true,
            text: "Platzierung über Distanz"
          }
        }
      },
        {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: {
                display: true,
                text: 'Strecke [m]'
              }
            },
            y: {
              type: 'time',
              time: {
                parser: 'hh:mm:ss.SSS',
                displayFormats: {
                  second: 'ss.SSS',
                  tooltip: 'mm:ss.SSS'
                }
              },
              min: '00:00:00,000',
              max: '00:00:20,000',
              unitTimeSteps: 100,
              title: {
                display: true,
                text: 'Rückstand [sek]'
              }
            }
          },
          plugins: {
            title: {
              display: true,
              text: "Rückstand über Distanz [sek]"
            }
          }
        }
      ]
    }
  },
  created() {
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();
  },
  methods: {
    getEvents(competition) {
      this.events = competition
      this.breadCrumbs.push({
        title: 'Competition',
        disabled: false,
        href: '#',
        onclick: () => {
          this.displayCompetitions = true
          this.displayRaceDataAnalysis = false
          this.displayEvents = false
          this.displayRaces = false
          this.breadCrumbs.splice(0)
        }
      })
      this.displayCompetitions = false
      this.displayEvents = true
    },
    getRaces(events) {
      this.races = events
      this.breadCrumbs.push({
        title: 'Event',
        disabled: false,
        href: '#',
        onclick: () => {
          this.displayCompetitions = false
          this.displayRaceDataAnalysis = false
          this.displayEvents = true
          this.displayRaces = false
          this.breadCrumbs.splice(1)
        }
      })
      this.displayEvents = false
      this.displayRaces = true
    },
    loadRaceAnalysis(raceName) {
      this.displayRaceDataAnalysis = true
      this.breadCrumbs.push(raceName)
    },
    checkScreen() {
      this.windowWidth = window.innerWidth;
      this.mobile = this.windowWidth <= 750
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

.nth-grey tr:nth-of-type(odd) {
  background-color: rgba(0, 0, 0, .05);
}

.filterToggleButton {
  position: fixed;
  z-index: 10;
  left: 0;
  border-radius: 0 5px 5px 0;
}

</style>