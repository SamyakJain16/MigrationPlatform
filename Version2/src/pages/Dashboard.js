import React from 'react';
import { Link } from 'react-router-dom';

function Dashboard() {
  return (
    <div className="bg-gray-100">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <Link to="/chat-with-pdf" className="bg-white p-4 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
          <h2 className="text-xl font-semibold mb-2 text-blue-600">Chat with PDF</h2>
          <p className="text-gray-600">Interact with PDF documents using AI.</p>
        </Link>
        <div className="bg-white p-4 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2 text-green-600">Summarize</h2>
          <p className="text-gray-600">Get quick summaries of your documents.</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-2 text-purple-600">Translate</h2>
          <p className="text-gray-600">Translate documents to different languages.</p>
        </div>
      </div>
      <div className="bg-white p-4 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4 text-red-600">Recent Activities</h2>
        <ul className="list-disc pl-5 text-gray-600 space-y-2">
          <li>New client application received</li>
          <li>Document translated for Client A</li>
          <li>Appointment scheduled with Client B</li>
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;