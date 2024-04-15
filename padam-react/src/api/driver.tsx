import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { DriverType } from "../types/DriverType";
import { HOST_URL } from "./constants";

const DRIVERS_KEY = "drivers";

export const useGetDriversMutation = () => {
  const queryClient = useQueryClient();
  return useMutation<Response, Error, DriverType>({
    mutationFn: (variables) =>
      fetch(`${HOST_URL}/drivers/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(variables),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [DRIVERS_KEY] });
    },
  });
};

export const useGetDrivers = () =>
  useQuery<DriverType, Error, DriverType[]>({
    queryKey: [DRIVERS_KEY],
    queryFn: () =>
      fetch(`${HOST_URL}/drivers`).then((response) => response.json()),
  });
