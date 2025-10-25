import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'Accept': 'application/json; charset=utf-8',
  },
});

// Add response interceptor to ensure proper UTF-8 handling
api.interceptors.response.use(
  (response) => {
    // Ensure response data is properly decoded as UTF-8
    if (response.headers['content-type']?.includes('application/json')) {
      // The response should already be properly decoded by axios
      // but we ensure the content-type is set correctly
      response.headers['content-type'] = 'application/json; charset=utf-8';
    }
    return response;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const calculateFinancialMetrics = async (financialData) => {
  try {
    const response = await api.post('/calculate', financialData);
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error('API Error:', error);
    
    // Handle different types of errors
    if (error.response) {
      const status = error.response.status;
      const errorData = error.response.data;
      
      if (status === 422) {
        // Pydantic validation error - return detailed message
        const errorMessage = typeof errorData.detail === 'string' 
          ? errorData.detail 
          : 'Erro de validação dos dados. Verifique os campos preenchidos.';
        
        return {
          success: false,
          error: errorMessage,
          validationError: true,
        };
      } else if (status === 400) {
        // Business logic validation error - also return detailed message
        const errorMessage = typeof errorData.detail === 'string' 
          ? errorData.detail 
          : 'Erro nos dados fornecidos. Verifique os valores inseridos.';
        
        return {
          success: false,
          error: errorMessage,
          validationError: true,
        };
      } else if (status === 500) {
        // Server error
        return {
          success: false,
          error: 'Erro interno do servidor. Tente novamente em alguns minutos.',
        };
      }
    } else if (error.request) {
      // Network error
      return {
        success: false,
        error: 'Erro de conexão. Verifique sua conexão com a internet e tente novamente.',
      };
    }
    
    // Fallback error
    return {
      success: false,
      error: error.message || 'Erro inesperado. Tente novamente.',
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
    link.setAttribute('download', `relatorio_${financialData.company_info.nome_empresa.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`);
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
