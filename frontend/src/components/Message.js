import React from "react";
import styles from "./Message.module.css";

const Message = ({ message }) => {
  const isUser = message.sender === "user";
  
  return (
    <div className={`${styles.messageContainer} ${isUser ? styles.userMessage : styles.botMessage}`}>
      <div className={styles.messageBubble}>
        <div className={styles.messageContent}>
          {message.content}
        </div>
        <div className={styles.messageTime}>
          {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
};

export default Message;
