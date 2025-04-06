import React from 'react';
import { useTheme } from '../context/ThemeContext';

const PapalModeToggle = () => {
  const { papalMode, togglePapalMode } = useTheme();

  return (
    <button 
      className={`btn ${papalMode ? 'btn-light' : 'btn-warning'} position-absolute top-0 end-0 m-3`}
      onClick={togglePapalMode}
    >
      {papalMode ? 'Tryb normalny' : 'Tryb papieski'}
    </button>
  );
};

export default PapalModeToggle; 