import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';  // Adjust this to your Django server URL

export const fetchProps = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/wnba-props/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching props:', error);
    throw error;
  }
};
