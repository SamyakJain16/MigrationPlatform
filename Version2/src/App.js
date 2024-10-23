// src/App.js
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Layout from './components/Layout';
import { ChatProvider } from './ChatContext';

function App() {
  return (
    <ChatProvider>
      <Router>
        <Layout />
      </Router>
    </ChatProvider>
  );
}

export default App;