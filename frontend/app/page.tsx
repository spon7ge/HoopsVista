"use client";

import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import Tabs from './components/Tabs';
import PredictionsDisplay from './components/PredictionsDisplay';

// Mock data
const mockPredictions = [
  {
    id: '1',
    imageUrl: '/lebron.png',
    playerName: 'LeBron James',
    prop: 'Points',
    propLine: 25.5,
    predictedProbability: 0.65,
  },
  {
    id: '2',
    playerName: 'Stephen Curry',
    prop: 'Points',
    propLine: 28.5,
    predictedProbability: 0.58,
  },
  {
    id: '3',
    playerName: 'Kevin Durant',
    prop: 'Points',
    propLine: 27.5,
    predictedProbability: 0.62,
  },
  {
    id: '4',
    playerName: 'Nikola Jokic',
    prop: 'Assists',
    propLine: 9.5,
    predictedProbability: 0.70,
  },
  {
    id: '5',
    playerName: 'Giannis Antetokounmpo',
    prop: 'Rebounds',
    propLine: 12.5,
    predictedProbability: 0.68,
  },  {
    id: '6',
    playerName: 'LeBron James',
    prop: 'Assists',
    propLine: 5.5,
    predictedProbability: 0.65,
  },  {
    id: '7',
    playerName: 'Luka Doncic',
    prop: 'Points',
    propLine: 35.5,
    predictedProbability: 0.65,
  }
  // Add more mock predictions with different props
];

export default function Home() {
  const [selectedTab, setSelectedTab] = useState('Points');
  const [searchTerm, setSearchTerm] = useState('');

  // Use useMemo to filter predictions
  const filteredPredictions = useMemo(() => {
    return mockPredictions.filter(pred => 
      pred.prop === selectedTab && 
      pred.playerName.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [searchTerm, selectedTab]);

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6 text-white">NBA Prop Predictions</h1>
        <Tabs 
          selectedTab={selectedTab} 
          onTabChange={setSelectedTab}
          searchTerm={searchTerm}
          onSearchChange={setSearchTerm}
        />
        <div className="mt-4">
          <PredictionsDisplay predictions={filteredPredictions} />
        </div>
      </div>
    </div>
  );
}