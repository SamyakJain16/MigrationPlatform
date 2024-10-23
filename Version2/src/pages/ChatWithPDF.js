import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';
import { Document, Page, pdfjs } from 'react-pdf';
import { useChat } from '../ChatContext';
import { debounce } from 'lodash'; // Make sure to install lodash if not already present


pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

const API_BASE_URL = 'http://localhost:8000';
const AGENT_ID = 'fixed_agent'; // You can change this or make it dynamic based on your needs
const STORAGE_KEY = 'pdfChats';



const ChatWithPDF = () => {
  const { pdfChats, setPdfChats } = useChat();
  const [pdfs, setPdfs] = useState([]);
  const [selectedPDF, setSelectedPDF] = useState(null);
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [scale, setScale] = useState(1.0);
  const [pdfError, setPdfError] = useState(null);
  const [currentMessage, setCurrentMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isMounted, setIsMounted] = useState(true);
  const abortControllerRef = useRef(null);


  useEffect(() => {
    console.log("Component mounted");
    setIsMounted(true);
    fetchPDFs();
    loadChatsFromStorage();

    return () => {
      console.log("Component unmounting");
      setIsMounted(false);
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      saveChatsToStorage();
    };
  }, []);

  useEffect(() => {
    // Save chats to storage whenever they change
    saveChatsToStorage();
  }, [pdfChats]);

  const loadChatsFromStorage = () => {
    const storedChats = localStorage.getItem(STORAGE_KEY);
    if (storedChats) {
      setPdfChats(JSON.parse(storedChats));
    }
  };

  const saveChatsToStorage = () => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(pdfChats));
    } catch (error) {
      console.error('Failed to save chats to local storage:', error);
      // Optionally, notify the user
    }
  };

  const fetchPDFs = async () => {
    console.log("Fetching PDFs");
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    abortControllerRef.current = new AbortController();

    try {
      const response = await axios.get(`${API_BASE_URL}/pdfs/${AGENT_ID}`, {
        signal: abortControllerRef.current.signal
      });
      console.log("Fetched PDFs:", response.data);
      if (isMounted) {
        console.log("Setting PDFs state");
        setPdfs(response.data);
      } else {
        console.log("Component unmounted, not setting state");
      }
    } catch (error) {
      if (axios.isCancel(error)) {
        console.log("Request was cancelled");
      } else {
        console.error('Error fetching PDFs:', error);
      }
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    try {
      setIsLoading(true);
      await axios.post(`${API_BASE_URL}/upload-pdf/${AGENT_ID}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      fetchPDFs();
    } catch (error) {
      console.error('Error uploading PDF:', error);
      alert(`Failed to upload PDF: ${error.response ? error.response.data.detail : error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePDFSelection = useCallback(
    debounce((pdfId) => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      setSelectedPDF(pdfId);
      setPageNumber(1);
      setPdfError(null);
    }, 300),
    []
  );

  const handleDeletePDF = async (pdfId) => {
    if (!window.confirm("Are you sure you want to delete this PDF?")) {
      return;
    }
    try {
      await axios.delete(`${API_BASE_URL}/pdfs/${AGENT_ID}/${pdfId}`);
      fetchPDFs();
      if (selectedPDF === pdfId) {
        setSelectedPDF(null);
        setNumPages(null);
        setPageNumber(1);
        setPdfError(null);
      }
    } catch (error) {
      console.error('Error deleting PDF:', error);
      alert("Failed to delete PDF");
    }
  };

  const handleSendMessage = async () => {
    if (currentMessage.trim() && selectedPDF) {
      setIsLoading(true);
      const newUserMessage = { id: Date.now(), sender: 'user', content: currentMessage };
      
      setPdfChats(prevChats => {
        const updatedChats = {
          ...prevChats,
          [selectedPDF]: [...(prevChats[selectedPDF] || []), newUserMessage]
        };
        saveChatsToStorage();
        return updatedChats;
      });

      try {
        if (abortControllerRef.current) {
          abortControllerRef.current.abort();
        }
        abortControllerRef.current = new AbortController();
        
        const response = await axios.post(
          `${API_BASE_URL}/query-pdf`,
          {
            query: currentMessage,
            pdf_id: selectedPDF,
            context: pdfChats[selectedPDF]?.slice(-5).map(msg => msg.content) || []
          },
          { signal: abortControllerRef.current.signal }
        );

        if (isMounted) {
          const newAIMessage = { id: Date.now(), sender: 'AI', content: response.data.answer };
          setPdfChats(prevChats => {
            const updatedChats = {
              ...prevChats,
              [selectedPDF]: [...(prevChats[selectedPDF] || []), newAIMessage]
            };
            saveChatsToStorage();
            return updatedChats;
          });
        }
      } catch (error) {
        if (axios.isCancel(error)) {
          console.log('Request was aborted');
        } else {
          console.error('Error querying PDF:', error);
          if (isMounted) {
            const errorMessage = { id: Date.now(), sender: 'AI', content: 'Sorry, I encountered an error while processing your request.' };
            setPdfChats(prevChats => ({
              ...prevChats,
              [selectedPDF]: [...(prevChats[selectedPDF] || []), errorMessage]
            }));
          }
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
          setCurrentMessage('');
        }
      }
    }
  };

  // New: Function to download chat history
  const downloadChats = () => {
    if (!selectedPDF) return;
    
    const chats = pdfChats[selectedPDF];
    const chatText = chats.map(msg => `${msg.sender}: ${msg.content}`).join('\n');
    const blob = new Blob([chatText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat_${selectedPDF}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const clearSelectedPDFChat = useCallback(() => {
    if (selectedPDF) {
      if (window.confirm("Are you sure you want to clear the chat history for this PDF?")) {
        try {
          setPdfChats(prevChats => {
            const newChats = { ...prevChats };
            delete newChats[selectedPDF];
            return newChats;
          });
          console.log(`Chat history cleared for PDF: ${selectedPDF}`);
        } catch (error) {
          console.error(`Error clearing chat history for PDF ${selectedPDF}:`, error);
          alert("An error occurred while clearing the chat history. Please try again.");
        }
      }
    }
  }, [selectedPDF, setPdfChats]);

  return (
    <div className="flex h-screen w-screen bg-gray-100 m-0 p-0 overflow-hidden">
      {/* Sidebar for PDF List */}
      <div className="bg-gray-800 text-white p-3 flex-shrink-0 h-full overflow-y-auto" style={{ width: '20%' }}>
        <div className="mb-4">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
            className="hidden"
            id="pdf-upload"
          />
          <label
            htmlFor="pdf-upload"
            className="w-full bg-blue-500 text-white py-1 rounded text-sm cursor-pointer text-center block"
          >
            Upload PDF
          </label>
        </div>
        <div className="space-y-1">
        <p class="p-2 text-[11px]">Number of PDFs: {pdfs.length}</p>
        {pdfs.length === 0 && <p>No PDFs available</p>}
          {pdfs.map((pdf) => (
            <div
              key={pdf.id}
              className={`p-2 rounded cursor-pointer text-sm flex items-center justify-between ${
                selectedPDF === pdf.id ? 'bg-gray-600' : 'hover:bg-gray-700'
              }`}
              onClick={() => handlePDFSelection(pdf.id)}
            >
              <span className="truncate flex-grow">{pdf.filename}</span>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeletePDF(pdf.id);
                }}
                className="text-red-500 hover:text-red-700 ml-2"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* PDF Viewer Section */}
      <div className="flex flex-col h-full flex-grow overflow-hidden">
        {/* PDF Viewer Header */}
        <div className="bg-gray-100 p-2 flex items-center justify-between border-b border-gray-300">
          <div className="flex items-center">
            <button
              className="text-gray-600 mr-2"
              onClick={() => setPageNumber(Math.max(1, pageNumber - 1))}
              disabled={!selectedPDF || pageNumber <= 1}
            >
              ←
            </button>
            <button
              className="text-gray-600 mr-2"
              onClick={() => setPageNumber(Math.min(numPages || 1, pageNumber + 1))}
              disabled={!selectedPDF || pageNumber >= (numPages || 1)}
            >
              →
            </button>
            <span className="text-sm">
              {selectedPDF ? `${pageNumber} / ${numPages || 1}` : 'No PDF selected'}
            </span>
          </div>
          <div className="flex items-center">
            <button
              className="text-gray-600 mr-2"
              onClick={() => setScale(Math.max(0.5, scale - 0.1))}
              disabled={!selectedPDF}
            >
              -
            </button>
            <button
              className="text-gray-600 mr-2"
              onClick={() => setScale(Math.min(2, scale + 0.1))}
              disabled={!selectedPDF}
            >
              +
            </button>
          </div>
        </div>

        {/* PDF Content */}
        <div className="flex-grow p-4 overflow-auto">
          {selectedPDF ? (
            <Document
              file={`${API_BASE_URL}/pdfs/${AGENT_ID}/${selectedPDF}`}
              onLoadSuccess={({ numPages }) => {
                console.log(`PDF loaded successfully with ${numPages} pages`);
                setNumPages(numPages);
              }}
              onLoadError={(error) => {
                console.error('Error loading PDF:', error);
                setPdfError(`Failed to load PDF: ${error.message}`);
              }}
              loading={<p>Loading PDF...</p>}
            >
              {pdfError ? (
                <p className="text-red-500">{pdfError}</p>
              ) : (
                <Page 
                  pageNumber={pageNumber} 
                  scale={scale}
                  renderTextLayer={false}
                  renderAnnotationLayer={false}
                />
              )}
            </Document>
          ) : (
            <div className="flex items-center justify-center h-full">
              <p className="text-gray-500">Select a PDF to view</p>
            </div>
          )}
        </div>
      </div>

      {/* Chat Interface Section */}
<div className="bg-white border-l border-gray-200 h-full flex flex-col mr-20" style={{ width: '30%' }}>
<div className="flex justify-between items-center mb-0 p-3">
      <h2 className="text-lg font-bold">Chat</h2>
      {selectedPDF && (
        <div className="flex space-x-3 mr-5">
          
        <i 
            className="material-icons cursor-pointer text-gray-500 hover:text-blue-700"
            style={{ fontSize: '24px' }}
            onClick={clearSelectedPDFChat}
            title="Clear chat"
          >
            restart_alt
          </i>
          
          <i 
            className="material-icons cursor-pointer text-gray-500 hover:text-blue-700"
            style={{ fontSize: '24px' }}
            onClick={downloadChats}
            title="Download chat"
          >
            download
          </i>
          
        </div>
      )}
    </div>
  <div className="flex-grow overflow-y-auto mb-3 bg-gray-50 p-3 rounded shadow-inner">
    {selectedPDF && pdfChats[selectedPDF]?.map((message) => (
      <div
        key={message.id}
        className={`mb-2 p-2 rounded ${
          message.sender === 'user' ? 'bg-blue-100 text-right' : 'bg-gray-200'
        }`}
      >
        <span className="font-bold">{message.sender === 'user' ? 'You' : 'AI'}:</span> {message.content}
      </div>
    ))}
    {isLoading && <div className="text-gray-500">AI is thinking...</div>}
  </div>
  <div className="p-3 border-t border-gray-300 flex items-center" style={{ minHeight: '60px' }}>
    <input
      type="text"
      className="flex-grow border rounded-l px-2 py-1 text-sm"
      placeholder="Ask a question..."
      value={currentMessage}
      onChange={(e) => setCurrentMessage(e.target.value)}
      disabled={!selectedPDF || isLoading}
    />
    <button
      className="bg-blue-500 text-white px-4 py-1 rounded-r text-sm"
      onClick={handleSendMessage}
      disabled={!selectedPDF || !currentMessage.trim() || isLoading}
    >
      Send
    </button>
  </div>
</div>

    </div>
  );
  };

export default ChatWithPDF;