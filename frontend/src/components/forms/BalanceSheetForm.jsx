import React, { useState, useMemo } from 'react';
import Input from '../common/Input';
import Card from '../common/Card';
import { balanceSheetFields } from '../../utils/fieldLabels';

const BalanceSheetForm = ({ data, onChange, year }) => {
  const [expandedSections, setExpandedSections] = useState({
    'Ativo Não Corrente': true,
    'Ativo Corrente': false,
    'Capital Próprio': false,
    'Passivo Não Corrente': false,
    'Passivo Corrente': false,
  });

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

  // Calculate section totals automatically
  const sectionTotals = useMemo(() => {
    const totals = {};
    
    // Calculate totals for each section
    Object.entries(balanceSheetFields).forEach(([sectionName, fields]) => {
      const total = fields.reduce((sum, field) => {
        return sum + (parseFloat(data[field.key]) || 0);
      }, 0);
      totals[sectionName] = total;
    });
    
    // Calculate main totals
    totals['Total Ativo Não Corrente'] = totals['Ativo Não Corrente'] || 0;
    totals['Total Ativo Corrente'] = totals['Ativo Corrente'] || 0;
    totals['Total Ativo'] = totals['Total Ativo Não Corrente'] + totals['Total Ativo Corrente'];
    
    totals['Total Capital Próprio'] = totals['Capital Próprio'] || 0;
    totals['Total Passivo Não Corrente'] = totals['Passivo Não Corrente'] || 0;
    totals['Total Passivo Corrente'] = totals['Passivo Corrente'] || 0;
    totals['Total Passivo'] = totals['Total Passivo Não Corrente'] + totals['Total Passivo Corrente'];
    
    totals['Total Passivo + Capital Próprio'] = totals['Total Passivo'] + totals['Total Capital Próprio'];
    
    return totals;
  }, [data]);

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-PT', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2,
    }).format(value);
  };

  const getBalanceStatus = () => {
    const difference = Math.abs(sectionTotals['Total Ativo'] - sectionTotals['Total Passivo + Capital Próprio']);
    if (difference < 1000) {
      return { status: 'balanced', message: 'Balanço equilibrado ✓', color: 'text-green-600' };
    } else {
      return { 
        status: 'unbalanced', 
        message: `Diferença: ${formatCurrency(difference)}`, 
        color: 'text-red-600' 
      };
    }
  };

  const balanceStatus = getBalanceStatus();

  return (
    <Card title={`Balanço - ${year === 'year_n' ? 'Ano N (Atual)' : year === 'year_n1' ? 'Ano N-1' : 'Ano N-2'}`}>
      {/* Balance Status Indicator */}
      <div className="mb-6 p-4 bg-gray-50 rounded-lg border">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
          <div>
            <h3 className="font-semibold text-gray-900 text-sm">Verificação do Balanço</h3>
            <p className={`text-sm font-medium ${balanceStatus.color}`}>
              {balanceStatus.message}
            </p>
          </div>
          <div className="text-xs text-gray-600">
            <div>Total Ativo: {formatCurrency(sectionTotals['Total Ativo'])}</div>
            <div>Total Passivo + CP: {formatCurrency(sectionTotals['Total Passivo + Capital Próprio'])}</div>
          </div>
        </div>
      </div>

      {Object.entries(balanceSheetFields).map(([sectionName, fields]) => (
        <div key={sectionName} className="mb-6">
          <button
            type="button"
            onClick={() => toggleSection(sectionName)}
            className="flex items-center justify-between w-full text-left font-semibold text-janua-navy mb-3 hover:text-opacity-80 transition-colors text-sm sm:text-base"
          >
            <div className="flex items-center gap-3">
              <span>{sectionName}</span>
              <span className="text-xs font-normal text-gray-600 bg-gray-100 px-2 py-1 rounded">
                {formatCurrency(sectionTotals[sectionName] || 0)}
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
                    {formatCurrency(sectionTotals[sectionName] || 0)}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      ))}

      {/* Main Totals Summary */}
      <div className="mt-6 bg-janua-navy text-white rounded-lg p-4">
        <h3 className="font-bold text-lg mb-3">Resumo dos Totais</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
          <div>
            <div className="flex justify-between mb-2">
              <span>Total Ativo Não Corrente:</span>
              <span className="font-medium">{formatCurrency(sectionTotals['Total Ativo Não Corrente'])}</span>
            </div>
            <div className="flex justify-between mb-2">
              <span>Total Ativo Corrente:</span>
              <span className="font-medium">{formatCurrency(sectionTotals['Total Ativo Corrente'])}</span>
            </div>
            <div className="flex justify-between font-bold text-base border-t border-white/30 pt-2">
              <span>TOTAL ATIVO:</span>
              <span>{formatCurrency(sectionTotals['Total Ativo'])}</span>
            </div>
          </div>
          
          <div>
            <div className="flex justify-between mb-2">
              <span>Total Capital Próprio:</span>
              <span className="font-medium">{formatCurrency(sectionTotals['Total Capital Próprio'])}</span>
            </div>
            <div className="flex justify-between mb-2">
              <span>Total Passivo:</span>
              <span className="font-medium">{formatCurrency(sectionTotals['Total Passivo'])}</span>
            </div>
            <div className="flex justify-between font-bold text-base border-t border-white/30 pt-2">
              <span>TOTAL PASSIVO + CP:</span>
              <span>{formatCurrency(sectionTotals['Total Passivo + Capital Próprio'])}</span>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default BalanceSheetForm;
