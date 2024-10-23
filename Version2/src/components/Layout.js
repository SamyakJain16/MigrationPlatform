import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Sidebar from './Sidebar';
import Dashboard from '../pages/Dashboard';
import Clients from '../pages/Clients';
import Documents from '../pages/Documents';
import ChatWithPDF from '../pages/ChatWithPDF';  // Update this line
import Analyzer from '../pages/Analyzer';

// Placeholder components
const Reports = () => <div>Reports Page</div>;
const Settings = () => <div>Settings Page</div>;

function Layout() {
  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <main className="flex-1 overflow-x-hidden overflow-y-auto p-6">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/clients/*" element={<Clients />} />
          <Route path="/documents/*" element={<Documents />} />
          <Route path="/chat-with-pdf" element={<ChatWithPDF />} />  // Add this line
          <Route path="/reports" element={<Reports />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/analyzer" element={<Analyzer />} />

<Route path="*" element={<div>Page Not Found</div>} />
        </Routes>
      </main>
    </div>
  );
}

export default Layout;