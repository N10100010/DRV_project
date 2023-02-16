import router from '../router'
import axios from "axios";
import { useLoginStore } from "../stores/loginStore";

// const loginStore = useLoginStore();

axios.interceptors.response.use(
    function (response) {
        return response
    }, function (error) {
        console.log(error.response.data)
        if (error.response.status === 401) {
            const loginStore = useLoginStore();
            loginStore.token = "";
            console.log(loginStore)
            router.push('/auth')
        }
        return Promise.reject(error)
    }
);

axios.interceptors.request.use((request) => {
    const loginStore = useLoginStore();
    if (loginStore.token) {
        // console.log('Add token to header', loginStore.token);
        request.headers.Authorization = `Bearer ${loginStore.token}`;
    }
    return request;
});