import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const calculateFinancialMetrics = async (financialData) => {
  try {
    const response = await api.post('/calculate', financialData);
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.error || error.message || 'Failed to calculate metrics',
    };
  }
};

export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    throw new Error('API health check failed');
  }
};

export const generatePDF = async (financialData) => {
  try {
    const response = await api.post('/generate-pdf', financialData, {
      responseType: 'blob', // Important for PDF download
    });
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `relatorio_${financialData.nome_entidade.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
    
    return {
      success: true,
      message: 'PDF gerado com sucesso',
    };
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.error || error.message || 'Failed to generate PDF',
    };
  }
};

export default api;
