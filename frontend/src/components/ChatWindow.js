import React, { useEffect, useState } from "react";
import MessageList from "./MessageList";
import UserInput from "./UserInput";
import ConversationHistoryPanel from "./ConversationHistoryPanel";
import styles from "./ChatWindow.module.css";
import { useChat } from "./ChatContext";
import { sendChatMessage, fetchMessages } from "../api";

const USER_ID = "demo-user-1";

const ChatWindow = () => {
  const { state, dispatch } = useChat();
  const [conversationId, setConversationId] = useState(null);
  const [showHistory, setShowHistory] = useState(false);

  // Load messages for selected conversation
  useEffect(() => {
    if (conversationId) {
      fetchMessages(conversationId).then((data) => {
        const messages = data.messages.map((m) => ({
          id: m._id,
          sender: m.sender,
          content: m.content,
          timestamp: m.timestamp
        }));
        dispatch({ type: "LOAD_CONVERSATION", payload: messages });
      });
    }
  }, [conversationId, dispatch]);

  const handleSend = async (text) => {
    if (!text.trim()) return;
    dispatch({ type: "SEND_MESSAGE", payload: text });
    try {
      const res = await sendChatMessage({ user_id: USER_ID, message: text, conversation_id: conversationId });
      setConversationId(res.conversation_id);
      dispatch({ type: "RECEIVE_MESSAGE", payload: res.ai_message.content });
    } catch (e) {
      dispatch({ type: "RECEIVE_MESSAGE", payload: "[Error: Could not reach backend]" });
    }
  };

  const handleNewChat = () => {
    // Clear current conversation and start fresh
    dispatch({ type: "CLEAR_CONVERSATION" });
    setConversationId(null);
  };

  return (
    <div className={styles.container}>
      {/* Header */}
      <div className={styles.header}>
        <div className={styles.brand}>
          <div className={styles.logo}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <div className={styles.brandInfo}>
            <h1>Think41 Assistant</h1>
            <p>E-commerce Support</p>
          </div>
        </div>
        <div className={styles.headerActions}>
          <button 
            className={`${styles.tabButton} ${!showHistory ? styles.active : ''}`}
            onClick={() => setShowHistory(false)}
          >
            Chat
          </button>
          <button 
            className={`${styles.tabButton} ${showHistory ? styles.active : ''}`}
            onClick={() => setShowHistory(true)}
          >
            History
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className={styles.mainContent}>
        {showHistory ? (
          <div className={styles.historyPanel}>
            <ConversationHistoryPanel 
              setConversationId={setConversationId} 
              userId={USER_ID}
              onClose={() => setShowHistory(false)}
            />
          </div>
        ) : (
          <div className={styles.chatArea}>
            {/* Chat Header with New Chat Button */}
            <div className={styles.chatHeader}>
              <button 
                className={styles.newChatButton}
                onClick={handleNewChat}
                title="Start a new conversation"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M12 5v14M5 12h14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                New Chat
              </button>
            </div>

            <div className={styles.messagesArea}>
              <MessageList messages={state.messages} />
              {state.loading && (
                <div className={styles.typingIndicator}>
                  <div className={styles.typingDots}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              )}
            </div>
            
            {/* Input Area */}
            <div className={styles.inputArea}>
              <UserInput 
                onSend={handleSend} 
                inputValue={state.input} 
                setInputValue={(val) => dispatch({ type: "SET_INPUT", payload: val })} 
                disabled={state.loading} 
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatWindow;
