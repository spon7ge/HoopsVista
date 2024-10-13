import React from 'react';

interface SearchBarProps {
  searchTerm: string;
  onSearchChange: (term: string) => void;
}

const SearchBar: React.FC<SearchBarProps> = ({ searchTerm, onSearchChange }) => {
  return (
    <input
      type="text"
      placeholder="Search"
      value={searchTerm}
      onChange={(e) => onSearchChange(e.target.value)}
      className="px-3 py-2 rounded-full bg-gray-800 text-white placeholder-gray-400 border border-gray-700 focus:outline-none focus:border-gray-700"
    />
  );
};

export default SearchBar;