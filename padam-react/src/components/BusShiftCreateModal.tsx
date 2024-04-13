import { Button, Modal, Form } from "react-bootstrap";
import { useState } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { useGetBusShiftMutation } from "../api/busShift";
import { useGetBuses } from "../api/bus";
import { useGetDrivers } from "../api/driver";
import { useGetStops } from "../api/stop";

export const BusShiftCreateModal = () => {
    const [show, setShow] = useState(false);

    const mutation = useGetBusShiftMutation();
    const busQuery = useGetBuses();
    const driverQuery = useGetDrivers();
    const stopQuery = useGetStops();

    const formik = useFormik({
        initialValues: {
            bus: "",
            driver: "",
            stops: [],
            departure_time: "",
            arrival_time: "",
            shift_duration: 0,
        },
        validationSchema: Yup.object({
            bus: Yup.string().max(10).required(),
            driver: Yup.string().max(20).required(),
            stops: Yup.array().max(50),
            departure_time: Yup.date(),
            arrival_time: Yup.date(),
            shift_duration: Yup.number(),
        }),
        onSubmit: (values) => {
            mutation.mutate(values);
        },
    });

    return (
        <>
            <Button onClick={() => setShow(true)}>Add Bus Shift</Button>

            <Modal show={show} onHide={() => setShow(false)}>
                <Form
                    onSubmit={(e) => {
                        e.preventDefault();
                        formik.handleSubmit();
                        setShow(false);
                    }}
                >
                    <Modal.Header closeButton>
                        <Modal.Title>Add Bus Shift</Modal.Title>
                    </Modal.Header>

                    <Modal.Body>
                        <Form.Label htmlFor="bus">Bus Licence Plate</Form.Label>
                        <Form.Control
                            as="select"
                            id="bus"
                            name="bus"
                            onChange={formik.handleChange}
                            value={formik.values.bus}
                        >
                            <option>Select a bus</option>
                            {busQuery.data?.map((bus) => {
                                return (
                                    <option key={`bus${bus.id}`} value={bus.id}>
                                        {bus.licence_plate}
                                    </option>
                                );
                            })}
                        </Form.Control>
                        <Form.Control.Feedback
                            type="invalid"
                            className={"d-block"}
                        >
                            {formik.errors.bus}
                        </Form.Control.Feedback>

                        <Form.Label htmlFor="driver">Driver</Form.Label>
                        <Form.Control
                            as="select"
                            id="driver"
                            name="driver"
                            onChange={formik.handleChange}
                            value={formik.values.driver}
                        >
                            <option>Select a driver</option>
                            {driverQuery.data?.map((driver) => {
                                return (
                                    <option key={`driver${driver.id}`} value={driver.id}>
                                        {driver.id}
                                    </option>
                                );
                            })}
                        </Form.Control>
                        <Form.Control.Feedback
                            type="invalid"
                            className={"d-block"}
                        >
                            {formik.errors.driver}
                        </Form.Control.Feedback>

                        <Form.Label htmlFor="stops">Stops</Form.Label>
                        <Form.Control
                            as="select"
                            id="stops"
                            name="stops"
                            onChange={formik.handleChange}
                            value={formik.values.stops}
                        >
                            <option>select a stop</option>
                            {stopQuery.data?.map((stop) => {
                                return (
                                    <option key={`stop${stop.id}`} value={stop.id}>
                                        {stop.place}
                                    </option>
                                );
                            })}
                        </Form.Control>
                        <Form.Control.Feedback
                            type="invalid"
                            className={"d-block"}
                        >
                            {formik.errors.stops}
                        </Form.Control.Feedback>

                        <Form.Label htmlFor="departure_time">
                            Departure
                        </Form.Label>
                        <Form.Control
                            type="datetime-local"
                            id="departure_time"
                            name="departure_time"
                            onChange={formik.handleChange}
                            value={formik.values.departure_time}
                        />
                        <Form.Control.Feedback
                            type="invalid"
                            className={"d-block"}
                        >
                            {formik.errors.departure_time}
                        </Form.Control.Feedback>

                        <Form.Label htmlFor="arrival_time">Arrival</Form.Label>
                        <Form.Control
                            type="datetime-local"
                            id="arrival_time"
                            name="arrival_time"
                            onChange={formik.handleChange}
                            value={formik.values.arrival_time}
                        />
                        <Form.Control.Feedback
                            type="invalid"
                            className={"d-block"}
                        >
                            {formik.errors.arrival_time}
                        </Form.Control.Feedback>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button type="submit" disabled={!formik.isValid}>
                            Submit
                        </Button>
                    </Modal.Footer>
                </Form>
            </Modal>
        </>
    );
};
