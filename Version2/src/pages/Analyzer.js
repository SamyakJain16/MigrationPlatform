import React, { useState, useEffect } from 'react';

const Analyzer = () => {
  const [documents, setDocuments] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [selectedOccupation, setSelectedOccupation] = useState(null);


  
  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await fetch('http://localhost:8000/documents/');
      if (!response.ok) throw new Error('Failed to fetch documents');
      const data = await response.json();
      setDocuments(data);
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  const handleDocumentSelect = (documentId) => {
    setSelectedDocument(documentId);
    setAnalysisResult(null);
    setSelectedOccupation(null);
  };

  const handleAnalyze = async () => {
    if (!selectedDocument) {
      alert('Please select a document to analyze.');
      return;
    }

    setIsAnalyzing(true);
    try {
      const response = await fetch('http://localhost:8000/analyze-document', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ document_id: selectedDocument }),
      });
      if (!response.ok) {
        throw new Error('Failed to analyze document');
      }
      const data = await response.json();
      setAnalysisResult(data.analysis_result);
    } catch (error) {
      console.error('Error analyzing document:', error);
      alert('Failed to analyze document. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const renderOccupationDetails = (occupation) => {
    return (
      <div className="bg-white shadow-lg rounded-lg overflow-hidden">
        <div className="bg-blue-600 text-white p-6">
          <h3 className="text-2xl font-bold">{occupation['Occupation Name']}</h3>
          <p className="text-sm mt-2">Occupation ID: {occupation['occupation_id']} | ANZSCO Code: {occupation['ANZSCO Code']}</p>
        </div>
        
        <div className="p-6 space-y-6">
          <div>
            <h4 className="text-lg font-semibold text-gray-700 mb-2">Occupation Details</h4>
            <p className="text-gray-600"><span className="font-medium">Caveats:</span> {occupation['Caveats'] || 'None'}</p>
            <p className="text-gray-600"><span className="font-medium">Assessing Authority:</span> {occupation['Assessing Authority']}</p>
          </div>
  
          <div>
            <h4 className="text-lg font-semibold text-gray-700 mb-2">Australian Government Migration Lists</h4>
            <div className="flex flex-wrap gap-2">
              {Object.entries(occupation['Australian Government Migration Lists'])
                .filter(([_, value]) => value === "1")
                .map(([key, _]) => (
                  <span key={key} className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                    {key}
                  </span>
                ))}
            </div>
          </div>
  
          <div>
            <h4 className="text-lg font-semibold text-gray-700 mb-2">Visa Type Availability</h4>
            <div className="flex flex-wrap gap-2">
              {Object.entries(occupation['Visa Type'])
                .filter(([_, value]) => value === "1")
                .map(([key, _]) => (
                  <span key={key} className="bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
                    {key}
                  </span>
                ))}
            </div>
          </div>

          <div>
      <h4 className="text-lg font-semibold text-gray-700 mb-2">State and Subregion Visa Availability</h4>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Object.entries(occupation['States']).map(([state, details], index) => (
          <div key={state} className={`${pastelColors[index % pastelColors.length]} p-4 rounded-md`}>
            <h5 className="font-semibold text-gray-700 mb-2">{state}</h5>
            <ul className="space-y-1">
              {Object.entries(details).map(([key, value]) => {
                if (typeof value === 'object') {
                  return (
                    <li key={`${state}-${key}`} className="ml-4">
                      <span className="font-medium">{key}</span>
                      <ul className="ml-4 mt-1">
                        {Object.entries(value)
                          .filter(([_, subValue]) => subValue === "1")
                          .map(([subKey, _]) => (
                            <li key={`${state}-${key}-${subKey}`} className="text-sm text-gray-600">
                              {subKey}
                            </li>
                          ))}
                      </ul>
                    </li>
                  );
                } else if (value === "1") {
                  return <li key={`${state}-${key}`} className="text-sm text-gray-600">{key}</li>;
                }
                return null;
              })}
            </ul>
          </div>
        ))}
      </div>
    </div>
                    

        </div>
      </div>
    );
  };


const pastelColors = [
    'bg-red-100',
    'bg-yellow-100',
    'bg-green-100',
    'bg-blue-100',
    'bg-indigo-100',
    'bg-purple-100',
    'bg-pink-100',
    'bg-orange-100',
    'bg-teal-100',
    'bg-cyan-100',
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-extrabold text-gray-800 mb-2">Document Analyzer</h1>
          <p className="text-lg text-gray-600">Unlock insights from your documents with AI</p>
        </header>
  
        {/* Main content area */}
        <div className="bg-white rounded-2xl shadow-xl p-8 space-y-8">
          {/* Document selection section */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Select a Document</h2>
            <div className="grid gap-4 sm:grid-cols-2">
              {documents.map(doc => (
                <div 
                  key={doc.id} 
                  className={` p-4 rounded-lg cursor-pointer transition-all duration-200 ${
                    selectedDocument === doc.id 
                      ? 'bg-blue-50 border-2 border-blue-500 shadow-md' 
                      : 'bg-gray-50 border border-gray-200 hover:border-blue-300 hover:shadow'
                  }`}
                  onClick={() => handleDocumentSelect(doc.id)}
                >
                  <p className="font-medium text-gray-800">{doc.filename}</p>
                  <p className="text-sm text-gray-500 mt-1">{new Date(doc.upload_date).toLocaleDateString()}</p>
                </div>
              ))}
            </div>
          </section>
  
          {/* Analyze button */}
          <section className="text-center">
            <button
              onClick={handleAnalyze}
              disabled={!selectedDocument || isAnalyzing}
              className={`px-8 py-3 rounded-full text-xs font-medium transition-all duration-200 ${
                !selectedDocument || isAnalyzing
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700 hover:shadow-lg transform hover:-translate-y-0.5'
              }`}
            >
              {isAnalyzing ? 'Analyzing...' : 'Analyze Document'}
            </button>
          </section>
  
          {/* Analysis result section */}
          {analysisResult && (
            <section className="bg-gray-50 p-6 rounded-xl space-y-4">
              <h2 className="text-2xl font-semibold text-gray-800">Analysis Result</h2>
              <select
                className="w-full p-3 border border-gray-300 rounded-lg bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
                onChange={(e) => setSelectedOccupation(analysisResult[parseInt(e.target.value)])}
                value={selectedOccupation ? analysisResult.indexOf(selectedOccupation) : ''}
              >
                <option value="">Select an occupation</option>
                {analysisResult.map((occupation, index) => (
                  <option key={index} value={index}>
                    {occupation['Occupation Name']}
                  </option>
                ))}
              </select>
              {selectedOccupation && renderOccupationDetails(selectedOccupation)}
            </section>
          )}
        </div>
      </div>
    </div>
  );
};
export default Analyzer;