import React from 'react';
import logo from './logo.svg';
import './App.css';
import data from '../../myapp/data/doodle.png';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        
      </header>

      <img src={data} alt="Image of data from S3"/>
    </div>
  );
}

export default App;
