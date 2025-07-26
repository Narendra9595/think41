import React from "react";
import ChatWindow from "./components/ChatWindow";
import { ChatProvider } from "./components/ChatContext";

function App() {
  return (
    <ChatProvider>
      <ChatWindow />
    </ChatProvider>
  );
}

export default App;
