import axios from 'axios';

const API_URL = 'http://localhost:8000/transportation/';

export const getBusShift = async() => {
    return await axios.get(`${API_URL}busshifts/`)
}

export const CreateBusShift = async (data) => {
    return await axios.post(`${API_URL}busshifts/`, data, {
        headers: {
            'Content-Type': 'application/json'
        }
    });
};
