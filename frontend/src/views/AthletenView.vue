<template>
  <v-btn color="blue" @click="setFilterState()" v-show="!filterOpen" class="filterToggleButton mt-6 pa-0 ma-0"
    height="180" size="x-small">
    <v-icon>mdi-filter</v-icon>
  </v-btn>
  <v-card style="box-shadow: none; z-index: 1">
    <v-layout>
      <v-navigation-drawer v-model="filterOpen" temporary
        v-bind:style='{ "margin-top": (mobile ? "71.25px" : "160px") }' style="background-color: white; border: none"
        width="600">
        <athleten-filter />
      </v-navigation-drawer>


      <v-container class="py-10 pt-0">
        <h1>Athleten</h1>
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
                    <th>Disziplin</th>
                    <td>{{ tableData.discipline }}</td>
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
                    <td>{{ tableData.bestTimeBoatClass }}</td>
                  </tr>
                  <tr>
                    <th>Bestzeit Bootsklasse OZ/Jahr</th>
                    <td>{{ tableData.bestTimeBoatClassCurrentOZ }}</td>
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
import { mapState } from "pinia";
import { useAthletenState } from "@/stores/athletenStore";

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
    setFilterState() {
      this.filterOpen = !this.filterOpen;
      const store = useAthletenState()
      store.setFilterState(this.filterState)
    },
    checkScreen() {
      this.windowWidth = window.innerWidth;
      this.mobile = this.windowWidth <= 750
    },
  },
  created() {
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();
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
    border: 1px solid #e0e0e0;
    font-size: 14px !important;
    text-align: left;
  }

  td {
    text-align: left;
    border: 1px solid #e0e0e0;
  }
}

.nth-grey tr:nth-child(odd) {
  background-color: rgba(0, 0, 0, .05);
}
</style>