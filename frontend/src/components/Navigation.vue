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
        document.querySelector('body').style.paddingTop = '4.5em';
        return;
      }
      this.mobile = false;
      this.mobileNav = false;
      document.querySelector('body').style.paddingTop = '10.6em';
      return;
    }
  }
}
</script>

<template>
  <div class="header-box">
    <header v-bind:style='{"padding-top" : (mobile? "0em" : "1.5em" )}' :class="{ 'scrolled-nav': scrollPosition }">
      <p id="desktop-title" v-show="!mobile">U ->- Row
        <li><a href="https://www.rudern.de/">Deutscher Ruderverband e.V.</a></li>
      </p>
      <nav v-bind:style='{"padding-top" : (!mobile? "2.1em" : "15px"), "padding-bottom" : (!mobile? "12px" : "5px")}'>
        <div v-show="!mobile" class="branding">
          <RouterLink to="/"><img alt="DRV Logo" class="logo" src="@/assets/images/DRV_Logo_white.svg" width="105" height="45"/></RouterLink>
        </div>
        <div v-show="mobile" class="branding-mobile">
          <RouterLink to="/"><img alt="DRV Logo" class="logo" src="@/assets/images/DRV_Logo_white.svg" width="64" height="30"/></RouterLink>
        </div>
        <ul v-show="!mobile" class="navigation">
          <li><RouterLink to="/">Allgemein</RouterLink>
            <!--<li>Test</li>-->
            <!--<li>Test</li>-->
          </li>
          <li><RouterLink to="/about">Women</RouterLink></li>
          <li><RouterLink to="/test">Men</RouterLink></li>
          <li><RouterLink to="/test">Sonstiges</RouterLink></li>
        </ul>
        <p v-show="mobile" id="mobile-title">U ->- Row</p>
        
        <div v-show="mobile" class="icon">
          <i @click="toggleMobileNav" class="far fa-bars" :class="{ 'icon-active': mobileNav }"></i>
        </div>
        <transition name="mobile-nav">
          <ul v-show="mobileNav" class="dropdown-nav">
            <li id="nav-header"><a href="https://www.rudern.de/">Deutscher Ruderverband e.V.</a></li>
            <li><RouterLink to="/" @click="toggleMobileNav">Allgemein</RouterLink>
              <!--<li>test</li>-->
            </li>
            <li><RouterLink to="/about" @click="toggleMobileNav">Women</RouterLink></li>
            <li><RouterLink to="/test" @click="toggleMobileNav">Men</RouterLink></li>
            <li><RouterLink to="/test" @click="toggleMobileNav">Sonstiges</RouterLink></li>
          </ul>
        </transition>
      </nav>
    </header>
  </div>
</template>
  
<style lang="scss" scoped>
header {
  top: 0;
  left: 0;
  right: 0;
  position: fixed;
  background-color: #5cc5ed;
  width: 100%;
  padding-bottom: 0.7em;
  z-index: 99;

  a.router-link-exact-active {
  color: #1369b0;
}

  nav {
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
      right: 10px;
      height: 100%;

      

      i {
        cursor: pointer;
        font-size: 24px;
        color: #fff;
        transition: 0.8s ease all;
      }
    }

    #mobile-title {
      margin-left: auto;
      margin-right: auto;
      width: 9em;
      align-self: center;
      color: #fff;
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
      max-width: 260px;
      height: 100%;
      background-color: #000000;
      top: 0;
      left: -2em;

      li {
        margin-left: 0;
        color: #fff;

        
      }

      #nav-header {
          font-size: 12px;
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
  @media(min-width: 750px) {
    border-top: 0.5rem solid #008000;
    border-bottom: 1rem solid #1369b0;
  }
  border-top: 0.25rem solid #008000;
  border-bottom: 0.5rem solid #1369b0;
  }
}

p {
  font-size: 14px;
  text-transform: uppercase;
  position: relative;
  display: flex;
  flex-direction: row;
  transition: 0.5s ease all;
  width: 90%;
  margin: 0 auto;
  @media(min-width: 1140px) {
    max-width: 1140px;
  }
  color: #d6f0fa;
  font-style: italic;

  a {
    color: #d6f0fa;
  }

  a:hover {
    color: #1369b0;
  }

  li {
    list-style: none;
    margin-left: auto;
  }
}
</style>