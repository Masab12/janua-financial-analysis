import React, { useState } from 'react';
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

  // Calculate intermediate results for display
  const calculateEBITDA = () => {
    return (
      (data.vendas_servicos_prestados || 0) +
      (data.subsidios_exploracao || 0) +
      (data.ganhos_perdas_subsidiarias || 0) +
      (data.variacao_inventarios_producao || 0) +
      (data.trabalhos_propria_entidade || 0) +
      (data.outros_rendimentos_ganhos || 0) -
      (data.cmvmc || 0) -
      (data.fornecimentos_servicos_externos || 0) -
      (data.gastos_pessoal || 0) -
      (data.imparidade_inventarios || 0) -
      (data.imparidade_dividas_receber || 0) -
      (data.provisoes || 0) -
      (data.imparidade_investimentos_nao_depreciaveis || 0) +
      (data.aumentos_reducoes_justo_valor || 0) -
      (data.outros_gastos_perdas || 0)
    );
  };

  const calculateEBIT = () => {
    return calculateEBITDA() - (data.gastos_depreciacoes_amortizacoes || 0);
  };

  const calculateResultBeforeTaxes = () => {
    return calculateEBIT() + (data.juros_rendimentos_obtidos || 0) - (data.juros_gastos_suportados || 0);
  };

  const calculateNetResult = () => {
    return calculateResultBeforeTaxes() - (data.imposto_rendimento || 0);
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    onChange(name, parseFloat(value) || 0);
  };

  const yearLabel = year === 'year_n2' ? 'Ano N-2 (Mais Antigo)' : 
                   year === 'year_n1' ? 'Ano N-1' : 'Ano N (Atual)';

  return (
    <Card title={`Demonstração de Resultados - ${yearLabel}`}>
      {Object.entries(incomeStatementFields).map(([sectionName, fields]) => (
        <div key={sectionName} className="mb-6">
          <button
            type="button"
            onClick={() => toggleSection(sectionName)}
            className="flex items-center justify-between w-full text-left font-semibold text-janua-navy mb-3 hover:text-opacity-80 transition-colors text-sm sm:text-base"
          >
            <span>{sectionName}</span>
            <span className="text-lg sm:text-xl flex-shrink-0 ml-2">
              {expandedSections[sectionName] ? '−' : '+'}
            </span>
          </button>
          
          {expandedSections[sectionName] && (
            <div className="space-y-4 pl-2 sm:pl-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4">
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
              
              {/* Show calculated results after each section */}
              {sectionName === 'Gastos e Perdas' && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-4">
                  <p className="text-sm font-medium text-blue-800">
                    Resultado antes de depreciações, gastos de financiamento e impostos: €{calculateEBITDA().toLocaleString('pt-PT', { minimumFractionDigits: 2 })}
                  </p>
                </div>
              )}
              
              {sectionName === 'Resultado antes de depreciações, gastos de financiamento e impostos' && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-4">
                  <p className="text-sm font-medium text-blue-800">
                    Resultado operacional (antes de gastos de financiamento e impostos): €{calculateEBIT().toLocaleString('pt-PT', { minimumFractionDigits: 2 })}
                  </p>
                </div>
              )}
              
              {sectionName === 'Resultado operacional (antes de gastos de financiamento e impostos)' && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-4">
                  <p className="text-sm font-medium text-blue-800">
                    Resultado antes de impostos: €{calculateResultBeforeTaxes().toLocaleString('pt-PT', { minimumFractionDigits: 2 })}
                  </p>
                </div>
              )}
              
              {sectionName === 'Resultado antes de impostos' && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mt-4">
                  <p className="text-sm font-medium text-green-800">
                    Resultado líquido do período: €{calculateNetResult().toLocaleString('pt-PT', { minimumFractionDigits: 2 })}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </Card>
  );
};

export default IncomeStatementForm;
