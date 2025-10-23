import React from 'react';

const IndicatorDisplay = ({ metric }) => {
  // Determine health status based on metric value and benchmarks
  const getHealthStatus = (metric) => {
    // This is a simplified health assessment - in a real implementation,
    // you would have specific benchmarks for each metric type
    const value = metric.year_n;
    
    // Example health logic (would need to be customized per metric)
    if (metric.unidade === '%') {
      if (value > 10) return { triangle: '▲', color: 'green', status: 'Saudável' };
      if (value < 0) return { triangle: '▼', color: 'red', status: 'Requer Atenção' };
      return { triangle: '►', color: 'neutral', status: 'Neutro' };
    }
    
    if (metric.unidade === 'ratio') {
      if (value > 1.5) return { triangle: '▲', color: 'green', status: 'Saudável' };
      if (value < 0.5) return { triangle: '▼', color: 'red', status: 'Requer Atenção' };
      return { triangle: '►', color: 'neutral', status: 'Neutro' };
    }
    
    // Default neutral status
    return { triangle: '►', color: 'neutral', status: 'Neutro' };
  };

  // Determine 3-year trend
  const getTrend = (metric) => {
    const current = metric.year_n;
    const oldest = metric.year_n2;
    
    // Calculate overall trend from oldest to current
    const totalChange = current - oldest;
    const percentChange = oldest !== 0 ? (totalChange / Math.abs(oldest)) * 100 : 0;
    
    if (Math.abs(percentChange) < 5) {
      return { triangle: '►', color: 'neutral', description: 'Estável nos últimos 3 anos' };
    } else if (percentChange > 0) {
      return { triangle: '▲', color: 'green', description: 'Crescimento nos últimos 3 anos' };
    } else {
      return { triangle: '▼', color: 'red', description: 'Declínio nos últimos 3 anos' };
    }
  };

  const healthStatus = getHealthStatus(metric);
  const trend = getTrend(metric);

  const getBackgroundColor = (color) => {
    switch (color) {
      case 'green':
        return 'bg-green-100 border-green-300';
      case 'red':
        return 'bg-red-100 border-red-300';
      default:
        return 'bg-gray-50 border-gray-200';
    }
  };

  const getTextColor = (color) => {
    switch (color) {
      case 'green':
        return 'text-green-800';
      case 'red':
        return 'text-red-800';
      default:
        return 'text-gray-700';
    }
  };

  const formatValue = (value, unit) => {
    if (value === null || value === undefined || isNaN(value)) return '-';
    
    if (unit === '€') {
      return `€${value.toLocaleString('pt-PT', { minimumFractionDigits: 2 })}`;
    } else if (unit === '%') {
      return `${value.toFixed(2)}%`;
    } else if (unit === 'ratio') {
      // Handle special case for very high values (like when no financial costs)
      if (value >= 999) {
        return `>999x`;
      }
      return `${value.toFixed(2)}x`;
    } else if (unit === 'dias') {
      return `${Math.round(value)} dias`;
    } else if (unit === 'vezes/ano' || unit === 'vezes') {
      return `${value.toFixed(2)}x`;
    }
    return value.toFixed(2);
  };

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 space-y-3">
      {/* Line 1: What the indicator means */}
      <div>
        <h4 className="font-semibold text-gray-900 text-sm">{metric.nome}</h4>
        <p className="text-xs text-gray-600 mt-1">
          {metric.interpretacao || 'Indicador financeiro importante para análise empresarial'}
        </p>
      </div>

      {/* Line 2: Current health status with colored background and triangle */}
      <div className={`border rounded-lg p-3 ${getBackgroundColor(healthStatus.color)}`}>
        <div className="flex items-center justify-between">
          <div>
            <p className={`text-sm font-medium ${getTextColor(healthStatus.color)}`}>
              Status Atual: {healthStatus.status}
            </p>
            <p className="text-xs text-gray-600 mt-1">
              Valor: {formatValue(metric.year_n, metric.unidade)}
            </p>
          </div>
          <div className={`text-2xl ${getTextColor(healthStatus.color)}`}>
            {healthStatus.triangle}
          </div>
        </div>
      </div>

      {/* Line 3: 3-year trend analysis */}
      <div className={`border rounded-lg p-3 ${getBackgroundColor(trend.color)}`}>
        <div className="flex items-center justify-between">
          <div>
            <p className={`text-sm font-medium ${getTextColor(trend.color)}`}>
              Tendência: {trend.description}
            </p>
            <div className={`flex space-x-4 text-xs mt-1 ${getTextColor(trend.color)}`}>
              <span>N-2: {formatValue(metric.year_n2, metric.unidade)}</span>
              <span>N-1: {formatValue(metric.year_n1, metric.unidade)}</span>
              <span>N: {formatValue(metric.year_n, metric.unidade)}</span>
            </div>
          </div>
          <div className={`text-2xl ${getTextColor(trend.color)}`}>
            {trend.triangle}
          </div>
        </div>
      </div>
    </div>
  );
};

export default IndicatorDisplay;