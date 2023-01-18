<template>
  <footer class="footer">
    <v-container>
      <RouterLink to="/impressum" style="color: white" class="pa-2">Impressum</RouterLink>
      <RouterLink to="/datenschutz" style="color: white" class="pa-2">Datenschutz</RouterLink>
    </v-container>
  </footer>
</template>


<style lang="scss" scoped>
.footer {
  text-align: center;
  margin: auto;
  left: 0;
  right: 0;
  width: 100%;
  background-color: #5cc5ed;
  justify-self: center;
  min-height: 100px;
}
</style>