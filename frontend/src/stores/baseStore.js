import axios from "axios";
import { defineStore } from "pinia";

export const useTestState = defineStore({
  id: "base",
  state: () => ({
    data: [], // store json data here
  }),
  getters: {
    // define getters here
    getTestData(state) {
      return state.data
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
