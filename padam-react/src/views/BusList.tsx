import { Table } from "react-bootstrap";
import { useGetBuses } from "../api/bus";
import { BusCreateModal } from "../components/BusCreateModal";

export function BusList() {
  const query = useGetBuses();

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
          {query.data?.map((bus) => (
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
