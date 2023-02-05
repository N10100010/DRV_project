import axios from "axios";
import {defineStore} from "pinia";

const calenderColors = ["#26A69A", "#B3E5FC", "#00B0FF", "#0097A7"]

export const useHomeStore = defineStore({
    id: "home",
    state: () => ({
        data: {
            calender_data: []
        }
    }),
    getters: {
        getCalenderData(state) {
            let calenderEntries = state.data.calender_data;
            return calenderEntries.map((entry, index) => {
                entry.customData["style"] = 'background-color:' + calenderColors[index % calenderColors.length];
                return entry;
            });
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