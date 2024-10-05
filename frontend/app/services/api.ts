import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';  // Adjust this to your Django server URL

export const predictAPI = async (data: { Name: string; Stat_Type: string; Line: number }) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/predict/`, data);
    return response.data;
  } catch (error) {
    console.error('Error making prediction:', error);
    throw error;
  }
};
