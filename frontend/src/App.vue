<script setup>
import { RouterView } from 'vue-router'
import Navigation from './components/Navigation.vue'
import FooterC from './components/Footer.vue';

/* get data via pinia store */
import { onMounted, computed } from "vue";
import { useTestState } from "./stores/baseStore";
const store = useTestState();
const getData = computed(() => {
  return store.getTestData;
});
onMounted(() => {
  store.fetchData();
});

</script>

<template>
  <header>
    <Navigation />
  </header>
  <v-container>
    <RouterView />


    <!-- added test for pinia store api response -->
    <p><b>Test-Abfrage für Pinia-State-Management Store:</b></p>
    <p>{{ getData }}</p>

  </v-container>
  <FooterC />
</template>

<style lang="scss" scoped>
.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

body {
  margin: 0;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  padding-left: 2em;
  padding-right: 2em;
}
</style>
