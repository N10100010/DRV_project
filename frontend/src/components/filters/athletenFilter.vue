<template>
  <v-container>
    <v-row>
      <v-col>
        <h2>Suche</h2>
      </v-col>
      <v-col class="text-right">
        <i class="mdi mdi-close" style="font-size: 25px; color: darkgrey" @click="hideFilter"></i>
      </v-col>
    </v-row>
    <v-form class="mt-2" id="athletenFilterFormular"
            v-model="formValid" lazy-validation
            @submit.prevent="onSubmit" ref="filterForm">
      <v-autocomplete :items="previewAthleteResults" v-model="selectedAthlete" clearable
                      variant="outlined" color="blue" label="Athlet" @input="searchAthletes"
                      class="pt-2" :rules="[v => !!v || 'Athletenname darf nicht leer sein']"
                      autofocus
      ></v-autocomplete>
      <h2 class="pt-3">Filter</h2>
      <v-divider></v-divider>
      <v-row class="pt-4">
      <v-col>
        <v-autocomplete :items="optionsNations" v-model="selectedNation"
                      variant="outlined" color="blue" label="Nation (optional)" clearable
                      density="comfortable"
      ></v-autocomplete>
      </v-col>
       <v-col>
          <v-select clearable :items="optionsBirthYear" variant="outlined"
                v-model="selectedBirthYear" label="Jahrgang (optional)" density="comfortable"
      ></v-select>
       </v-col>
      </v-row>
      <v-chip-group filter color="blue" v-model="selectedGenders">
        <v-chip v-for="genderType in genderTypeOptions">{{ genderType.charAt(0).toUpperCase() + genderType.slice(1) }}
        </v-chip>
      </v-chip-group>
      <v-chip-group filter color="blue" v-model="selectedAgeGroups">
        <v-chip v-for="ageGroup in ageGroupOptions">{{ ageGroup.charAt(0).toUpperCase() + ageGroup.slice(1) }}</v-chip>
      </v-chip-group>
      <v-select class="pt-3" label="Bootsklasse (optional)" clearable chips density="comfortable"
                :items="optionsBoatClasses" v-model="selectedBoatClasses" variant="outlined"
      ></v-select>
      <v-container class="pa-0 pt-8 text-right">
        <v-btn color="grey" class="mx-2" @click="clearFormInputs">
          <v-icon>mdi-backspace-outline</v-icon>
        </v-btn>
        <v-btn color="blue" class="mx-2" type="submit" @click="setFilterState">Übernehmen</v-btn>
      </v-container>
    </v-form>
  </v-container>
</template>


<script>
import Checkbox from "@/components/filters/checkbox.vue";
import {mapState} from "pinia";
import {useAthletenState} from "@/stores/athletenStore";
import {useBerichteState} from "@/stores/berichteStore";

export default {
  components: {Checkbox},
  computed: {
    ...mapState(useAthletenState, {
      previewAthleteResults: "getPreviewAthleteResults"
    }),
    ...mapState(useAthletenState, {
      filterOptions: "getAthletenFilterOptions"
    }),
    ...mapState(useAthletenState, {
      showFilter: "getFilterState"
    })
  },
  data() {
    return {
      // general
      mobile: false,
      hoverFilter: false,
      drawer: null,
      formValid: true,

      // athletes
      selectedAthlete: null,

      // year
      birthYear: null,
      optionsBirthYear: [],

      // nations
      optionsNations: [],
      selectedNation: "GER (Deutschland)",

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
      if (searchInput.length > 2) {
        store.postSearchAthlete({
          "searchInput": searchInput
        })
      }
    },

    async onSubmit() {
      const {valid} = await this.$refs.filterForm.validate()
      if (valid) {
        this.hideFilter()
        await this.submitFormData()
      } else {
        alert("Bitte überprüfen Sie die Eingaben.")
      }
    },
    hideFilter() {
      const store = useAthletenState()
      store.setFilterState(this.showFilter)
    },
    submitFormData() {
      const store = useAthletenState()
      return store.postFormData({
        "athlete_name": this.selectedAthlete,
        "birth_year": this.birthYear,
        "gender": this.selectedGenders,
        "competition_category_ids": this.compTypes.filter(item => this.optionsCompTypes.includes(item.displayName)).map(item => item.id),
        "nation_ioc": this.selectedNation
      }).then(() => {
        console.log("Form data sent...")
      }).catch(error => {
        console.error(error)
      })
    },
    clearFormInputs() {
      this.selectedAthlete = null
      this.selectedNation = "GER (Deutschland)"
      this.selectedBirthYear = null
      this.selectedGenders = 0
      this.selectedAgeGroups = 0
      this.selectedBoatClasses = this.optionsBoatClasses[0]
    },
    checkScreen() {
      this.windowWidth = window.innerWidth
      this.mobile = this.windowWidth <= 769
    },
    setFilterState() {
      this.filterOpen = !this.filterOpen;
      const store = useAthletenState()
      store.setFilterState(this.filterState)
    },
  },
  watch: {
    selectedGenders: function (newVal,) {
      if (newVal !== undefined) {
        this.selectedBoatClasses = null
        let optionsList = []
        if (newVal === 0) { // men
          optionsList.push(...Object.keys(this.filterOptions[0].boat_class.men))
        }
        if (newVal === 1) { // women
          optionsList.push(...Object.keys(this.filterOptions[0].boat_class.women))
        }
        if (newVal === 2) { // mixed
          optionsList = []
          let test = []
          for (const mixedOption of Object.values(this.filterOptions[0].boat_class.mixed)) {
            test.push(Object.values(mixedOption))
          }
          this.optionsBoatClasses = test.map(item => item[0]).flat()
        }
        if (newVal === 3) { // all
          this.ageGroupOptions = []
          this.optionsBoatClasses = ["Alle"]
          this.selectedBoatClasses = this.optionsBoatClasses
        }
        this.ageGroupOptions = optionsList.filter((v, i, a) => a.indexOf(v) === i); // exclude non-unique values
        let boatClassOptions = []
        Object.entries(Object.values(this.filterOptions[0].boat_class)[newVal]).forEach(([key, value], index) => {
          if (index === this.selectedAgeGroups) {
            Object.entries(value).forEach(([, val]) => {
              if (typeof val === "object") {
                boatClassOptions.push(Object.values(val)[0])
              }
            })
          }
        });
        if (newVal !== 2 && newVal !== 3) {
          this.optionsBoatClasses = boatClassOptions
          this.selectedBoatClasses = boatClassOptions[0]
        } else if (newVal === 2) {
          this.selectedBoatClasses = this.optionsBoatClasses[0]
        }
      }
    },
    selectedAgeGroups: function (newVal,) {
      if (newVal !== undefined) {
        this.selectedBoatClasses = null
        let genderObj = Object.values(this.filterOptions[0].boat_class)[this.selectedGenders]
        let boatClassOptions = []

        Object.entries(genderObj).forEach(([key, value], index) => {
          if (index === newVal) {
            Object.entries(value).forEach(([, val]) => {
              if (typeof val === "object") {
                boatClassOptions.push(Object.values(val)[0])
              }
            })
          }
        });
        this.selectedBoatClasses = boatClassOptions[0]
        if (this.selectedGenders !== 2 && this.selectedGenders !== 3) {
          this.optionsBoatClasses = boatClassOptions
        }
      }
    }
  }
}

</script>

<style scoped>
.mdi-close:hover{
  cursor: pointer;
}
</style>