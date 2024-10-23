import React, { useState, useEffect } from 'react';
import DocumentSelector from '/Users/mayankjain/Downloads/platformreact/migration-agent-portal/src/pages/AnalyzerFolder/components/DocumentSelector.js';
import AnalyzeButton from '/Users/mayankjain/Downloads/platformreact/migration-agent-portal/src/pages/AnalyzerFolder/components/AnalyzeButton.js';
import OccupationSelector from '/Users/mayankjain/Downloads/platformreact/migration-agent-portal/src/pages/AnalyzerFolder/components/OccupationSelector';
import OccupationDetails from '/Users/mayankjain/Downloads/platformreact/migration-agent-portal/src/pages/AnalyzerFolder/components/OccupationDetails';

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
      console.log('Analysis Result:', data.analysis_result); // Log the result
      setAnalysisResult(data.analysis_result);
    } catch (error) {
      console.error('Error analyzing document:', error);
      alert('Failed to analyze document. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 p-6">
      <div className="max-w-4xl mx-auto">
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-extrabold text-gray-800 mb-2">Document Analyzer</h1>
          <p className="text-lg text-gray-600">Unlock insights from your documents with AI</p>
        </header>

        <div className="bg-white rounded-2xl shadow-xl p-8 space-y-8">
          <DocumentSelector
            documents={documents}
            selectedDocument={selectedDocument}
            onSelectDocument={handleDocumentSelect}
          />

          <AnalyzeButton
            onAnalyze={handleAnalyze}
            isDisabled={!selectedDocument || isAnalyzing}
            isAnalyzing={isAnalyzing}
          />

          {analysisResult && Array.isArray(analysisResult) && analysisResult.length > 0 && (
            <section className="bg-gray-50 p-6 rounded-xl space-y-4">
              <h2 className="text-2xl font-semibold text-gray-800">Analysis Result</h2>
              <OccupationSelector
                occupations={analysisResult}
                selectedOccupation={selectedOccupation}
                onSelectOccupation={setSelectedOccupation}
              />
              {selectedOccupation && <OccupationDetails occupation={selectedOccupation} />}
            </section>
          )}
        </div>
      </div>
    </div>
  );
};

export default Analyzer;