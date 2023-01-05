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
        getBarChartData(state) {
            return {
                labels: state.data[0].plot_data.histogram.labels,
                datasets: [
                    {
                        type: 'bar',
                        label: "Anzahl Rennen",
                        backgroundColor: '#1E90FF',
                        data: state.data[0].plot_data.histogram.data
                    },
                    {
                        type: 'line',
                        label: 'Anzahl Rennen',
                        backgroundColor: "red",
                        borderColor: "red",
                        data: state.data[0].plot_data.histogram.data,
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
    }
})
