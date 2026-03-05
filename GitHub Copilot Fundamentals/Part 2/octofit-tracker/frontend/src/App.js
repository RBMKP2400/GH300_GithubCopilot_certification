import React from 'react';
import { HashRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';
import logo from './logo.png';

function Home() {
  return (
    <div className="container mt-5 text-center">
      <img src={logo} alt="OctoFit Tracker" style={{ maxWidth: '200px' }} className="mb-4" />
      <h1 className="display-4">🏋️ OctoFit Tracker</h1>
      <p className="lead text-muted">
        Track your fitness goals, compete with teammates, and become a superhero! 💪
      </p>
      <div className="row mt-4">
        {[
          { to: '/users', icon: '👥', label: 'Users', color: 'primary' },
          { to: '/teams', icon: '🦸', label: 'Teams', color: 'success' },
          { to: '/activities', icon: '��️', label: 'Activities', color: 'info' },
          { to: '/leaderboard', icon: '🏆', label: 'Leaderboard', color: 'warning' },
          { to: '/workouts', icon: '💪', label: 'Workouts', color: 'danger' },
        ].map(item => (
          <div key={item.to} className="col-md-4 mb-3">
            <NavLink to={item.to} className={`btn btn-outline-${item.color} btn-lg w-100`}>
              {item.icon} {item.label}
            </NavLink>
          </div>
        ))}
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <NavLink className="navbar-brand" to="/">
            🏋️ OctoFit Tracker
          </NavLink>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
          >
            <span className="navbar-toggler-icon" />
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              {[
                { to: '/users', label: 'Users' },
                { to: '/teams', label: 'Teams' },
                { to: '/activities', label: 'Activities' },
                { to: '/leaderboard', label: 'Leaderboard' },
                { to: '/workouts', label: 'Workouts' },
              ].map(item => (
                <li key={item.to} className="nav-item">
                  <NavLink
                    className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
                    to={item.to}
                  >
                    {item.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/users" element={<Users />} />
        <Route path="/teams" element={<Teams />} />
        <Route path="/activities" element={<Activities />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/workouts" element={<Workouts />} />
      </Routes>
    </Router>
  );
}

export default App;
