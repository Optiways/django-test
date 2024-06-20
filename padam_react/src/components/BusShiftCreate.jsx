import React, { useEffect, useState } from 'react';
import Select from 'react-select';
import { CreateBusShift } from '../api/busShift.tsx';
import { getBuses } from '../api/bus.tsx';
import { getDrivers } from '../api/Driver.tsx';
import { getBusStops } from '../api/busStop.tsx';
import moment from 'moment';

const BusShiftCreate = () => {
    const [busShift, setBusShift] = useState({ bus: '', driver: '', stops: [] });
    const [buses, setBuses] = useState([]);
    const [drivers, setDrivers] = useState([]);
    const [stopsOptions, setStopsOptions] = useState([]);
    const [errors, setErrors] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            try {
                const busRes = await getBuses();
                const driverRes = await getDrivers();
                const stopRes = await getBusStops();

                const formattedBuses = busRes.data.map(bus => ({
                    value: bus.id,
                    label: `number ${bus.id} - ${bus.licence_plate}`
                }));
                const formattedDrivers = driverRes.data.map(driver => ({
                    value: driver.id,
                    label: `${driver.id} - ${driver.user.username} `
                }));
                const formattedStops = stopRes.data.map(stop => ({
                    value: stop.id,
                    label: `${stop.place.name} arrive at ${moment(stop.arrival_time).format('MMMM Do YYYY, h:mm:ss a')} `
                }));

                setBuses(formattedBuses);
                setDrivers(formattedDrivers);
                setStopsOptions(formattedStops);
            } catch (error) {
                console.error("Failed to fetch data: ", error);
            }
        };

        fetchData();
    }, []);

    const handleChange = (selectedOption, actionMeta) => {
        const { name } = actionMeta;
        if (name === 'stops') {
            const values = selectedOption ? selectedOption.map(option => option.value) : [];
            setBusShift(prevState => ({
                ...prevState,
                [name]: values
            }));
        } else {
            const value = selectedOption ? selectedOption.value : '';
            setBusShift(prevState => ({
                ...prevState,
                [name]: value
            }));
        }
    };

    const handleSubmit = async e => {
        e.preventDefault();
        try {
            const formattedData = { ...busShift };
            const response = await CreateBusShift(formattedData);
            console.log('Created Bus Shift: ', response.data);
            alert('Bus shift created successfully!');
        } catch (error) {
            if (error.response && error.response.data) {
                setErrors(error.response.data);
            } else {
                console.error('Error creating bus shift:', error);
                alert('Failed to create bus shift.');
            }
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <Select
                    name="bus"
                    options={buses}
                    onChange={handleChange}
                />
                {errors.bus && <div className="error">{errors.bus}</div>}
            </div>
            <div>
                <Select
                    name="driver"
                    options={drivers}
                    onChange={handleChange}
                />
                {errors.driver && <div className="error">{errors.driver}</div>}
            </div>
            <div>
                <Select
                    isMulti
                    name="stops"
                    options={stopsOptions}
                    className="basic-multi-select"
                    classNamePrefix="select"
                    onChange={handleChange}
                />
                {errors.stops && <div className="error">{errors.stops}</div>}
            </div>
            <button type="submit">Create Bus Shift</button>
        </form>
    );
};

export default BusShiftCreate;
