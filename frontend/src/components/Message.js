import React from "react";
import styles from "./Message.module.css";

const Message = ({ sender, content }) => (
  <div
    className={
      sender === "user"
        ? styles.userMessage
        : styles.aiMessage
    }
  >
    <span>{content}</span>
  </div>
);

export default Message;
