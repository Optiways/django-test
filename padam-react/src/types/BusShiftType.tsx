export type BusShiftType = {
    bus: string;
    driver: string;
    stops: Array<number>;
    departure_time: string;
    arrival_time: string;
    shift_duration: number;
    id?: number;
  };
  