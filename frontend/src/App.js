import React from "react";
import ChatWindow from "./components/ChatWindow";
import { ChatProvider } from "./components/ChatContext";
import "./App.css";

function App() {
  return (
    <div className="App">
      <ChatProvider>
        <ChatWindow />
      </ChatProvider>
    </div>
  );
}

export default App;
