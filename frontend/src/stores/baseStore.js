import axios from "axios";
import { defineStore } from "pinia";

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
                    "lag [s]": "00:00:03,12",
                    "relDiffToAvgSpeed [%]": -1.3
                  },
                  "1000": {
                    "time [t]": "00:03:13,82",
                    "pace [t]": "00:01:50,72",
                    "rank": 1,
                    "lag [s]": "00:00:00,00",
                    "relDiffToAvgSpeed [%]": 4.3
                  },
                  "1500": {
                    "time [t]": "00:04:52,00",
                    "pace [t]": "00:01:50,72",
                    "rank": 1,
                    "lag [s]": "00:00:00,00",
                    "relDiffToAvgSpeed [%]": 2.3
                  },
                  "2000": {
                    "time [t]": "00:06:29,14",
                    "pace [t]": "00:01:50,72",
                    "rank": 1,
                    "lag [s]": "00:00:00,00",
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
                    }
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
    getSpeedChartData(state) {
      return {
            labels: Object.keys(state.data.raceData[0].data[0].gpsData.distance),
            datasets: [
                {
                label: state.data.raceData[0].data[0].nation_ioc,
                backgroundColor: '#f5bd00',
                borderColor: '#f5bd00',
                data: Object.values(state.data.raceData[0].data[0].gpsData.distance)
                    .map(distanceObj => distanceObj['speed [m/s]'])
              },
            ]
      }
    },
    getStrokeChartData(state) {
      return {
            labels: Object.keys(state.data.raceData[0].data[0].gpsData.distance),
            datasets: [
                {
                label: state.data.raceData[0].data[0].nation_ioc,
                backgroundColor: 'blue',
                borderColor: 'blue',
                data: Object.values(state.data.raceData[0].data[0].gpsData.distance)
                    .map(distanceObj => distanceObj['stroke [1/min]'])
              },
            ]
      }
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
    }
  }
});
