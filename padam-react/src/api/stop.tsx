import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { StopType } from "../types/StopType";
import { HOST_URL } from "./constants";

const STOPS_KEY = "stops";

export const useGetStopMutation = () => {
  const queryClient = useQueryClient();
  return useMutation<Response, Error, StopType>({
    mutationFn: (variables) =>
      fetch(`${HOST_URL}/stops/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(variables),
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [STOPS_KEY] });
    },
  });
};

export const useGetStops = () =>
  useQuery<StopType, Error, StopType[]>({
    queryKey: [STOPS_KEY],
    queryFn: () =>
      fetch(`${HOST_URL}/stops`).then((response) => response.json()),
  });
