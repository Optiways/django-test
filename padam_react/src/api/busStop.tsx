import axios from 'axios';

const API_URL = 'http://localhost:8000/transportation/';

export const getBusStops = async () => {
    return await axios.get(`${API_URL}busstops/`)
}

export const CreateBusStops = async (data) => {
    return await axios.post(`${API_URL}busstops/`, data)
}