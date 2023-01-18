<template>
  <v-container class="pa-10">
  <h1>Allgemeines</h1>
  <v-divider></v-divider>
  <v-container class="pa-0 mt-8" style="min-height: 450px">
    <h2>Aktuelles</h2>
    <v-alert class="mb-10">
      Platzhalter für Inhalte (z.B. Letzte/aktuelle Weltbestzeiten, Aktuelle Trend Fahrzeiten etc.)
    </v-alert>
    <h2>Kalender</h2>
    <div class="text-center section">
    <v-calendar
      class="custom-calendar"
      :masks="masks"
      :attributes="attributes"
      disable-page-swipe
      is-expanded
    >
      <template v-slot:day-content="{ day, attributes }">
        <div class="flex flex-col h-full z-10 overflow-hidden">
          <span class="day-label text-sm">{{ day.day }}</span>
          <div class="flex-grow overflow-y-auto overflow-x-auto">
            <router-link style="color: white" to="/wettkampfresultate">
            <p
              v-for="attr in attributes"
              :key="attr.key"
              class="text-xs leading-tight rounded-sm p-1 mt-0 mb-1"
              :style=attr.customData.style
            >{{ attr.customData.title }}
            </p>
              </router-link>
          </div>
        </div>
      </template>
    </v-calendar>
  </div>
  </v-container>
  </v-container>
</template>



<script>
import {mapState} from "pinia";
import {useHomeStore} from "@/stores/homeStore";

export default {
  computed: {
    ...mapState(useHomeStore, {
      calenderData: "getCalenderData"
    }),
  },
  data() {
    return {
      masks: {
        weekdays: 'WWW',
      },
      attributes: [],
    };
  },
  created() {
    this.attributes = this.calenderData
  },
  watch: {
    calenderData(newVal) {
      this.attributes = newVal
    }
  }
};
</script>
