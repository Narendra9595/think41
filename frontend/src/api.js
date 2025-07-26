import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000/api";

export const sendChatMessage = async ({ user_id, message, conversation_id }) => {
  const res = await axios.post(`${API_BASE}/chat`, { user_id, message, conversation_id });
  return res.data;
};

export const fetchConversations = async (user_id) => {
  // GET /users/{user_id}/conversations
  const res = await axios.get(`${API_BASE.replace('/api','')}/users/${user_id}/conversations`);
  return { conversations: res.data };
};

export const fetchMessages = async (conversation_id) => {
  // GET /conversations/{conv_id}/messages
  const res = await axios.get(`${API_BASE.replace('/api','')}/conversations/${conversation_id}/messages`);
  return { messages: res.data };
};
