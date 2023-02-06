import axios from "axios";
import {defineStore} from "pinia";

// function to convert milliseconds to min:sec:ms
const formatMilliseconds = ms => {
    if (!ms) {
        return '00:00.000';
    }
    return new Date(ms).toISOString().slice(14, -2);
};


// predefined colors for charts
const COLORS = ['#0C67F7', '#93E9ED', '#E0A9FA', '#E0B696', '#E0FAAC', '#F0E95A'];

export const useRennstrukturAnalyseState = defineStore({
    id: "base",
    state: () => ({
        filterOpen: false,
        loadingState: false,
        tableExport: [],
        data: {
            filterOptions: [{
                // TODO: Year also has to be defined by backend data
                "year": [{"start_year": 1950}, {"end_year": 2025}],
                "competition_category_ids": []
            }],
            raceData: [{
                "race_id": 195638,
                "displayName": "Men's Eight Heat 1",
                "startDate": "2022-06-16 14:12:00",
                "venue": "Malta/Poznan, Poland",
                "boatClass": "Men's Eight",
                "worldBestTimeBoatClass": 358360,
                "bestTimeBoatClassCurrentOZ": 358360,
                "pdf_urls": {
                    "result": "https://d3fpn4c9813ycf.cloudfront.net/pdfDocuments/WCH_2018/WCH_2018_ROWWSCULL2------------HEAT000100--_C73X7962.PDF",
                    "race_data": "https://d3fpn4c9813ycf.cloudfront.net/pdfDocuments/ECM2022/ECM2022_ROWXSCULL2--PR2-------PREL000100--_C77X3426.PDF"
                },
                "data": [
                    {
                        "nation_ioc": "CZE",
                        "lane": 2,
                        "rank": 1,
                        "run": "FB",
                        "progressionCode": "SA/B",
                        "athletes": [
                            {
                                "id": 98245435,
                                "firstName": "Lukas",
                                "lastName": "Helesic",
                                "position": "b"
                            },
                            {
                                "id": 954345365,
                                "firstName": "S Jakub",
                                "lastName": "Podrazil",
                                "position": "s"
                            }
                        ],
                        "intermediates": {
                            "500": {
                                "time [t]": 144200,
                                "pace [t]": 144200,
                                "rank": 2,
                                "deficit [s]": 1500,
                                "relDiffToAvgSpeed [%]": -1.3
                            },
                            "1000": {
                                "time [t]": 144200,
                                "pace [t]": 144200,
                                "rank": 1,
                                "deficit [s]": 0,
                                "relDiffToAvgSpeed [%]": 4.3
                            },
                            "1500": {
                                "time [t]": 144200,
                                "pace [t]": 144200,
                                "rank": 1,
                                "deficit [s]": 0,
                                "relDiffToAvgSpeed [%]": 2.3
                            },
                            "2000": {
                                "time [t]": 144200,
                                "pace [t]": 144200,
                                "rank": 1,
                                "deficit [s]": 0,
                                "relDiffToAvgSpeed [%]": 1.3
                            }
                        },
                        "gpsData": {
                            "distance": {
                                "50": {
                                    "speed [m/s]": 5.2,
                                    "stroke [1/min]": 34.1,
                                    "propulsion [m/stroke]": 8.3
                                },
                                "100": {
                                    "speed [m/s]": 4.9,
                                    "stroke [1/min]": 33.4,
                                    "propulsion [m/stroke]": 8.8
                                },
                                "150": {
                                    "speed [m/s]": 4.7,
                                    "stroke [1/min]": 35.0,
                                    "propulsion [m/stroke]": 7.1
                                },
                                "200": {
                                    "speed [m/s]": 4.6,
                                    "stroke [1/min]": 38.0,
                                    "propulsion [m/stroke]": 8.1
                                },
                                "250": {
                                    "speed [m/s]": 4.9,
                                    "stroke [1/min]": 32.0,
                                    "propulsion [m/stroke]": 7.2
                                },
                                "300": {
                                    "speed [m/s]": 4.7,
                                    "stroke [1/min]": 35.0,
                                    "propulsion [m/stroke]": 7.1
                                },
                                "350": {
                                    "speed [m/s]": 4.6,
                                    "stroke [1/min]": 38.0,
                                    "propulsion [m/stroke]": 8.1
                                },
                                "400": {
                                    "speed [m/s]": 4.9,
                                    "stroke [1/min]": 32.0,
                                    "propulsion [m/stroke]": 7.2
                                },
                                "500": {
                                    "speed [m/s]": 3.9,
                                    "stroke [1/min]": 43.0,
                                    "propulsion [m/stroke]": 3.6
                                },
                                "1000": {
                                    "speed [m/s]": 5.9,
                                    "stroke [1/min]": 43.0,
                                    "propulsion [m/stroke]": 3.6
                                },
                                "1500": {
                                    "speed [m/s]": 5.9,
                                    "stroke [1/min]": 43.0,
                                    "propulsion [m/stroke]": 3.6
                                },
                                "2000": {
                                    "speed [m/s]": 5.9,
                                    "stroke [1/min]": 43.0,
                                    "propulsion [m/stroke]": 3.6
                                },
                            }
                        }

                    },
                    {
                        "nation_ioc": "DEU",
                        "lane": 3,
                        "rank": 2,
                        "run": "FB",
                        "progressionCode": "R",
                        "athletes": [
                            {
                                "id": 98245435,
                                "firstName": "Max",
                                "lastName": "Maier",
                                "position": "b"
                            },
                            {
                                "id": 954345365,
                                "firstName": "S Jakub",
                                "lastName": "Podrazil",
                                "position": "s"
                            }
                        ],
                        "intermediates": {
                            "500": {
                                "time [t]": 144200,
                                "pace [t]": 144200,
                                "rank": 1,
                                "deficit [s]": 0,
                                "relDiffToAvgSpeed [%]": -1.3
                            },
                            "1000": {
                                "time [t]": 144200,
                                "pace [t]": 144200,
                                "rank": 2,
                                "deficit [s]": 2660,
                                "relDiffToAvgSpeed [%]": 4.3
                            },
                            "1500": {
                                "time [t]": 144200,
                                "pace [t]": 144200,
                                "rank": 2,
                                "deficit [s]": 4000,
                                "relDiffToAvgSpeed [%]": 2.3
                            },
                            "2000": {
                                "time [t]": 144200,
                                "pace [t]": 144200,
                                "rank": 2,
                                "deficit [s]": 5340,
                                "relDiffToAvgSpeed [%]": 1.3
                            }
                        },
                        "gpsData": {
                            "distance": {
                                "50": {
                                    "speed [m/s]": 4.6,
                                    "stroke [1/min]": 32.7,
                                    "propulsion [m/stroke]": 7.3
                                },
                                "100": {
                                    "speed [m/s]": 4.5,
                                    "stroke [1/min]": 36.5,
                                    "propulsion [m/stroke]": 7.5
                                },
                                "150": {
                                    "speed [m/s]": 4.9,
                                    "stroke [1/min]": 32.0,
                                    "propulsion [m/stroke]": 7.8
                                },
                                "200": {
                                    "speed [m/s]": 5.2,
                                    "stroke [1/min]": 36.3,
                                    "propulsion [m/stroke]": 6.1
                                },
                                "250": {
                                    "speed [m/s]": 5.1,
                                    "stroke [1/min]": 37.4,
                                    "propulsion [m/stroke]": 7.2
                                },
                                "300": {
                                    "speed [m/s]": 3.9,
                                    "stroke [1/min]": 30.0,
                                    "propulsion [m/stroke]": 8.2
                                },
                                "350": {
                                    "speed [m/s]": 4.4,
                                    "stroke [1/min]": 35.0,
                                    "propulsion [m/stroke]": 3.9
                                },
                                "400": {
                                    "speed [m/s]": 4.9,
                                    "stroke [1/min]": 37.0,
                                    "propulsion [m/stroke]": 4.6
                                },
                                "500": {
                                    "speed [m/s]": 5.9,
                                    "stroke [1/min]": 43.0,
                                    "propulsion [m/stroke]": 3.6
                                },
                                "1000": {
                                    "speed [m/s]": 5.9,
                                    "stroke [1/min]": 43.0,
                                    "propulsion [m/stroke]": 3.6
                                },
                                "1500": {
                                    "speed [m/s]": 5.9,
                                    "stroke [1/min]": 43.0,
                                    "propulsion [m/stroke]": 3.6
                                },
                                "2000": {
                                    "speed [m/s]": 5.9,
                                    "stroke [1/min]": 43.0,
                                    "propulsion [m/stroke]": 3.6
                                },
                            }
                        }
                    }
                ]
            }],
            analysis: null
        },
    }),
    getters: {
        getFilterState(state) {
            return state.filterOpen
        },
        getAnalysisData(state) {
            return state.data.analysis
        },
        getCompetitionData(state) {
            const data = state.data.raceData[0]
            data.worldBestTimeBoatClass = formatMilliseconds(data.worldBestTimeBoatClass);
            data.bestTimeBoatClassCurrentOZ = formatMilliseconds(data.bestTimeBoatClassCurrentOZ);
            return data
        },
        getRaceAnalysisFilterOptions(state) {
            return state.data.filterOptions
        },
        getOldTableData(state) {
            return state.data.raceData[0].data
        },
        getLoadingState(state) {
            return state.loadingState
        },
        getTableData(state) {
            if (!state.data.raceData[0].data[0].intermediates.hasOwnProperty('0')) {
                return
            }
            const tableHead = ['Platz', 'Bahn', 'Nation', 'Mannschaft'];
            const intermediateDistances = state.data.raceData[0].data[0].intermediates
            for (const key in intermediateDistances) {
                // ignore first as this is the starting value
                if (key !== '0') {
                    tableHead.push(key + "m", "Position")
                }
            }

            const tableData = [];
            tableData.push(tableHead);
            state.data.raceData[0].data.forEach(dataObj => {
                console.log(dataObj.intermediates)
                if (dataObj.intermediates !== '0') {
                    const rowData = [];
                    const athleteNames = [];
                    rowData.push(dataObj.rank, dataObj.lane, dataObj.nation_ioc);
                    for (const [key, athlete] of Object.entries(dataObj.athletes)) {
                        athleteNames.push("(" + athlete.position + ") " + athlete.firstName
                            .concat(" ", athlete.lastName)
                        )
                    }
                    const firstArray = [];
                    const secondArray = [];
                    const speedValues = [];
                    const strokeValues = [];
                    const propulsionValues = [];

                    for (const [key, gpsData] of Object.entries(dataObj.gpsData)) {
                        for (const intermediateDistance in intermediateDistances) {
                            const objectKeys = Object.keys(gpsData);
                            if (objectKeys.includes(intermediateDistance)) {
                                speedValues.push(gpsData[intermediateDistance]["speed [m/s]"] + "[m/s]")
                                strokeValues.push(gpsData[intermediateDistance]["stroke [1/min]"] + "[1/min]")
                                propulsionValues.push(gpsData[intermediateDistance]["propulsion [m/stroke]"] + "[m/Schlag]")
                            }
                        }
                    }
                    rowData.push(athleteNames);
                    for (const [index, [key, intermediate]] of Object.entries(dataObj.intermediates).entries()) {
                        firstArray.push(
                            formatMilliseconds(intermediate["time [t]"]),
                            formatMilliseconds(intermediate["pace [t]"]),
                            formatMilliseconds(intermediate["deficit [s]"])
                        )
                        secondArray.push(["(" + intermediate["rank"] + ")", speedValues[index], strokeValues[index], propulsionValues[index]])
                    }
                    const chunkSize = 3;
                    const tempArray = [];
                    for (let i = 0; i < firstArray.length; i += chunkSize) {
                        tempArray.push(firstArray.slice(i, i + chunkSize));

                    }
                    tempArray.forEach((value, index) => {
                        rowData.push(value)
                        rowData.push(secondArray[index])
                    })
                    tableData.push(rowData);
                }
            })
            state.tableExport = tableData
            return tableData;
        },

        getDeficitInMeters(state) {
            // TODO: How to integrate the time here?
            // determine winner
            const winnerIdx = state.data.raceData[0].data.findIndex(team => team.rank === 1);
            const winnerData = state.data.raceData[0].data.map(dataObj => dataObj.gpsData.distance)[winnerIdx]
            const winnerTeamSpeeds = Object.fromEntries(Object.entries(winnerData).map(
                ([key, val]) => [key, val["speed [m/s]"]]));

            // calculate difference to winner based on speed
            let speedPerTeam = {};
            for (const i in state.data.raceData[0].data) {
                const speedData = state.data.raceData[0].data.map(dataObj => dataObj.gpsData.distance)[i];
                let diffSpeedValues = {}
                for (const [key, val] of Object.entries(speedData)) {
                    const speedWinner = winnerTeamSpeeds[key]
                    const speedCurrentTeam = val["speed [m/s]"]
                    let time = 0
                    if (speedWinner !== 0) {
                        time = 50 / speedWinner;
                    }
                    diffSpeedValues[key] = (speedWinner * time) - (speedCurrentTeam * time);
                }
                speedPerTeam[i] = diffSpeedValues
            }
            let colorIndex = 0;
            const datasets = []
            Object.entries(speedPerTeam).forEach(([key, value]) => {
                const label = key;
                const backgroundColor = COLORS[colorIndex % 6];
                const borderColor = COLORS[colorIndex % 6];
                const data = Object.values(value);
                datasets.push({label, backgroundColor, borderColor, data});
                colorIndex++;
            });
            const allKeys = Object.values(speedPerTeam).map(obj => Object.keys(obj))
            return {
                labels: Array.from(new Set([].concat(...allKeys))),
                datasets
            };
        },
        getGPSChartData(state) {
            const chartDataKeys = ['speed [m/s]', 'stroke [1/min]', 'propulsion [m/stroke]'];
            return chartDataKeys.map(key => {
                const datasets = [];
                let colorIndex = 0;
                state.data.raceData[0].data.forEach(dataObj => {
                    const label = dataObj.nation_ioc;
                    const backgroundColor = COLORS[colorIndex % 6];
                    const borderColor = COLORS[colorIndex % 6];
                    dataObj.gpsData.distance["0"] = {'speed [m/s]': 0, 'stroke [1/min]': 0, 'propulsion [m/stroke]': 0}
                    const data = Object.values(dataObj.gpsData.distance).map(obj => obj[key]);
                    datasets.push({label, backgroundColor, borderColor, data});
                    colorIndex++;
                });
                return {
                    labels: Object.keys(state.data.raceData[0].data[0].gpsData.distance),
                    datasets
                };
            })
        },
        getIntermediateChartData(state) {
            const intermediateDataKeys = ["rank", "deficit [s]"];
            return intermediateDataKeys.map(key => {
                const datasets = [];
                let colorIndex = 0;
                state.data.raceData[0].data.forEach(dataObj => {
                    const label = dataObj.nation_ioc;
                    const backgroundColor = COLORS[colorIndex % 6];
                    const borderColor = COLORS[colorIndex % 6];
                    // add zero values as start point
                    dataObj.intermediates["0"] = {"rank": 0, "deficit [s]": 0}
                    let data = Object.values(dataObj.intermediates).map(distanceObj => distanceObj[key]);
                    if (key === "deficit [s]") {
                        data = data.map(x => formatMilliseconds(x))
                    }
                    datasets.push({label, backgroundColor, borderColor, data});
                    colorIndex++;
                });
                const chartLabels = Object.keys(state.data.raceData[0].data[0].intermediates)
                return {
                    labels: chartLabels,
                    datasets
                };
            })
        }
    },
    actions: {
        async getFilterOptions() {
            try {
                this.data.filterOptions[0].competition_category_ids = await axios.get(
                    'http://localhost:5000/competition_category/'
                )
            } catch (error) {
                console.error(error)
            }
        },
        async postFormData(formData) {


            setTimeout(() => {
                this.data.analysis = [
                    {
                        "id": 395871,
                        "display_name": "2022 World Rowing Cup II",
                        "venue": "Malta/Poznan, Poland",
                        "start_date": "2022-06-16 00:00:00",
                        "competition_category": "World Rowing Cup",
                        "events": [
                            {
                                "id": 734839,
                                "display_name": "Lightweight Women's Single Sculls",
                                "races": [
                                    {"id": 187573, "display_name": "Final FB"},
                                    {"id": 424754, "display_name": "Heat 1"}
                                ]
                            },
                            {
                                "id": 748394,
                                "display_name": "Men's Four",
                                "races": [
                                    {"id": 195638, "display_name": "Men's Eight Heat 1"},
                                    {"id": 823759, "display_name": "Men's Eight Final FA"},
                                    {"id": 748394, "display_name": "Men's Eight Repechage"},
                                    {"id": 839473, "display_name": "Men's Eight Heat 2"}
                                ]
                            }
                        ]
                    },
                    {
                        "id": 395871,
                        "display_name": "2022 World Rowing Cup III",
                        "venue": "Malta/Poznan, Poland",
                        "start_date": "2022-06-16 00:00:00",
                        "competition_category": "World Rowing Cup",
                        "events": [
                            {
                                "id": 734839,
                                "display_name": "Lightweight Women's Single Sculls",
                                "races": [
                                    {"id": 187573, "display_name": "Final FB"},
                                    {"id": 424754, "display_name": "Heat 1"}
                                ]
                            },
                            {
                                "id": 748394,
                                "display_name": "Men's Four",
                                "races": [
                                    {"id": 195638, "display_name": "Men's Eight Heat 1"},
                                    {"id": 823759, "display_name": "Men's Eight Final FA"},
                                    {"id": 748394, "display_name": "Men's Eight Repechage"},
                                    {"id": 839473, "display_name": "Men's Eight Heat 2"}
                                ]
                            }
                        ]
                    }
                ]
                this.loadingState = false
            }, 800);
            /*
            await axios.post('http://localhost:5000//competition', {formData})
                .then(response => {
                    // Bearbeite die Antwort des Backends hier
                }).catch(error => {
                    // Bearbeite den Fehler hier
                });
            */
        },
        setFilterState(filterState) {
            this.filterOpen = !filterState
        },
        setToLoadingState() {
            this.loadingState = true
        },
        exportTableData() {
            const csvContent = "data:text/csv;charset=utf-8," + this.tableExport.map(e => e.join(",")).join("\n");
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "rennstruktur.csv");
            document.body.appendChild(link);
            link.click();
        }
    }
});