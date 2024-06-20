import React, { useEffect, useState } from 'react';
import { getBusStops } from "../api/busStop.tsx";
import moment from 'moment';

const BusStopList = () => {
    const [busStops, setBusStops] = useState([]);

    useEffect(() => {
        const fetchBusStops = async () => {
            const response = await getBusStops();
            setBusStops(response.data);
        };
        fetchBusStops();
    }, []);

    return (
        <div>
            <h2>Bus Stops</h2>
            <ul>
                {busStops.map(stop => (
                    <li key={stop.id}>Stop ID: {stop.id}, Place: {stop.place.name}, Time: {moment(stop.arrival_time).format('MMMM Do YYYY, h:mm:ss a')}</li>
                    
                ))}
            </ul>
        </div>
    );
};

export default BusStopList;
