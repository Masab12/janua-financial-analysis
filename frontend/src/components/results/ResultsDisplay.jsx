import React, { useState } from 'react';
import Card from '../common/Card';
import SummaryBox from './SummaryBox';
import IndicatorDisplay from './IndicatorDisplay';
import { generatePDF } from '../../services/api';

const ResultsDisplay = ({ results, originalData }) => {
  if (!results) return null;

  const { empresa, metrics, timestamp } = results;
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false);
  
  // Debug: Log which metrics are undefined
  console.log('📋 Available metrics:', Object.keys(metrics));
  const undefinedMetrics = Object.entries(metrics)
    .filter(([, value]) => value === null || value === undefined)
    .map(([key]) => key);
  if (undefinedMetrics.length > 0) {
    console.warn('⚠️ Undefined metrics:', undefinedMetrics);
  }

  const formatCurrency = (value) => {
    if (value === null || value === undefined || isNaN(value)) return '-';
    return new Intl.NumberFormat('pt-PT', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatRatio = (value) => {
    if (value === null || value === undefined || isNaN(value)) return '-';
    return value.toFixed(4);
  };

  const renderMetricValue = (metric) => {
    if (!metric) return '-';
    
    // Special handling for resumo_balanco_funcional (dict format)
    if (metric.status && metric.mensagem) {
      return (
        <div className="space-y-2">
          <span className="text-xl sm:text-2xl font-semibold text-janua-navy">{metric.status}</span>
          <p className="text-xs sm:text-sm text-gray-600">{metric.mensagem}</p>
        </div>
      );
    }
    
    const { year_n, unidade, interpretacao, tendencia } = metric;
    
    // Handle undefined or null year_n
    if (year_n === null || year_n === undefined || isNaN(year_n)) {
      return (
        <div className="space-y-2">
          <span className="text-xl sm:text-2xl font-semibold text-gray-400">-</span>
          {interpretacao && (
            <p className="text-xs sm:text-sm text-gray-600">{interpretacao}</p>
          )}
        </div>
      );
    }
    
    let displayValue;
    if (unidade === '€') {
      displayValue = formatCurrency(year_n);
    } else if (unidade === '%') {
      // Backend already returns percentages in 0-100 range, no need to multiply by 100
      displayValue = `${year_n.toFixed(2)}%`;
    } else {
      displayValue = formatRatio(year_n);
    }

    return (
      <div className="space-y-2">
        <div className="flex items-center gap-2 flex-wrap">
          {tendencia && <span className="text-base sm:text-lg">{tendencia}</span>}
          <span className="text-xl sm:text-2xl font-semibold text-janua-navy">{displayValue}</span>
        </div>
        {interpretacao && (
          <p className="text-xs sm:text-sm text-gray-600">{interpretacao}</p>
        )}
      </div>
    );
  };

  const metricSections = [
    {
      title: '1. Dimensão / Produção',
      metrics: [
        { key: 'consumos_intermedios', label: 'CI - Consumos Intermédios' },
        { key: 'valor_bruto_producao', label: 'VBP - Valor Bruto da Produção' },
        { key: 'valor_acrescentado_bruto', label: 'VAB - Valor Acrescentado Bruto' },
        { key: 'taxa_crescimento', label: 'TC - Taxa de Crescimento' },
        { key: 'excedente_bruto_exploracao', label: 'EBE - Excedente Bruto de Exploração' },
        { key: 'excedente_liquido_producao', label: 'ELP - Excedente Líquido de Produção' },
      ],
    },
    {
      title: '2. Rácios do Balanço',
      metrics: [
        { key: 'racio_autonomia_financeira', label: 'RAF - Rácio de Autonomia Financeira' },
        { key: 'racio_endividamento', label: 'RE - Rácio de Endividamento' },
        { key: 'racio_solvabilidade', label: 'RS - Rácio de Solvabilidade' },
        { key: 'racio_solvabilidade_restrito', label: 'RSR - Rácio de Solvabilidade Restrito' },
      ],
    },
    {
      title: '3. Balanço Funcional',
      metrics: [
        { key: 'resumo_balanco_funcional', label: 'RBF - Resumo do Balanço Funcional' },
        { key: 'ativo_economico', label: 'AE - Ativo Económico' },
      ],
    },
    {
      title: '4. Indicadores de Longo Prazo',
      metrics: [
        { key: 'racio_estrutura', label: 'RE - Rácio de Estrutura' },
        { key: 'racio_estabilidade_financiamento', label: 'REF - Rácio de Estabilidade de Financiamento' },
        { key: 'racio_estrutura_passivo', label: 'REP - Rácio de Estrutura do Passivo' },
        { key: 'racio_cobertura_aplicacoes_fixas_recursos', label: 'RCAFR - Cobertura de Aplicações Fixas por Recursos' },
        { key: 'racio_cobertura_aplicacoes_fixas_capital', label: 'RCAFC - Cobertura de Aplicações Fixas por Capital' },
        { key: 'racio_estrutura_endividamento', label: 'REE - Rácio de Estrutura de Endividamento' },
        { key: 'racio_cobertura_gastos_financiamento', label: 'RCGF - Rácio de Cobertura dos Gastos de Financiamento' },
        { key: 'racio_gastos_financiamento', label: 'RGF - Rácio de Gastos de Financiamento' },
      ],
    },
    {
      title: '5. Rácios de Atividade (Curto Prazo)',
      metrics: [
        { key: 'rotacao_inventarios', label: 'RI - Rotação de Inventários' },
        { key: 'duracao_media_inventarios', label: 'DMI - Duração Média de Inventários (dias)' },
        { key: 'prazo_medio_recebimento', label: 'PMR - Prazo Médio de Recebimento (dias)' },
        { key: 'prazo_medio_pagamento', label: 'PMP - Prazo Médio de Pagamento (dias)' },
        { key: 'duracao_ciclo_operacional', label: 'DCO - Duração do Ciclo Operacional (dias)' },
        { key: 'duracao_ciclo_financeiro', label: 'DCF - Duração do Ciclo Financeiro (dias)' },
      ],
    },
    {
      title: '6. Rácios de Atividade (Médio/Longo Prazo)',
      metrics: [
        { key: 'rotacao_aplicacoes_fixas_liquidas_exploracao', label: 'RAFLE - Rotação das Aplicações Fixas Líquidas' },
        { key: 'rotacao_ativo_corrente', label: 'RAC - Rotação do Ativo Corrente' },
        { key: 'rotacao_capital_proprio_atividade', label: 'RCP - Rotação do Capital Próprio (Atividade)' },
        { key: 'rotacao_ativo_medio_longo', label: 'RAML - Rotação do Ativo de Médio e Longo Prazo' },
      ],
    },
    {
      title: '7. Rácios de Rentabilidade',
      metrics: [
        { key: 'return_on_assets', label: 'ROA - Rentabilidade do Ativo' },
        { key: 'return_on_equity', label: 'ROE - Rentabilidade do Capital Próprio' },
        { key: 'rentabilidade_operacional_vendas', label: 'ROV - Rentabilidade Operacional das Vendas' },
        { key: 'rentabilidade_liquida_vendas', label: 'RLV - Rentabilidade Líquida das Vendas' },
        { key: 'rendibilidade_operacional_ativo', label: 'ROPA - Rendibilidade Operacional do Ativo' },
        { key: 'rendibilidade_capital_proprio', label: 'RCP - Rendibilidade do Capital Próprio' },
        { key: 'equacao_fundamental_rendibilidade', label: 'EFR - Equação Fundamental da Rendibilidade' },
      ],
    },
    {
      title: '8. Rácios de Eficiência',
      metrics: [
        { key: 'rotacao_ativo', label: 'RAT - Rotação do Ativo Total' },
        { key: 'rotacao_ativo_fixo', label: 'RAFx - Rotação do Ativo Fixo' },
        { key: 'produtividade_ativo', label: 'PA - Produtividade do Ativo' },
        { key: 'produtividade_capital_proprio', label: 'PCP - Produtividade do Capital Próprio' },
      ],
    },
    {
      title: '9. Rácios de Liquidez',
      metrics: [
        { key: 'liquidez_geral', label: 'LG - Liquidez Geral' },
        { key: 'liquidez_reduzida', label: 'LR - Liquidez Reduzida' },
        { key: 'liquidez_imediata', label: 'LI - Liquidez Imediata' },
      ],
    },
    {
      title: '10. Rácios de Risco',
      metrics: [
        { key: 'grau_alavanca_financeira', label: 'GAF - Grau de Alavanca Financeira' },
        { key: 'grau_alavanca_operacional', label: 'GAO - Grau de Alavanca Operacional' },
        { key: 'cobertura_juros', label: 'CI - Cobertura de Juros' },
        { key: 'indice_solidez_financeira', label: 'ISF - Índice de Solidez Financeira' },
      ],
    },
    {
      title: '11. Análise DuPont & Composição',
      metrics: [
        { key: 'margem_liquida', label: 'ML - Margem Líquida' },
        { key: 'rotacao_ativo_total', label: 'RAT - Rotação do Ativo Total' },
        { key: 'roe_dupont', label: 'ROE (DuPont) - Rentabilidade do Capital Próprio' },
        { key: 'multiplicador_capital', label: 'MC - Multiplicador de Capital' },
        { key: 'leverage_financeiro', label: 'LF - Leverage Financeiro' },
        { key: 'rentabilidade_ajustada', label: 'RA - Rentabilidade Ajustada' },
        { key: 'taxa_media_juros_capital_alheio', label: 'TMJCA - Taxa Média de Juros do Capital Alheio' },
        { key: 'grau_combinado_alavanca', label: 'GCA - Grau Combinado de Alavanca' },
        { key: 'margem_seguranca', label: 'MS - Margem de Segurança' },
      ],
    },
  ];

  const handleGeneratePDF = async () => {
    if (!originalData) {
      alert('Dados originais não disponíveis para gerar PDF');
      return;
    }

    setIsGeneratingPDF(true);
    try {
      const result = await generatePDF(originalData);
      if (!result.success) {
        alert(`Erro ao gerar PDF: ${result.error}`);
      }
    } catch (error) {
      alert('Erro ao gerar PDF. Por favor, tente novamente.');
    } finally {
      setIsGeneratingPDF(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-4">
          <div className="flex-1">
            <h2 className="text-2xl md:text-3xl font-bold text-janua-navy">{empresa}</h2>
            <span className="text-xs sm:text-sm text-gray-500">
              {new Date(timestamp).toLocaleString('pt-PT')}
            </span>
          </div>
          <div className="flex flex-col sm:flex-row gap-3">
            <button
              onClick={handleGeneratePDF}
              disabled={isGeneratingPDF}
              className="bg-janua-navy text-white px-6 py-3 rounded-lg font-medium hover:bg-opacity-90 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 justify-center"
            >
              {isGeneratingPDF ? (
                <>
                  <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  A gerar PDF...
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  Gerar Relatório PDF
                </>
              )}
            </button>
          </div>
        </div>
        
        <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
          <p className="text-green-800 font-medium text-sm sm:text-base">
            Análise financeira concluída com sucesso
          </p>
        </div>

        {/* Personal Comments Section */}
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-4">
          <h3 className="font-medium text-purple-800 mb-3">Comentários Pessoais</h3>
          <p className="text-sm text-purple-700 mb-4">
            Adicione comentários que serão incluídos no relatório PDF:
          </p>
          <textarea
            placeholder="Adicione aqui os seus comentários sobre a análise financeira..."
            className="w-full px-3 py-2 border border-purple-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
            rows={4}
          />
        </div>

        {/* Edit Data Section */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-medium text-blue-800 mb-3">Editar Dados</h3>
          <p className="text-sm text-blue-700 mb-4">
            Pretende alterar algum dado e recalcular a análise?
          </p>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => window.editData && window.editData('company')}
              className="bg-white text-blue-700 border border-blue-300 px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-50 transition-all"
            >
              Editar Informações da Empresa
            </button>
            <button
              onClick={() => window.editData && window.editData('balance')}
              className="bg-white text-blue-700 border border-blue-300 px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-50 transition-all"
            >
              Editar Balanço
            </button>
            <button
              onClick={() => window.editData && window.editData('income')}
              className="bg-white text-blue-700 border border-blue-300 px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-50 transition-all"
            >
              Editar Demonstração de Resultados
            </button>
          </div>
        </div>
      </Card>

      {/* Summary Box with Key Indicators */}
      <SummaryBox metrics={metrics} />

      {metricSections.map((section) => (
        <Card key={section.title} title={section.title}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {section.metrics.map((metric) => {
              const metricData = metrics[metric.key];
              if (!metricData) return null;

              // Handle special case for resumo_balanco_funcional (dict format)
              if (metric.key === 'resumo_balanco_funcional' && metricData.status) {
                return (
                  <div key={metric.key} className="md:col-span-2">
                    <div className="bg-white border border-gray-200 rounded-lg p-4">
                      <h4 className="font-semibold text-gray-900 text-sm mb-2">{metric.label}</h4>
                      <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-sm font-medium text-blue-800">
                              Status: {metricData.status}
                            </p>
                            <p className="text-xs text-blue-600 mt-1">
                              {metricData.mensagem}
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              }

              // Use enhanced IndicatorDisplay for regular metrics
              return (
                <div key={metric.key}>
                  <IndicatorDisplay 
                    metric={{
                      ...metricData,
                      nome: metric.label
                    }} 
                  />
                </div>
              );
            })}
          </div>
        </Card>
      ))}
    </div>
  );
};

export default ResultsDisplay;
