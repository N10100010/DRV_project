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
          v-bind:style='{"margin-top" : (mobile? "71.25px" : "160px" )}'
          style="background-color: white; border: none"
          width="600">
        <medaillenspiegel-filter/>
      </v-navigation-drawer>
      <v-container class="pa-10">
        <h1>Medaillenspiegel</h1>
        <v-divider></v-divider>
        <v-container class="pa-0 mt-8">
          <v-row>
            <v-col cols="6">
              <v-table class="tableStyles">
                <tbody class="nth-grey">
                <tr v-for="header in headers" :key="header">
                  <th>{{ header }}</th>
                  <td v-for="value in items[header]">{{ value }}</td>
                </tr>
                </tbody>
              </v-table>
            </v-col>
            <v-col cols="6">
              <BarChart :data="medalChartData"></BarChart>
            </v-col>
          </v-row>
        </v-container>
      </v-container>
    </v-layout>
  </v-card>
</template>

<script setup>
import MedaillenspiegelFilter from "@/components/filters/medaillenspiegelFilter.vue";
import BarChart from "@/components/charts/BarChart.vue";
</script>

<script>
import {mapState} from "pinia";
import {useBerichteState} from "@/stores/berichteStore";
import {useMedaillenspiegelState} from "@/stores/medaillenspiegelStore";

export default {
  computed: {
    ...mapState(useMedaillenspiegelState, {
      filterState: "getFilterState"
    }),
    ...mapState(useMedaillenspiegelState, {
      medalChartData: "getBarChartData"
    }),
    ...mapState(useMedaillenspiegelState, {
      filterState: "getFilterState"
    })
  },
  methods: {
    setFilterState() {
      this.filterOpen = !this.filterOpen;
      const store = useMedaillenspiegelState()
      store.setFilterState(this.filterState)
    },
    checkScreen() {
      this.windowWidth = window.innerWidth;
      this.mobile = this.windowWidth <= 750
    }
  },
  data() {
    return {
      mobile: false,
      filterOpen: false,
      chartData: {
        "data": [4, 5, 2, 5]
      },
      headers: [
        'Platz',
        'Punkte',
        'Nation_IOC',
        'Medaillen_Gold',
        'Medaillen_Silber',
        'Medaillen_Bronze',
        'Medaillen_Gesamt',
        'Finale_A',
        'Finale_B'
      ],
      items: {
        'Platz': ['1'],
        'Punkte': ['1000'],
        'Nation_IOC': ['USA'],
        'Medaillen_Gold': ['5'],
        'Medaillen_Silber': ['3'],
        'Medaillen_Bronze': ['2'],
        'Medaillen_Gesamt': ['10'],
        'Finale_A': ['Ja'],
        'Finale_B': ['Nein']
      }
    }
  },
  created() {
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();
  },
  watch: {
    filterState(newValue) {
      this.filterOpen = newValue;
    },
    filterOpen: function (newVal, oldVal) {
      if (oldVal === true && newVal === false && this.filterState === true) {
        const store = useMedaillenspiegelState()
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
  }

  td {
    text-align: center;
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
}

</style>