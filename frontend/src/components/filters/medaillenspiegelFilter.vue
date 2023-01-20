<template>
  <v-container>
    <v-row>
       <v-col>
      <h2>Filter</h2>
       </v-col>
    <v-col class="text-right">
      <i class="mdi mdi-close" style="font-size: 25px; color: darkgrey" @click="hideFilter"></i>
    </v-col>
    </v-row>
    <v-divider></v-divider>
    <v-form class="mt-2" id="berichteFilterFormular" @submit.prevent="onSubmit"
            v-model="formValid" lazy-validation ref="filterForm">
      <v-container class="pa-0 d-flex pt-3">
        <v-col cols="6" class="pa-0 pr-2">
          <v-select clearable label="Von" :items="optionsStartYear"
                    variant="outlined" v-model="startYear" density="comfortable"
                    :rules="[v => !!v || 'Wähle ein Jahr als Anfangswert',
                    (v) => parseInt(v) <= parseInt(endYear) || 'Zeitraum Anfang darf nicht nach dem Ende liegen.']"
          ></v-select>
        </v-col>
        <v-col cols="6" class="pa-0 pl-2">
          <v-select clearable label="Bis" :items="optionsEndYear"
                    v-model="endYear" variant="outlined" density="comfortable"
                    :rules="[v => !!v || 'Wähle ein Jahr als Endwert',
                        (v) => parseInt(v) >= parseInt(startYear) || 'Zeitraum Ende darf nicht vor dem Anfang liegen.']"
          ></v-select>
        </v-col>
      </v-container>
      <v-select class="pt-2" clearable chips multiple color="blue"
                label="Wettkampfklassen" :items="optionsCompTypes"
                v-model="selectedCompTypes" variant="outlined"
                :rules="[v => v.length > 0 || 'Wähle mindestens eine Wettkampfklasse']"
      ></v-select>
      <v-label>Medaillentyp</v-label>
      <v-chip-group filter color="blue" v-model="selectedMedalTypes">
        <v-chip v-for="medalType in optionsMedalTypes">{{ medalType }}</v-chip>
      </v-chip-group>
      <v-autocomplete class="pt-4" :items="optionsNations" multiple v-model="selectedNation"
                      variant="outlined" color="blue" label="Nation" density="comfortable"
                      :rules="[v => !!v || 'Wähle mindestens eine Nation']"
      ></v-autocomplete>
      <v-label>Bootsklasse</v-label>
      <v-chip-group filter color="blue" v-model="selectedGenders">
        <v-chip v-for="genderType in genderTypeOptions">{{ genderType.charAt(0).toUpperCase() + genderType.slice(1) }}
        </v-chip>
      </v-chip-group>
      <v-chip-group filter color="blue" v-model="selectedAgeGroups">
        <v-chip v-for="ageGroup in ageGroupOptions">{{ ageGroup.charAt(0).toUpperCase() + ageGroup.slice(1) }}</v-chip>
      </v-chip-group>
      <v-select class="pt-3" label="Bootsklassen" clearable chips density="comfortable"
                :items="optionsBoatClasses" v-model="selectedBoatClasses" variant="outlined"
                :rules="[v => !!v || 'Wähle mindestens eine Bootsklasse']"
      ></v-select>
      <v-container class="pa-0 pt-8 text-right">
        <v-btn color="grey" class="mx-2" @click="clearFormInputs">
          <v-icon>mdi-backspace-outline</v-icon>
        </v-btn>
        <v-btn color="blue" class="mx-2" type="submit">Übernehmen</v-btn>
      </v-container>
    </v-form>
  </v-container>
</template>


<script>
import Checkbox from "@/components/filters/checkbox.vue";
import {mapState} from "pinia";
import {useMedaillenspiegelState} from "@/stores/medaillenspiegelStore";
import {useBerichteState} from "@/stores/berichteStore";

export default {
  components: {Checkbox},
  computed: {
    ...mapState(useMedaillenspiegelState, {
      filterOptions: "getMedaillenspiegelFilterOptions"
    }),
    ...mapState(useMedaillenspiegelState, {
      showFilter: "getFilterState"
    }),
  },
  data() {
    return {
      // general
      mobile: false,
      hoverFilter: false,
      drawer: null,
      formValid: true,

      // competition type
      compTypes: [], // list of dicts with objects containing displayName, id and key
      optionsCompTypes: ["Olympics", "World Rowing Championships", "Qualifications"], // default strings
      selectedCompTypes: ["Olympics", "World Rowing Championships", "Qualifications"],

      // year
      startYear: 0,
      endYear: 0,
      optionsStartYear: [],
      optionsEndYear: [],

      // medal types
      optionsMedalTypes: [],
      selectedMedalTypes: [0],

      // nations
      optionsNations: [],
      selectedNation: "GER (Deutschland)",

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
    this.optionsEndYear = Array.from({length: this.endYear - this.startYear + 1}, (_, i) => this.endYear - i)

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
      const store = useMedaillenspiegelState()
      store.setFilterState(this.showFilter)
    },
    submitFormData() {
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
    clearFormInputs() {
      this.selectedGenders = 0
      this.startYear = 1950
      this.endYear = new Date().getFullYear()
      this.selectedCompTypes = ["Olympics", "World Rowing Championships", "Qualifications"]
      this.selectedRanks = [0, 1, 2, 3]
      this.selectedRuns = [0, 1, 2]
    },
    checkScreen() {
      this.windowWidth = window.innerWidth
      this.mobile = this.windowWidth <= 769
    }
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
    },
  }
}

</script>

<style scoped>
.mdi-close:hover{
  cursor: pointer;
}
</style>