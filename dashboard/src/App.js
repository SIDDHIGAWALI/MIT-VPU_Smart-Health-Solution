import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [stats, setStats] = useState({});
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch data from your FastAPI backend
    Promise.all([
      fetch('http://127.0.0.1:8000/dashboard-stats'),
      fetch('http://127.0.0.1:8000/hospitals')
    ])
      .then(([statsRes, hospitalsRes] ) => Promise.all([statsRes.json(), hospitalsRes.json()]))
      .then(([statsData, hospitalsData]) => {
        setStats(statsData);
        setHospitals(hospitalsData);
        setLoading(false);
      })
      .catch(err => {
        console.error('API Error:', err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="loading">Loading dashboard...</div>;

  return (
    <div className="App">
      <header>
        <h1>🩺 Smart Health Solapur</h1>
        <p>Solapur Municipal Corporation - Real-time Monitoring</p>
      </header>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Cases</h3>
          <div className="stat-number">{stats.total_cases?.toLocaleString() || 0}</div>
        </div>
        <div className="stat-card">
          <h3>Available Beds</h3>
          <div className="stat-number">{stats.available_beds || 0}</div>
        </div>
        <div className="stat-card">
          <h3>High Risk Wards</h3>
          <div className="stat-number">{stats.high_risk_wards?.length || 0}</div>
        </div>
      </div>

      {/* Hospitals List */}
      <div className="hospitals-section">
        <h2>🏥 Hospitals Status</h2>
        <div className="hospitals-grid">
          {hospitals.map(hospital => (
            <div key={hospital.hospital} className="hospital-card">
              <h4>{hospital.hospital}</h4>
              <div className="bed-info">
                <span className="available">{hospital.available_beds}</span>
                <span className="total">/{hospital.total_beds} beds</span>
              </div>
              <div className="ward">{hospital.ward}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
