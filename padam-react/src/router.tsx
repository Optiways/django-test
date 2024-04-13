import * as React from "react";
import { createBrowserRouter } from "react-router-dom";

import { BusList } from "./views/BusList";
import { BusShiftList } from "./views/BusShiftList";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <BusList />,
  },
  {
    path: "/bus-shift/",
    element: <BusShiftList />,
  },
]);
