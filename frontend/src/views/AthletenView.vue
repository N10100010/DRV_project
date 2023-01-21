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
        <athleten-filter/>
      </v-navigation-drawer>


      <v-container class="pa-10">
        <h1>Athleten</h1>
        <v-divider></v-divider>
        <v-container class="pa-0 mt-8" style="min-height: 400px">
          <v-row>
            <v-col cols="6">
              <!--
             <v-table >
                <tbody>
                  <tr v-for="header in headers" :key="header">
                    <th>{{ header }}</th>
                    <td v-for="value in items[header]">{{ value }}</td>
                  </tr>
                </tbody>
              </v-table>
              -->
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

export default {
  computed: {
    ...mapState(useAthletenState, {
      filterState: "getFilterState"
    })
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
    }
  },
  created() {
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();
  },
  data() {
    return {
      mobile: false,
      filterOpen: this.filterState,
      headers: ["Test", "Test", "Test"]
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

<style scoped>
.filterToggleButton {
  position: fixed;
  z-index: 10;
  left: 0;
  border-radius: 0 5px 5px 0;
  color: #1369b0;
}

</style>