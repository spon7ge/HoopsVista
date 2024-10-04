import React from 'react';

interface TabsProps {
  selectedTab: string;
  onTabChange: (tab: string) => void;
}

const Tabs: React.FC<TabsProps> = ({ selectedTab, onTabChange }) => {
  const tabs = [
    "Points",
    "Assists",
    "Rebounds",
    "3 Points Made",
    "Points + Assists",
    "Points + Rebounds",
    "Assists + Rebounds",
    "Points + Assists + Rebounds"
  ];

  return (
    <div className="flex space-x-2 mb-4 overflow-x-auto">
      {tabs.map((tab) => (
        <button
          key={tab}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-150 ${
            selectedTab === tab
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
          onClick={() => onTabChange(tab)}
        >
          {tab}
        </button>
      ))}
    </div>
  );
};

export default Tabs;