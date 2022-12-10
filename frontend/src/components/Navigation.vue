<script>
export default {
  name: "navigation",
  data() {
    return {
      scrollPosition: null,
      mobile: null,
      mobileNav: null,
      windowWidth: null
    };
  },
  created() {
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();
  },

  methods: {
    toggleMobileNav() {
      this.mobileNav = !this.mobileNav;
    },

    checkScreen() {
      this.windowWidth = window.innerWidth;
      if(this.windowWidth <= 750){
        this.mobile = true;
        return;
      }
      this.mobile = false;
      this.mobileNav = false;
      return;
    }
  }
}
  

</script>

<template>
  <div class="header-box">
    <header v-bind:style='{"padding-top" : (mobile? "0.1em" : "2.7em" )}' :class="{ 'scrolled-nav': scrollPosition }">
      <nav class>
        
        <div class="branding">
          <img alt="DRV Logo" class="logo" src="@/assets/DRV_Logo_white.svg" width="100" height="70"/>
        </div>
        <ul v-show="!mobile" class="navigation">
          <li><RouterLink to="/">Allgemein</RouterLink>
            <!--<li>Test</li>-->
            <!--<li>Test</li>-->
          </li>
          <li><RouterLink to="/about">Women</RouterLink></li>
          <li><RouterLink to="">Men</RouterLink></li>
          <li><RouterLink to="">Sonstiges</RouterLink></li>
        </ul>
        
        <div class="icon">
          <i @click="toggleMobileNav" v-show="mobile" class="far fa-bars" :class="{ 'icon-active': mobileNav }"></i>
        </div>
        <transition name="mobile-nav">
          <ul v-show="mobileNav" class="dropdown-nav">
            <li @click="toggleMobileNav"><RouterLink to="/">Allgemein</RouterLink>
              <!--<li>test</li>-->
            </li>
            <li @click="toggleMobileNav"><RouterLink to="/about">Women</RouterLink></li>
            <li @click="toggleMobileNav"><RouterLink to="">Men</RouterLink></li>
            <li @click="toggleMobileNav"><RouterLink to="">Sonstiges</RouterLink></li>
          </ul>
        </transition>
      </nav>
    </header>
  </div>
</template>
  
<style lang="scss" scoped>
header {
  background-color: #5cc5ed;
  width: 100%;
  z-index: 99;
  padding-bottom: 0.5em;

  nav {
    position: relative;
    display: flex;
    flex-direction: row;
    padding: 12px 0;
    transition: 0.5s ease all;
    width: 90%;
    margin: 0 auto;
    @media(min-width: 1140px) {
      max-width: 1140px;
    }

    ul {
      list-style: none;
    }
    
    li {
      text-transform: uppercase;
      font-size: large;
      font-style: italic;
      padding: 16px;
      margin-left: 16px;
    }

    a {
      color: #fff;
    }

    a:hover {
      color: #1369b0;
    }

    .navigation {
      display: flex;
      align-items: center;
      flex: 1;
    }

    .icon {
      display: flex;
      align-items: center;
      position: absolute;
      top: 0;
      right: 24px;
      height: 100%;

      i {
        cursor: pointer;
        font-size: 24px;
        color: #fff;
        transition: 0.8s ease all;
      }
    }

    .icon-active {
      transform: rotate(180deg);

    }

    .dropdown-nav {
      z-index: 1;
      display: flex;
      flex-direction: column;
      position: fixed;
      width: 100%;
      max-width: 250px;
      height: 100%;
      background-color: #000000;
      top: 0;
      left: 0;

      li {
        margin-left: 0;
        color: #fff;
      }
    }

    .mobile-nav-enter-active,
    .mobile-nav-leave-active {
      transition: 1s ease all;
    }

    .mobile-nav-enter-from,
    .mobile-nav-leave-to {
      transform: translateX(-250px);
    }

    .mobile-nav-enter-to {
      transform: translateX(0);
    }

    


  }
  header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  border-top: 0.5em solid #008000;
  border-bottom: 1em solid #1369b0;
  }

  
}



.branding {
  padding-left: 0em;
}

p {
  padding-top: 16px;
  padding: 16px;
  color: #d6f0fa;
  font-style: italic;
  font-size: 14px;
}
</style>