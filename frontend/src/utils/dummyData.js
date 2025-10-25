/**
 * Realistic dummy data for testing and demonstration purposes
 * Based on a typical Portuguese SME in the retail sector
 */

export const dummyFinancialData = {
  company_info: {
    nome_empresa: "Comercial Portuguesa Lda",
    setor_atividade: "Comércio a Retalho de Produtos Alimentares",
    objetivo_empresa: "Análise de viabilidade para expansão e abertura de nova loja",
    email_empresario: "gestor@comercialportuguesa.pt"
  },
  balanco: {
    year_n2: {
      // Ativo Não Corrente
      ativos_fixos_tangiveis: 185000,
      propriedades_investimento: 0,
      goodwill: 0,
      ativos_intangiveis: 8500,
      investimentos_financeiros: 0,
      acionistas_socios_nc: 0,
      outros_ativos_financeiros: 0,
      ativos_impostos_diferidos: 0,
      outros_ativos_nao_correntes: 0,
      
      // Ativo Corrente
      inventarios: 45000,
      clientes: 32000,
      adiantamentos_fornecedores: 2500,
      estado_outros_entes_publicos_ativo: 4200,
      acionistas_socios_corrente: 0,
      outras_contas_receber: 1800,
      diferimentos_ativo: 800,
      ativos_financeiros_correntes: 0,
      outros_ativos_correntes: 0,
      caixa_depositos_bancarios: 28000,
      
      // Capital Próprio
      capital_realizado: 75000,
      acoes_quotas_proprias: 0,
      outros_instrumentos_capital_proprio: 0,
      premios_emissao: 0,
      reservas_legais: 15000,
      outras_reservas: 25000,
      resultados_transitados: 45000,
      ajustamentos_ativos_financeiros: 0,
      excedentes_revalorizacao: 0,
      outras_variacoes_capital_proprio: 0,
      resultado_liquido_periodo: 29821, // Net result for year N-2
      interesses_minoritarios: 0,
      
      // Passivo Não Corrente
      provisoes_nc: 0,
      financiamentos_obtidos_nc: 62000,
      responsabilidades_beneficios_pos_emprego: 0,
      passivos_impostos_diferidos: 0,
      outras_contas_pagar_nc: 0,
      outros_passivos_nao_correntes: 0,
      
      // Passivo Corrente
      fornecedores: 38000,
      adiantamentos_clientes: 1200,
      estado_outros_entes_publicos_passivo: 8500,
      acionistas_socios_passivo: 0,
      financiamentos_obtidos_corrente: 22000,
      outras_contas_pagar_corrente: 15000,
      diferimentos_passivo: 1100,
      outros_passivos_correntes: 0
    },
    year_n1: {
      // Ativo Não Corrente
      ativos_fixos_tangiveis: 178000,
      propriedades_investimento: 0,
      goodwill: 0,
      ativos_intangiveis: 7800,
      investimentos_financeiros: 0,
      acionistas_socios_nc: 0,
      outros_ativos_financeiros: 0,
      ativos_impostos_diferidos: 0,
      outros_ativos_nao_correntes: 0,
      
      // Ativo Corrente
      inventarios: 48500,
      clientes: 35000,
      adiantamentos_fornecedores: 2800,
      estado_outros_entes_publicos_ativo: 3800,
      acionistas_socios_corrente: 0,
      outras_contas_receber: 2100,
      diferimentos_ativo: 600,
      ativos_financeiros_correntes: 0,
      outros_ativos_correntes: 0,
      caixa_depositos_bancarios: 32000,
      
      // Capital Próprio
      capital_realizado: 75000,
      acoes_quotas_proprias: 0,
      outros_instrumentos_capital_proprio: 0,
      premios_emissao: 0,
      reservas_legais: 15000,
      outras_reservas: 25000,
      resultados_transitados: 70000,
      ajustamentos_ativos_financeiros: 0,
      excedentes_revalorizacao: 0,
      outras_variacoes_capital_proprio: 0,
      resultado_liquido_periodo: -921, // Net result for year N-1 (negative)
      interesses_minoritarios: 0,
      
      // Passivo Não Corrente
      provisoes_nc: 0,
      financiamentos_obtidos_nc: 55000,
      responsabilidades_beneficios_pos_emprego: 0,
      passivos_impostos_diferidos: 0,
      outras_contas_pagar_nc: 0,
      outros_passivos_nao_correntes: 0,
      
      // Passivo Corrente
      fornecedores: 42000,
      adiantamentos_clientes: 1500,
      estado_outros_entes_publicos_passivo: 9200,
      acionistas_socios_passivo: 0,
      financiamentos_obtidos_corrente: 20000,
      outras_contas_pagar_corrente: 9700,
      diferimentos_passivo: 1400,
      outros_passivos_correntes: 0
    },
    year_n: {
      // Ativo Não Corrente
      ativos_fixos_tangiveis: 172000,
      propriedades_investimento: 0,
      goodwill: 0,
      ativos_intangiveis: 7200,
      investimentos_financeiros: 0,
      acionistas_socios_nc: 0,
      outros_ativos_financeiros: 0,
      ativos_impostos_diferidos: 0,
      outros_ativos_nao_correntes: 0,
      
      // Ativo Corrente
      inventarios: 52000,
      clientes: 38000,
      adiantamentos_fornecedores: 3200,
      estado_outros_entes_publicos_ativo: 3500,
      acionistas_socios_corrente: 0,
      outras_contas_receber: 2400,
      diferimentos_ativo: 700,
      ativos_financeiros_correntes: 0,
      outros_ativos_correntes: 0,
      caixa_depositos_bancarios: 35000,
      
      // Capital Próprio
      capital_realizado: 75000,
      acoes_quotas_proprias: 0,
      outros_instrumentos_capital_proprio: 0,
      premios_emissao: 0,
      reservas_legais: 15000,
      outras_reservas: 25000,
      resultados_transitados: 95000,
      ajustamentos_ativos_financeiros: 0,
      excedentes_revalorizacao: 0,
      outras_variacoes_capital_proprio: 0,
      resultado_liquido_periodo: 24634, // Net result for year N
      interesses_minoritarios: 0,
      
      // Passivo Não Corrente
      provisoes_nc: 0,
      financiamentos_obtidos_nc: 48000,
      responsabilidades_beneficios_pos_emprego: 0,
      passivos_impostos_diferidos: 0,
      outras_contas_pagar_nc: 0,
      outros_passivos_nao_correntes: 0,
      
      // Passivo Corrente
      fornecedores: 45000,
      adiantamentos_clientes: 1800,
      estado_outros_entes_publicos_passivo: 7800,
      acionistas_socios_passivo: 0,
      financiamentos_obtidos_corrente: 18000,
      outras_contas_pagar_corrente: 1000,
      diferimentos_passivo: 1200,
      outros_passivos_correntes: 0
    }
  },
  demonstracao_resultados: {
    year_n2: {
      vendas_servicos_prestados: 420000,
      subsidios_exploracao: 0,
      ganhos_perdas_subsidiarias: 0,
      variacao_inventarios_producao: 0,
      trabalhos_propria_entidade: 0,
      cmvmc: 252000, // 60% of sales
      fornecimentos_servicos_externos: 58800, // 14% of sales
      gastos_pessoal: 84000, // 20% of sales
      imparidade_inventarios: 0,
      imparidade_dividas_receber: 0,
      provisoes: 0,
      imparidade_investimentos_nao_depreciaveis: 0,
      aumentos_reducoes_justo_valor: 0,
      outros_rendimentos_ganhos: 8400, // 2% of sales
      outros_gastos_perdas: 4200, // 1% of sales
      gastos_depreciacoes_amortizacoes: 18500,
      juros_rendimentos_obtidos: 0,
      juros_gastos_suportados: 6200,
      imposto_rendimento: 1200
    },
    year_n1: {
      vendas_servicos_prestados: 450000,
      subsidios_exploracao: 0,
      ganhos_perdas_subsidiarias: 0,
      variacao_inventarios_producao: 0,
      trabalhos_propria_entidade: 0,
      cmvmc: 270000, // 60% of sales
      fornecimentos_servicos_externos: 63000, // 14% of sales
      gastos_pessoal: 90000, // 20% of sales
      imparidade_inventarios: 0,
      imparidade_dividas_receber: 0,
      provisoes: 0,
      imparidade_investimentos_nao_depreciaveis: 0,
      aumentos_reducoes_justo_valor: 0,
      outros_rendimentos_ganhos: 9000, // 2% of sales
      outros_gastos_perdas: 4500, // 1% of sales
      gastos_depreciacoes_amortizacoes: 19200,
      juros_rendimentos_obtidos: 0,
      juros_gastos_suportados: 5800,
      imposto_rendimento: 1500
    },
    year_n: {
      vendas_servicos_prestados: 485000,
      subsidios_exploracao: 0,
      ganhos_perdas_subsidiarias: 0,
      variacao_inventarios_producao: 0,
      trabalhos_propria_entidade: 0,
      cmvmc: 291000, // 60% of sales
      fornecimentos_servicos_externos: 67900, // 14% of sales
      gastos_pessoal: 97000, // 20% of sales
      imparidade_inventarios: 0,
      imparidade_dividas_receber: 0,
      provisoes: 0,
      imparidade_investimentos_nao_depreciaveis: 0,
      aumentos_reducoes_justo_valor: 0,
      outros_rendimentos_ganhos: 9700, // 2% of sales
      outros_gastos_perdas: 4850, // 1% of sales
      gastos_depreciacoes_amortizacoes: 17800,
      juros_rendimentos_obtidos: 0,
      juros_gastos_suportados: 5400,
      imposto_rendimento: 2800
    }
  }
};

