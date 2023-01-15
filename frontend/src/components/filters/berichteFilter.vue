<template>
  <v-container :style="{'height': mobile ? '135%' : '100%'}">
  <h2>Filter</h2>
    <v-divider></v-divider>

    <v-form class="mt-2" id="berichteFilterFormular" @submit.prevent="onSubmit">

      <v-chip-group filter color="blue" v-model="selectedGenders">
        <v-chip v-for="genderType in genderTypeOptions">{{genderType.charAt(0).toUpperCase() + genderType.slice(1)}}</v-chip>
      </v-chip-group>
      <v-chip-group filter color="blue" v-model="selectedAgeGroups">
        <v-chip v-for="ageGroup in ageGroupOptions">{{ageGroup.charAt(0).toUpperCase() + ageGroup.slice(1)}}</v-chip>
      </v-chip-group>
      <v-select class="pt-3" label="Bootsklassen" clearable chips density="comfortable"
                :items="optionsBoatClasses" v-model="selectedBoatClasses" variant="outlined"
      ></v-select>
      <v-container class="pa-0 d-flex pt-3">
        <v-col cols="6" class="pa-0 pr-2">
          <v-select clearable label="Von" :items="optionsStartYear"
            variant="outlined" v-model="startYear" density="comfortable"
          ></v-select>
        </v-col>
        <v-col cols="6" class="pa-0 pl-2">
          <v-select clearable label="Bis" :items="optionsEndYear"
            v-model="endYear" variant="outlined" density="comfortable"
          ></v-select>
        </v-col>
      </v-container>
      <v-select class="pt-3" chips multiple density="comfortable"
                label="Wettkampfklassen" :items="optionsCompTypes"
                v-model="selectedCompTypes" variant="outlined"
      ></v-select>
      <v-chip-group class="pt-2" filter color="blue" multiple v-model="selectedRuns">
        <v-chip density="comfortable" v-for="runOption in optionsRuns">{{runOption.charAt(0).toUpperCase() + runOption.slice(1)}}</v-chip>
      </v-chip-group>
      <v-select label="Lauf" class="pt-2"
                clearable :items="optionsRunsFineSelection" v-model="selectedRunsFineSelection"
                multiple variant="outlined" chips></v-select>
      <v-label class="pt-1">Platzierung (optional)</v-label>
      <v-chip-group filter color="blue" multiple v-model="selectedRanks">
        <v-chip v-for="rankName in ranksDisplayNames">{{rankName}}</v-chip>
      </v-chip-group>

      <v-container class="pa-0 pt-4 text-right">
        <v-btn color="grey" class="mx-2" @click="clearFormInputs"><v-icon>mdi-backspace-outline</v-icon></v-btn>
        <v-btn color="blue" class="mx-2" type="submit">Übernehmen</v-btn>
      </v-container>

    </v-form>
  </v-container>
</template>


<script>
import Checkbox from "@/components/filters/checkbox.vue";
import {mapState} from "pinia";
import {useBerichteState} from "@/stores/berichteStore";

