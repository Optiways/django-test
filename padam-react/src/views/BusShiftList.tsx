import { Table } from "react-bootstrap";
import { useGetBuses } from "../api/bus";
import { useGetBusShifts } from "../api/busShift";
import { BusCreateModal } from "../components/BusCreateModal";
import { BusShiftCreateModal } from "../components/BusShiftCreateModal";
import { DriverCreateModal } from "../components/DriverCreateModal";
import { useGetDrivers } from "../api/driver";

export function BusShiftList() {
    const busShiftsQuery = useGetBusShifts();

    return (
        <div>
            <h1>Bus Shifts</h1>
            <BusShiftCreateModal />
            <Table striped>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Bus</th>
                        <th>Driver</th>
                        <th>Stops</th>
                        <th>Departure</th>
                        <th>Arrival</th>
                    </tr>
                </thead>
                <tbody>
                    {busShiftsQuery.data?.map((bus_shifts) => {
                        return (
                            <tr key={bus_shifts.id}>
                                <td>{bus_shifts.id}</td>
                                <td>{bus_shifts.bus}</td>
                                <td>{bus_shifts.driver}</td>
                                <td>
                                    {Array.isArray(bus_shifts.stops)
                                        ? bus_shifts.stops.join(", ")
                                        : bus_shifts.stops}
                                </td>
                                <td>
                                    {new Intl.DateTimeFormat("en-US", {
                                        year: "numeric",
                                        month: "long",
                                        day: "2-digit",
                                        hour: "2-digit",
                                        minute: "2-digit",
                                        hour12: true,
                                    }).format(
                                        new Date(bus_shifts.departure_time)
                                    )}
                                </td>
                                <td>
                                    {new Intl.DateTimeFormat("en-US", {
                                        year: "numeric",
                                        month: "long",
                                        day: "2-digit",
                                        hour: "2-digit",
                                        minute: "2-digit",
                                        hour12: true,
                                    }).format(
                                        new Date(bus_shifts.arrival_time)
                                    )}
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
            </Table>
        </div>
    );
}
