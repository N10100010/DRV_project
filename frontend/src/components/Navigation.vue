<script setup>
</script>

<template>
    <header :class="{ 'scrolled-nav': scrollPosition }">
      <nav>
        <div class="branding">
          <img scr="@assets/DRV_Logo.png" alt="">
        </div>
        <ul v-show="!mobile" class="navigation">
          <li><RouterLink to="/">Allgemein</RouterLink></li>
          <li><router-link class="link" :to="{name: ''}">Women</router-link></li>
          <li><router-link class="link" :to="{name: ''}">Men</router-link></li>
          <li><router-link class="link" :to="{name: ''}">Sonstiges</router-link></li>
        </ul>
        <div class="icon">
          <i @click="toggleMobileNav" v-show="mobile" class="far fa-bars" :class="{'icon-active' : mobileNav}"></i>
        </div>
        <transition name="mobile-nav">
          <ul v-show="mobileNav" class="dropdown-nav">
            <li><router-link class="link" :to="{name: ''}">Allgemein</router-link></li>
            <li><router-link class="link" :to="{name: ''}">Women</router-link></li>
            <li><router-link class="link" :to="{name: ''}">Men</router-link></li>
            <li><router-link class="link" :to="{name: ''}">Sonstiges</router-link></li>
          </ul>
        </transition>
      </nav>
    </header>
  </template>
  
  <style lang="scss" scoped>
  </style>