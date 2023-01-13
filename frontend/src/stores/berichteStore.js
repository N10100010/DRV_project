import axios from "axios";
import { defineStore } from "pinia";

export const useBerichteState = defineStore({
    id: "berichte",
    state: () => ({
        filterOpen: false,
        filterOptions: [{
            "year": [{"start_year": 1950}, {"end_year": 2025}],
            "boat_class": {
                'men': {
                    'junior': {
                        'single': {"JM1x": "Junior Men's Single Sculls"},
                        'double': {"JM2x": "Junior Men's Double Sculls"},
                        'quad': {"JM4x": "Junior Men's Quadruple Sculls"},
                        'pair': {"JM2-": "Junior Men's Pair"},
                        'coxed_four': {"JM4+": "Junior Men's Coxed Four"},
                        'four': {"JM4-": "Junior Men's Four"} ,
                        'eight': {"JM8-": "Junior Men's Eight"}
                    },
                    'u19': {},
                    'u23': {
                        'single': {"BM1x": "U23 Men's Single Sculls"},
                        'double': {"BM2x": "U23 Men's Double Sculls"},
                        'quad': {"BM4x": "U23 Men's Quadruple Sculls"},
                        'pair': {"BM2-": "U23 Men's Pair"},
                        'coxed_four': {"BM4+": "U23 Men's Coxed Four"},
                        'four': {"BM4-": "U23 Men's Four"},
                        'eight': {"BM8+": "U23 Men's Eight"},
                        'lw_single': {"BLM1x": "U23 Lightweight Men's Single Sculls"},
                        'lw_double': {"BLM2x": "U23 Lightweight Men's Double Sculls"},
                        'lw_quad': {"BLM4x": "U23 Lightweight Men's Quadruple Sculls"},
                        'lw_pair': {"BLM2-": "U23 Lightweight Men's Pair"},
                    },
                    'adult': {
                        'single': {"M1x": "Men's Single Sculls"},
                        'double': {"M2x": "Men's Double Sculls"},
                        'quad': {"M4x": "Men's Quadruple Sculls"},
                        'pair': {"M2-": "Men's Pair"},
                        'four': {"M4-": "Men's Four"},
                        'eight': {"M8+": "Men's Eight"},
                        'lw_single': {"LM1x": "Lightweight Men's Single Sculls"},
                        'lw_double': {"LM2x": "Lightweight Men's Double Sculls"},
                        'lw_quad': {"LM4x": "Lightweight Men's Quadruple Sculls"},
                        'lw_pair': {"LM2-": "Lightweight Men's Pair"},
                    },
                    'pr': {
                        '1': {"PR1 M1x": "PR1 Men's Single Sculls"},
                        '2': {"PR2 M1x": "PR2 Men's Single Sculls"},
                        '3': {"PR3 M2-": "PR3 Men's Pair"}
                    }
                },
                'women': {
                    'junior': {
                        'single': {"JW1x": "Junior Women's Single Sculls"},
                        'double': {"JW2x": "Junior Women's Double Sculls"},
                        'quad': {"JW4x": "Junior Women's Quadruple Sculls"},
                        'pair': {"JW2-": "Junior Women's Pair"},
                        'coxed_four': {"JW4+": "Junior Women's Coxed Four"},
                        'four': {"JW4-": "Junior Women's Four"} ,
                        'eight': {"JW8-": "Junior Women's Eight"}
                    },
                    'u19': {},
                    'u23': {
                        'single': {"BW1x": "U23 Women's Single Sculls"},
                        'double': {"BW2x": "U23 Women's Double Sculls"},
                        'quad': {"BW4x": "U23 Women's Quadruple Sculls"},
                        'pair': {"BW2-": "U23 Women's Pair"},
                        'coxed_four': {"BW4+": "U23 Women's Coxed Four"},
                        'four': {"BW4-": "U23 Women's Four"},
                        'eight': {"BW8+": "U23 Women's Eight"},
                        'lw_single': {"BLW1x": "U23 Lightweight Women's Single Sculls"},
                        'lw_double': {"BLW2x": "U23 Lightweight Women's Double Sculls"},
                        'lw_quad': {"BLW4x": "U23 Lightweight Women's Quadruple Sculls"},
                        'lw_pair': {"BLW2-": "U23 Lightweight Women's Pair"},
                    },
                    'adult': {
                        'single': {"W1x": "Women's Single Sculls"},
                        'double': {"W2x": "Women's Double Sculls"},
                        'quad': {"W4x": "Women's Quadruple Sculls"},
                        'pair': {"W2-": "Women's Pair"},
                        'four': {"W4-": "Women's Four"},
                        'eight': {"W8+": "Women's Eight"},
                        'lw_single': {"LW1x": "Lightweight Women's Single Sculls"},
                        'lw_double': {"LW2x": "Lightweight Women's Double Sculls"},
                        'lw_quad': {"LW4x": "Lightweight Women's Quadruple Sculls"},
                        'lw_pair': {"LW2-": "Lightweight Women's Pair"},
                    },
                    'pr': {
                        '1': {"PR1 W1x": "PR1 Women's Single Sculls"},
                        '2': {"PR2 W1x": "PR2 Women's Single Sculls"},
                        '3': {"PR3 W2-": "PR3 Women's Pair"}
                    }
                },
                'mixed': {
                    'double_2': {"PR2 Mix2x": "PR2 Mixed Double Sculls"},
                    'double_3': {"PR3 Mix2x": "PR3 Mixed Double Sculls"},
                    'four': {"PR3 Mix4+": "PR3 Mixed Coxed Four"},
                },
                'all': {
                    'all': 'all'
                },
            },
            "competition_category_ids": [
                {"displayName":  "Olympics", "id": "89346342"},
                {"displayName":  "World Rowing Championships", "id": "89346362"},
                {"displayName":  "Qualifications", "id": "89346362"},
            ],
            "runs": {
                "finale": [
                    {"displayName": "fa"},
                    {"displayName": "fb"},
                    {"displayName": "fc"},
                    {"displayName": "fd"},
                    {"displayName": "f..."}
                ],
                "halbfinale": [
                    {"displayName": "sa/b, sa/b/c"},
                    {"displayName": "sc/d, sd/e/f"},
                    {"displayName": "s..."}
                ],
                "viertelfinale": [
                    {"displayName": "q1-4"},
                ],
                "hoffnungslaeufe": null,
                "vorlaeufe": null,
            },
            "ranks": ["1", "2", "3", "4-6"],
        }],
        data: [{
            "results": 872,
            "boat_class": "Men's Eight",
            "start_date": "2020-06-16 14:12:00",
            "end_date": "2022-06-16 14:12:00",
            "world_best_time_boat_class": "00:05:58,36",
            "best_in_period": "00:05:58,36",
            "mean": {
                "mm:ss,00": "00:05:58,36",
                "m/s": 4.54,
                "pace 500m": "00:02:05,40",
                "pace 1000m": "00:02:05,40"
            },
            "std_dev": "00:00:23,42",
            "median": "00:05:32,36",
            "gradation_fastest": {
                "no_of_samples": 345,
                "time": "00:06:06,36"
            },
            "gradation_medium": {
                "no_of_samples": 239,
                "time": "00:06:13,52"
            },
            "gradation_slow": {
                "no_of_samples": 167,
                "time": "00:07:52,37"
            },
            "gradation_slowest": {
                "no_of_samples": 463,
                "time": "00:08:04,62"
            },
            "plot_data": {
                "histogram": {
                    "labels":
                        [
                            "00:06:34", "00:06:36", "00:06:38",
                            "00:06:40", "00:06:42", "00:06:44",
                            "00:06:46", "00:06:48", "00:06:50",
                            "00:06:52", "00:06:54", "00:06:56",
                            "00:06:58", "00:07:00", "00:07:02",
                            "00:07:04", "00:07:06", "00:07:08",
                        ],
                    "data": [20, 26, 45, 180, 503, 98, 55, 23, 16, 4, 2, 3, 1, 3, 1, 4, 3, 2]
                },
                "scatterPlot": {
                    "labels": [
                        '1930-01-01', '1940-01-01', '1950-01-01', '1960-01-01','1970-01-01',
                        '1980-01-01', '1990-01-01', '2000-01-01', '2010-01-01', '2020-01-01',
                    ],
                    "data": [
                        "00:06:54", "00:06:53", "00:06:55", "00:06:50", "00:06:48",
                        "00:06:43", "00:06:46", "00:06:40", "00:06:39", "00:06:40"
                    ]
                }
            }
        }]
    }),
    getters: {
        getFilterState(state) {
            return state.filterOpen
        },
        getReportFilterOptions(state) {
            return state.filterOptions
        },
        getTableData(state) {
            return state.data[0]
        },
        getBarChartData(state) {
            return {
                labels: state.data[0].plot_data.histogram.labels,
                datasets: [
                    {
                        type: 'line',
                        label: 'Anzahl Rennen',
                        backgroundColor: "red",
                        borderColor: "red",
                        data: state.data[0].plot_data.histogram.data,
                    },
                    {
                        type: 'bar',
                        label: "Anzahl Rennen",
                        backgroundColor: '#1E90FF',
                        data: state.data[0].plot_data.histogram.data
                    }
                    ]
            }
        },
        getScatterChartData(state) {
            const plotData = [];
            const scatterData = state.data[0].plot_data.scatterPlot;
            for (let i = 0; i < scatterData.labels.length; i++) {
                plotData.push({
                    x: scatterData.labels[i],
                    y: scatterData.data[i]
                });
            }
            return {
                datasets: [
                    {
                        type: 'scatter',
                        label: 'Scatter Dataset',
                        data: plotData,
                        backgroundColor: '#1E90FF',
                        borderColor: '#1E90FF'
                    }
                ]
            }
        }
    },
    actions: {
        async postFormData(formData) {
            await axios.post('https://jsonplaceholder.typicode.com/users',{ formData })
                .then(response => {
                    // Bearbeite die Antwort des Backends hier

                }).catch(error => {
                    // Bearbeite den Fehler hier
                })
        },
        setFilterState(filterState) {
            this.filterOpen = !filterState
        }
    }
})
