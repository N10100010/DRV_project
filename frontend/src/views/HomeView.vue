<template>
  <v-container :class="mobile ? 'px-5 main-container' : 'px-10 pt-0 main-container'">
    <v-col cols="12" class="pa-0 pt-0">
      <h1 class="py-3">Kalender</h1>
      <v-divider></v-divider>
      <v-row class="ma-0" style="display: flex; justify-content: space-between;">
  <v-chip-group filter color="blue" v-model="selectedView">
    <v-chip>Monat</v-chip>
    <v-chip>Jahr</v-chip>
  </v-chip-group>
  <v-list class="d-flex pa-0" style="background-color: transparent">
    <v-list-item v-for="(value, key) of legend" :key="key" class="d-flex pa-1">
      <div class="d-flex align-center">
        <div :style="{ backgroundColor: value, width: '25px', height: '25px', borderRadius: '2px', display: 'inline-block' }"></div>
        <p style="display: inline-block; padding-left: 5px;">{{ key }}</p>
      </div>
    </v-list-item>
  </v-list>
</v-row>

      <div class="text-center section">
        <v-calendar
            class="custom-calendar"
            :masks="masks"
            :attributes="attributes"
            disable-page-swipe
            is-expanded
            :style="{
              'border-radius': '0'}"
            :rows="selectedView ? 3 : 1"
            :columns="selectedView ? 4 : 1"
        >
          <template v-slot:day-content="{ day, attributes }">
            <div class="h-full z-10" style="min-height: 60px; display: flex; flex-direction: column;">
              <span class="day-label text-sm">{{ day.day }}</span>
              <div>
                <router-link style="color: white; display: flex; flex-direction: column;" to="/rennstrukturanalyse">
                  <div v-for="attr in attributes" class="rounded-sm my-1"
                            :key="attr.key" :style=attr.customData.style>
                    <p
                        class="leading-tight pa-1"
                        :style="{
                      wordWrap: 'break-word', display: 'inline-block',
                      lineHeight: 'normal', maxWidth: mobile ? '45px' : '120px', fontSize: mobile ? '11px' : '14px'
                    }"
                    >
                      {{ selectedView ? "" : attr.customData.title}}
                    </p>
                  </div>
                </router-link>
              </div>
            </div>
          </template>
        </v-calendar>
      </div>
    </v-col>
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
    ...mapState(useHomeStore, {
      legend: "getCalenderLegend"
    }),
  },
  data() {
    return {
      mobile: false,
      opacity: 0.65,
      masks: {
        weekdays: 'WWW',
      },
      attributes: [],
      selectedView: 0
    };
  },
  created() {
    this.attributes = this.calenderData
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();

    const store = useHomeStore()
    store.fetchCalendarData()
  },
  methods: {
    checkScreen() {
      this.windowWidth = window.innerWidth;
      this.mobile = this.windowWidth <= 750
      let navbarHeight = window.innerWidth < 750 ? '71.25px' : '160px';
      document.documentElement.style.setProperty('--navbar-height', navbarHeight);
    }
  },
  watch: {
    calenderData(newVal) {
      this.attributes = newVal
    },
     selectedView(newVal) {

    }
  }
};
</script>

<style scoped>
.main-container {
  min-height: calc(100vh - (var(--navbar-height)) - 95px);
}
</style>