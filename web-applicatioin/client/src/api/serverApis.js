import axios from 'axios';

const API = axios.create({ baseURL: `${process.env.REACT_APP_SERVER_BASE_URL}` });

export const signin = (data) => API.post('/user/signin', data);



