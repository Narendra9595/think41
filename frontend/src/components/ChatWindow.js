import React from "react";
import MessageList from "./MessageList";
import UserInput from "./UserInput";
import styles from "./ChatWindow.module.css";

const ChatWindow = () => {
  const [messages, setMessages] = React.useState([
    { id: 1, sender: "user", content: "Hello AI!" },
    { id: 2, sender: "ai", content: "Hello! How can I help you today?" }
  ]);

  const handleSend = (text) => {
    if (!text.trim()) return;
    setMessages([
      ...messages,
      { id: messages.length + 1, sender: "user", content: text }
    ]);
    setTimeout(() => {
      setMessages((msgs) => [
        ...msgs,
        { id: msgs.length + 1, sender: "ai", content: "AI response placeholder." }
      ]);
    }, 500);
  };

  return (
    <div className={styles.chatWindow}>
      <header className={styles.header}>AI Chat</header>
      <MessageList messages={messages} />
      <UserInput onSend={handleSend} />
    </div>
  );
};

export default ChatWindow;
