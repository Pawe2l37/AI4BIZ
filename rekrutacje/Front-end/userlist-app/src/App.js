import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import './App.css';
import UserList from './components/UserList';
import PapalModeToggle from './components/PapalModeToggle';
import { ThemeProvider, useTheme } from './context/ThemeContext';

const AppContent = () => {
  const { papalMode } = useTheme();
  
  return (
    <div className={`App ${papalMode ? 'papal-mode' : ''}`}>
      <header className={`${papalMode ? 'bg-warning' : 'bg-primary'} text-${papalMode ? 'dark' : 'white'} text-center py-4 mb-4 position-relative`}>
        <PapalModeToggle />
        <h1>Lista Użytkowników</h1>
        <p>Mini-aplikacja React z wykorzystaniem JSONPlaceholder API</p>
      </header>
      <main className="container">
        <UserList />
      </main>
      <footer className={`text-center py-3 mt-5 ${papalMode ? 'bg-warning-subtle' : 'bg-light'}`}>
        <p>© 2025 Lista Użytkowników</p>
      </footer>
    </div>
  );
};

function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  );
}

export default App;
