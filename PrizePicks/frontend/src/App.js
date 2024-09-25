// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;
// src/App.js

import React, { useState } from 'react';
import Tabs from './components/Tabs';
import SearchBar from './components/SearchBar';
import PredictionsDisplay from './components/PredictionsDisplay';

function App() {
  const tabs = ['Points', 'Assists', 'Rebounds'];
  const [selectedTab, setSelectedTab] = useState(tabs[0]);
  const [searchQuery, setSearchQuery] = useState('');
  const [predictions, setPredictions] = useState([
    // Your predictions data here
  ]);

  const handleTabSelect = (tab) => {
    setSelectedTab(tab);
    // Add logic to update predictions based on the selected tab
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
    // Add logic to filter predictions based on the search query
  };

  // Filter predictions based on search query and selected tab
  const filteredPredictions = predictions.filter((prediction) => {
    const matchesSearch = prediction.name
      .toLowerCase()
      .includes(searchQuery.toLowerCase());
    const matchesTab = prediction.propType === selectedTab;
    return matchesSearch && matchesTab;
  });

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center">
        <Tabs tabs={tabs} onTabSelect={handleTabSelect} />
        <SearchBar onSearch={handleSearch} />
      </div>
      <PredictionsDisplay predictions={filteredPredictions} />
    </div>
  );
}

export default App;

