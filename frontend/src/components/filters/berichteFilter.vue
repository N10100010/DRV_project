<template>
  <v-container>
  <h2>Filter</h2>
    <v-divider></v-divider>

    <v-form class="mt-2" id="berichteFilterFormular" @submit.prevent="onSubmit">
      <v-label>Geschlecht</v-label>
      <v-chip-group filter color="blue" multiple v-model="genders">
        <v-chip>männlich</v-chip>
        <v-chip>weiblich</v-chip>
      </v-chip-group>
      <v-label class="pt-2">Altersklasse</v-label>
      <v-chip-group filter color="blue" multiple v-model="ageGroups">

        <v-chip>Open</v-chip>
        <v-chip>U19</v-chip>
        <v-chip>U23</v-chip>
        <v-chip>Elite</v-chip>
        <v-chip>Para</v-chip>

      </v-chip-group>
      <v-select
        label="Bootsklassen"
        clearable
        multiple chips
        :items="optionsBoatClasses"
        v-model="optionsBoatClasses"
        variant="underlined"
        hide-details
      ></v-select>
      <v-label class="pt-2">Zeitraum</v-label>
      <v-container class="pa-0 d-flex">
        <v-col cols="6" class="pa-0">
          <v-select
            clearable
            label="Von"
            :items="optionsStartYear"
            variant="underlined"
            v-model="startYear"
            hide-details
          ></v-select>
        </v-col>
        <v-col cols="6" class="pa-0">
          <v-select
            clearable
            label="Bis"
            :items="optionsEndYear"
            v-model="endYear"
            variant="underlined"
            hide-details
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
                hide-details
      ></v-select>
      <v-label class="pt-2">Lauf (optional)</v-label>
      <v-chip-group filter color="blue" multiple v-model="runTopLevel">
        <v-chip>Finale</v-chip>
        <v-chip>Halbfinale</v-chip>
        <v-chip>Viertelfinale</v-chip>
        <v-chip>Hoffnungsläufe</v-chip>
        <v-chip>Vorläufe</v-chip>
      </v-chip-group>
      <v-select
        label="Lauf"
        clearable
        :items="auswahlLauf"
        variant="underlined"
        hide-details
        chips
      ></v-select>
      <v-label class="pt-2">Platzierung (optional)</v-label>
      <v-chip-group filter color="blue" multiple v-model="ranks">
        <v-chip v-for="rankName in ranksDisplayNames">{{rankName}}</v-chip>
      </v-chip-group>

      <v-container class="pa-0 pt-4 text-right">
        <v-btn color="grey" class="mx-2"><v-icon>mdi-backspace-outline</v-icon></v-btn>
        <v-btn color="blue" class="mx-2" type="submit" @click="setFilterState">Übernehmen</v-btn>
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
      optionsCompTypes: ["Olympics", "World Rowing Championships", "Qualifications"], // default strings

      // year
      startYear: 0,
      endYear: 0,
      optionsStartYear: [],
      optionsEndYear: [],

      // ranks
      ranksDisplayNames: [],
      ranksDict: {},
      ranks: [0, 1, 2, 3],

      // boat classes
      boatClassTypes: [],
      genders: [0, 1],
      ageGroups: [0, 1, 2, 3, 4],
      optionsBoatClasses: [],

      // runs
      runTopLevel: [0, 1, 2],
      runs: [0, 1, 2, 3, 4],
      auswahlLauf: [
          'Alle'
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
    window.addEventListener('resize', this.checkScreen)
    this.checkScreen()

    // handle form data
    this.startYear = Object.values(this.reportFilterOptions[0].year[0])[0]
    this.endYear = Object.values(this.reportFilterOptions[0].year[1])[0]
    this.optionsStartYear = Array.from({length: this.endYear - this.startYear + 1}, (_, i) => this.startYear + i)
    this.optionsEndYear = Array.from({length: this.endYear - this.startYear + 1}, (_, i) => this.startYear + i)
    // TODO: nice to have wäre ein check der jeweils nur die gültigen Auswahlmöglichkeiten anzeigt

    // create dict from keys to get mapping from ui-element index to corresponding rank display name
    this.ranksDict = Object.fromEntries(this.reportFilterOptions[0].ranks.map((x, idx) => [idx, x]))
    this.ranks = Object.keys(this.ranksDict)
    this.ranksDisplayNames = Object.values(this.ranksDict)

    // competition category id
    this.compTypes = this.reportFilterOptions[0].competition_category_ids
    this.optionsCompTypes = this.compTypes.map(item => item.displayName)

    this.boatClassTypes = this.reportFilterOptions[0].boat_class
    this.optionsBoatClasses = this.reportFilterOptions[0].boat_class.map(item => item.displayName)
  },
  methods: {
    onSubmit() {
      // define store
      const store = useBerichteState()
      // access form data
      const startYear = this.startYear
      const endYear = this.endYear
      const competitionType = this.compTypes.filter(item => this.optionsCompTypes.includes(item.displayName)).map(item => item.id)
      const ranks = this.ranks.map(key => this.ranksDict[key])
      const ageGroups = this.ageGroups
      const runs = this.runs
      const boatClasses = this.boatClassTypes.filter(item => this.optionsBoatClasses.includes(item.displayName)).map(item => item.id)

      // send data via pinia store action postFormData
      return store.postFormData({
        "years": [{"start_year": startYear}, {"end_year": endYear}],
        "competition_category_ids": competitionType,
        "boat_classes": boatClasses,
        "groups": ageGroups,
        "runs": runs,
        "ranks": ranks
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
      const store = useBerichteState()
      store.setFilterState(this.showFilter)
    }
  }
}

</script>