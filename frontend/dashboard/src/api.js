import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000/api",
   headers: {
    "x-token": "mon-token-secret",  
  },
});

export default API;
