import React from 'react';
import { useTheme } from '../context/ThemeContext';

const UserCard = ({ user }) => {
  const { papalMode } = useTheme();
  
  return (
    <div className={`card ${papalMode ? 'card-papal' : ''}`}>
      <div className="card-body">
        <h5 className="card-title">{user.name}</h5>
        <h6 className="card-subtitle mb-2 text-muted">@{user.username}</h6>
        <div className="card-text">
          <p>
            <i className={`bi bi-envelope ${papalMode ? 'text-warning' : ''}`}></i> {user.email}
          </p>
          <p>
            <i className={`bi bi-telephone ${papalMode ? 'text-warning' : ''}`}></i> {user.phone}
          </p>
          <p>
            <i className={`bi bi-globe ${papalMode ? 'text-warning' : ''}`}></i> {user.website}
          </p>
          <p>
            <i className={`bi bi-building ${papalMode ? 'text-warning' : ''}`}></i> {user.company.name}
          </p>
        </div>
      </div>
    </div>
  );
};

export default UserCard; 