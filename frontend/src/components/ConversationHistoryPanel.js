import React from "react";
import styles from "./ConversationHistoryPanel.module.css";
import { useChat } from "./ChatContext";

const mockConversations = [
  { id: "c1", title: "Order Inquiry", messages: [
    { id: 1, sender: "user", content: "What is the status of my order?" },
    { id: 2, sender: "ai", content: "Your order is being processed." }
  ]},
  { id: "c2", title: "Product Info", messages: [
    { id: 1, sender: "user", content: "Tell me about product X." },
    { id: 2, sender: "ai", content: "Product X is a high-quality item." }
  ]}
];

const ConversationHistoryPanel = () => {
  const { dispatch } = useChat();
  const handleLoad = (conv) => {
    dispatch({ type: "LOAD_CONVERSATION", payload: conv.messages });
  };
  return (
    <aside className={styles.panel}>
      <div className={styles.header}>Past Conversations</div>
      <ul className={styles.list}>
        {mockConversations.map((conv) => (
          <li key={conv.id} className={styles.item}>
            <button className={styles.button} onClick={() => handleLoad(conv)}>
              {conv.title}
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default ConversationHistoryPanel;
