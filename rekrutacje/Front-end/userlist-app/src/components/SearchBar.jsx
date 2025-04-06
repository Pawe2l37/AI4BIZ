import React from 'react';
import { useTheme } from '../context/ThemeContext';

const SearchBar = ({ searchQuery, setSearchQuery }) => {
  const { papalMode } = useTheme();
  
  return (
    <div className="mb-4">
      <div className={`input-group ${papalMode ? 'papal-search' : ''}`}>
        <span className={`input-group-text ${papalMode ? 'bg-warning-subtle border-warning' : ''}`}>
          <i className={`bi bi-search ${papalMode ? 'text-warning-emphasis' : ''}`}></i>
        </span>
        <input
          type="text"
          className={`form-control ${papalMode ? 'bg-warning-subtle border-warning' : ''}`}
          placeholder="Wyszukaj użytkownika..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        {searchQuery && (
          <button
            className={`btn ${papalMode ? 'btn-outline-warning' : 'btn-outline-secondary'}`}
            type="button"
            onClick={() => setSearchQuery('')}
          >
            <i className="bi bi-x-circle"></i>
          </button>
        )}
      </div>
    </div>
  );
};

export default SearchBar; 