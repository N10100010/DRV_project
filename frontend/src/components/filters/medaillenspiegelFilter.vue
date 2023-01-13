<template>
  <v-container>
  <h2>Filter</h2>
    <v-divider></v-divider>

    <v-form class="mt-2" id="berichteFilterFormular" @submit.prevent="onSubmit">

      <v-label class="pt-2">Zeitraum</v-label>
      <v-container class="pa-0 d-flex">
        <v-col cols="6" class="pa-0">
          <v-select
            clearable
            label="Von"
            :items="optionsStartYear"
            variant="underlined"
            v-model="startYear"
          ></v-select>
        </v-col>
        <v-col cols="6" class="pa-0">
          <v-select
            clearable
            label="Bis"
            :items="optionsEndYear"
            v-model="endYear"
            variant="underlined"
          ></v-select>
        </v-col>
      </v-container>
      <v-select class="pt-2"
                clearable chips multiple
                color="blue"
                label="Wettkampfklassen"
                :items="optionsCompTypes"
                v-model="optionsCompTypes"
                variant="underlined"
      ></v-select>
      <v-label>Medaillientyp</v-label>
      <v-chip-group filter color="blue" multiple v-model="selectedMedalTypes">
        <v-chip v-for="medalType in optionsMedalTypes">{{medalType}}</v-chip>
      </v-chip-group>
      <v-autocomplete :items="optionsNations" v-model="selectedNation"
          variant="underlined" color="blue" label="Nation"
      ></v-autocomplete>
      <v-label>Geschlecht</v-label>
      <v-chip-group filter color="blue" v-model="selectedGenders">
        <v-chip v-for="genderType in genderTypeOptions">{{genderType}}</v-chip>
      </v-chip-group>
      <v-label class="pt-2">Altersklasse</v-label>
      <v-chip-group filter color="blue" v-model="selectedAgeGroups">
        <v-chip v-for="ageGroup in ageGroupOptions">{{ageGroup}}</v-chip>
      </v-chip-group>
      <v-select label="Bootsklassen" clearable chips
                :items="optionsBoatClasses" v-model="selectedBoatClasses" variant="underlined"
      ></v-select>

      <v-container class="pa-0 pt-8 text-right">
        <v-btn color="grey" class="mx-2"><v-icon>mdi-backspace-outline</v-icon></v-btn>
        <v-btn color="blue" class="mx-2" type="submit" @click="setFilterState">Übernehmen</v-btn>
      </v-container>

    </v-form>
  </v-container>
</template>


<script>
import Checkbox from "@/components/filters/checkbox.vue";
import {mapState} from "pinia";
import {useMedaillenspiegelState} from "@/stores/medaillenspiegelStore";

export default {
  components: {Checkbox},
  computed: {
    ...mapState(useMedaillenspiegelState, {
      filterOptions: "getMedaillenspiegelFilterOptions"}),
    ...mapState(useMedaillenspiegelState, {
      showFilter: "getFilterState"}),
  },
  data() {
    return {
      // general
      mobile: false,
      hoverFilter: false,
      drawer: null,

      // competition type
      compTypes: [], // list of dicts with objects containing displayName, id and key
      optionsCompTypes: ["Olympics", "World Rowing Championships", "Qualifications"], // default strings

      // year
      startYear: 0,
      endYear: 0,
      optionsStartYear: [],
      optionsEndYear: [],

      // medal types
      optionsMedalTypes: [],
      selectedMedalTypes: [],

      // nations
      optionsNations: [],
      selectedNation: null,

      // boat classes
      genderTypeOptions: [],
      selectedGenders: [0],
      ageGroupOptions: [],
      selectedAgeGroups: 0,
      optionsBoatClasses: [],
      selectedBoatClasses: this.optionsBoatClasses,
    }
  },
  created() {
    window.addEventListener('resize', this.checkScreen)
    this.checkScreen()

    // handle form data
    this.startYear = Object.values(this.filterOptions[0].year[0])[0]
    this.endYear = Object.values(this.filterOptions[0].year[1])[0]
    this.optionsStartYear = Array.from({length: this.endYear - this.startYear + 1}, (_, i) => this.startYear + i)
    this.optionsEndYear = Array.from({length: this.endYear - this.startYear + 1}, (_, i) => this.startYear + i)

    // competition category id
    this.compTypes = this.filterOptions[0].competition_category_ids
    this.optionsCompTypes = this.compTypes.map(item => item.displayName)

    // medal types
    this.optionsMedalTypes = this.filterOptions[0].medal_types.map(item => item.displayName)

    // nation_code
    let countryCodes = Object.keys(this.filterOptions[0].nations)
    let countryNames = Object.values(this.filterOptions[0].nations)
    let finalCountryNames = []
    for (const [idx, countryCode] of countryCodes.entries()) {
      finalCountryNames.push(countryCode + " (" + countryNames[idx] + ")")
    }
    this.optionsNations = finalCountryNames

    // boatclasses
    this.genderTypeOptions = Object.keys(this.filterOptions[0].boat_class)
    let ageGroupOptions = Object.keys(this.filterOptions[0].boat_class.men)
    ageGroupOptions.push(...Object.keys(this.filterOptions[0].boat_class.women))
    this.ageGroupOptions = ageGroupOptions.filter((v, i, a) => a.indexOf(v) === i); // exclude non-unique values

    let boatClassOptions = []
    let values = Object.values(this.filterOptions[0].boat_class)[0]
    Object.entries(values).forEach(([key, value], index) => {
          if (index === 0) {
            Object.entries(value).forEach(([, val]) => {
              if (typeof val === "object") {
                boatClassOptions.push(Object.values(val)[0])
              }
            })
          }
      });
    this.selectedBoatClasses = boatClassOptions[0]
    this.optionsBoatClasses = boatClassOptions
  },
  methods: {
    onSubmit() {
      // define store
      const store = useMedaillenspiegelState()
      // access form data
      const startYear = this.startYear
      const endYear = this.endYear
      const competitionTypes = this.compTypes.filter(item => this.optionsCompTypes.includes(item.displayName)).map(item => item.id)
      const nationCode = this.selectedNation
      const medalTypes = this.selectedMedalTypes
      const gender = this.selectedGenders

      // send data via pinia store action postFormData
      return store.postFormData({
        "years": [{"start_year": startYear}, {"end_year": endYear}],
        "gender": gender,
        "competition_category_ids": competitionTypes,
        "nation_ioc": nationCode,
        "medal_types": medalTypes
      }).then(() => {
        console.log("Form data sent...")
      }).catch(error => {
        console.error(error)
      })
    },
    checkScreen() {
      this.windowWidth = window.innerWidth
      this.mobile = this.windowWidth <= 769
    },
    setFilterState() {
      const store = useMedaillenspiegelState()
      store.setFilterState(this.showFilter)
    }
  }
}

</script>