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
      // general
      mobile: false,
      hoverFilter: false,
      drawer: null,
      formValid: true,
      // competition type
      compTypes: [], // list of dicts with objects containing displayName, id and key
      optionsCompTypes: [],
      selectedCompTypes: [
        "European Championships",
        "Olympics",
        "World Rowing Championships",
        "Qualifications",
        "World Championships I",
        "World Championships II",
        "World Championships III",
        "World Rowing Cup"
      ],
      // year
      startYear: 0,
      endYear: 0,
      optionsStartYear: [],
      optionsEndYear: [],
      // boat classes
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
    this.ageGroupOptions = []
    this.selectedBoatClasses = ["Alle"]
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
        "years": {
          "start_year": this.startYear,
          "end_year": this.endYear
        },
        "competition_category_ids": this.compTypes.filter(item => this.optionsCompTypes.includes(item.displayName))
            .map(item => item.id),
        "boat_classes": this.selectedBoatClasses,
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
          optionsList.push(...Object.keys(this.reportFilterOptions[0].boat_class.men))
          this.optionsDisciplines = ["Skull", "Riemen"]
        }
        if (newVal === 1) { // women
          optionsList.push(...Object.keys(this.reportFilterOptions[0].boat_class.women))
          this.optionsDisciplines = ["Skull", "Riemen"]
        }
        if (newVal === 2) { // mixed
          optionsList = []
          let test = []
          for (const mixedOption of Object.values(this.reportFilterOptions[0].boat_class.mixed)) {
            test.push(Object.values(mixedOption))
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
        Object.entries(Object.values(this.reportFilterOptions[0].boat_class)[newVal]).forEach(([key, value], index) => {
          if (index === this.selectedAgeGroups || this.selectedGenders === 2) {
            Object.entries(value).forEach(([, val]) => {
              if (typeof val === "object") {
                boatClassOptions.push(Object.values(val)[0])
              } else {
                boatClassOptions.push(val)
              }
            })
          }
        });
        if (newVal !== 3) {
          boatClassOptions = boatClassOptions.filter(item => this.selectedDiscipline ? !item.includes("Sculls") : item.includes("Sculls"));
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
        // filter discipline
        boatClassOptions = boatClassOptions.filter(item => this.selectedDiscipline ? !item.includes("Sculls") : item.includes("Sculls"));
        // set boat class options
        this.selectedBoatClasses = boatClassOptions[0]
        if (this.selectedGenders !== 3) {
          this.optionsBoatClasses = boatClassOptions
        }
      }
    },
    selectedDiscipline: function (newVal,) {
      if (newVal !== undefined) {
        this.selectedBoatClasses = null
        let genderObj = Object.values(this.reportFilterOptions[0].boat_class)[this.selectedGenders]
        let boatClassOptions = []
        Object.entries(genderObj).forEach(([key, value], index) => {
          if (index === this.selectedAgeGroups || this.selectedGenders === 2) {
            Object.entries(value).forEach(([, val]) => {
              if (typeof val === "object") {
                boatClassOptions.push(Object.values(val)[0])
              } else {
                boatClassOptions.push(val)
              }
            })
          }
        });
        boatClassOptions = boatClassOptions.filter(item => newVal ? !item.includes("Sculls") : item.includes("Sculls"));
        this.selectedBoatClasses = boatClassOptions[0]
        if (this.selectedGenders !== 3) {
          this.optionsBoatClasses = boatClassOptions
        }
      }
    },
    selectedRuns: function (newVal,) {
      if (newVal !== undefined) {
        let newList = Object.values(newVal)
        const selectionOptions = Object.values(this.reportFilterOptions[0].runs).filter(item => item !== null)
        let newFineSelectionEntries = selectionOptions.flatMap((item, idx) => {
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

<style scoped>
.mdi-close:hover {
  cursor: pointer;
}
</style>