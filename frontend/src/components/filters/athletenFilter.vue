<template>
  <v-container>
  <h2>Filter</h2>
    <v-divider></v-divider>

    <v-form class="mt-2" id="berichteFilterFormular" @submit.prevent="onSubmit">
      <v-autocomplete :items="previewAthleteResults" v-model="selectedAthlete" clearable
          variant="underlined" color="blue" label="Athletenname" @input="searchAthletes"
      ></v-autocomplete>
      <br/>
      <v-autocomplete :items="optionsNations" v-model="selectedNation"
          variant="underlined" color="blue" label="Nation" clearable
      ></v-autocomplete>
      <v-select
            clearable
            :items="optionsBirthYear"
            variant="underlined"
            v-model="selectedBirthYear"
            label="Jahrgang"
          ></v-select>
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
import {useAthletenState} from "@/stores/athletenStore";

export default {
  components: {Checkbox},
  computed: {
    ...mapState(useAthletenState, {
      previewAthleteResults: "getPreviewAthleteResults"}),
    ...mapState(useAthletenState, {
      filterOptions: "getAthletenFilterOptions"}),
    ...mapState(useAthletenState, {
      showFilter: "getFilterState"}),
  },
  data() {
    return {
      // general
      mobile: false,
      hoverFilter: false,
      drawer: null,

      // athletes
      selectedAthlete: [],

      // year
      birthYear: 0,
      optionsBirthYear: [],

      // nations
      optionsNations: [],
      selectedNation: null,

      // boat classes
      genderTypeOptions: [],
      selectedGenders: [0],
      ageGroupOptions: [],
      selectedAgeGroups: 0,
      selectedBirthYear: null,
      optionsBoatClasses: [],
      selectedBoatClasses: this.optionsBoatClasses,
    }
  },
  created() {
    window.addEventListener('resize', this.checkScreen)
    this.checkScreen()

    //handle form data
    this.startYear = Object.values(this.filterOptions[0].year[0])[0]
    this.endYear = Object.values(this.filterOptions[0].year[1])[0]
    this.optionsBirthYear = Array.from({length: this.endYear - this.startYear + 1}, (_, i) => this.startYear + i)

    // competition category id
    this.compTypes = this.filterOptions[0].competition_category_ids
    this.optionsCompTypes = this.compTypes.map(item => item.displayName)

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
    searchAthletes(e) {
      const store = useAthletenState()
      const searchInput = e.target.value
      if(searchInput.length > 2) {
        store.postSearchAthlete({
          "searchInput": searchInput
        })
      }
    },

    onSubmit() {
      // define store
      const store = useTeamsState()
      // access form data
      const birthYear = this.birthYear
      const competitionTypes = this.compTypes.filter(item => this.optionsCompTypes.includes(item.displayName)).map(item => item.id)
      const nationCode = this.selectedNation
      const gender = this.selectedGenders

      // send data via pinia store action postFormData
      return store.postFormData({
        "birthYear": birthYear,
        "gender": gender,
        "competition_category_ids": competitionTypes,
        "nation_ioc": nationCode
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
      const store = useTeamsState()
      store.setFilterState(this.showFilter)
    }
  }
}

</script>