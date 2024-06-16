import axios from 'axios';

const API_URL = 'http://localhost:8000/fleet/';

export const getDrivers = async () => {
    return await axios.get(`${API_URL}drivers/`);
}