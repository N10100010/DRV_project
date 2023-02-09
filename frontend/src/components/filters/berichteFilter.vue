<template>
  <v-container :style="{'height': mobile ? '135%' : '100%'}">
    <v-row>
      <v-col>
        <h2>Filter</h2>
      </v-col>
      <v-col class="text-right">
        <i class="mdi mdi-close" style="font-size: 25px; color: darkgrey" @click="hideFilter"></i>
      </v-col>
    </v-row>
    <v-divider></v-divider>
    <v-form class="mt-2" id="berichteFilterFormular"
            v-model="formValid" lazy-validation
            @submit.prevent="onSubmit" ref="filterForm">
      <v-chip-group filter color="blue" v-model="selectedYearShortCutOptions">
        <v-chip v-for="yearShortCut in yearShortCutOptions" v-if="yearShortCutOptions">{{ yearShortCut }}
        </v-chip>
      </v-chip-group>
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

      <v-chip-group filter color="blue" v-model="selectedGenders">
        <v-chip v-for="genderType in genderTypeOptions">{{ genderType.charAt(0).toUpperCase() + genderType.slice(1) }}
        </v-chip>
      </v-chip-group>
      <v-chip-group filter color="blue" v-model="selectedAgeGroups">
        <v-chip v-for="ageGroup in ageGroupOptions">{{ ageGroup.charAt(0).toUpperCase() + ageGroup.slice(1) }}</v-chip>
      </v-chip-group>
      <v-chip-group filter color="blue" v-model="selectedDiscipline">
        <v-chip v-for="discipline in optionsDisciplines">{{ discipline }}</v-chip>
      </v-chip-group>
      <v-select class="pt-3" label="Bootsklassen" clearable chips density="comfortable"
                :items="optionsBoatClasses"
                v-model="selectedBoatClasses" variant="outlined"
                :rules="[v => !!v || 'Wähle mindestens eine Bootsklasse']"
      ></v-select>
      <v-select class="pt-3" chips multiple density="comfortable"
                label="Event(s)" :items="optionsCompTypes"
                v-model="selectedCompTypes" variant="outlined"
                :rules="[v => v.length > 0 || 'Wähle mindestens eine Wettkampfklasse']"
      ></v-select>
      <v-chip-group class="pt-2" filter color="blue" multiple v-model="selectedRuns">
        <v-chip density="comfortable" v-for="runOption in optionsRuns">
          {{ runOption.charAt(0).toUpperCase() + runOption.slice(1) }}
        </v-chip>
      </v-chip-group>
      <v-select label="Lauf" class="pt-2"
                clearable :items="optionsRunsFineSelection" v-model="selectedRunsFineSelection"
                multiple variant="outlined" chips
                :rules="[v => v.length > 0 || 'Wähle mindestens eine Laufkategorie']">
      </v-select>

      <v-label class="pt-1">Platzierung (optional)</v-label>
      <v-chip-group filter color="blue" multiple v-model="selectedRanks">
        <v-chip v-for="rankName in ranksDisplayNames">{{ rankName }}</v-chip>
      </v-chip-group>

      <v-container class="pa-0 pt-4 text-right">
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
import {useBerichteState} from "@/stores/berichteStore";