export default {
  components: {Checkbox},
  computed: {
    ...mapState(useBerichteState, {
      reportFilterOptions: "getReportFilterOptions"}),
    ...mapState(useBerichteState, {
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
      optionsCompTypes: ["Olympics", "World Rowing Championships", "Qualifications"],
      selectedCompTypes: ["Olympics", "World Rowing Championships", "Qualifications"],
      // year
      startYear: 0,
      endYear: 0,
      optionsStartYear: [],
      optionsEndYear: [],
      // boat classes
      genderTypeOptions: [],
      selectedGenders: [0],
      ageGroupOptions: [],
      selectedAgeGroups: 0,
      optionsBoatClasses: [],
      selectedBoatClasses: this.optionsBoatClasses,
      // runs
      optionsRuns: [],
      selectedRuns: [0, 1, 2],
      optionsRunsFineSelection: null,
      selectedRunsFineSelection: ["fa", "fb", "fc", "fd", "f...", "sa/b, sa/b/c", "sc/d, sd/e/f", "s...", "q1-4"],
      // ranks
      ranksDisplayNames: [],
      ranksDict: {},
      selectedRanks: [0, 1, 2, 3]
    }
  },
  created() {
    window.addEventListener('resize', this.checkScreen)
    this.checkScreen()

    // handle form data
    this.startYear = Object.values(this.reportFilterOptions[0].year[0])[0]
    this.endYear = Object.values(this.reportFilterOptions[0].year[1])[0]
    this.optionsStartYear = Array.from({length: this.endYear - this.startYear + 1}, (_, i) => this.startYear + i)
    this.optionsEndYear = Array.from({length: this.endYear - this.startYear + 1}, (_, i) => this.endYear - i)

    // create dict from keys to get mapping from ui-element index to corresponding rank display name
    this.ranksDict = Object.fromEntries(this.reportFilterOptions[0].ranks.map((x, idx) => [idx, x]))
    this.ranks = Object.keys(this.ranksDict)
    this.ranksDisplayNames = Object.values(this.ranksDict)

    // competition category id
    this.compTypes = this.reportFilterOptions[0].competition_category_ids
    this.optionsCompTypes = this.compTypes.map(item => item.displayName)

    // boatclasses
    this.genderTypeOptions = Object.keys(this.reportFilterOptions[0].boat_class)
    let ageGroupOptions = Object.keys(this.reportFilterOptions[0].boat_class.men)
    ageGroupOptions.push(...Object.keys(this.reportFilterOptions[0].boat_class.women))
    this.ageGroupOptions = ageGroupOptions.filter((v, i, a) => a.indexOf(v) === i); // exclude non-unique values

    let boatClassOptions = []
    let values = Object.values(this.reportFilterOptions[0].boat_class)[0]
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

    // runs
    this.optionsRuns = Object.keys(this.reportFilterOptions[0].runs)
    let runOptionsSelectionNames = Object.values(this.reportFilterOptions[0].runs).filter(item => item !== null)
    this.optionsRunsFineSelection = runOptionsSelectionNames.flatMap((item, idx) => {
      if (this.selectedRuns.includes(idx)) {
        return item.map(item => item.displayName)
      }
    })

  },
  methods: {
    onSubmit() {
      // define store
      const store = useBerichteState()
      store.setFilterState(this.showFilter) // hide filter on submit

      // access form data
      const startYear = this.startYear
      const endYear = this.endYear
      const competitionType = this.compTypes.filter(item => this.optionsCompTypes.includes(item.displayName)).map(item => item.id)
      const ranks = this.ranks.map(key => this.ranksDict[key])
      const runs = this.selectedRuns
      const runsFine = this.selectedRunsFineSelection
      const boatClasses = this.selectedBoatClasses

      // send data via pinia store action postFormData
      return store.postFormData({
        "years": {
          "start_year": startYear,
          "end_year": endYear
        },
        "competition_category_ids": competitionType,
        "boat_classes": boatClasses,
        "runs": runs,
        "runs_fine": runsFine,
        "ranks": ranks
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
    selectedGenders: function (newVal, ) {
      if (newVal !== undefined) {
        this.selectedBoatClasses = null
        let optionsList = []
        if (newVal === 0) { // men
          optionsList.push(...Object.keys(this.reportFilterOptions[0].boat_class.men))
        }
        if (newVal === 1) { // women
          optionsList.push(...Object.keys(this.reportFilterOptions[0].boat_class.women))
        }
        if (newVal === 2) { // mixed
          optionsList = []
          let test = []
          for (const mixedOption of Object.values(this.reportFilterOptions[0].boat_class.mixed)) {
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
        Object.entries(Object.values(this.reportFilterOptions[0].boat_class)[newVal]).forEach(([key, value], index) => {
            if (index === this.selectedAgeGroups) {
              Object.entries(value).forEach(([, val]) => {
                if (typeof val === "object") {
                  boatClassOptions.push(Object.values(val)[0])
                }
              })
            }
        });
        if (newVal !==2 && newVal !== 3) {
          this.optionsBoatClasses = boatClassOptions
          this.selectedBoatClasses = boatClassOptions[0]
        } else if (newVal === 2) {
          this.selectedBoatClasses = this.optionsBoatClasses[0]
        }
      }
    },
    selectedAgeGroups: function (newVal, ) {
      if (newVal !== undefined) {
        this.selectedBoatClasses = null
        let genderObj = Object.values(this.reportFilterOptions[0].boat_class)[this.selectedGenders]
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
    selectedRuns: function (newVal, ) {
      if (newVal !== undefined) {
        let newList = Object.values(newVal)
        const selectionOptions = Object.values(this.reportFilterOptions[0].runs).filter(item => item !== null)
        let newFineSelectionEntries =  selectionOptions.flatMap((item, idx) => {
          if (newList.includes(idx)) {
            return item.map(item => item.displayName)
          }
        })
        this.selectedRunsFineSelection = newFineSelectionEntries.filter(item => item !== undefined)
        this.optionsRunsFineSelection = newFineSelectionEntries.filter(item => item !== undefined)
      }
    }
  }
}
</script>