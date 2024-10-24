import React from 'react';
import SearchBar from './SearchBar';

interface TabsProps {
  selectedTab: string;
  onTabChange: (tab: string) => void;
  searchTerm: string;
  onSearchChange: (term: string) => void;
}

const Tabs: React.FC<TabsProps> = ({ selectedTab, onTabChange, searchTerm, onSearchChange }) => {
  const tabs = [
    "Points",
    "Assists",
    "Rebounds",
    "3-PT Made",
    "Pts+Asts",
    "Pts+Rebs",
    "Rebs+Asts",
    "Pts+Rebs+Asts",
    "Blocked Shots",
    "Steals",
    "Blks+Stls",
    "Turnovers"
  ];

  return (
    <div className="flex justify-between items-center mb-4 overflow-x-auto">
      <div className="flex space-x-2">
        {tabs.map((tab) => (
          <button
            key={tab}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-150 ${
              selectedTab === tab
                ? 'bg-white text-black'
                : 'bg-gray-800 text-white hover:bg-gray-700'
            }`}
            onClick={() => onTabChange(tab)}
          >
            {tab}
          </button>
        ))}
      </div>
      <div className="ml-4 flex-shrink-0">
        <SearchBar searchTerm={searchTerm} onSearchChange={onSearchChange} />
      </div>
    </div>
  );
};

export default Tabs;