export default {
  components: {Checkbox},
  computed: {
    ...mapState(useBerichteState, {
      reportFilterOptions: "getReportFilterOptions"
    }),
    ...mapState(useBerichteState, {
      showFilter: "getFilterState"
    })
  },
  data() {
    return {
      // api filter data
      filterData: [],
      // general
      mobile: false,
      hoverFilter: false,
      drawer: null,
      formValid: true,
      // competition type
      compTypes: [], // list of dicts with objects containing displayName, id and key
      optionsCompTypes: [],
      selectedCompTypes: ["World Rowing Championships"],
      // year
      startYear: 0,
      endYear: 0,
      optionsStartYear: [],
      optionsEndYear: [],
      yearShortCutOptions: ["Aktuelles Jahr", "Aktueller OZ", "letzter OZ"],
      selectedYearShortCutOptions: [0],
      // boat classes
      boatClasses: {},
      genderTypeOptions: [],
      selectedGenders: [3],
      ageGroupOptions: [],
      selectedAgeGroups: 0,
      optionsDisciplines: [],
      selectedDiscipline: 0,
      optionsBoatClasses: [],
      selectedBoatClasses: null,
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

    const store = useBerichteState()
    store.fetchReportFilterOptions()
    this.initializeFilter(this.reportFilterOptions[0])
  },
  methods: {
    initializeFilter(data) {
      this.startYear = Object.values(data.years[0])[0];
      this.endYear = Object.values(data.years[1])[0];

      this.optionsStartYear = Array.from({length: this.endYear - this.startYear + 1}, (_, i) => this.startYear + i)
      this.optionsEndYear = Array.from({length: this.endYear - this.startYear + 1}, (_, i) => this.endYear - i)

      // create dict from keys to get mapping from ui-element index to corresponding rank display name
      this.ranksDict = Object.fromEntries(data.ranks.map((x, idx) => [idx, x]))
      this.ranks = Object.keys(this.ranksDict)
      this.ranksDisplayNames = Object.values(this.ranksDict)

      // competition category id
      this.compTypes = data.competition_categories
      this.optionsCompTypes = this.compTypes.map(item => item.display_name)

      // boatclasses
      this.boatClasses = {}
      this.genderTypeOptions = Object.keys(data.boat_classes)
      let ageGroupOptions = Object.keys(data.boat_classes.men)
      ageGroupOptions.push(...Object.keys(data.boat_classes.women))
      this.ageGroupOptions = ageGroupOptions.filter((v, i, a) => a.indexOf(v) === i); // exclude non-unique values

      let boatClassOptions = []
      let values = Object.values(data.boat_classes)[0]
      Object.entries(values).forEach(([key, value], index) => {
        if (index === 0) {
          Object.entries(value).forEach(([, val]) => {
            boatClassOptions.push(val[0])
            this.boatClasses[val[0]] = val[2]
          })
        }
      });
      this.ageGroupOptions = []
      this.selectedBoatClasses = ["Alle"]
      this.optionsBoatClasses = boatClassOptions

      // runs
      this.optionsRuns = Object.keys(data.runs)
      let runOptionsSelectionNames = Object.values(data.runs).filter(item => item !== null)
      this.optionsRunsFineSelection = runOptionsSelectionNames.flatMap((item, idx) => {
        if (this.selectedRuns.includes(idx)) {
          return item.map(item => item.display_name)
        }
      })
    },
    async onSubmit() {
      const {valid} = await this.$refs.filterForm.validate()
      if (valid) {
        this.hideFilter()
        this.submitFormData()
      } else {
        alert("Bitte überprüfen Sie die Eingaben.")
      }
    },
    hideFilter() {
      const store = useBerichteState()
      store.setFilterState(this.showFilter)
    },
    submitFormData() {
      const formData = {
        "years": {"start_year": this.startYear, "end_year": this.endYear},
        "competition_categories": this.compTypes.filter(item =>
            this.selectedCompTypes.includes(item.display_name)).map(item => item.id),
        "boat_classes": this.boatClasses[this.selectedBoatClasses],
        "runs": this.selectedRuns,
        "runs_fine": this.selectedRunsFineSelection,
        "ranks": this.ranks.map(key => this.ranksDict[key])
      }
      const store = useBerichteState()
      store.postFormData(formData)
          .then(() => {
            console.log("Form data sent...")
          })
          .catch(error => {
            console.error(error)
          })
    },
    clearFormInputs() {
      this.selectedGenders = 3
      this.ageGroupOptions = []
      this.selectedBoatClasses = ["Alle"]
      this.startYear = 1950
      this.endYear = new Date().getFullYear()
      this.selectedCompTypes = []
      this.selectedRanks = [0, 1, 2, 3]
      this.selectedRuns = [0, 1, 2]
    },
    checkScreen() {
      this.windowWidth = window.innerWidth
      this.mobile = this.windowWidth <= 769
    }
  },
  watch: {
    selectedYearShortCutOptions: function (newVal,) {
      if (newVal !== 'undefined') {
        if (newVal === 0) {
          this.startYear = new Date().getFullYear();
          this.endYear = new Date().getFullYear();
        } else if (newVal === 1) {
          // TODO: implement OZ
        } else if (newVal === 2) {
          // TODO: implement last OZ
        }
      }
    },
    selectedGenders: function (newVal,) {
      if (newVal !== undefined && this.filterData !== undefined) {
        this.selectedBoatClasses = null
        let optionsList = []
        if (newVal === 0) { // men
          optionsList.push(...Object.keys(this.filterData.boat_classes.men))
          this.optionsDisciplines = ["Skull", "Riemen"]
        }
        if (newVal === 1) { // women
          optionsList.push(...Object.keys(this.filterData.boat_classes.women))
          this.optionsDisciplines = ["Skull", "Riemen"]
        }
        if (newVal === 2) { // mixed
          optionsList = []
          let test = []
          for (const mixedOption of Object.values(this.filterData.boat_classes.mixed)) {
            test.push(Object.keys(mixedOption))
          }
          this.optionsBoatClasses = test.map(item => item[0]).flat()
          this.optionsDisciplines = ["Skull", "Riemen"]
        }
        if (newVal === 3) { // all
          this.ageGroupOptions = []
          this.optionsBoatClasses = ["Alle"]
          this.selectedBoatClasses = this.optionsBoatClasses
          this.optionsDisciplines = []
        }
        this.ageGroupOptions = optionsList.filter((v, i, a) => a.indexOf(v) === i); // exclude non-unique values
        let boatClassOptions = []
        Object.entries(Object.values(this.filterData.boat_classes)[newVal]).forEach(([key, value], index) => {
          if (index === this.selectedAgeGroups && this.selectedGenders !== 2) {
            Object.entries(value).forEach(([, val]) => {
              boatClassOptions.push(val[0])
              this.boatClasses[val[0]] = val[2]
            })
          } else if (this.selectedGenders === 2) {
            Object.entries(value).forEach(([, val]) => {
              boatClassOptions.push(val)
              this.boatClasses[val] = val[2]
            })
          }
        });
        if (newVal !== 3) {
          boatClassOptions = boatClassOptions.filter(item => this.selectedDiscipline ?
              !(item[item.length - 1] === 'x') : (item[item.length - 1] === 'x'))
          this.optionsBoatClasses = boatClassOptions
          this.selectedBoatClasses = boatClassOptions[0]
        }
      }
    },
    selectedAgeGroups: function (newVal,) {
      if (newVal !== undefined && this.filterData !== undefined) {
        this.selectedBoatClasses = null
        let genderObj = Object.values(this.filterData.boat_classes)[this.selectedGenders]
        let boatClassOptions = []
        Object.entries(genderObj).forEach(([key, value], index) => {
          if (index === newVal) {
            Object.entries(value).forEach(([, val]) => {
              boatClassOptions.push(val[0])
              this.boatClasses[val[0]] = val[2]
            })
          }
        });
        if (this.selectedGenders !== 3) {
          boatClassOptions = boatClassOptions.filter(item => this.selectedDiscipline ?
              !(item[item.length - 1] === 'x') : (item[item.length - 1] === 'x'))
          this.selectedBoatClasses = boatClassOptions[0]
          this.optionsBoatClasses = boatClassOptions
        }
      }
    },
    selectedDiscipline: function (newVal,) {
      if (newVal !== undefined && this.filterData !== undefined) {
        this.selectedBoatClasses = null
        let genderObj = Object.values(this.filterData.boat_classes)[this.selectedGenders]
        let boatClassOptions = []
        Object.entries(genderObj).forEach(([key, value], index) => {
          if (index === this.selectedAgeGroups && this.selectedGenders !== 2) {
            Object.entries(value).forEach(([, val]) => {
              boatClassOptions.push(val[0])
              this.boatClasses[val[0]] = val[2]
            })
          } else if (this.selectedGenders === 2) {
            Object.entries(value).forEach(([, val]) => {
              boatClassOptions.push(val)
              this.boatClasses[val] = val[2]
            })
          }
        });
        boatClassOptions = boatClassOptions.filter(item => newVal ?
            !(item[item.length - 1] === 'x') : (item[item.length - 1] === 'x'))
        this.selectedBoatClasses = boatClassOptions[0]
        if (this.selectedGenders !== 3) {
          this.optionsBoatClasses = boatClassOptions
        }
      }
    },
    selectedRuns: function (newVal,) {
      if (newVal !== undefined && this.reportFilterOptions !== undefined) {
        let newList = Object.values(newVal)
        const selectionOptions = Object.values(this.filterData.runs).filter(item => item !== null)
        let newFineSelectionEntries = selectionOptions.flatMap((item, idx) => {
          if (newList.includes(idx)) {
            return item.map(item => item.display_name)
          }
        })
        this.selectedRunsFineSelection = newFineSelectionEntries.filter(item => item !== undefined)
        this.optionsRunsFineSelection = newFineSelectionEntries.filter(item => item !== undefined)
      }
    },
    async reportFilterOptions(newVal,) {
      this.filterData = newVal[0]
    },
    filterData: function (newVal,) {
      this.initializeFilter(newVal)
    }
  }
}
</script>

<style scoped>
.mdi-close:hover {
  cursor: pointer;
}
</style>