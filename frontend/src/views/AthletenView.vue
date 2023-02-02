<template>
  <v-btn color="blue"
         @click="setFilterState()" v-show="!filterOpen"
         :class="mobile ? 'filterToggleButtonMobile mt-6 pa-0 ma-0' : 'filterToggleButton mt-6 pa-0 ma-0'"
         :height="mobile ? 100: 180"
         size="x-small"
  >
  <p style="writing-mode: vertical-rl; font-size: 16px; transform: rotate(180deg);"><v-icon style="transform: rotate(180deg); font-size: 14px; padding-left: 6px; padding-top: 10px;">mdi-filter</v-icon>FILTER</p>
  </v-btn>
  <v-card style="box-shadow: none; z-index: 1">
    <v-layout>
      <v-navigation-drawer v-model="filterOpen" temporary
                           v-bind:style='{ "margin-top": (mobile ? "71.25px" : "160px") }'
                           style="background-color: white; border: none"
                           width="600">
        <athleten-filter/>
      </v-navigation-drawer>

      <v-container :class="mobile ? 'px-5 py-0 pb-8 main-container' : 'px-10 py-0 pb-8 main-container'">
        <v-col cols="12" class="d-flex flex-row px-0" style="align-items: center">
          <h1>Athleten</h1>
          <v-icon id="tooltip-athlete-icon" color="grey" class="ml-2 v-icon--size-large">mdi-information-outline</v-icon>
          <v-tooltip
              activator="#tooltip-athlete-icon"
              location="end"
              open-on-hover
          >Auf der Athleten-Seite findest du die Stammdaten des Athletens und kannst
            eine Übersicht zu seinen Ergebnissen (inkl. Medaillenspiegel) betrachten.
          </v-tooltip>
          <v-icon @click="openPrintDialog()" color="grey" class="ml-2 v-icon--size-large">mdi-printer</v-icon>
        </v-col>
        <v-divider></v-divider>
        <v-container class="pa-0 mt-8" style="min-height: 400px">
          <v-row>
            <v-col :cols="mobile ? 12 : 4">
              <h2>{{ tableData.firstName }} {{ tableData.lastName }}</h2>
              <v-table class="tableStyles" density="compact">
                <tbody class="nth-grey">
                <tr>
                  <th>Nation</th>
                  <td>{{ tableData.nation_ioc }}</td>
                </tr>
                <tr>
                  <th>Geburtsdatum</th>
                  <td>{{ tableData.dateOfBirth }}</td>
                </tr>
                <tr>
                  <th>Geschlecht</th>
                  <td>{{ tableData.gender == 'male' ? 'Männlich' : 'Weiblich' }}</td>
                </tr>
                <tr>
                  <th>Gewicht</th>
                  <td>{{ tableData.weight }} kg</td>
                </tr>
                <tr>
                  <th>Größe</th>
                  <td>{{ tableData.height }} cm</td>
                </tr>
                <tr>
                  <th>Bootsklasse</th>
                  <td>{{ tableData.currentBoatClass }}</td>
                </tr>
                <tr>
                  <th>Disziplin(en)</th>
                  <td><p v-for="item in tableData.disciplines">{{ item }}</p></td>
                </tr>
                <tr>
                  <th>Rennanzahl</th>
                  <td>{{ tableData.numberOfRaces }}</td>
                </tr>
                <tr>
                  <th>Medaillen Gesamt</th>
                  <td>{{ tableData.medals_total }}</td>
                </tr>
                <tr>
                  <th>Medaillen Gold</th>
                  <td>{{ tableData.medals_gold }}</td>
                </tr>
                <tr>
                  <th>Medaillen Silber</th>
                  <td>{{ tableData.medals_silver }}</td>
                </tr>
                <tr>
                  <th>Medaillen Bronze</th>
                  <td>{{ tableData.medals_bronze }}</td>
                </tr>
                <tr>
                  <th>Platzierungen Finale A</th>
                  <td>{{ tableData.placements_final_A }}</td>
                </tr>
                <tr>
                  <th>Platzierungen Finale B</th>
                  <td>{{ tableData.placements_final_B }}</td>
                </tr>
                <tr>
                  <th>Bestzeit Bootsklasse</th>
                  <td>{{ formatMilliseconds(tableData.bestTimeBoatClass) }}</td>
                </tr>
                <tr>
                  <th>Bestzeit Bootsklasse OZ/Jahr</th>
                  <td>{{ formatMilliseconds(tableData.bestTimeBoatClassCurrentOZ) }}</td>
                </tr>
                </tbody>
              </v-table>
            </v-col>
            <v-col v-if="!mobile">
              <h2>Rennliste</h2>
              <v-table class="tableStyles" density="compact">
                <thead>
                <tr>
                  <th>Wettkampf</th>
                  <th>Startzeit</th>
                  <th>Platzierung</th>
                  <th>Austragungsort</th>
                  <th>Bootsklasse</th>
                </tr>
                </thead>
                <tbody class="nth-grey">
                <tr v-for="(race, idx) in tableData.raceList">
                  <td>{{ race.raceName }}</td>
                  <td>{{ race.startDate }}</td>
                  <td>{{ race.rank }}</td>
                  <td>{{ race.venue }}</td>
                  <td>{{ race.boatClass }}</td>
                </tr>
                </tbody>
              </v-table>
            </v-col>
            <v-col cols="12" v-if="mobile" density="comfortable">
              <h2>Rennliste</h2>
              <v-table class="tableStyles">
                <thead>
                <tr>
                  <th>Wettkampf</th>
                  <th>Startzeit</th>
                  <th>Platzierung</th>
                  <th>Austragungsort</th>
                  <th>Bootsklasse</th>
                </tr>
                </thead>
                <tbody class="nth-grey">
                <tr v-for="(race, idx) in tableData.raceList">
                  <td>{{ race.raceName }}</td>
                  <td>{{ race.startDate }}</td>
                  <td>{{ race.rank }}</td>
                  <td>{{ race.venue }}</td>
                  <td>{{ race.boatClass }}</td>
                </tr>
                </tbody>
              </v-table>
            </v-col>
          </v-row>
        </v-container>
      </v-container>
    </v-layout>
  </v-card>
