import React, { useEffect, useState } from 'react';

// Use environment variable for backend API URL
const API = process.env.REACT_APP_API_URL;

export default function VehicleList() {
  const [vehicles, setVehicles] = useState([]);

  useEffect(() => { fetchVehicles(); }, []);

  async function fetchVehicles() {
    try {
      const r = await fetch(API + '/vehicles/');
      const data = await r.json();
      setVehicles(data);
    } catch (e) {
      console.error(e);
    }
  }

  return (
    <div>
      <button onClick={fetchVehicles}>Refresh</button>
      <ul>
        {vehicles.map(v => 
          <li key={v.id}>
            {v.vin} — {v.make} {v.model} ({v.year})
          </li>
        )}
      </ul>
    </div>
  );
}
