import React, { useState } from 'react';
import { dummyFinancialData } from '../../utils/dummyData';

const DummyDataButtonSmall = ({ onFillData, className = "" }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleFillDummyData = async () => {
    setIsLoading(true);
    
    try {
      await onFillData(dummyFinancialData);
      
      // Show brief success message
      const successMsg = document.createElement('div');
      successMsg.className = 'fixed top-4 right-4 bg-green-500 text-white px-3 py-2 rounded-lg shadow-lg z-50 text-xs';
      successMsg.textContent = '✅ Dados preenchidos!';
      document.body.appendChild(successMsg);
      
      setTimeout(() => {
        if (document.body.contains(successMsg)) {
          document.body.removeChild(successMsg);
        }
      }, 2000);
      
    } catch (error) {
      console.error('Error filling dummy data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handleFillDummyData}
      disabled={isLoading}
      className={`
        inline-flex items-center gap-1 px-2 py-1 text-xs text-gray-500 
        hover:text-janua-navy hover:bg-gray-50 rounded transition-colors
        disabled:opacity-50 disabled:cursor-not-allowed
        ${className}
      `}
      title="Preencher com dados de exemplo"
    >
      <svg 
        className="w-3 h-3" 
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          strokeWidth={2} 
          d="M13 10V3L4 14h7v7l9-11h-7z" 
        />
      </svg>
      {isLoading ? 'Preenchendo...' : 'Exemplo'}
    </button>
  );
};

export default DummyDataButtonSmall;