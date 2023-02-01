<script setup>
import TeamsFilter from "@/components/filters/teamsFilter.vue";
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
         <teams-filter/>
        </v-navigation-drawer>

  <v-container :class="mobile ? 'px-5 py-0 main-container' : 'px-10 py-0 main-container'">
    <v-col cols="12" class="d-flex flex-row px-0" style="align-items: center">
    <h1>Teams</h1>
      <v-icon id="tooltip-teams-icon" color="grey" class="ml-2 v-icon--size-large">mdi-information-outline
          </v-icon>
          <v-tooltip
              activator="#tooltip-teams-icon"
              location="end"
              open-on-hover
          >Hier findest du die Zusammensetzung der gewählten Nationalmannschaft
            mit Besetzung der Bootsklassen.
          </v-tooltip>
    </v-col>
    <v-divider></v-divider>
    <v-container class="pa-0 mt-8" style="min-height: 400px">
      <v-row>
        <v-col cols="12">
          <h2>{{ Object.values(tableData["year"][0])[0] }} bis {{ Object.values(tableData["year"][1])[0] }}</h2>
            <v-table class="tableStyles" density="comfortable">
              <thead>
                <tr>
                  <th>Team</th>
                  <th>Nation</th>
                  <th>Bootsklasse</th>
                  <th>Athleten</th>
                </tr>
              </thead>
              <tbody class="nth-grey">
                <tr v-for="(team, idx) in tableData.teams">
                  <td>{{ idx + 1 }}</td>
                  <td>{{ team.nation_ioc }}</td>
                  <td>{{ team.boatClass }}</td>

                  <!--
                  <td>
                    <p v-for="item, idx in team.athletes">
                      {{ team.athletes[idx].firstName }} {{ team.athletes[idx].lastName }}<br>
                    </p>
                  </td>
                  <td>
                    <p v-for="item, idx in team.athletes">
                      {{ team.athletes[idx].discipline }}<br>
                    </p>
                  </td>
                  <td>
                    <p v-for="item, idx in team.athletes">
                      {{ team.athletes[idx].gender == 'male' ? 'Männlich' : 'Weiblich' }}<br>
                    </p>
                  </td>
                  -->

                  <!--
                  <td>
                    <template v-for="athlete, idx in team.athletes">
                      <p class="distance">{{ athlete.firstName }} {{ athlete.lastName }}</p>                    
                      <p class="distance">{{ athlete.gender == 'male' ? 'Männlich' : 'Weiblich' }}</p>
                      <p class="distance">{{ athlete.discipline }}</p>
                      
                      <br v-if="idx+1 < team.athletes.length">
                    </template>
                  </td>
                  -->

                  <!--
                  <td>
                    <p v-for="athlete, idx in team.athletes" class="distance">
                      <p>{{ athlete.firstName }} {{ athlete.lastName }}</p>                    
                      <p>{{ athlete.gender == 'male' ? 'Männlich' : 'Weiblich' }}</p>
                      <p>{{ athlete.discipline }}</p>
                    </p>
                  </td>
                  -->

                  <td>
                    <template v-for="(athlete, idx) in team.athletes" class="pt-1 pb-1 distance">
                      <p>
                        <b>{{ athlete.firstName }} {{ athlete.lastName }}</b>
                      ({{ athlete.discipline }})</p>
                    </template>
                  </td>

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

<script>
import { mapState } from "pinia";
import { useTeamsState } from "@/stores/teamsStore";

export default {
  computed: {
    ...mapState(useTeamsState, {
      filterState: "getFilterState"
    }),
    ...mapState(useTeamsState, {
      tableData: "getTableData"
    })
  },
  methods: {
    setFilterState() {
      this.filterOpen = !this.filterOpen;
      const store = useTeamsState()
      store.setFilterState(this.filterState)
    },
    checkScreen() {
      this.windowWidth = window.innerWidth;
      this.mobile = this.windowWidth <= 750
      let navbarHeight = window.innerWidth < 750 ? '71.25px' : '160px';
      document.documentElement.style.setProperty('--navbar-height', navbarHeight);
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
    }
  },
  watch: {
    filterState(newValue) {
      this.filterOpen = newValue;
    },
    filterOpen: function (newVal, oldVal) {
      if (oldVal === true && newVal === false && this.filterState === true) {
        const store = useTeamsState()
        store.setFilterState(oldVal)
      }
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
.distance {
  display: inline-block;
  padding-right: 10px;
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
  min-height: calc(100vh - (var(--navbar-height)) - 100px);
}

@media print {
  i, .filterToggleButton, .filterToggleButtonMobile {
    display: none;
  }
}
</style>
