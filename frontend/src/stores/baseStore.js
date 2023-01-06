import axios from "axios";
import { defineStore } from "pinia";


const COLORS = ['#1E90FF', '#EE7621', '#66CD00', '#CD0000', '#7A67EE', '#32ffff'];
export const useRennstrukturAnalyseState = defineStore({
  id: "base",
  state: () => ({
    data: {
      raceData: [ {
            "race_id": 195638,
            "displayName": "Men's Eight Heat 1",
            "startDate": "2022-06-16 14:12:00",
            "venue": "Malta/Poznan, Poland",
            "boatClass": "Men's Eight",
            "worldBestTimeBoatClass": "00:05:58,36",
            "bestTimeBoatClassCurrentOZ": "00:05:58,36",
            "data": [
              {
                "nation_ioc": "CZE",
                "lane": 2,
                "rank": 1,
                "run": "FB",
                "progressionCode": "1-3SA/B 4..SC/D",
                "athletes": [
                  {
                    "id": 98245435,
                    "firstName": "Lukas",
                    "lastName": "Helesic"
                  },
                  {
                    "id": 954345365,
                    "firstName": "S Jakub",
                    "lastName": "Podrazil"
                  }
                ],
                "intermediates": {
                  "500": {
                    "time [t]": "00:02:24,12",
                    "pace [t]": "00:02:24,12",
                    "rank": 2,
                    "deficit [s]": "00:00:03,12",
                    "relDiffToAvgSpeed [%]": -1.3
                  },
                  "1000": {
                    "time [t]": "00:03:13,82",
                    "pace [t]": "00:01:50,72",
                    "rank": 1,
                    "deficit [s]": "00:00:00,00",
                    "relDiffToAvgSpeed [%]": 4.3
                  },
                  "1500": {
                    "time [t]": "00:04:52,00",
                    "pace [t]": "00:01:50,72",
                    "rank": 1,
                    "deficit [s]": "00:00:00,00",
                    "relDiffToAvgSpeed [%]": 2.3
                  },
                  "2000": {
                    "time [t]": "00:06:29,14",
                    "pace [t]": "00:01:50,72",
                    "rank": 1,
                    "deficit [s]": "00:00:00,00",
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
                "progressionCode": "1-3SA/B 4..SC/D",
                "athletes": [
                  {
                    "id": 98245435,
                    "firstName": "Max",
                    "lastName": "Maier"
                  },
                  {
                    "id": 954345365,
                    "firstName": "S Jakub",
                    "lastName": "Podrazil"
                  }
                ],
                "intermediates": {
                  "500": {
                    "time [t]": "00:01:24,12",
                    "pace [t]": "00:02:24,12",
                    "rank": 2,
                    "deficit [s]": "00:00:03,12",
                    "relDiffToAvgSpeed [%]": -1.3
                  },
                  "1000": {
                    "time [t]": "00:03:13,82",
                    "pace [t]": "00:01:50,72",
                    "rank": 1,
                    "deficit [s]": "00:00:00,00",
                    "relDiffToAvgSpeed [%]": 4.3
                  },
                  "1500": {
                    "time [t]": "00:04:52,00",
                    "pace [t]": "00:01:50,72",
                    "rank": 1,
                    "deficit [s]": "00:00:00,00",
                    "relDiffToAvgSpeed [%]": 2.3
                  },
                  "2000": {
                    "time [t]": "00:06:29,14",
                    "pace [t]": "00:01:50,72",
                    "rank": 1,
                    "deficit [s]": "00:00:00,00",
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
          } ],
      analysis: [
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
                { "id": 187573, "display_name": "Final FB" },
                { "id": 424754, "display_name": "Heat 1" }
              ]
            },
            {
              "id": 748394,
              "display_name": "Men's Four",
              "races": [
                { "id": 195638, "display_name": "Men's Eight Heat 1" },
                { "id": 823759, "display_name": "Men's Eight Final FA" },
                { "id": 748394, "display_name": "Men's Eight Repechage" },
                { "id": 839473, "display_name": "Men's Eight Heat 2" }
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
                { "id": 187573, "display_name": "Final FB" },
                { "id": 424754, "display_name": "Heat 1" }
              ]
            },
            {
              "id": 748394,
              "display_name": "Men's Four",
              "races": [
                { "id": 195638, "display_name": "Men's Eight Heat 1" },
                { "id": 823759, "display_name": "Men's Eight Final FA" },
                { "id": 748394, "display_name": "Men's Eight Repechage" },
                { "id": 839473, "display_name": "Men's Eight Heat 2" }
              ]
            }
          ]
        }
        ]
    },
  }),
  getters: {
    getAnalysisData(state) {
      return state.data.analysis
    },
    getCompetitionData(state) {
      return state.data.raceData[0]
    },
    getOldTableData(state) {
      return state.data.raceData[0].data
    },
    getTableData(state) {
      const tableHead = ['Platz', 'Bahn', 'Nation', 'Mannschaft'];
      const intermediateDistances = state.data.raceData[0].data[0].intermediates
      for(const key in intermediateDistances) {
        tableHead.push(key + "m", "Position")
      }

      const tableData = [];
      tableData.push(tableHead);
      state.data.raceData[0].data.forEach(dataObj => {
        const rowData = [];
        const athleteNames = [];
        rowData.push(dataObj.rank, dataObj.lane, dataObj.nation_ioc);
        for(const [key, athlete] of Object.entries(dataObj.athletes)) {
          athleteNames.push(athlete.firstName.concat(" ", athlete.lastName))
        }
        const firstArray = [];
        const secondArray = [];

        const speedValues = [];
        const strokeValues = [];
        const propulsionValues = [];
          
        for(const [key, gpsData] of Object.entries(dataObj.gpsData)) {
          for(const intermediateDistance in intermediateDistances) {
            const objectKeys = Object.keys(gpsData);
            if(objectKeys.includes(intermediateDistance)) {
              speedValues.push(gpsData[intermediateDistance]["speed [m/s]"] + "[m/s]")
              strokeValues.push(gpsData[intermediateDistance]["stroke [1/min]"] + "[1/min]")
              propulsionValues.push(gpsData[intermediateDistance]["propulsion [m/stroke]"] + "[m/Schlag]")
            }
          }
        }

        rowData.push(athleteNames);
        for(const [index,[key, intermediate]] of Object.entries(dataObj.intermediates).entries()) {
          firstArray.push(intermediate["time [t]"], intermediate["pace [t]"], intermediate["deficit [s]"])
          secondArray.push(["("+ intermediate["rank"] + ")", speedValues[index], strokeValues[index], propulsionValues[index]])
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
      })

      return tableData;
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
          const data = Object.values(dataObj.gpsData.distance).map(distanceObj => distanceObj[key]);
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
          const data = Object.values(dataObj.intermediates).map(distanceObj => distanceObj[key]);
          datasets.push({label, backgroundColor, borderColor, data});
          colorIndex++;
        });
        return {
          labels: Object.keys(state.data.raceData[0].data[0].intermediates),
          datasets
        };
      })
    }
  },
  actions: {
    // define actions here
    async fetchData() {
      try {
        const response = await axios.get(
          'https://jsonplaceholder.typicode.com/users'
        );
        this.data = response.data[0];
      } catch (error) {
        console.error(error);
      }
    },
    async postFormData(formData) {
      await axios.post('https://jsonplaceholder.typicode.com/users',{ formData })
          .then(response => {
            // Bearbeite die Antwort des Backends hier
          }).catch(error => {
            // Bearbeite den Fehler hier
      });
    }
  }
});