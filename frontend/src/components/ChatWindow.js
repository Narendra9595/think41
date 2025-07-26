import React from "react";
import MessageList from "./MessageList";
import UserInput from "./UserInput";
import styles from "./ChatWindow.module.css";
import { useChat } from "./ChatContext";

const ChatWindow = () => {
  const { state, dispatch } = useChat();

  const handleSend = (text) => {
    if (!text.trim()) return;
    dispatch({ type: "SEND_MESSAGE", payload: text });
    setTimeout(() => {
      dispatch({ type: "RECEIVE_MESSAGE", payload: "AI response placeholder." });
    }, 500);
  };

  return (
    <div className={styles.chatWindow}>
      <header className={styles.header}>AI Chat</header>
      <MessageList messages={state.messages} />
      {state.loading && (
        <div style={{ textAlign: "center", color: "#888", marginBottom: 8 }}>AI is typing...</div>
      )}
      <UserInput onSend={handleSend} inputValue={state.input} setInputValue={(val) => dispatch({ type: "SET_INPUT", payload: val })} disabled={state.loading} />
    </div>
  );
}

export default ChatWindow;
