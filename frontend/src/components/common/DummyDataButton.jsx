import React, { useState } from 'react';
import { dummyFinancialData, validateDummyData } from '../../utils/dummyData';

const DummyDataButton = ({ onFillData, className = "" }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const handleFillDummyData = async () => {
    setIsLoading(true);
    
    try {
      // Validate dummy data first
      const validation = validateDummyData();
      
      if (!validation.isValid) {
        console.warn('Dummy data validation issues:', validation.errors);
      }
      
      // Fill the data
      await onFillData(dummyFinancialData);
      
      // Show success feedback
      setShowConfirm(false);
      
      // Optional: Show a brief success message
      const successMsg = document.createElement('div');
      successMsg.className = 'fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50 text-sm';
      successMsg.textContent = '✅ Dados de exemplo preenchidos com sucesso!';
      document.body.appendChild(successMsg);
      
      setTimeout(() => {
        if (document.body.contains(successMsg)) {
          document.body.removeChild(successMsg);
        }
      }, 3000);
      
    } catch (error) {
      console.error('Error filling dummy data:', error);
      
      // Show error message
      const errorMsg = document.createElement('div');
      errorMsg.className = 'fixed top-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg z-50 text-sm';
      errorMsg.textContent = '❌ Erro ao preencher dados de exemplo';
      document.body.appendChild(errorMsg);
      
      setTimeout(() => {
        if (document.body.contains(errorMsg)) {
          document.body.removeChild(errorMsg);
        }
      }, 3000);
    } finally {
      setIsLoading(false);
    }
  };

  if (showConfirm) {
    return (
      <div className={`relative ${className}`}>
        <div className="absolute right-0 top-full mt-2 bg-white border border-gray-300 rounded-lg shadow-lg p-4 z-50 min-w-80">
          <div className="text-sm text-gray-700 mb-3">
            <p className="font-medium mb-2">Preencher com dados de exemplo?</p>
            <p className="text-xs text-gray-600 mb-2">
              Isto irá substituir todos os dados atuais com informações de uma empresa comercial portuguesa típica.
            </p>
            <div className="text-xs text-gray-500">
              <p>• Empresa: Comercial Portuguesa Lda</p>
              <p>• Setor: Comércio a Retalho</p>
              <p>• 3 anos de dados financeiros</p>
            </div>
          </div>
          <div className="flex gap-2 justify-end">
            <button
              onClick={() => setShowConfirm(false)}
              className="px-3 py-1 text-xs text-gray-600 hover:text-gray-800 transition-colors"
            >
              Cancelar
            </button>
            <button
              onClick={handleFillDummyData}
              disabled={isLoading}
              className="px-3 py-1 text-xs bg-janua-navy text-white rounded hover:bg-opacity-90 transition-colors disabled:opacity-50"
            >
              {isLoading ? 'Preenchendo...' : 'Confirmar'}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <button
      onClick={() => setShowConfirm(true)}
      className={`
        inline-flex items-center gap-2 px-3 py-2 text-xs font-medium
        rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-20
        border
        ${className}
      `}
      title="Preencher formulário com dados de exemplo para teste"
    >
      <svg 
        className="w-4 h-4" 
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          strokeWidth={2} 
          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" 
        />
      </svg>
      Dados de Exemplo
    </button>
  );
};

export default DummyDataButton;