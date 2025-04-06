import React, { createContext, useState, useContext } from 'react';

const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [papalMode, setPapalMode] = useState(false);

  const togglePapalMode = () => {
    setPapalMode(!papalMode);
  };

  return (
    <ThemeContext.Provider value={{ papalMode, togglePapalMode }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);

export default ThemeContext; 