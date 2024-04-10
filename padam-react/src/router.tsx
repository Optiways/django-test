import * as React from "react";
import { createBrowserRouter } from "react-router-dom";

import { BusList } from "./views/BusList";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <BusList />,
  },
]);
