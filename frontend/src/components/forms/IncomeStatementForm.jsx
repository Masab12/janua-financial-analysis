import React, { useState, useMemo } from 'react';
import Input from '../common/Input';
import Card from '../common/Card';
import { incomeStatementFields } from '../../utils/fieldLabels';

const IncomeStatementForm = ({ data, onChange, year }) => {
  const [expandedSections, setExpandedSections] = useState({
    'Rendimentos e Ganhos': true,
    'Gastos e Perdas': false,
    'Resultado antes de depreciações, gastos de financiamento e impostos': false,
    'Resultado operacional (antes de gastos de financiamento e impostos)': false,
    'Resultado antes de impostos': false,
  });

  // Calculate intermediate results and section totals
  const calculations = useMemo(() => {
    // Calculate section totals
    const sectionTotals = {};
    Object.entries(incomeStatementFields).forEach(([sectionName, fields]) => {
      const total = fields.reduce((sum, field) => {
        return sum + (parseFloat(data[field.key]) || 0);
      }, 0);
      sectionTotals[sectionName] = total;
    });

    // Calculate key financial metrics
    const totalRendimentos = sectionTotals['Rendimentos e Ganhos'] || 0;
    const totalGastos = sectionTotals['Gastos e Perdas'] || 0;
    
    const ebitda = totalRendimentos - totalGastos;
    const ebit = ebitda - (data.gastos_depreciacoes_amortizacoes || 0);
    const resultBeforeTaxes = ebit + (data.juros_rendimentos_obtidos || 0) - (data.juros_gastos_suportados || 0);
    const netResult = resultBeforeTaxes - (data.imposto_rendimento || 0);

    return {
      sectionTotals,
      ebitda,
      ebit,
      resultBeforeTaxes,
      netResult,
      totalRendimentos,
      totalGastos
    };
  }, [data]);

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-PT', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2,
    }).format(value);
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    // Handle both comma and dot decimal separators
    const cleanValue = value.replace(',', '.');
    onChange(name, parseFloat(cleanValue) || 0);
  };

  const yearLabel = year === 'year_n2' ? 'Ano N-2 (Mais Antigo)' : 
                   year === 'year_n1' ? 'Ano N-1' : 'Ano N (Atual)';

  return (
    <Card title={`Demonstração de Resultados - ${yearLabel}`}>
      {/* Key Metrics Summary */}
      <div className="mb-6 bg-gray-50 rounded-lg p-4 border">
        <h3 className="font-semibold text-gray-900 text-sm mb-3">Resumo dos Resultados</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>EBITDA:</span>
              <span className={`font-medium ${calculations.ebitda >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {formatCurrency(calculations.ebitda)}
              </span>
            </div>
            <div className="flex justify-between">
              <span>EBIT:</span>
              <span className={`font-medium ${calculations.ebit >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {formatCurrency(calculations.ebit)}
              </span>
            </div>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span>Resultado antes de impostos:</span>
              <span className={`font-medium ${calculations.resultBeforeTaxes >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {formatCurrency(calculations.resultBeforeTaxes)}
              </span>
            </div>
            <div className="flex justify-between font-bold">
              <span>Resultado líquido:</span>
              <span className={calculations.netResult >= 0 ? 'text-green-600' : 'text-red-600'}>
                {formatCurrency(calculations.netResult)}
              </span>
            </div>
          </div>
        </div>
      </div>

      {Object.entries(incomeStatementFields).map(([sectionName, fields]) => (
        <div key={sectionName} className="mb-6">
          <button
            type="button"
            onClick={() => toggleSection(sectionName)}
            className="flex items-center justify-between w-full text-left font-semibold text-janua-navy mb-3 hover:text-opacity-80 transition-colors text-sm sm:text-base"
          >
            <div className="flex items-center gap-3">
              <span>{sectionName}</span>
              <span className="text-xs font-normal text-gray-600 bg-gray-100 px-2 py-1 rounded">
                {formatCurrency(calculations.sectionTotals[sectionName] || 0)}
              </span>
            </div>
            <span className="text-lg sm:text-xl flex-shrink-0 ml-2">
              {expandedSections[sectionName] ? '−' : '+'}
            </span>
          </button>
          
          {expandedSections[sectionName] && (
            <div className="pl-2 sm:pl-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4 mb-3">
                {fields.map((field) => (
                  <Input
                    key={field.key}
                    label={field.label}
                    name={field.key}
                    value={data[field.key] || 0}
                    onChange={handleInputChange}
                    type="number"
                  />
                ))}
              </div>
              
              {/* Section Total Display */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mt-3">
                <div className="flex justify-between items-center">
                  <span className="font-medium text-blue-900 text-sm">
                    Total {sectionName}:
                  </span>
                  <span className="font-bold text-blue-900">
                    {formatCurrency(calculations.sectionTotals[sectionName] || 0)}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      ))}

      {/* Final Results Summary */}
      <div className="mt-6 bg-janua-navy text-white rounded-lg p-4">
        <h3 className="font-bold text-lg mb-3">Demonstração de Resultados - Resumo</h3>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span>Total de Rendimentos e Ganhos:</span>
            <span className="font-medium">{formatCurrency(calculations.totalRendimentos)}</span>
          </div>
          <div className="flex justify-between">
            <span>Total de Gastos e Perdas:</span>
            <span className="font-medium">{formatCurrency(calculations.totalGastos)}</span>
          </div>
          <div className="border-t border-white/30 pt-2 mt-3">
            <div className="flex justify-between font-bold text-base">
              <span>RESULTADO LÍQUIDO DO PERÍODO:</span>
              <span className={calculations.netResult >= 0 ? 'text-green-300' : 'text-red-300'}>
                {formatCurrency(calculations.netResult)}
              </span>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default IncomeStatementForm;
