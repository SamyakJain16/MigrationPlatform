import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Documents() {
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await axios.get('http://localhost:8000/documents/');
      setDocuments(response.data);
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:8000/documents/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      fetchDocuments(); // Refresh the list after upload
    } catch (error) {
      console.error('Error uploading document:', error);
      alert(`Failed to upload document: ${error.response ? error.response.data.detail : error.message}`);
    }
  };

  const handleDeleteDocument = async (documentId) => {
    if (!window.confirm("Are you sure you want to delete this document?")) {
      return;
    }
    try {
      await axios.delete(`http://localhost:8000/documents/${documentId}`);
      fetchDocuments(); // Refresh the list after deletion
    } catch (error) {
      console.error('Error deleting document:', error);
      alert("Failed to delete document");
    }
  };

  return (
    <div className="text-premium-gold-light">
      <h1 className="text-3xl font-bold mb-6 text-premium-gold">Documents</h1>
      <div className="mb-4">
        <input
          type="file"
          onChange={handleFileUpload}
          className="hidden"
          id="document-upload"
        />
        <label
          htmlFor="document-upload"
          className="bg-premium-gold text-premium-black px-4 py-2 rounded cursor-pointer"
        >
          Upload Document
        </label>
      </div>
      <table className="w-full">
        <thead>
          <tr className="bg-premium-gold-dark text-premium-black">
            <th className="p-2 text-left">Name</th>
            <th className="p-2 text-left">Size</th>
            <th className="p-2 text-left">Date</th>
            <th className="p-2 text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          {documents.map(doc => (
            <tr key={doc.id} className="border-b border-premium-gold-dark">
              <td className="p-2">{doc.filename}</td>
              <td className="p-2">{doc.size} bytes</td>
              <td className="p-2">{new Date(doc.upload_date).toLocaleDateString()}</td>
              <td className="p-2">
                <button
                  onClick={() => handleDeleteDocument(doc.id)}
                  className="bg-red-500 text-white px-2 py-1 rounded"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Documents;