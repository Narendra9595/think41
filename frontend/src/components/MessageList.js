import React, { useEffect, useRef } from "react";
import Message from "./Message";
import styles from "./MessageList.module.css";

const MessageList = ({ messages }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className={styles.messageList}>
      {messages.length === 0 ? (
        <div className={styles.welcomeMessage}>
          <h3>Welcome to Think41 Chat Assistant!</h3>
          <p>I can help you with:</p>
          <ul>
            <li>📦 Order status and tracking</li>
            <li>👕 Product availability and details</li>
            <li>🔄 Return and refund policies</li>
            <li>💳 Payment and shipping information</li>
          </ul>
          <p>Just ask me anything about your shopping experience!</p>
        </div>
      ) : (
        messages.map((message, index) => (
          <Message key={index} message={message} />
        ))
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
