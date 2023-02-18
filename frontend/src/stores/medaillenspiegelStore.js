import axios from "axios";
import {defineStore} from "pinia";

const COLORS = [
    '#0C67F7', '#D8C9BF', '#93E9ED',
    '#B5A68D', '#E0A9FA', '#E0FAAC',
    '#F0E95A', '#807E6D', '#5EFF5E',
    '#FF5E5E', '#FF9C5E', '#5EFF9C',
    '#9C5EFF', '#010101', '#C5B5B5',
    '#E0B696', '#7C6B6B', '#5EFFBE'
]

export const useMedaillenspiegelState = defineStore({
    id: "medaillenspiegel",
    state: () => ({
        filterOpen: false,
        loading: true,
        tableExport: [],
        filterOptions: [{
            "years": [{"start_year": ""}, {"end_year": ""}],
            "boat_classes": {},
            "competition_categories": [{"":""}],
            "nations": {"": ""},
            "medal_types": [{"":""}]
        }],
        data: {
                "results": 0,
                "start_date": 0,
                "end_date": 0,
                "comp_types": [],
                "category": 0,
                "boat_classes": [],
                "data": []
            }
    }),
    getters: {
        getFilterState(state) {
            return state.filterOpen
        },
        getMedaillenspiegelFilterOptions(state) {
            return state.filterOptions
        },
        getFilterSelection(state) {
            return state.data
        },
        getLoadingState(state) {
            return state.loading
        },
        getTableData(state) {
            let tableData = [["Platz", "Nation", "Gold", "Silber", "Bronze", "Gesamt", "Finale A", "Finale B"]];
            const valueKeys = ["rank", "nation", "gold", "silver", "bronze", "total", "final_a", "final_b"];
            const data = state.data.data
            for (const el of data) {
                let temp1Array = []
                for (const valueKey of valueKeys) {
                    temp1Array.push(el[valueKey]);
                }
                tableData.push(temp1Array)
            }
            state.tableExport = tableData
            return tableData
        },
        getBarChartData(state) {
            const data = state.data.data
            let dataSets = []
            const labels = ["Gold", "Silver", "Bronze", "Total"]
            for (const [index, country] of data.entries()) {
                dataSets.push({
                    type: 'bar',
                    label: country.nation,
                    backgroundColor: COLORS[index % COLORS.length],
                    data: [country.gold, country.silver, country.bronze, country.total]
                })
            }
            return {
                labels: labels,
                datasets: dataSets
            }
        },
    },
    actions: {
        async fetchMedaillenspiegelFilterOptions() {
            await axios.get(`${import.meta.env.VITE_BACKEND_API_BASE_URL}/get_medals_filter_options`)
                .then(response => {
                    this.filterOptions = response.data
                }).catch(error => {
                    console.error(`Request failed: ${error}`)
                })
        },
        async postFormData(data) {
            this.loading = true
             await axios.post(`${import.meta.env.VITE_BACKEND_API_BASE_URL}/get_medals`, {data})
                .then(response => {
                    this.data = response.data
                    this.loading = false
                }).catch(error => {
                    console.error(`Request failed: ${error}`)
                })
        },
        setFilterState(filterState) {
            this.filterOpen = !filterState
        },
        exportTableData() {
            const csvContent = "data:text/csv;charset=utf-8," + this.tableExport.map(e => e.join(",")).join("\n");
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "medaillenspiegel.csv");
            document.body.appendChild(link);
            link.click();
        }
    }
})
