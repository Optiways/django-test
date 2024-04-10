import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { BusType } from "../types/BusType";
import { HOST_URL } from "./constants";

const BUSES_KEY = "buses";

export const useGetBusMutation = () => {
  const queryClient = useQueryClient();
  return useMutation<Response, Error, BusType>({
    mutationFn: (variables) =>
      fetch(`${HOST_URL}/buses/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(variables),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [BUSES_KEY] });
    },
  });
};

export const useGetBuses = () =>
  useQuery<BusType, Error, BusType[]>({
    queryKey: [BUSES_KEY],
    queryFn: () =>
      fetch(`${HOST_URL}/buses`).then((response) => response.json()),
  });
