import axios from "axios";

// const API = axios.create({ baseURL: `${process.env.REACT_APP_SERVER_BASE_URL}` });
const API = axios.create({ baseURL: `http://localhost:5000` });

export const signin = (data) => API.post("/user/signin", data);

export const productsList = (name, count) => API.get(`/products/${name}/${count}`);
export const product = (id) => API.get(`/product/${id}`);
