<template>
  <v-container :class="mobile ? 'px-5 main-container' : 'px-10 pt-0 main-container'">
    <v-col cols="12" class="pa-0 pt-0" justify="center">
      <h1 class="py-3">Login</h1>
      <v-col cols="6" class="px-0">
        <v-alert type="info" variant="tonal">
          Diese Seite ist passwortgeschützt. Bitte melde dich an um fortzufahren.
        </v-alert>
      </v-col>
      <v-col cols="12" sm="8" md="4" class="px-0">
        <v-form class="px-0">
          <v-text-field
              label="Nutzername"
              v-model="username"
              variant="outlined"
              density="compact"></v-text-field>
          <v-text-field
              label="Passwort"
              type="password"
              v-model="password"
              variant="outlined"
              density="compact"></v-text-field>
          <v-btn color="#1369b0" style="color: white" @click="login">Login</v-btn>
        </v-form>
      </v-col>
    </v-col>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      username: 'drv_test_user',
      password: '000000'
    }
  },
  created() {
    this.attributes = this.calenderData
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();
  },
  methods: {
    login() {

      const token = 'test_token_value'
      const expires = Date.now() + 7 * 24 * 60 * 60 * 1000

      localStorage.setItem('token', token)
      localStorage.setItem('expires', expires)

      if (Date.now() >= localStorage.getItem('expires')) {
        localStorage.removeItem('token')
        localStorage.removeItem('expires')
      } else {
        console.log("Wird ausgeüfhrt.")
        const url = new URL(window.location.href);
        const redirectTo = url.searchParams.get("redirect_to");
        if (redirectTo) {
          window.location.href = redirectTo;
        }
      }
    },
    checkScreen() {
      this.windowWidth = window.innerWidth;
      this.mobile = this.windowWidth <= 750
      let navbarHeight = window.innerWidth < 750 ? '71.25px' : '160px';
      document.documentElement.style.setProperty('--navbar-height', navbarHeight);
    }
  }
}
</script>

<style scoped>
.main-container {
  min-height: calc(100vh - (var(--navbar-height)) - 95px);
}
</style>
