import axios from 'axios';

const baseURL = "http://127.0.0.1:8000/api/"

const axiosInstance = axios.create({
    baseURL: baseURL,
    timeout: 10000,
    headers: {
        Authorisation: localStorage.getItem('access_token')
        ? 'JWT ' + localStorage.getItem('access token')
        : null,
        'Content-Type': 'application/json',
        accept: 'application/json'
    },
});

export default axiosInstance;