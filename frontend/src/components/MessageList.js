import React, { useRef, useEffect } from "react";
import Message from "./Message";
import styles from "./MessageList.module.css";

const MessageList = ({ messages }) => {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className={styles.messageList}>
      {messages.map((msg) => (
        <Message key={msg.id} sender={msg.sender} content={msg.content} />
      ))}
      <div ref={bottomRef} />
    </div>
  );
};

export default MessageList;
