import React, { useState } from 'react';
import Input from '../common/Input';
import Card from '../common/Card';
import { incomeStatementFields } from '../../utils/fieldLabels';

const IncomeStatementForm = ({ data, onChange, year }) => {
  const [expandedSections, setExpandedSections] = useState({
    'Rendimentos': true,
    'Gastos': false,
    'Resultados': false,
  });

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

  return (
    <Card title={`Demonstração de Resultados - ${year === 'year_n' ? 'Ano N (Atual)' : year === 'year_n1' ? 'Ano N-1' : 'Ano N-2'}`}>
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
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4 pl-2 sm:pl-4">
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
          )}
        </div>
      ))}
    </Card>
  );
};

export default IncomeStatementForm;
