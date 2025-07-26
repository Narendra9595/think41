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

  // Load messages for selected conversation
  useEffect(() => {
    if (conversationId) {
      fetchMessages(conversationId).then((data) => {
        const messages = data.messages.map((m, i) => ({
          id: i + 1,
          sender: m.sender,
          content: m.content
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

  // Provide function to ConversationHistoryPanel to set conversationId
  return (
    <div style={{ display: "flex", height: "80vh", maxWidth: 720, margin: "40px auto", borderRadius: 16, boxShadow: "0 4px 24px rgba(0,0,0,0.10)", background: "#fff", overflow: "hidden" }}>
      <ConversationHistoryPanel setConversationId={setConversationId} userId={USER_ID} />
      <div className={styles.chatWindow} style={{ flex: 1 }}>
        <header className={styles.header}>AI Chat</header>
        <MessageList messages={state.messages} />
        {state.loading && (
          <div style={{ textAlign: "center", color: "#888", marginBottom: 8 }}>AI is typing...</div>
        )}
        <UserInput onSend={handleSend} inputValue={state.input} setInputValue={(val) => dispatch({ type: "SET_INPUT", payload: val })} disabled={state.loading} />
      </div>
    </div>
  );
}

export default ChatWindow;
