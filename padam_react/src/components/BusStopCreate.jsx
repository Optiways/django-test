import React, { useState } from 'react';
import { CreateBusStops } from '../api/busStop.tsx';

const BusStopCreate = () => {
    const [busStop, setBusStop] = useState({
        place: '',
        arrival_time: ''
    });

    const handleChange = e => {
        const { name, value } = e.target;
        setBusStop(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async e => {
        e.preventDefault();
        try {
            const response = await CreateBusStops(busStop);
            console.log('Created Bus Stop: ', response.data);
            alert('Bus stop created successfully!');
        } catch (error) {
            console.error('Error creating bus stop:', error);
            alert('Failed to create bus stop.');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="number" name="place" value={busStop.place} onChange={handleChange} placeholder="Place ID" />
            <input type="text" name="arrival_time" value={busStop.arrival_time} onChange={handleChange} placeholder="Arrival Time (YYYY-MM-DD HH:MM:SS)" />
            <button type="submit">Create Bus Stop</button>
        </form>
    );
};

export default BusStopCreate;
