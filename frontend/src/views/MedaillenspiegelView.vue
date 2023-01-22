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
          v-bind:style='{"margin-top" : (mobile? "71.25px" : "160px" )}'
          style="background-color: white; border: none"
          width="600">
        <medaillenspiegel-filter/>
      </v-navigation-drawer>
      <v-container class="pa-10">
        <v-col cols="6" class="d-flex flex-row px-0" style="align-items: center">
          <h1>Medaillenspiegel</h1>
          <v-icon id="tooltip-analyis-icon" color="grey" class="ml-2 v-icon--size-large">mdi-information-outline
          </v-icon>
          <v-tooltip
              activator="#tooltip-analyis-icon"
              location="end"
              open-on-hover
          >Im Rahmen des Medaillenspiegels können die Erfolge von Nationen betrachtet werden.<br>
            Wähle hierzu aus den Filteroptionen im Filter (links) einen Zeitraum und eine Nation aus.
          </v-tooltip>
        </v-col>
        <v-divider></v-divider>
        <v-container class="pa-0 mt-8">
          <v-col cols="6" class="pl-0">
            <v-alert type="success" variant="tonal" class="ma-0 pa-3" closable>
              <v-row>
                <v-col cols="6">
                  <b><p>{{ filterSelection.results }} Datensätze</p></b>
                  <p>Von: {{ filterSelection.start_date.slice(0, 4) }}</p>
                  <p>Bis: {{ filterSelection.end_date.slice(0, 4) }}</p>
                </v-col>
                <v-col cols="6">
                  <b><p>Bootsklassen: {{ filterSelection.boat_class }}</p></b>
                </v-col>
              </v-row>
            </v-alert>
          </v-col>
          <v-row>
            <v-col cols="6">
              <v-table class="tableStyles" density="comfortable">
                <tbody class="nth-grey">
                <tr v-for="(el, idx) in tableData[0]">
                  <th>{{ el }}</th>
                  <td>
                    <template v-if="typeof tableData[1][idx] === 'object'" v-for="(value, key) in tableData[1][idx]">
                      {{ value }} ({{ key }}) <br/>
                    </template>
                    <template v-else>
                      {{ tableData[1][idx] }}
                    </template>
                  </td>
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
    }),
    ...mapState(useMedaillenspiegelState, {
      filterSelection: "getFilterSelection"
    }),
    ...mapState(useMedaillenspiegelState, {
      tableData: "getTableData"
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
  color: #1369b0;
}

</style>