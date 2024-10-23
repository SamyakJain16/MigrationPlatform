// src/services/api.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/api'; // Replace with your actual API URL

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getClients = () => api.get('/clients');
export const getRecentActivity = () => api.get('/recent-activity');

export default api;