</template>

<script setup>
import AthletenFilter from "@/components/filters/athletenFilter.vue";
</script>

<script>
import {mapState} from "pinia";
import {useAthletenState} from "@/stores/athletenStore";
import router from "@/router";

export default {
  computed: {
    ...mapState(useAthletenState, {
      filterState: "getFilterState"
    }),
    ...mapState(useAthletenState, {
      tableData: "getTableData"
    }),
  },
  methods: {
    openPrintDialog() {
      window.print();
    },
    setFilterState() {
      this.filterOpen = !this.filterOpen;
      const store = useAthletenState()
      store.setFilterState(this.filterState)
    },
    checkScreen() {
      this.windowWidth = window.innerWidth;
      this.mobile = this.windowWidth <= 750
      let navbarHeight = window.innerWidth < 750 ? '71.25px' : '160px';
      document.documentElement.style.setProperty('--navbar-height', navbarHeight);
    },
    formatMilliseconds(ms) {
      return new Date(ms).toISOString().slice(14, -2)
    }
  },
  created() {
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();

    // possible solution for permanent url --> in the real scenario there must be a fetch to the backend
    window.onload = () => {
      const url = new URL(window.location.href);
      const race_id = url.searchParams.get("athlete_id");
      if (race_id !== null) {
        console.log("Permanent URL active: " + race_id)
        // make api call with respective id here
        // ...
        // ...
      }
    }
  },
  data() {
    return {
      mobile: false,
      filterOpen: this.filterState,
    }
  },
  watch: {
    filterState(newValue) {
      this.filterOpen = newValue;
    },
    filterOpen: function (newVal, oldVal) {
      if (oldVal === true && newVal === false && this.filterState === true) {
        const store = useAthletenState()
        store.setFilterState(oldVal)
      }
    },
    tableData: function (newVal,) {
      /*
      if (newVal !== undefined) {
        router.push(this.$route.path + `?athlete_id=${newVal.id}`)
      }
      */
    }
  }
}
</script>

<style lang="scss" scoped>
.filterToggleButton {
  position: fixed;
  z-index: 10;
  left: 0;
  border-radius: 0 5px 5px 0;
  color: #1369b0;
}

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
.main-container {
  min-height: calc(100vh - (var(--navbar-height)) - 95px);
}

@media print {
  i, .filterToggleButton, .filterToggleButtonMobile {
    display: none;
  }
}
</style>
