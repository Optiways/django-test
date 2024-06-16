import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import BusShiftList from './components/BusShiftList';
import BusShiftCreate from './components/BusShiftCreate';
import BusStopList from './components/BusStopList';
import BusStopCreate from './components/BusStopCreate';

const AppRouter = () => {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/bus-shifts">Bus Shifts</Link></li>
            <li><Link to="/create-bus-shift">Create Bus Shift</Link></li>
            <li><Link to="/bus-stops">Bus Stops</Link></li>
            <li><Link to="/create-bus-stop">Create Bus Stop</Link></li>
          </ul>
        </nav>
        <Routes>
            <Route path="/bus-shifts" element={<BusShiftList />} />
            <Route path="/create-bus-shift" element={<BusShiftCreate />} />
            <Route path="/bus-stops" element={<BusStopList />} />
            <Route path="/create-bus-stop" element={<BusStopCreate />} />
        </Routes>
      </div>
    </Router>
  );
};

export default AppRouter;
