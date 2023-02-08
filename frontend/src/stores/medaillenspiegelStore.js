import axios from "axios";
import {defineStore} from "pinia";

const COLORS = ['#0C67F7', '#93E9ED', '#E0A9FA', '#E0B696', '#E0FAAC', '#F0E95A'];

export const useMedaillenspiegelState = defineStore({
    id: "medaillenspiegel",
    state: () => ({
        filterOpen: false,
        tableExport: [],
        filterOptions: [{
            "years": [{"start_year": ""}, {"end_year": ""}],
            "boat_classes": {},
            "competition_categories": [{"":""}],
            "nations": {"": ""},
            "medal_types": [{"":""}]
        }],
        data: [
            {
                "results": 4,
                "start_date": "2020",
                "end_date": "2022",
                "events": "EM",
                "category": "Olympisch",
                "boat_classes": [
                    {"M1x": "Men's Single Sculls"},
                    {"M2x": "Men's Double Sculls"}
                ],
                "table_data": [
                    {
                        "nation_ioc": "GER",
                        "rank": "1",
                        "points": 900,
                        "medals_gold": 2,
                        "medals_silver": 5,
                        "medals_bronze": 5,
                        "medals_total": 17,
                        "final_a": 12,
                        "final_b": 6,
                        "final_c": 0,
                        "final_d": 0
                    },
                    {
                        "nation_ioc": "FRA",
                        "rank": "2",
                        "points": 760,
                        "medals_gold": 5,
                        "medals_silver": 5,
                        "medals_bronze": 5,
                        "medals_total": 15,
                        "final_a": 12,
                        "final_b": 6,
                        "final_c": 0,
                        "final_d": 0
                    },
                    {
                        "nation_ioc": "ITA",
                        "rank": "3",
                        "points": 700,
                        "medals_gold": 2,
                        "medals_silver": 3,
                        "medals_bronze": 5,
                        "medals_total": 10,
                        "final_a": 12,
                        "final_b": 6,
                        "final_c": 0,
                        "final_d": 0
                    },
                    {
                        "nation_ioc": "RUS",
                        "rank": "4",
                        "points": 500,
                        "medals_gold": 1,
                        "medals_silver": 4,
                        "medals_bronze": 6,
                        "medals_total": 11,
                        "final_a": 12,
                        "final_b": 6,
                        "final_c": 0,
                        "final_d": 0
                    }]
            }
        ]
    }),
    getters: {
        getFilterState(state) {
            return state.filterOpen
        },
        getMedaillenspiegelFilterOptions(state) {
            return state.filterOptions
        },
        getFilterSelection(state) {
            return state.data[0]
        },
        getTableData(state) {
            let tableData = [["Platz", "Nation", "Punkte", "Gold", "Silber", "Bronze", "Medaillen", "Finale A", "Finale B", "Finale C", "Finale D"]];
            const valueKeys = ["rank", "nation_ioc", "points", "medals_gold", "medals_silver", "medals_bronze", "medals_total", "final_a", "final_b", "final_c", "final_d"];
            const data = state.data[0].table_data
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
            const data = state.data[0].table_data
            let dataSets = []
            const labels = ["Gold", "Silver", "Bronze", "Total"]
            for (const [index, country] of data.entries()) {
                dataSets.push({
                    type: 'bar',
                    label: country.nation_ioc,
                    backgroundColor: COLORS[index % COLORS.length],
                    data: [country.medals_gold, country.medals_silver, country.medals_bronze, country.medals_total]
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
            await axios.get('http://localhost:5000/get_medals_filter_options')
                .then(response => {
                    this.filterOptions = response.data
                }).catch(error => {
                    console.error(`Request failed: ${error}`)
                })
        },
        async postFormData(formData) {
            // handle form logic here
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