/**
 * Get dummy data with Portuguese number formatting for display
 */
export const getDummyDataFormatted = () => {
  const formatNumber = (num) => {
    if (num === 0) return "0,00";
    return num.toLocaleString('pt-PT', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  };

  const formatData = (obj) => {
    const formatted = {};
    for (const [key, value] of Object.entries(obj)) {
      if (typeof value === 'object' && value !== null) {
        formatted[key] = formatData(value);
      } else if (typeof value === 'number') {
        formatted[key] = formatNumber(value);
      } else {
        formatted[key] = value;
      }
    }
    return formatted;
  };

  return formatData(dummyFinancialData);
};

/**
 * Validate that dummy data creates a balanced balance sheet
 */
export const validateDummyData = () => {
  const validation = {
    isValid: true,
    errors: [],
    balanceChecks: {}
  };

  ['year_n2', 'year_n1', 'year_n'].forEach(year => {
    const balance = dummyFinancialData.balanco[year];
    
    // Calculate totals
    const totalAssets = 
      balance.ativos_fixos_tangiveis + balance.ativos_intangiveis +
      balance.inventarios + balance.clientes + balance.adiantamentos_fornecedores +
      balance.estado_outros_entes_publicos_ativo + balance.outras_contas_receber +
      balance.diferimentos_ativo + balance.caixa_depositos_bancarios;
    
    const totalEquity = 
      balance.capital_realizado + balance.reservas_legais + balance.outras_reservas +
      balance.resultados_transitados;
    
    const totalLiabilities = 
      balance.financiamentos_obtidos_nc + balance.fornecedores +
      balance.adiantamentos_clientes + balance.estado_outros_entes_publicos_passivo +
      balance.financiamentos_obtidos_corrente + balance.outras_contas_pagar_corrente +
      balance.diferimentos_passivo;
    
    const difference = Math.abs(totalAssets - (totalEquity + totalLiabilities));
    
    validation.balanceChecks[year] = {
      totalAssets,
      totalEquity,
      totalLiabilities,
      difference,
      isBalanced: difference < 1000
    };
    
    if (difference >= 1000) {
      validation.isValid = false;
      validation.errors.push(`${year}: Balance equation not satisfied (difference: €${difference.toLocaleString('pt-PT')})`);
    }
  });

  return validation;
};