<template>
  <v-container :class="mobile ? 'px-5 main-container' : 'px-10 pt-0 main-container'">
  <v-col cols="12" class="pa-0 pt-0">
    <h1 class="py-3">Kalender</h1>
    <v-divider></v-divider>
    <div class="text-center section pt-5">
    <v-calendar
      class="custom-calendar"
      :masks="masks"
      :attributes="attributes"
      disable-page-swipe
      is-expanded
      style="border-radius: 0"
    >
      <template v-slot:day-content="{ day, attributes }">
        <div class="flex flex-col h-full z-10 overflow-hidden" style="height: 75px">
          <span class="day-label text-sm">{{ day.day }}</span>
          <div class="flex-grow">
            <router-link style="color: white" to="/wettkampfresultate">
            <p
              v-for="attr in attributes"
              :key="attr.key"
              class="leading-tight rounded-sm p-1 mt-0 mb-1"
              :style=attr.customData.style
            > {{mobile ?  attr.customData.shortTitle : attr.customData.title }}
            </p>
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
  },
  data() {
    return {
      mobile: false,
      masks: {
        weekdays: 'WWW',
      },
      attributes: [],
    };
  },
  created() {
    this.attributes = this.calenderData
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();
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
    }
  }
};
</script>

<style scoped>
.main-container {
  min-height: calc(100vh - (var(--navbar-height)) - 100px);
}
</style>