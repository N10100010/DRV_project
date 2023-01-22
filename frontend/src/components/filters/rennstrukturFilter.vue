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
    <v-form id="rennstrukturFilterFormular" class="mt-2" @submit.prevent="onSubmit"
            ref="filterForm" v-model="formValid" lazy-validation>
      <v-select class="pt-2" clearable density="comfortable" label="Year"
                :items="optionsYear" v-model="selectedYear"
                variant="outlined" :rules="[v => !!v || 'Wähle ein Jahr']"
      ></v-select>
      <v-select class="pt-3" density="comfortable"
                label="Wettkampfklasse" :items="optionsCompTypes"
                v-model="selectedCompTypes" variant="outlined"
      ></v-select>

      <!-- The following content might be optional as it is a redundant selection criteria -->
      <!--
      <v-label class="pt-2">Geschlecht (optional)</v-label>
      <v-chip-group filter color="blue" mandatory v-model="gender">
        <v-chip v-for="gender in genders" :value="gender">{{ gender }}</v-chip>
      </v-chip-group>
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
        <!--
        <v-btn color="grey" class="mx-2"><v-icon>mdi-backspace-outline</v-icon></v-btn>
        -->
        <v-btn color="blue" class="mx-2" type="submit">Übernehmen</v-btn>
      </v-container>
    </v-form>
  </v-container>
</template>


<script>
import Checkbox from "@/components/filters/checkbox.vue";
import {useRennstrukturAnalyseState} from "@/stores/baseStore";
import {mapActions, mapState} from "pinia";
import {useBerichteState} from "@/stores/berichteStore";

export default {
  components: {Checkbox},
  computed: {
    ...mapState(useRennstrukturAnalyseState, {
      raceAnalysisFilterOptions: "getRaceAnalysisFilterOptions"
    }),
    ...mapState(useRennstrukturAnalyseState, {
      showFilter: "getFilterState"
    }),
  },
  data() {
    return {
      competition_type: '',
      year: new Date().getFullYear(),
      gender: '',
      mobile: false,
      hoverFilter: false,
      drawer: null,
      formValid: true,

      // competition type
      compTypes: [], // list of dicts with objects containing displayName, id and key
      optionsCompTypes: [],
      selectedCompTypes: ["Olympics"],
      // year
      optionsYear: [],
      selectedYear: new Date().getFullYear(),
      genders: ["männlich", "weiblich", "mixed"],
    }
  },
  created() {
    window.addEventListener('resize', this.checkScreen);
    this.checkScreen();

    // year
    this.startYear = Object.values(this.raceAnalysisFilterOptions[0].year[0])[0]
    this.endYear = Object.values(this.raceAnalysisFilterOptions[0].year[1])[0]
    this.optionsYear = Array.from({length: this.endYear - this.startYear + 1}, (_, i) => this.endYear - i)

    // competition category id
    this.compTypes = this.raceAnalysisFilterOptions[0].competition_category_ids
    this.optionsCompTypes = this.compTypes.map(item => item.displayName)
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
      const store = useRennstrukturAnalyseState()
      store.setFilterState(this.showFilter)
    },
    submitFormData() {
      const store = useRennstrukturAnalyseState()
      store.setToLoadingState()
      const formData = {
        "year": this.year,
        "competition_type": this.selectedCompTypes,
      }
      // send data via pinia store action postFormData
      return store.postFormData(formData).then(() => {
        console.log("Form data sent...")
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

<style scoped>
.mdi-close:hover{
  cursor: pointer;
}
</style>