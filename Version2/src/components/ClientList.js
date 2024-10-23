// src/components/ClientList.js
import React, { useState, useEffect } from 'react';
import { getClients } from '../services/api';

function ClientList() {
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getClients()
      .then(response => {
        setClients(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching clients:', error);
        setError('Failed to fetch clients');
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading clients...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <h3 className="text-xl font-semibold mb-4">Recent Clients</h3>
      <ul>
        {clients.map((client) => (
          <li key={client.id} className="mb-2 p-2 hover:bg-gray-100 rounded">
            <span className="font-medium">{client.name}</span>
            <span className="ml-2 text-sm text-gray-500">{client.status}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ClientList;