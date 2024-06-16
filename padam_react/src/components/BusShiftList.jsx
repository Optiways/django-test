import React, { useEffect, useState } from 'react';
import { getBusShift } from '../api/busShift.tsx';
import moment from 'moment';

const BusShiftList = () => {
    const [busShifts, setBusShifts] = useState([]);

    useEffect(() => {
        const fetchBusShifts = async () => {
            const response = await getBusShift();
            setBusShifts(response.data);
        };
        fetchBusShifts();
    }, []);

    return (
        <div>
            <h2>Bus Shifts</h2>
            <table>
                <thead>
                    <tr>
                        <th>Shift ID</th>
                        <th>Bus</th>
                        <th>Driver</th>
                        <th>Departure Time</th>
                        <th>Arrival Time</th>
                        <th>Duration</th>
                        <th>Stops</th>
                    </tr>
                </thead>
                <tbody>
                    {busShifts.map(shift => (
                        <tr key={shift.id}>
                            <td>{shift.id}</td>
                            <td>{shift.bus}</td>
                            <td>{shift.driver}</td>
                            <td>{moment(shift.departure_time).format('MMMM Do YYYY, h:mm:ss a')}</td>
                            <td>{moment(shift.arrival_time).format('MMMM Do YYYY, h:mm:ss a')}</td>
                            <td>{shift.shift_duration}</td>
                            <td>{shift.stops.map((stop, index) => <span key={index}>{stop}, </span>)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default BusShiftList;
