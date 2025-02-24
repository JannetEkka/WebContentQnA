import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

// Configure axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json'
  }
});

// Extract content from URLs
export const extractContent = async (urls) => {
  try {
    const response = await apiClient.post('/extract', { urls });
    return response.data;
  } catch (error) {
    console.error('API error when extracting content:', error);
    throw error;
  }
};

// Get answer to a question
export const getAnswer = async (question, urls, modelType = 'default') => {
  try {
    const response = await apiClient.post('/answer', { 
      question, 
      urls,
      model_type: modelType 
    });
    return response.data;
  } catch (error) {
    console.error('API error when getting answer:', error);
    throw error;
  }
};

// Get available models
export const getAvailableModels = async () => {
  try {
    const response = await apiClient.get('/models');
    return response.data;
  } catch (error) {
    console.error('API error when getting available models:', error);
    throw error;
  }
};

export default {
  extractContent,
  getAnswer,
  getAvailableModels
};