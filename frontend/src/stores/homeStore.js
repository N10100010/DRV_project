import axios from "axios";
import {defineStore} from "pinia";

export const useHomeStore = defineStore({
    id: "home",
    state: () => ({
        data: {
            calender_data: []
        },
        legend: {}
    }),
    getters: {
        getCalenderData(state) {
            let calenderEntries = state.data.calender_data;

            const color_scheme = {
                "Paralympics": "#776622",
                "World Rowing Cup": "#00B0FF",
                "World Rowing Championships": "#26A69A",
                "World Rowing U23 Championships": "#0097A7",
                "Olympics": "#B3E5FC",
                "Masters": "#742042",
                "World Rowing Under 19 Championships": "#0017A7",
                "Indoor Championships": "#9238BE",
                "Continental Championships": "#EE8822",
                "International Regattas": "#3245BE",
                "Coastal Championships": "#AADDEE",
                "Other World Rowing Competitions": "#882233",
                "World Rowing Combined Championships": "#00FF22"
            }

            return calenderEntries.map((entry, index) => {
                const hexCode = color_scheme[entry.comp_type]
                state.legend[entry.comp_type] = hexCode
                entry.customData["style"] = 'background-color:' + hexCode;
                return entry;
            });
        },
        getCalenderLegend(state) {
            return state.legend
        }
    },
    actions: {
        async fetchCalendarData() {
            try {
                const response = await axios.get(`http://localhost:5000/calendar/`);
                this.data.calender_data = response.data;
            } catch (error) {
                console.error(error);
            }
        }
    }
});