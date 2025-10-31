import React from 'react';
import VehicleList from './VehicleList';
import Chat from './Chat';

export default function App(){
  return (
    <div style={{padding:20,fontFamily:'Arial'}}>
      <h1>Vehicle Maintenance UI (Minimal)</h1>
      <div style={{display:'flex',gap:40}}>
        <div style={{flex:1}}>
          <h2>Vehicles</h2>
          <VehicleList />
        </div>
        <div style={{flex:1}}>
          <h2>AI Chat</h2>
          <Chat />
        </div>
      </div>
    </div>
  );
}
