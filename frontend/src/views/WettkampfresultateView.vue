<script setup>
import RennstrukturFilter from "@/components/filters/rennstrukturFilter.vue";
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
          width="500">
        <rennstruktur-filter/>
      </v-navigation-drawer>
      <v-container class="pa-10">
        <h1>Wettkampfresultate</h1>
        <v-divider></v-divider>
        <v-breadcrumbs style="color: grey; height: 22px" class="pa-0 mt-4" :items="breadCrumbs"></v-breadcrumbs>
        <v-container class="pa-0 mt-8" v-if="!displayResults">
          <v-row>
            <v-col cols="12">
              <h2>Suchergebnisse</h2>
              <v-container class="pa-0" style="min-height: 500px">
                <v-col cols="6" class="pa-0">
                  <!-- competition list -->
                  <v-list density="compact" v-show="displayCompetitions">
                    <v-list-item
                        min-height="80"
                        style="background-color: whitesmoke; border-radius: 5px; border-left: 8px solid #5cc5ed;"
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
                        style="background-color: whitesmoke; border-radius: 5px; border-left: 8px solid #5cc5ed;"
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
                        style="background-color: whitesmoke; border-radius: 5px; border-left: 8px solid #5cc5ed;"
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
        <v-container v-if="displayResults" class="pa-0 mt-8" style="min-height: 500px">

          <p>{{ tableData }}</p>

        </v-container>
      </v-container>
    </v-layout>
  </v-card>
</template>


<script>
import {mapState} from "pinia";
import {useWettkampfresultateStore} from "@/stores/wettkampfresultateStore";
import {useBerichteState} from "@/stores/berichteStore";
import {useRennstrukturAnalyseState} from "@/stores/baseStore";

export default {
  computed: {
    ...mapState(useWettkampfresultateStore, {
      getAnalysis: "getAnalysisData"
    }),
    ...mapState(useWettkampfresultateStore, {
      competitionData: 'getCompetitionData'
    }),
    ...mapState(useWettkampfresultateStore, {
      tableData: "getTableData"
    }),
    ...mapState(useRennstrukturAnalyseState, {
      filterState: "getFilterState"
    })
  },
  data() {
    return {
      filterOpen: true,
      mobile: false,
      breadCrumbs: [],
      displayResults: false,
      displayCompetitions: true,
      displayEvents: false,
      displayRaces: false,
      events: {},
      races: {},
    }
  },
  created() {
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();
    this.filterOpen = this.filterState
  },
  methods: {
    checkScreen() {
      this.windowWidth = window.innerWidth;
      this.mobile = this.windowWidth <= 750
    },
    setFilterState() {
      this.filterOpen = !this.filterOpen;
      const store = useRennstrukturAnalyseState()
      store.setFilterState(this.filterState)
    },
    getEvents(competition) {
      this.events = competition
      this.breadCrumbs.push({
        title: 'Competition',
        disabled: false,
        href: '#',
        onclick: () => {
          this.displayCompetitions = true
          this.displayResults = false
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
          this.displayResults = false
          this.displayEvents = true
          this.displayRaces = false
          this.breadCrumbs.splice(1)
        }
      })
      this.displayEvents = false
      this.displayRaces = true
    },
    loadRaceAnalysis(raceName) {
      this.displayResults = true
      this.breadCrumbs.push(raceName)
    }
  },
  watch: {
    filterState(newValue) {
      this.filterOpen = newValue;
    },
    filterOpen: function (newVal, oldVal) {
      if (oldVal === true && newVal === false && this.filterState === true) {
        const store = useRennstrukturAnalyseState()
        store.setFilterState(oldVal)
      }
    }
  }
}

</script>

<style scoped>
.filterToggleButton {
  position: fixed;
  z-index: 10;
  left: 0;
  border-radius: 0 5px 5px 0;
  color: #1369b0;
}
</style>