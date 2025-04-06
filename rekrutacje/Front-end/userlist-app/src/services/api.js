import axios from 'axios';

const API_URL = 'https://jsonplaceholder.typicode.com';

const api = {
  getUsers: async () => {
    try {
      const response = await axios.get(`${API_URL}/users`);
      return response.data;
    } catch (error) {
      console.error('Błąd podczas pobierania użytkowników:', error);
      throw error;
    }
  }
};

export default api; 