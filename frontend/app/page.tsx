import React, { useState, useEffect } from 'react';
import Tabs from './components/Tabs';
import SearchBar from './components/SearchBar';
import PredictionsDisplay from './components/PredictionsDisplay';

// Mock data
const mockPredictions = [
  {
    id: '1',
    playerName: 'LeBron James',
    prop: 'Points',
    propLine: 25.5,
    predictedProbability: 0.65,
  },
  {
    id: '2',
    playerName: 'Stephen Curry',
    playerImage: 'Points',
    propLine: 28.5,
    predictedProbability: 0.58,
  },
  {
    id: '3',
    playerName: 'Kevin Durant',
    playerImage: 'Points',
    propLine: 27.5,
    predictedProbability: 0.62,
  },
  // Add more mock predictions as needed
];

export default function Home() {
  const [selectedTab, setSelectedTab] = useState('Points');
  const [searchTerm, setSearchTerm] = useState('');
  const [predictions, setPredictions] = useState(mockPredictions);

  // Simulate filtering based on search term
  useEffect(() => {
    const filteredPredictions = mockPredictions.filter(pred => 
      pred.playerName.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setPredictions(filteredPredictions);
  }, [searchTerm]);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">NBA Prop Predictions</h1>
      <SearchBar searchTerm={searchTerm} onSearchChange={setSearchTerm} />
      <Tabs selectedTab={selectedTab} onTabChange={setSelectedTab} />
      <PredictionsDisplay predictions={predictions} />
    </div>
  );
}