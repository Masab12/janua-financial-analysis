import React, { useState } from 'react';

const SummaryBox = ({ metrics }) => {
  const [expandedCards, setExpandedCards] = useState({});

  const toggleCard = (key) => {
    setExpandedCards(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  if (!metrics) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">
          Resumo da Análise Financeira
        </h2>
        <p className="text-gray-600">Nenhum dado disponível</p>
      </div>
    );
  }

  // Analyze overall financial health
  const analyzeFinancialHealth = () => {
    const concerns = [];
    const positives = [];
    const attention = [];

    // ROE Analysis
    const roe = metrics.return_on_equity?.year_n || 0;
    if (roe > 15) {
      positives.push('Excelente rentabilidade para os acionistas');
    } else if (roe > 5) {
      positives.push('Boa rentabilidade do capital próprio');
    } else if (roe > 0) {
      attention.push('Rentabilidade do capital próprio abaixo do ideal');
    } else {
      concerns.push('Rentabilidade negativa - empresa está a gerar prejuízos');
    }

    // Autonomia Financeira
    const raf = metrics.racio_autonomia_financeira?.year_n || 0;
    if (raf > 0.5) {
      positives.push('Forte independência financeira');
    } else if (raf > 0.33) {
      positives.push('Autonomia financeira adequada');
    } else if (raf > 0.2) {
      attention.push('Dependência elevada de financiamento externo');
    } else {
      concerns.push('Autonomia financeira crítica - risco elevado');
    }

    // Liquidez Geral
    const lg = metrics.liquidez_geral?.year_n || 0;
    if (lg > 1.5) {
      positives.push('Boa capacidade para pagar dívidas de curto prazo');
    } else if (lg > 1.0) {
      attention.push('Liquidez justa - atenção à gestão de tesouraria');
    } else {
      concerns.push('Liquidez insuficiente - possíveis dificuldades em pagar dívidas de curto prazo');
    }

    // Endividamento
    const re = metrics.racio_endividamento?.year_n || 0;
    if (re < 0.5) {
      positives.push('Nível de endividamento saudável');
    } else if (re < 0.66) {
      attention.push('Endividamento moderado - monitorizar evolução');
    } else {
      concerns.push('Nível de endividamento elevado - atenção ao risco financeiro');
    }

    // Cobertura de Gastos de Financiamento
    const rcgf = metrics.racio_cobertura_gastos_financiamento?.year_n || 0;
    if (rcgf > 3) {
      positives.push('Excelente capacidade para cobrir juros');
    } else if (rcgf > 1.5) {
      positives.push('Boa cobertura de gastos financeiros');
    } else if (rcgf > 1) {
      attention.push('Cobertura de juros justa');
    } else {
      concerns.push('Dificuldade em cobrir gastos financeiros');
    }

    // Resumo do Balanço
    const rbf = metrics.resumo_balanco_funcional;
    if (rbf?.status === 'Bom') {
      positives.push('Estrutura de balanço equilibrada');
    } else if (rbf?.status === 'Médio') {
      attention.push('Estrutura de balanço requer atenção');
    } else if (rbf?.status === 'Mau') {
      concerns.push('Desequilíbrio na estrutura financeira');
    }

    // Overall status
    let status = 'stable';
    let statusText = 'Situação Financeira Estável';
    let statusColor = 'text-yellow-700';
    let bgColor = 'bg-yellow-50';
    let borderColor = 'border-yellow-200';

    if (concerns.length === 0 && positives.length >= 4) {
      status = 'good';
      statusText = 'Situação Financeira Saudável';
      statusColor = 'text-green-700';
      bgColor = 'bg-green-50';
      borderColor = 'border-green-200';
    } else if (concerns.length >= 3) {
      status = 'concern';
      statusText = 'Situação Financeira Requer Atenção';
      statusColor = 'text-red-700';
      bgColor = 'bg-red-50';
      borderColor = 'border-red-200';
    }

    return { status, statusText, statusColor, bgColor, borderColor, concerns, positives, attention };
  };

  const health = analyzeFinancialHealth();

  // Get 8 key indicators
  const keyIndicators = [
    {
      key: 'roe',
      name: 'Return on Equity (ROE)',
      value: metrics.return_on_equity?.year_n,
      unit: '%',
      description: 'Rentabilidade do capital próprio. Valores >5% são considerados bons. Indica retorno para os acionistas.',
      interpretation: metrics.return_on_equity?.interpretacao,
      trend: metrics.return_on_equity?.tendencia
    },
    {
      key: 'roa',
      name: 'Return on Assets (ROA)',
      value: metrics.return_on_assets?.year_n,
      unit: '%',
      description: 'Rentabilidade dos ativos. Valores >3% são considerados bons. Indica eficiência na utilização dos ativos.',
      interpretation: metrics.return_on_assets?.interpretacao,
      trend: metrics.return_on_assets?.tendencia
    },
    {
      key: 'raf',
      name: 'Autonomia Financeira (RAF)',
      value: metrics.racio_autonomia_financeira?.year_n,
      unit: 'ratio',
      description: 'Mede a independência financeira. Valores >33% são considerados adequados.',
      interpretation: metrics.racio_autonomia_financeira?.interpretacao,
      trend: metrics.racio_autonomia_financeira?.tendencia
    },
    {
      key: 'rcgf',
      name: 'Cobertura de Gastos de Financiamento (RCGF)',
      value: metrics.racio_cobertura_gastos_financiamento?.year_n,
      unit: 'x',
      description: 'Mede a capacidade da empresa de cobrir gastos financeiros com resultados operacionais. Valores >1 indicam boa cobertura.',
      interpretation: metrics.racio_cobertura_gastos_financiamento?.interpretacao,
      trend: metrics.racio_cobertura_gastos_financiamento?.tendencia
    },
    {
      key: 'rbf',
      name: 'Resumo do Balanço',
      value: metrics.resumo_balanco_funcional?.status || 'Em desenvolvimento',
      unit: 'status',
      description: 'Avaliação global da estrutura financeira.',
      interpretation: metrics.resumo_balanco_funcional?.mensagem,
      trend: '►'
    },
    {
      key: 'lg',
      name: 'Liquidez Geral (LG)',
      value: metrics.liquidez_geral?.year_n,
      unit: 'ratio',
      description: 'Capacidade de pagar dívidas de curto prazo. Valores >1 indicam boa liquidez. Benchmark: ≥1.0',
      interpretation: metrics.liquidez_geral?.interpretacao,
      trend: metrics.liquidez_geral?.tendencia
    },
    {
      key: 'rat',
      name: 'Rotação do Ativo (RAT)',
      value: metrics.rotacao_ativo?.year_n,
      unit: '%',
      description: 'Eficiência na utilização dos ativos para gerar vendas. Valores mais altos indicam maior eficiência.',
      interpretation: metrics.rotacao_ativo?.interpretacao,
      trend: metrics.rotacao_ativo?.tendencia
    },
    {
      key: 'gaf',
      name: 'Grau de Alavanca Financeira (GAF)',
      value: metrics.grau_alavanca_financeira?.year_n,
      unit: 'ratio',
      description: 'Mede o risco financeiro. Valores próximos de 1 indicam baixo risco, valores elevados indicam alto risco financeiro.',
      interpretation: metrics.grau_alavanca_financeira?.interpretacao,
      trend: metrics.grau_alavanca_financeira?.tendencia
    }
  ];

  const formatValue = (value, unit) => {
    if (value === null || value === undefined || isNaN(value)) return '-';

    if (unit === '%') {
      return `${value.toFixed(2)}%`;
    } else if (unit === 'x') {
      return `${value.toFixed(2)}x`;
    } else if (unit === 'ratio') {
      return `${(value * 100).toFixed(2)}%`;
    } else if (unit === 'status') {
      return value;
    }
    return value.toFixed(2);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      {/* Header */}
      <div className="border-b border-gray-200 pb-4 mb-6">
        <h2 className="text-2xl font-bold" style={{ color: '#0d2037' }}>
          Resumo da Análise Financeira
        </h2>
        <p className="text-sm text-gray-600 mt-1">Principais indicadores de performance</p>
      </div>

      {/* Overall Status */}
      <div className={`${health.bgColor} ${health.borderColor} border-l-4 p-4 mb-6 rounded`}>
        <div className="flex items-start">
          <div className="flex-shrink-0">
            {health.status === 'good' && <span className={`text-2xl ${health.statusColor}`}>✓</span>}
            {health.status === 'stable' && <span className={`text-2xl ${health.statusColor}`}>⚠</span>}
            {health.status === 'concern' && <span className={`text-2xl ${health.statusColor}`}>⚠</span>}
          </div>
          <div className="ml-3 flex-1">
            <h3 className={`text-sm font-medium ${health.statusColor}`}>
              {health.statusText}
            </h3>

            {health.positives.length > 0 && (
              <div className="mt-2">
                <p className="text-sm font-semibold text-gray-700">Pontos Fortes:</p>
                <ul className="mt-1 text-sm text-gray-600 list-disc list-inside">
                  {health.positives.map((point, idx) => (
                    <li key={idx}>{point}</li>
                  ))}
                </ul>
              </div>
            )}

            {health.attention.length > 0 && (
              <div className="mt-2">
                <p className="text-sm font-semibold text-gray-700">Pontos de Atenção:</p>
                <ul className="mt-1 text-sm text-gray-600 list-disc list-inside">
                  {health.attention.map((point, idx) => (
                    <li key={idx}>{point}</li>
                  ))}
                </ul>
              </div>
            )}

            {health.concerns.length > 0 && (
              <div className="mt-2">
                <p className="text-sm font-semibold text-red-700">Preocupações:</p>
                <ul className="mt-1 text-sm text-red-600 list-disc list-inside">
                  {health.concerns.map((point, idx) => (
                    <li key={idx}>{point}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Recommendations */}
            <div className="mt-3 pt-3 border-t border-gray-200">
              <p className="text-sm font-semibold text-gray-700">Recomendações:</p>
              <ul className="mt-1 text-sm text-gray-600 list-disc list-inside">
                {health.concerns.length >= 2 && (
                  <li>Priorizar a melhoria da situação financeira antes de novos investimentos</li>
                )}
                {health.concerns.some(c => c.includes('Liquidez')) && (
                  <li>Melhorar a gestão de tesouraria e renegociar prazos com fornecedores</li>
                )}
                {health.concerns.some(c => c.includes('endividamento')) && (
                  <li>Reduzir o endividamento e reforçar o capital próprio</li>
                )}
                {health.status === 'good' && (
                  <li>Manter a boa performance e considerar oportunidades de crescimento</li>
                )}
                {health.status === 'stable' && (
                  <li>Monitorizar os indicadores de atenção e implementar melhorias graduais</li>
                )}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Key Indicators */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Indicadores Principais</h3>

        {keyIndicators.map((indicator) => (
          <div key={indicator.key} className="border border-gray-200 rounded-lg overflow-hidden">
            <button
              onClick={() => toggleCard(indicator.key)}
              className="w-full px-4 py-3 bg-gray-50 hover:bg-gray-100 transition-colors flex items-center justify-between"
            >
              <div className="flex items-center space-x-3">
                <span className="text-2xl">{indicator.trend}</span>
                <div className="text-left">
                  <h4 className="font-semibold text-gray-800">{indicator.name}</h4>
                  <p className="text-sm text-gray-600">
                    {formatValue(indicator.value, indicator.unit)}
                  </p>
                </div>
              </div>
              <span className="text-gray-500 text-xl">
                {expandedCards[indicator.key] ? '▲' : '▼'}
              </span>
            </button>

            {expandedCards[indicator.key] && (
              <div className="px-4 py-3 bg-white border-t border-gray-200">
                <p className="text-sm text-gray-700 mb-2">{indicator.description}</p>
                {indicator.interpretation && (
                  <p className="text-sm text-gray-600 italic">
                    {indicator.trend} {indicator.interpretation}
                  </p>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Footer Note */}
      <div className="mt-6 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-500 text-center">
          Este resumo apresenta os oito indicadores-chave da análise financeira.
          Consulte os detalhes completos abaixo para ver todos os 51 rácios calculados.
        </p>
      </div>
    </div>
  );
};

export default SummaryBox;


