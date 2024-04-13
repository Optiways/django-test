import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { BusShiftType } from "../types/BusShiftType";
import { HOST_URL } from "./constants";

const BUSES_SHIFT_KEY = "bus_shifts";

export const useGetBusShiftMutation = () => {
  const queryClient = useQueryClient();
  return useMutation<Response, Error, BusShiftType>({
    mutationFn: (variables) =>
      fetch(`${HOST_URL}/bus_shifts/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(variables),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [BUSES_SHIFT_KEY] });
    },
  });
};

export const useGetBusShifts = () =>
  useQuery<BusShiftType, Error, BusShiftType[]>({
    queryKey: [BUSES_SHIFT_KEY],
    queryFn: () =>
      fetch(`${HOST_URL}/bus_shifts`).then((response) => response.json()),
  });
