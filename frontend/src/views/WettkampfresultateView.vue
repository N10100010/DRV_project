<script setup>
import RennstrukturFilter from "@/components/filters/rennstrukturFilter.vue";
</script>

<template>
  <v-btn color="blue"
         @click="drawer = !drawer" v-show="!drawer"
         style="position: fixed; z-index: 999; left: 0; border-radius: 0"
         class="mt-8"
  >
    <v-icon>mdi-filter</v-icon>
  </v-btn>
  <v-card style="box-shadow: none; z-index: 1">
      <v-layout>
        <v-navigation-drawer
      v-model="drawer"
      temporary
      style="margin-top: 160px; background-color: white; border: none"
      width="500">
    <rennstruktur-filter/>
  </v-navigation-drawer>



  <v-container class="pa-10" style="max-width: 1024px">
  <h1>Wettkampfresultate</h1>
  <v-divider></v-divider>
  <v-container class="pa-0 mt-8" style="min-height: 500px">
    <v-row>
      <v-col cols="6">
        <h2>Tabellen</h2>
        <v-container style="background-color: whitesmoke; height: 80%">
          <p>Placeholder for Table(s)</p>
        </v-container>
      </v-col>
      <v-col cols="6">
      </v-col>
    </v-row>
  </v-container>
    </v-container>

         </v-layout>
</v-card>
</template>

<script>

export default {
  data() {
    return {
      drawer: true,
      mobile: false
    }}}
</script>