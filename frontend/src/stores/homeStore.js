import axios from "axios";
import {defineStore} from "pinia";

const year = new Date().getFullYear()
const month = new Date().getMonth()
const calenderColors = ["#26A69A", "#B3E5FC", "#00B0FF", "#0097A7"]

export const useHomeStore = defineStore({
    id: "home",
    state: () => ({
        data: {
            calender_data: [
                {
                    key: 1,
                    customData: {
                        title: 'Olympics',
                        shortTitle: 'Oly'
                    },
                    dates: {start: new Date(year, month, 14), end: new Date(year, month, 18)},
                },
                {
                    key: 2,
                    customData: {
                        title: 'World Rowing',
                        shortTitle: 'WR'
                    },
                    dates: new Date(year, month, 2),
                },
                {
                    key: 3,
                    customData: {
                        title: "Qualifications",
                    },
                    dates: new Date(year, month, 2),
                },
                {
                    key: 4,
                    customData: {
                        title: "U23",
                        shortTitle: "U23"
                    },
                    dates: {start: new Date(year, month, 8), end: new Date(year, month, 12)},
                }
            ]
        }
    }),
    getters: {
        getCalenderData(state) {
            let calenderEntries = state.data.calender_data
            for (const [index, entry] of calenderEntries.entries()) {
                entry.customData["style"] = 'background-color:' + calenderColors[index]
            }
            return calenderEntries
        }
    },
    actions: {
        // define actions here
        async fetchData() {
            try {
                const response = await axios.get(
                    'https://test.com/get_report_filter_options'
                );
                this.data = response.data[0];
            } catch (error) {
                console.error(error);
            }
        }
    }
});