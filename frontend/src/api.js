import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const sendChatMessage = async (data) => {
  try {
    const response = await api.post('/api/chat', data);
    return response.data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};

export const fetchMessages = async (conversationId) => {
  try {
    const response = await api.get(`/conversations/${conversationId}/messages`);
    return {
      messages: response.data
    };
  } catch (error) {
    console.error('Error fetching messages:', error);
    return {
      messages: []
    };
  }
};

export const fetchConversations = async (userId) => {
  try {
    const response = await api.get(`/users/${userId}/conversations`);
    return {
      conversations: response.data
    };
  } catch (error) {
    console.error('Error fetching conversations:', error);
    return {
      conversations: []
    };
  }
}; 