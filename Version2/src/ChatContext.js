// src/ChatContext.js
import React, { createContext, useState, useContext } from 'react';

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [pdfChats, setPdfChats] = useState({});

  return (
    <ChatContext.Provider value={{ pdfChats, setPdfChats }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => useContext(ChatContext);