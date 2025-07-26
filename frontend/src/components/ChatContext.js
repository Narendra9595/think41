import React, { createContext, useContext, useReducer } from "react";

const ChatContext = createContext();

const initialState = {
  messages: [
    { id: 1, sender: "user", content: "Hello AI!" },
    { id: 2, sender: "ai", content: "Hello! How can I help you today?" }
  ],
  loading: false,
  input: ""
};

function chatReducer(state, action) {
  switch (action.type) {
    case "SEND_MESSAGE":
      return {
        ...state,
        messages: [
          ...state.messages,
          { id: state.messages.length + 1, sender: "user", content: action.payload }
        ],
        loading: true,
        input: ""
      };
    case "RECEIVE_MESSAGE":
      return {
        ...state,
        messages: [
          ...state.messages,
          { id: state.messages.length + 1, sender: "ai", content: action.payload }
        ],
        loading: false
      };
    case "SET_INPUT":
      return { ...state, input: action.payload };
    case "LOAD_CONVERSATION":
      return {
        ...state,
        messages: action.payload,
        loading: false,
        input: ""
      };
    default:
      return state;
  }
}

export function ChatProvider({ children }) {
  const [state, dispatch] = useReducer(chatReducer, initialState);
  return (
    <ChatContext.Provider value={{ state, dispatch }}>
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  return useContext(ChatContext);
}
