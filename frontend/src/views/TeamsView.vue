<script setup>
import TeamsFilter from "@/components/filters/teamsFilter.vue";
import 'chartjs-adapter-moment';
import {Chart as ChartJS, LinearScale, PointElement, Tooltip, Legend, TimeScale} from "chart.js";
ChartJS.register(LinearScale, PointElement, Tooltip, Legend, TimeScale);

</script>

<template>

  <v-btn color="blue"
         @click="setFilterState()" v-show="!filterOpen"
         class="filterToggleButton mt-6 pa-0 ma-0 bg-light-blue"
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
         <teams-filter/>
        </v-navigation-drawer>

  <v-container class="pa-10">
    <h1>Teams</h1>
    <v-divider></v-divider>
    <v-container class="pa-0 mt-8" style="min-height: 400px">
      <v-row>
        <v-col cols="12">
          <v-container style="background-color: whitesmoke; min-height: 200px;">
            <v-table>
              <thead>
                <tr>
                  <th>Nation</th>
                  <th>Bootsklasse</th>
                  <th>Athleten</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <!--<td>{{ tableData }}</td>-->
                  <!--<td>{{ tableData.boatClass }}</td>
                  <td>
                    <p v-for="athlete in tableData.athletes">
                      {{ athlete.firstName }}
                      {{ athlete.lastName }}<br>
                      {{ athlete.gender }}
                    </p>
                  </td>-->
                </tr>
              </tbody>
            </v-table>
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

<style scoped>
.filterToggleButton {
  position: fixed;
  z-index: 10;
  left: 0;
  border-radius: 0 5px 5px 0;
}

</style>