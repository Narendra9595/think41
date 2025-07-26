import React, { useEffect, useState } from "react";
import styles from "./ConversationHistoryPanel.module.css";
import { fetchConversations } from "../api";

const ConversationHistoryPanel = ({ setConversationId, userId }) => {
  const [conversations, setConversations] = useState([]);
  useEffect(() => {
    fetchConversations(userId).then((data) => {
      setConversations(data.conversations || []);
    });
  }, [userId]);

  return (
    <aside className={styles.panel}>
      <div className={styles.header}>Past Conversations</div>
      <ul className={styles.list}>
        {conversations.length === 0 && <li className={styles.item}><span style={{color:'#888'}}>No conversations</span></li>}
        {conversations.map((conv) => (
          <li key={conv._id} className={styles.item}>
            <button className={styles.button} onClick={() => setConversationId(conv._id)}>
              {conv.title || conv._id.slice(-6)}
            </button>
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default ConversationHistoryPanel;
