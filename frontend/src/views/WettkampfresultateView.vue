<script setup>
import RennstrukturFilter from "@/components/filters/rennstrukturFilter.vue";
</script>

<template>
  <v-btn color="blue"
         @click="drawer = !drawer" v-show="!drawer"
         style="position: fixed; z-index: 10; left: 0; border-radius: 0"
         class="mt-8"
  ><v-icon>mdi-filter</v-icon>
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
    <v-container v-if="displayResults" class="pa-0 mt-8" style="min-height: 500px">

      <p>{{tableData}}</p>

    </v-container>
  </v-container>
      </v-layout>
  </v-card>
</template>


<script>
import { mapState } from "pinia";
import { useWettkampfresultateStore } from "@/stores/wettkampfresultateStore";

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
    })
  },
    data() {
      return {
        drawer: true,
        breadCrumbs: [],
        displayResults: false,
        displayCompetitions: true,
        displayEvents: false,
        displayRaces: false,
        events: {},
        races: {},
      }
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
    }
}

</script>