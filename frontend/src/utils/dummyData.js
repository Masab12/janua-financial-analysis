// DUMMY DATA FOR TESTING - REMOVE BEFORE PRODUCTION
// This file contains pre-filled data to make testing easier

export const dummyData = {
  nome_entidade: "Empresa Teste Lda",
  balanco: {
    year_n: {
      // Ativo Não Corrente
      ativos_fixos_tangiveis: 150000,
      propriedades_investimento: 0,
      goodwill: 0,
      ativos_intangiveis: 5000,
      investimentos_financeiros: 3000,
      acionistas_socios_nc: 0,
      outros_ativos_financeiros: 0,
      ativos_impostos_diferidos: 0,
      outros_ativos_nao_correntes: 2000,
      
      // Ativo Corrente
      inventarios: 25000,
      clientes: 20000,
      adiantamentos_fornecedores: 0,
      estado_outros_entes_publicos_ativo: 2000,
      acionistas_socios_corrente: 0,
      outras_contas_receber: 3000,
      diferimentos_ativo: 0,
      ativos_financeiros_correntes: 0,
      outros_ativos_correntes: 0,
      caixa_depositos_bancarios: 30000,
      
      // Totais Ativo (calculados automaticamente)
      total_ativo_nao_corrente: 160000,
      total_ativo_corrente: 80000,
      total_ativo: 240000,
      
      // Capital Próprio
      capital_realizado: 50000,
      acoes_quotas_proprias: 0,
      outros_instrumentos_capital_proprio: 0,
      premios_emissao: 0,
      reservas_legais: 5000,
      outras_reservas: 10000,
      resultados_transitados: 20000,
      ajustamentos_ativos_financeiros: 0,
      excedentes_revalorizacao: 0,
      outras_variacoes_capital_proprio: 0,
      resultado_liquido_periodo: 14000,  // MUST match Income Statement!
      interesses_minoritarios: 0,
      total_capital_proprio: 99000,
      
      // Passivo Não Corrente
      provisoes_nc: 2000,
      financiamentos_obtidos_nc: 70000,
      responsabilidades_beneficios_pos_emprego: 0,
      passivos_impostos_diferidos: 0,
      outras_contas_pagar_nc: 0,
      outros_passivos_nao_correntes: 0,
      total_passivo_nao_corrente: 72000,
      
      // Passivo Corrente
      fornecedores: 40000,
      adiantamentos_clientes: 0,
      estado_outros_entes_publicos_passivo: 10000,
      acionistas_socios_passivo: 0,
      financiamentos_obtidos_corrente: 15000,
      outras_contas_pagar_corrente: 4000,
      diferimentos_passivo: 0,
      outros_passivos_correntes: 0,
      total_passivo_corrente: 69000,
      
      total_passivo: 141000,
      total_capital_passivo: 240000,
    },
    
    year_n1: {
      // Ativo Não Corrente
      ativos_fixos_tangiveis: 155000,
      propriedades_investimento: 0,
      goodwill: 0,
      ativos_intangiveis: 4000,
      investimentos_financeiros: 3000,
      acionistas_socios_nc: 0,
      outros_ativos_financeiros: 0,
      ativos_impostos_diferidos: 0,
      outros_ativos_nao_correntes: 2000,
      
      // Ativo Corrente
      inventarios: 23000,
      clientes: 22000,
      adiantamentos_fornecedores: 0,
      estado_outros_entes_publicos_ativo: 2500,
      acionistas_socios_corrente: 0,
      outras_contas_receber: 3000,
      diferimentos_ativo: 0,
      ativos_financeiros_correntes: 0,
      outros_ativos_correntes: 0,
      caixa_depositos_bancarios: 32000,
      
      total_ativo_nao_corrente: 164000,
      total_ativo_corrente: 82500,
      total_ativo: 246500,
      
      // Capital Próprio
      capital_realizado: 50000,
      acoes_quotas_proprias: 0,
      outros_instrumentos_capital_proprio: 0,
      premios_emissao: 0,
      reservas_legais: 5000,
      outras_reservas: 10000,
      resultados_transitados: 22000,
      ajustamentos_ativos_financeiros: 0,
      excedentes_revalorizacao: 0,
      outras_variacoes_capital_proprio: 0,
      resultado_liquido_periodo: 12400,  // MUST match Income Statement!
      interesses_minoritarios: 0,
      total_capital_proprio: 99400,
      
      // Passivo Não Corrente
      provisoes_nc: 2000,
      financiamentos_obtidos_nc: 68000,
      responsabilidades_beneficios_pos_emprego: 0,
      passivos_impostos_diferidos: 0,
      outras_contas_pagar_nc: 0,
      outros_passivos_nao_correntes: 0,
      total_passivo_nao_corrente: 70000,
      
      // Passivo Corrente
      fornecedores: 43000,
      adiantamentos_clientes: 0,
      estado_outros_entes_publicos_passivo: 10000,
      acionistas_socios_passivo: 0,
      financiamentos_obtidos_corrente: 18000,
      outras_contas_pagar_corrente: 6100,
      diferimentos_passivo: 0,
      outros_passivos_correntes: 0,
      total_passivo_corrente: 77100,
      
      total_passivo: 147100,
      total_capital_passivo: 246500,
    },
    
    year_n2: {
      // Ativo Não Corrente
      ativos_fixos_tangiveis: 170000,
      propriedades_investimento: 0,
      goodwill: 0,
      ativos_intangiveis: 4000,
      investimentos_financeiros: 3000,
      acionistas_socios_nc: 0,
      outros_ativos_financeiros: 0,
      ativos_impostos_diferidos: 0,
      outros_ativos_nao_correntes: 2000,
      
      // Ativo Corrente
      inventarios: 20000,
      clientes: 26000,
      adiantamentos_fornecedores: 0,
      estado_outros_entes_publicos_ativo: 3000,
      acionistas_socios_corrente: 0,
      outras_contas_receber: 4000,
      diferimentos_ativo: 0,
      ativos_financeiros_correntes: 0,
      outros_ativos_correntes: 0,
      caixa_depositos_bancarios: 38000,
      
      total_ativo_nao_corrente: 179000,
      total_ativo_corrente: 91000,
      total_ativo: 270000,
      
      // Capital Próprio
      capital_realizado: 50000,
      acoes_quotas_proprias: 0,
      outros_instrumentos_capital_proprio: 0,
      premios_emissao: 0,
      reservas_legais: 5000,
      outras_reservas: 12000,
      resultados_transitados: 25000,
      ajustamentos_ativos_financeiros: 0,
      excedentes_revalorizacao: 0,
      outras_variacoes_capital_proprio: 0,
      resultado_liquido_periodo: 10000,  // MUST match Income Statement!
      interesses_minoritarios: 0,
      total_capital_proprio: 102000,
      
      // Passivo Não Corrente
      provisoes_nc: 3000,
      financiamentos_obtidos_nc: 77000,
      responsabilidades_beneficios_pos_emprego: 0,
      passivos_impostos_diferidos: 0,
      outras_contas_pagar_nc: 0,
      outros_passivos_nao_correntes: 0,
      total_passivo_nao_corrente: 80000,
      
      // Passivo Corrente
      fornecedores: 45000,
      adiantamentos_clientes: 0,
      estado_outros_entes_publicos_passivo: 10000,
      acionistas_socios_passivo: 0,
      financiamentos_obtidos_corrente: 20000,
      outras_contas_pagar_corrente: 13000,
      diferimentos_passivo: 0,
      outros_passivos_correntes: 0,
      total_passivo_corrente: 88000,
      
      total_passivo: 168000,
      total_capital_passivo: 270000,
    },
  },
  
  demonstracao_resultados: {
    year_n: {
      // Rendimentos
      vendas_servicos_prestados: 410000,
      subsidios_exploracao: 2000,
      ganhos_perdas_subsidiarias: 0,
      variacao_inventarios_producao: 1000,
      trabalhos_propria_entidade: 0,
      outros_rendimentos_ganhos: 3000,
      
      // Gastos
      cmvmc: 250000,
      fornecimentos_servicos_externos: 60000,
      gastos_pessoal: 70000,
      imparidade_inventarios: 0,
      imparidade_dividas_receber: 500,
      provisoes: 0,
      imparidade_investimentos_nao_depreciavel: 0,
      aumentos_reducoes_justo_valor: 0,
      outros_gastos_perdas: 3000,
      gastos_depreciacao_amortizacao: 10000,
      imparidade_ativos_depreciacao: 0,
      
      // Juros (only these fields, results are computed by backend)
      juros_rendimentos_obtidos: 500,
      juros_gastos_suportados: 4000,
      imposto_rendimento: 5000,
    },
    
    year_n1: {
      // Rendimentos
      vendas_servicos_prestados: 395000,
      subsidios_exploracao: 1500,
      ganhos_perdas_subsidiarias: 0,
      variacao_inventarios_producao: 800,
      trabalhos_propria_entidade: 0,
      outros_rendimentos_ganhos: 2000,
      
      // Gastos
      cmvmc: 245000,
      fornecimentos_servicos_externos: 55000,
      gastos_pessoal: 68000,
      imparidade_inventarios: 0,
      imparidade_dividas_receber: 400,
      provisoes: 0,
      imparidade_investimentos_nao_depreciavel: 0,
      aumentos_reducoes_justo_valor: 0,
      outros_gastos_perdas: 2000,
      gastos_depreciacao_amortizacao: 9000,
      imparidade_ativos_depreciacao: 0,
      
      // Juros (only these fields, results are computed by backend)
      juros_rendimentos_obtidos: 300,
      juros_gastos_suportados: 3800,
      imposto_rendimento: 4000,
    },
    
    year_n2: {
      // Rendimentos
      vendas_servicos_prestados: 380000,
      subsidios_exploracao: 1200,
      ganhos_perdas_subsidiarias: 0,
      variacao_inventarios_producao: 600,
      trabalhos_propria_entidade: 0,
      outros_rendimentos_ganhos: 2000,
      
      // Gastos
      cmvmc: 240000,
      fornecimentos_servicos_externos: 52000,
      gastos_pessoal: 65000,
      imparidade_inventarios: 0,
      imparidade_dividas_receber: 300,
      provisoes: 0,
      imparidade_investimentos_nao_depreciavel: 0,
      aumentos_reducoes_justo_valor: 0,
      outros_gastos_perdas: 2000,
      gastos_depreciacao_amortizacao: 8000,
      imparidade_ativos_depreciacao: 0,
      
      // Juros (only these fields, results are computed by backend)
      juros_rendimentos_obtidos: 200,
      juros_gastos_suportados: 3500,
      imposto_rendimento: 3200,
    },
  },
};
