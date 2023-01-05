<template>
  <v-container>
  <h2>Filter</h2>
    <v-divider></v-divider>
    <v-form id="rennstrukturFilterFormular" class="mt-2" @submit.prevent="onSubmit">

      <v-select class="pt-2"
        clearable
        label="Year"
        :items="auswahlYear"
        v-model="year"
        variant="underlined"
      ></v-select>

      <v-select class="pt-2"
                color="blue"
                clearable
                label="Wettkampfklassen"
                :items="auswahlWettkampfklassen"
                v-model="competition_type"
                variant="underlined"
      ></v-select>

      <v-label class="pt-2">Geschlecht (optional)</v-label>
      <v-chip-group filter color="blue" mandatory v-model="gender">
        <v-chip v-for="gender in genders" :value="gender">{{ gender }}</v-chip>
      </v-chip-group>


      <!-- The following content might be optional as it is a redundant selection criteria -->

      <!--
      <v-label class="pt-2">Altersklasse (optional)</v-label>
      <v-chip-group filter color="blue" mandatory>
        <v-chip>Open</v-chip>
        <v-chip>U19</v-chip>
        <v-chip>U23</v-chip>
      </v-chip-group>
      <v-label class="pt-2">Lauf (optional)</v-label>
      <v-chip-group filter color="blue">
        <v-chip>Finale</v-chip>
        <v-chip>Halbfinale</v-chip>
        <v-chip>Viertelfinale</v-chip>
        <v-chip>Hoffnungsläufe</v-chip>
        <v-chip>Vorläufe</v-chip>
      </v-chip-group>
      <v-select
          class="pt-2"
          clearable
          label="Lauf"
          :items="auswahlLauf"
          variant="underlined"
      ></v-select>
      -->
      <v-container class="pa-0 pt-6 text-right">
        <v-btn color="grey" class="mx-2"><v-icon>mdi-backspace-outline</v-icon></v-btn>
        <v-btn color="blue" class="mx-2" type="submit">Übernehmen</v-btn>
      </v-container>
    </v-form>
  </v-container>
</template>


<script>
import Checkbox from "@/components/filters/checkbox.vue";
import { useRennstrukturAnalyseState } from "@/stores/baseStore";
import {mapActions} from "pinia";

export default {
  components: { Checkbox },
  data() {
    return {
      competition_type: '',
      year: new Date().getFullYear(),
      gender: '',
      mobile: false,
      hoverFilter: false,
      drawer: null,
      auswahlYear: [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
      auswahlWettkampfklassen: [
        'European Championships',
        'Olympics',
        'Qualifications',
        'World Championships',
        'World Rowing Cup'
      ],
      genders: ["männlich", "weiblich"],
      auswahlLauf: [
          'FA', 'FB', 'FC', 'FD', 'F...'
      ],
      auswahlErgebnisse: [
        { id: 1, name: '1. Plätze (Gold-Standard, GS)', selected: false },
        { id: 2, name: 'Plätze 1-3', selected: false },
        { id: 3, name: 'Podium-Standard PS (Zeit zum Erreichen einer Medaille)', selected: false },
      ],
      auswahlRennkategorien: [
        {
          name: "Finals",
          auswahl: [
              { id: 1, name: 'FA', selected: false },
              { id: 2, name: 'FB', selected: false },
              { id: 3, name: 'FC', selected: false },
              { id: 4, name: 'FC', selected: false },
              { id: 4, name: 'F...', selected: false }
          ]
        },
        {
          name: "Halbfinals",
          auswahl: [
              { id: 1, name: 'SA/B SA/', selected: false },
              { id: 2, name: 'BB', selected: false },
              { id: 3, name: 'SC/D', selected: false },
              { id: 4, name: 'SD/E/F', selected: false },
              { id: 4, name: 'S...', selected: false }
          ]
        },
        {
          name: "Viertelfinals",
          auswahl: [
              { id: 1, name: 'Q1-4', selected: false },
              { id: 2, name: 'Q5-8', selected: false }
          ]
        }
      ]
    }
  },
  created() {
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();
  },

  methods: {
    onSubmit() {
      // define store
      const store = useRennstrukturAnalyseState();

      // access form data
      const year = this.year;
      const competition_type = this.competition_type;
      const gender = this.gender;

      // send data via pinia store action postFormData
      return store.postFormData({ year, competition_type, gender }).then(() => {
        alert("Form data sent...")
      }).catch(error => {
        console.error(error)
      });
    },
    checkScreen() {
      this.windowWidth = window.innerWidth;
      this.mobile = this.windowWidth <= 769;
    }
  }
}

</script>