import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';  // Adjust this to your Django server URL

export const fetchProps = async () => {
  try {
    console.log('Fetching props from:', `${API_BASE_URL}/api/wnba-props/`);
    const response = await axios.get(`${API_BASE_URL}/api/wnba-props/`);
    console.log('Response received:', response.data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('Axios error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        config: {
          url: error.config?.url,
          method: error.config?.method,
        }
      });
    } else {
      console.error('Unexpected error:', error);
    }
    throw error;
  }
};
