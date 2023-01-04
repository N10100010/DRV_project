import axios from "axios";
import { defineStore } from "pinia";

export const useBerichteState = defineStore({
    id: "berichte",
    state: () => ({
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
                            "06:34", "06:36", "06:38",
                            "06:40", "06:42", "06:44",
                            "06:46", "06:48", "06:50",
                            "06:52", "06:54", "06:56",
                            "06:58", "07:00", "07:02",
                            "07:04", "07:06", "07:08",
                        ],
                    "data": [20, 26, 45, 180, 503, 98, 55, 23, 16, 4, 2, 3, 1, 3, 1, 4, 3, 2]
                },
                "scatterPlot": {

                }
            }
        }]
    }),
    getters: {
        getBarChartData(state) {
            return {
                labels: state.data[0].plot_data.histogram.labels,
                datasets: [
                    {
                        type: 'bar',
                        label: "Histogram Component",
                        backgroundColor: "blue",
                        data: state.data[0].plot_data.histogram.data
                    },
                    {
                        type: 'line',
                        label: 'Line Component',
                        backgroundColor: "red",
                        data: state.data[0].plot_data.histogram.data,
                    }
                    ]
            }
        },
        getScatterChartData(state) {
            return {
                datasets: [
                    {
                        type: 'scatter',
                        label: 'Scatter Dataset',
                        data: [
                            {x: 3, y: 6},
                            {x: 4, y: 4.5},
                            {x: 5, y: 6},
                            {x: 6, y: 4.8},
                            {x: 7, y: 7},
                            {x: 8, y: 4},
                        ],
                        backgroundColor: 'blue',
                        borderColor: 'blue'
                    }
                ]
            }
        }
    }
})
