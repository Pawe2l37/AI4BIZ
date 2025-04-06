import React, { useState, useEffect } from 'react';
import UserCard from './UserCard';
import SearchBar from './SearchBar';
import api from '../services/api';

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setLoading(true);
        const data = await api.getUsers();
        setUsers(data);
        setFilteredUsers(data);
        setLoading(false);
      } catch (err) {
        setError('Wystąpił błąd podczas pobierania danych');
        setLoading(false);
        console.error(err);
      }
    };

    fetchUsers();
  }, []);

  useEffect(() => {
    const filtered = users.filter(
      (user) =>
        user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        user.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
        user.email.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredUsers(filtered);
  }, [searchQuery, users]);

  if (loading) {
    return (
      <div className="d-flex justify-content-center my-5">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Ładowanie...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger" role="alert">
        {error}
      </div>
    );
  }

  return (
    <div className="container">
      <SearchBar searchQuery={searchQuery} setSearchQuery={setSearchQuery} />
      
      {filteredUsers.length === 0 ? (
        <div className="alert alert-info">
          Nie znaleziono użytkowników pasujących do kryteriów wyszukiwania
        </div>
      ) : (
        <div className="user-list">
          {filteredUsers.map((user) => (
            <div className="mb-3 w-100" key={user.id}>
              <UserCard user={user} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default UserList; 