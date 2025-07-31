import React, { createContext, useContext, useReducer } from 'react';

const ChatContext = createContext();

const initialState = {
  messages: [],
  input: '',
  loading: false
};

const chatReducer = (state, action) => {
  switch (action.type) {
    case 'SEND_MESSAGE':
      return {
        ...state,
        messages: [...state.messages, {
          id: Date.now(),
          sender: 'user',
          content: action.payload,
          timestamp: new Date()
        }],
        input: '',
        loading: true
      };
    case 'RECEIVE_MESSAGE':
      return {
        ...state,
        messages: [...state.messages, {
          id: Date.now(),
          sender: 'bot',
          content: action.payload,
          timestamp: new Date()
        }],
        loading: false
      };
    case 'SET_INPUT':
      return {
        ...state,
        input: action.payload
      };
    case 'LOAD_CONVERSATION':
      return {
        ...state,
        messages: action.payload,
        loading: false
      };
    case 'CLEAR_CONVERSATION':
      return {
        ...state,
        messages: [],
        input: '',
        loading: false
      };
    default:
      return state;
  }
};

export const ChatProvider = ({ children }) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  return (
    <ChatContext.Provider value={{ state, dispatch }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
}; 