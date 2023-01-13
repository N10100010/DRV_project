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
export default {
  data() {
    const month = new Date().getMonth();
    const year = new Date().getFullYear();
    return {
      masks: {
        weekdays: 'WWW',
      },
      attributes: [
        {
          key: 1,
          customData: {
            title: 'Olympics',
            style: 'background-color: #64B5F6'
          },
          dates: { start: new Date(year, 0, 14), end: new Date(year, 0, 18) },
        },
        {
          key: 2,
          customData: {
            title: 'World Rowing',
            style: 'background-color: #3949AB'
          },
          dates: new Date(year, month, 2),
        },
        {
          key: 3,
          customData: {
            title: "Qualifications",
            style: 'background-color: #CDDC39'
          },
          dates: new Date(year, month, 5),
        },
        {
          key: 4,
          customData: {
            title: 'World Rowing',
            style: 'background-color: #3949AB'
          },
          dates: new Date(year, month, 5),
        },
        {
          key: 4,
          customData: {
            title: 'World Rowing',
            style: 'background-color: #3949AB'
          },
          dates: new Date(year, month, 7),
        },
        {
          key: 5,
          customData: {
            title: "Other Event",
            style: 'background-color: #26A69A'
          },
          dates: new Date(year, month, 11),
        },
        {
          key: 7,
          customData: {
            title: "Event",
            style: 'background-color: #3949AB'
          },
          dates: new Date(year, month, 22),
        },
        {
          key: 8,
          customData: {
            title: 'One More',
            style: 'background-color: #26C6DA'
          },
          dates: new Date(year, month, 25),
        },
      ],
    };
  },
};
</script>
