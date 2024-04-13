import { Table } from "react-bootstrap";
import { useGetBuses } from "../api/bus";
import { useGetBusShifts } from "../api/busShift";
import { BusCreateModal } from "../components/BusCreateModal";
import { BusShiftCreateModal } from "../components/BusShiftCreateModal";
import { DriverCreateModal } from "../components/DriverCreateModal";
import { useGetDrivers } from "../api/driver";

export function BusList() {
    const busQuery = useGetBuses();

    return (
            <div>
                <h1>Buses</h1>
                <BusCreateModal />
                <Table striped>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Licence Plate</th>
                        </tr>
                    </thead>
                    <tbody>
                        {busQuery.data?.map((bus) => (
                            <tr key={bus.id}>
                                <td>{bus.id}</td>
                                <td>{bus.licence_plate}</td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            </div>
    );
}
