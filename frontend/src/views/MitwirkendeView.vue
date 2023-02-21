<template>
  <v-container :class="mobile ? 'px-5 py-2 main-container' : 'px-10 pt-0 main-container'">
    <v-col cols="12" class="d-flex flex-row px-0" style="align-items: center">
      <h1>Mitwirkende</h1>
    </v-col>
    <v-divider></v-divider>
    <v-container class="pa-0 mt-2" style="min-height: 450px">
      <v-row class="mt-2 mb-2" style="min-height: 450px">
      <v-col :cols="mobile ? 12 : 6">
        <h2>UI/UX</h2>
        <p>Anke Müller</p>
        <br>
        <h2>Frontend</h2>
        <p>Harri Faßbender<br />
          Julian Fritzmann</p>
        <br>
        <h2>Backend</h2>
        <p>Nicolas Reinhart<br />
          Raphael Wettinger<br />
          Harri Faßbender</p>
      </v-col>
      <v-col :cols="mobile ? 12 : 6">
        <h2>Entwicklung</h2>
        <p>Diese Web-App wurde im Wintersemester 2022/2023 im Rahmen eines Innovationsprojekts in Kooperation mit dem Deutschen Ruderverband am Institute for Applied Artificial Intelligence (IAAI) an der Hochschule der Medien Stuttgart entwickelt.</p>
        <br>
        <a href="https://ai.hdm-stuttgart.de/" class="pr-5"><img src="@/assets/images/IAAI_Logo_black.svg" width="100"></a>
        <a href="https://www.hdm-stuttgart.de/" class="pl-5"><img src="@/assets/images/HDM_Logo_black.svg" width="80"></a>
      </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script>
export default {
  created(){
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();
    window.scrollTo(0, 0)
  },
  methods: {
    checkScreen() {
      this.windowWidth = window.innerWidth;
      this.mobile = this.windowWidth < 890
      let navbarHeight = window.innerWidth < 890 ? '71.25px' : '160px';
      document.documentElement.style.setProperty('--navbar-height', navbarHeight);
    }
  },
  data() {
    return {
      mobile: false,
    }
  }
}
</script>

<style lang="scss" scoped>
.main-container {
  min-height: calc(100vh - (var(--navbar-height)) - 95px);
}
</style>