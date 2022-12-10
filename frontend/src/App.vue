<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import Navigation from './components/Navigation.vue'
import BarChart from './components/charts/BarChart.vue';
</script>

<template>
  <header>
    <div>

      
      <div><Navigation/></div>
      


     
    </div>
  </header>
  <body>
    <div ><BarChart/></div>
    <RouterView />
  </body>
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
  display: flex;
  flex-direction: column;
  align-items: stretch;
  padding-left: 2em;
  padding-right: 2em;
}
</style>
