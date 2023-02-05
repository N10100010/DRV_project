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
            nextMonthComps
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
                      {{ attr.customData.title }}
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
    }
  }
};
</script>

<style scoped>
.main-container {
  min-height: calc(100vh - (var(--navbar-height)) - 95px);
}
</style>