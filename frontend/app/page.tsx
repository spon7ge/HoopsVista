"use client";

import React, { useState, useEffect } from 'react';
import Tabs from './components/Tabs';
import PlayersDisplay from './components/PlayersDisplay';
import { fetchProps } from './services/api';

interface Prop {
  name: string;
  type: string;
  line: number;
  odds: number;
}

export default function Home() {
  const [selectedTab, setSelectedTab] = useState('Points');
  const [searchTerm, setSearchTerm] = useState('');
  const [props, setProps] = useState<Record<string, Prop[]>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadProps = async () => {
      try {
        setIsLoading(true);
        console.log('Fetching props...');
        const data = await fetchProps();
        console.log('Fetched props:', data);
        setProps(data);
        setError(null);
      } catch (error) {
        console.error('Error fetching props:', error);
        setError('Failed to load data. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };

    loadProps();
  }, []);



  const filteredProps = props[selectedTab]?.filter(prop => 
    prop.name.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6 text-white">HoopsVista</h1>
        <Tabs 
          selectedTab={selectedTab} 
          onTabChange={setSelectedTab}
          searchTerm={searchTerm}
          onSearchChange={setSearchTerm}
        />
        <hr className="border-t border-white-300 my-4 w-full" />
        <div className="mt-4">
          {isLoading ? (
            <p>Loading...</p>
          ) : error ? (
            <p className="text-red-500">{error}</p>
          ) : (
            <PlayersDisplay players={filteredProps} />
          )}
        </div>
      </div>
    </div>
  );
}
