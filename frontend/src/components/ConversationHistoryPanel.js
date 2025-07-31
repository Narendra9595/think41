import React, { useState, useEffect } from 'react';
import { fetchConversations } from '../api';
import styles from './ConversationHistoryPanel.module.css';

const ConversationHistoryPanel = ({ setConversationId, userId, onClose }) => {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadConversations = async () => {
      try {
        setLoading(true);
        const data = await fetchConversations(userId);
        console.log('Received conversations:', data.conversations);
        setConversations(data.conversations || []);
      } catch (error) {
        console.error('Error loading conversations:', error);
        setConversations([]);
      } finally {
        setLoading(false);
      }
    };

    loadConversations();
  }, [userId]);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const handleConversationClick = (conversationId) => {
    setConversationId(conversationId);
    if (onClose) onClose();
  };

  if (loading) {
    return (
      <div className={styles.historyPanel}>
        <div className={styles.header}>
          <h3 className={styles.title}>Conversation History</h3>
          <button className={styles.closeButton} onClick={onClose}>×</button>
        </div>
        <div className={styles.content}>
          <div className={styles.loading}>
            <div className={styles.spinner}></div>
            <p>Loading conversations...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.historyPanel}>
      <div className={styles.header}>
        <h3 className={styles.title}>Conversation History</h3>
        <button className={styles.closeButton} onClick={onClose}>×</button>
      </div>
      <div className={styles.content}>
        {conversations.length === 0 ? (
          <div className={styles.empty}>
            <p>No conversations yet</p>
            <small>Start chatting to see your history here</small>
          </div>
        ) : (
          <div className={styles.conversationList}>
            {conversations.map((conversation) => (
              <div
                key={conversation._id}
                className={styles.conversationItem}
                onClick={() => handleConversationClick(conversation._id)}
              >
                <div className={styles.conversationInfo}>
                  <div className={styles.conversationTitle}>
                    {conversation.title || 'New conversation'}
                  </div>
                  <div className={styles.conversationDate}>
                    {formatDate(conversation.updated_at)}
                  </div>
                </div>
                <div className={styles.conversationArrow}>→</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ConversationHistoryPanel;
