from app.models.balance_sheet import BalanceSheet
from app.models.income_statement import IncomeStatement
from app.models.financial_data import MetricValue, PerformanceMetrics
from datetime import datetime

class FinancialCalculator:
    """
    Implementa todos os cálculos do Excel (sheet Performance).
    Fórmulas baseadas 100% no ficheiro Excel fornecido pelo cliente.
    """
    
    def __init__(self, balanco: BalanceSheet, demonstracao: IncomeStatement):
        self.bs = balanco
        self.dr = demonstracao
    
    def calculate_all(self) -> PerformanceMetrics:
        """Calcula TODAS as 51 métricas do Excel Performance sheet"""
        
        return PerformanceMetrics(
            # ========== Dimensão / Produção (6) ==========
            consumos_intermedios=self._calc_consumos_intermedios(),
            valor_bruto_producao=self._calc_valor_bruto_producao(),
            valor_acrescentado_bruto=self._calc_valor_acrescentado_bruto(),
            taxa_crescimento=self._calc_taxa_crescimento(),
            excedente_bruto_exploracao=self._calc_excedente_bruto_exploracao(),
            excedente_liquido_producao=self._calc_excedente_liquido_producao(),
            
            # ========== Rácios do Balanço (4) ==========
            racio_autonomia_financeira=self._calc_autonomia_financeira(),
            racio_endividamento=self._calc_endividamento(),
            racio_solvabilidade=self._calc_solvabilidade(),
            racio_solvabilidade_restrito=self._calc_solvabilidade_restrito(),
            
            # ========== Balanço Funcional (2) ==========
            resumo_balanco_funcional=self._calc_resumo_balanco_funcional(),
            ativo_economico=self._calc_ativo_economico(),
            
            # ========== Indicadores Longo Prazo (8) ==========
            racio_estrutura=self._calc_racio_estrutura(),
            racio_estabilidade_financiamento=self._calc_estabilidade_financiamento(),
            racio_estrutura_passivo=self._calc_estrutura_passivo(),
            racio_cobertura_aplicacoes_fixas_recursos=self._calc_cobertura_aplicacoes_recursos(),
            racio_cobertura_aplicacoes_fixas_capital=self._calc_cobertura_aplicacoes_capital(),
            racio_estrutura_endividamento=self._calc_estrutura_endividamento(),
            racio_cobertura_gastos_financiamento=self._calc_cobertura_gastos_financiamento(),
            racio_gastos_financiamento=self._calc_gastos_financiamento(),
            
            # ========== Rácios de Atividade (6) ==========
            rotacao_inventarios=self._calc_rotacao_inventarios(),
            duracao_media_inventarios=self._calc_duracao_media_inventarios(),
            prazo_medio_recebimento=self._calc_prazo_medio_recebimento(),
            prazo_medio_pagamento=self._calc_prazo_medio_pagamento(),
            duracao_ciclo_operacional=self._calc_duracao_ciclo_operacional(),
            duracao_ciclo_financeiro=self._calc_duracao_ciclo_financeiro(),
            
            # ========== Rácios de Atividade Médio/Longo Prazo (4) ==========
            rotacao_aplicacoes_fixas_liquidas_exploracao=self._calc_rotacao_aplicacoes_fixas_liquidas_exploracao(),
            rotacao_ativo_corrente=self._calc_rotacao_ativo_corrente(),
            rotacao_capital_proprio_atividade=self._calc_rotacao_capital_proprio_atividade(),
            rotacao_ativo_medio_longo=self._calc_rotacao_ativo_medio_longo(),
            
            # ========== Rentabilidade (7) ==========
            return_on_assets=self._calc_return_on_assets(),
            return_on_equity=self._calc_return_on_equity(),
            rentabilidade_operacional_vendas=self._calc_rentabilidade_operacional_vendas(),
            rentabilidade_liquida_vendas=self._calc_rentabilidade_liquida_vendas(),
            rendibilidade_operacional_ativo=self._calc_rendibilidade_operacional_ativo(),
            rendibilidade_capital_proprio=self._calc_rendibilidade_capital_proprio(),
            equacao_fundamental_rendibilidade=self._calc_equacao_fundamental_rendibilidade(),
            
            # ========== Eficiência (4) ==========
            rotacao_ativo=self._calc_rotacao_ativo(),
            rotacao_ativo_fixo=self._calc_rotacao_ativo_fixo(),
            produtividade_ativo=self._calc_produtividade_ativo(),
            produtividade_capital_proprio=self._calc_produtividade_capital_proprio(),
            
            # ========== Liquidez (3) ==========
            liquidez_geral=self._calc_liquidez_geral(),
            liquidez_reduzida=self._calc_liquidez_reduzida(),
            liquidez_imediata=self._calc_liquidez_imediata(),
            
            # ========== Risco (4) ==========
            grau_alavanca_financeira=self._calc_grau_alavanca_financeira(),
            grau_alavanca_operacional=self._calc_grau_alavanca_operacional(),
            cobertura_juros=self._calc_cobertura_juros(),
            indice_solidez_financeira=self._calc_indice_solidez_financeira(),
            
            # ========== Análise DuPont & Composição (9) ==========
            margem_liquida=self._calc_margem_liquida(),
            rotacao_ativo_total=self._calc_rotacao_ativo_total(),
            roe_dupont=self._calc_roe_dupont(),
            multiplicador_capital=self._calc_multiplicador_capital(),
            leverage_financeiro=self._calc_leverage_financeiro(),
            rentabilidade_ajustada=self._calc_rentabilidade_ajustada(),
            taxa_media_juros_capital_alheio=self._calc_taxa_media_juros_capital_alheio(),
            grau_combinado_alavanca=self._calc_grau_combinado_alavanca(),
            margem_seguranca=self._calc_margem_seguranca()
        )
    
    # Dimensão / Produção
    
    def _calc_consumos_intermedios(self) -> MetricValue:
        """
        CI = CMVMC + FSE + Outros Gastos e Perdas
        Excel: ='DR'!K13+'DR'!K14+'DR'!E28
        FIXED: Added outros_gastos_perdas component
        """
        n = (self.dr.year_n.cmvmc + 
             self.dr.year_n.fornecimentos_servicos_externos +
             self.dr.year_n.outros_gastos_perdas)
        n1 = (self.dr.year_n1.cmvmc + 
              self.dr.year_n1.fornecimentos_servicos_externos +
              self.dr.year_n1.outros_gastos_perdas)
        n2 = (self.dr.year_n2.cmvmc + 
              self.dr.year_n2.fornecimentos_servicos_externos +
              self.dr.year_n2.outros_gastos_perdas)
        
        return MetricValue(
            nome="Consumos intermédios (CI)",
            unidade="€",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao=self._get_ci_interpretation(n, n1, n2)
        )
    
    def _calc_valor_bruto_producao(self) -> MetricValue:
        """
        VBP = Vendas + Variação Inventários + Trabalhos Próprios + Subsídios + Outros Rendimentos
        Excel: ='DR'!E5+'DR'!E8+'DR'!E9+'DR'!E6+'DR'!E18
        """
        n = (self.dr.year_n.vendas_servicos_prestados +
             self.dr.year_n.variacao_inventarios_producao +
             self.dr.year_n.trabalhos_propria_entidade +
             self.dr.year_n.subsidios_exploracao +
             self.dr.year_n.outros_rendimentos_ganhos)
        
        n1 = (self.dr.year_n1.vendas_servicos_prestados +
              self.dr.year_n1.variacao_inventarios_producao +
              self.dr.year_n1.trabalhos_propria_entidade +
              self.dr.year_n1.subsidios_exploracao +
              self.dr.year_n1.outros_rendimentos_ganhos)
        
        n2 = (self.dr.year_n2.vendas_servicos_prestados +
              self.dr.year_n2.variacao_inventarios_producao +
              self.dr.year_n2.trabalhos_propria_entidade +
              self.dr.year_n2.subsidios_exploracao +
              self.dr.year_n2.outros_rendimentos_ganhos)
        
        return MetricValue(
            nome="Valor Bruto de Produção (VBP)",
            unidade="€",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao=self._get_vbp_interpretation(n, n1, n2)
        )
    
    def _calc_valor_acrescentado_bruto(self) -> MetricValue:
        """
        VAB = VBP - CI
        Excel: =J4-J3
        """
        vbp = self._calc_valor_bruto_producao()
        ci = self._calc_consumos_intermedios()
        
        n = vbp.year_n - ci.year_n
        n1 = vbp.year_n1 - ci.year_n1
        n2 = vbp.year_n2 - ci.year_n2
        
        return MetricValue(
            nome="Valor Acrescentado Bruto (VAB)",
            unidade="€",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao=self._get_vab_interpretation(n, n1, n2)
        )
    
    def _calc_taxa_crescimento(self) -> MetricValue:
        """
        Taxa de crescimento entre N+1 e N+2
        Excel: =(K5-J5)/J5 where row 5 is VAB
        FIXED: Now uses VAB instead of partial VBP
        """
        vab = self._calc_valor_acrescentado_bruto()
        
        if vab.year_n1 != 0:
            tc = (vab.year_n2 - vab.year_n1) / vab.year_n1
        else:
            tc = 0
        
        return MetricValue(
            nome="Taxa de Crescimento (TC)",
            unidade="%",
            year_n=0,
            year_n1=0,
            year_n2=tc * 100,
            tendencia="▲" if tc > 0 else ("▼" if tc < 0 else "▶"),
            interpretacao=self._get_tc_interpretation(tc)
        )
    
    def _calc_excedente_bruto_exploracao(self) -> MetricValue:
        """
        EBE = EBITDA (calculado na demonstração de resultados)
        Excel formula complexa envolvendo vários campos
        """
        n = self.dr.year_n.ebitda
        n1 = self.dr.year_n1.ebitda
        n2 = self.dr.year_n2.ebitda
        
        return MetricValue(
            nome="Excedente Bruto de Exploração (EBE)",
            unidade="€",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao=self._get_ebe_interpretation(n, n1, n2)
        )
    
    def _calc_excedente_liquido_producao(self) -> MetricValue:
        """
        ELP = Resultado Operacional + Imparidades (inventários + dívidas + investimentos) + Outros Gastos
        Excel Row 6: ='DR'!E25+'DR'!E13+'DR'!E14+'DR'!E16+'DR'!E17
        E25 = EBIT, E13 = Imparidade inventários, E14 = Imparidade dívidas,
        E16 = Imparidade investimentos, E17 = Outros gastos
        """
        n = (self.dr.year_n.ebit +
             self.dr.year_n.imparidade_inventarios +
             self.dr.year_n.imparidade_dividas_receber +
             self.dr.year_n.imparidade_investimentos_nao_depreciaveis +
             self.dr.year_n.outros_gastos_perdas)
        
        n1 = (self.dr.year_n1.ebit +
              self.dr.year_n1.imparidade_inventarios +
              self.dr.year_n1.imparidade_dividas_receber +
              self.dr.year_n1.imparidade_investimentos_nao_depreciaveis +
              self.dr.year_n1.outros_gastos_perdas)
        
        n2 = (self.dr.year_n2.ebit +
              self.dr.year_n2.imparidade_inventarios +
              self.dr.year_n2.imparidade_dividas_receber +
              self.dr.year_n2.imparidade_investimentos_nao_depreciaveis +
              self.dr.year_n2.outros_gastos_perdas)
        
        return MetricValue(
            nome="Excedente Líquido de Produção (ELP)",
            unidade="€",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1), # Fixed: Added trend
            interpretacao=self._get_elp_interpretation(n, n1, n2) # Fixed: Corrected interpretacao
        )
    
    # Rácios do Balanço
    
    def _calc_autonomia_financeira(self) -> MetricValue:
        """
        RAF = Capital Próprio / Total Ativo
        Excel: =BS!E47/BS!E30
        """
        n = self._safe_divide(self.bs.year_n.total_capital_proprio, #   Fixed: Corrected numerator
                              self.bs.year_n.total_ativo)
        n1 = self._safe_divide(self.bs.year_n1.total_capital_proprio, 
                               self.bs.year_n1.total_ativo)
        n2 = self._safe_divide(self.bs.year_n2.total_capital_proprio, 
                               self.bs.year_n2.total_ativo)
        
        return MetricValue(
            nome="Rácio de Autonomia Financeira (RAF)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao=self._get_raf_interpretation(n2)
        )
    
    def _calc_endividamento(self) -> MetricValue:
        """
        RE = Passivo / Ativo
        """
        n = self._safe_divide(self.bs.year_n.total_passivo, 
                              self.bs.year_n.total_ativo)
        n1 = self._safe_divide(self.bs.year_n1.total_passivo, 
                               self.bs.year_n1.total_ativo)
        n2 = self._safe_divide(self.bs.year_n2.total_passivo, 
                               self.bs.year_n2.total_ativo)
        
        return MetricValue(
            nome="Rácio de Endividamento (RE)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao=self._get_re_interpretation(n2)
        )
    
    def _calc_solvabilidade(self) -> MetricValue:
        """
        RS = Capital Próprio / Passivo
        Excel: =BS!E47/BS!E68
        """
        n = self._safe_divide(self.bs.year_n.total_capital_proprio, 
                              self.bs.year_n.total_passivo)
        n1 = self._safe_divide(self.bs.year_n1.total_capital_proprio, 
                               self.bs.year_n1.total_passivo)
        n2 = self._safe_divide(self.bs.year_n2.total_capital_proprio, 
                               self.bs.year_n2.total_passivo)
        
        return MetricValue(
            nome="Rácio de Solvabilidade (RS)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao=self._get_rs_interpretation(n2)
        )
    
    def _calc_solvabilidade_restrito(self) -> MetricValue:
        """
        RSSR = Ativo / Passivo
        Excel: =BS!E30/BS!E68
        """
        n = self._safe_divide(self.bs.year_n.total_ativo, 
                              self.bs.year_n.total_passivo)
        n1 = self._safe_divide(self.bs.year_n1.total_ativo, 
                               self.bs.year_n1.total_passivo)
        n2 = self._safe_divide(self.bs.year_n2.total_ativo, 
                               self.bs.year_n2.total_passivo)
        
        return MetricValue(
            nome="Rácio de Solvabilidade em Sentido Restrito (RSSR)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao=self._get_rssr_interpretation(n2)
        )
    
    def _calc_resumo_balanco_funcional(self) -> dict:
        """
        Análise do Balanço Funcional
        Based on Excel logic: checks FM, NFM, and Tesouraria
        Returns: Bom, Médio, or Mau
        """
        # Calculate Fundo de Maneio (FM) = Ativo Corrente - Passivo Corrente
        fm = self.bs.year_n.total_ativo_corrente - self.bs.year_n.total_passivo_corrente
        
        # Calculate NFM (Necessidades Fundo Maneio) = Inventários + Clientes - Fornecedores
        nfm = (self.bs.year_n.inventarios + 
               self.bs.year_n.clientes - 
               self.bs.year_n.fornecedores)
        
        # Calculate Tesouraria = FM - NFM
        tesouraria = fm - nfm
        
        # Determine status based on Excel logic
        # Bom: FM > 0, NFM < 0, Tesouraria > 0 OR FM > 0, NFM > 0, Tesouraria > 0
        # Médio: FM > 0, NFM > 0, Tesouraria < 0 OR FM < 0, NFM < 0, Tesouraria > 0
        # Mau: Otherwise
        
        if fm > 0 and nfm < 0 and tesouraria > 0:
            status = "Bom"
            mensagem = "Situação financeira muito favorável: necessidades operacionais cobertas e excedente financeiro disponível."
        elif fm > 0 and nfm > 0 and tesouraria > 0:
            status = "Bom"
            mensagem = "Situação financeira equilibrada, com fundo de maneio suficiente para cobrir as necessidades operacionais."
        elif fm > 0 and nfm > 0 and tesouraria < 0:
            status = "Médio"
            mensagem = "Fundo de maneio positivo, mas insuficiente. Empresa depende parcialmente de financiamentos bancários."
        elif fm < 0 and nfm < 0 and tesouraria > 0:
            status = "Médio"
            mensagem = "Situação financeira razoável, com necessidades operacionais cobertas, mas risco devido a recursos estáveis insuficientes."
        elif fm < 0 and nfm > 0 and tesouraria < 0:
            status = "Mau"
            mensagem = "Situação financeira delicada: recursos estáveis insuficientes e elevada dependência de financiamentos de curto prazo."
        elif fm < 0 and nfm < 0 and tesouraria < 0:
            status = "Mau"
            mensagem = "Situação financeira crítica, com desequilíbrio elevado: fundo de maneio negativo e tesouraria deficitária. Risco iminente de incapacidade em cumprir compromissos financeiros."
        else:
            status = "Mau"
            mensagem = "Situação financeira crítica, com desequilíbrio elevado: fundo de maneio negativo e tesouraria deficitária. Risco iminente de incapacidade em cumprir compromissos financeiros."
        
        return {
            "status": status,
            "mensagem": mensagem
        }
    
    def _calc_ativo_economico(self) -> MetricValue:
        """Ativo Económico = Ativo Não Corrente + NFM"""
        n = self.bs.year_n.total_ativo_nao_corrente
        n1 = self.bs.year_n1.total_ativo_nao_corrente
        n2 = self.bs.year_n2.total_ativo_nao_corrente
        
        return MetricValue(
            nome="Ativo Económico",
            unidade="€",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1)
        )
    
    # Indicadores de Longo Prazo
    
    def _calc_racio_estrutura(self) -> MetricValue:
        """
        RDE = Passivo / Capital Próprio
        Excel: =BS!E50/BS!E47
        """
        n = self._safe_divide(self.bs.year_n.total_passivo, 
                              self.bs.year_n.total_capital_proprio)
        n1 = self._safe_divide(self.bs.year_n1.total_passivo, 
                               self.bs.year_n1.total_capital_proprio)
        n2 = self._safe_divide(self.bs.year_n2.total_passivo, 
                               self.bs.year_n2.total_capital_proprio)
        
        return MetricValue(
            nome="Rácio de Estrutura (RDE)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao=self._get_rde_interpretation(n, n1, n2)
        )
    
    def _calc_estabilidade_financiamento(self) -> MetricValue:
        """REF = Capitais Permanentes / Ativo Total"""
        # Capitais Permanentes = Capital Próprio + Passivo Não Corrente
        n_cap_perm = self.bs.year_n.total_capital_proprio + self.bs.year_n.total_passivo_nao_corrente
        n1_cap_perm = self.bs.year_n1.total_capital_proprio + self.bs.year_n1.total_passivo_nao_corrente
        n2_cap_perm = self.bs.year_n2.total_capital_proprio + self.bs.year_n2.total_passivo_nao_corrente
        
        n = self._safe_divide(n_cap_perm, self.bs.year_n.total_ativo)
        n1 = self._safe_divide(n1_cap_perm, self.bs.year_n1.total_ativo)
        n2 = self._safe_divide(n2_cap_perm, self.bs.year_n2.total_ativo)
        
        return MetricValue(
            nome="Rácio de Estabilidade de Financiamento (REF)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao=self._get_ref_interpretation(n, n1, n2)
        )
    
    def _calc_estrutura_passivo(self) -> MetricValue:
        """REP = Passivo Corrente / Passivo Não Corrente"""
        n = self._safe_divide(self.bs.year_n.total_passivo_corrente, 
                              self.bs.year_n.total_passivo_nao_corrente)
        n1 = self._safe_divide(self.bs.year_n1.total_passivo_corrente, 
                               self.bs.year_n1.total_passivo_nao_corrente)
        n2 = self._safe_divide(self.bs.year_n2.total_passivo_corrente, 
                               self.bs.year_n2.total_passivo_nao_corrente)
        
        return MetricValue(
            nome="Rácio de Estrutura do Passivo (REP)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao=self._get_rep_interpretation(n, n1, n2)
        )
    
    def _calc_cobertura_aplicacoes_recursos(self) -> MetricValue:
        """RCAFLRE - Cobertura de Aplicações Fixas por Recursos Estáveis"""
        # Recursos Estáveis = Capital Próprio + Passivo NC
        # Aplicações Fixas = Ativo NC
        
        n_rec = self.bs.year_n.total_capital_proprio + self.bs.year_n.total_passivo_nao_corrente
        n1_rec = self.bs.year_n1.total_capital_proprio + self.bs.year_n1.total_passivo_nao_corrente
        n2_rec = self.bs.year_n2.total_capital_proprio + self.bs.year_n2.total_passivo_nao_corrente
        
        n = self._safe_divide(n_rec, self.bs.year_n.total_ativo_nao_corrente)
        n1 = self._safe_divide(n1_rec, self.bs.year_n1.total_ativo_nao_corrente)
        n2 = self._safe_divide(n2_rec, self.bs.year_n2.total_ativo_nao_corrente)
        
        return MetricValue(
            nome="Rácio de Cobertura das Aplicações Fixas Líquidas por Recursos Estáveis (RCAFLRE)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao=self._get_rcaflre_interpretation(n, n1, n2)
        )
    
    def _calc_cobertura_aplicacoes_capital(self) -> MetricValue:
        """RCAFLCP - Cobertura de Aplicações Fixas por Capital Próprio"""
        n = self._safe_divide(self.bs.year_n.total_capital_proprio, 
                              self.bs.year_n.total_ativo_nao_corrente)
        n1 = self._safe_divide(self.bs.year_n1.total_capital_proprio, 
                               self.bs.year_n1.total_ativo_nao_corrente)
        n2 = self._safe_divide(self.bs.year_n2.total_capital_proprio, 
                               self.bs.year_n2.total_ativo_nao_corrente)
        
        return MetricValue(
            nome="Rácio de Cobertura das Aplicações Fixas Líquidas por Capital Próprio (RCAFLCP)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao=self._get_rcaflcp_interpretation(n, n1, n2)
        )
    
    # Helper methods
    
    def _safe_divide(self, numerator: float, denominator: float) -> float:
        """Safe division to avoid divide by zero"""
        if denominator == 0:
            return 0.0
        return numerator / denominator
    
    def _get_trend(self, current: float, previous: float, lower_is_better: bool = False) -> str:
        """
        Calculate trend arrow based on 5% threshold
        ▲ = improving, ▼ = declining, ▶ = stable
        """
        if previous == 0:
            return "▶"
        
        change_pct = (current - previous) / abs(previous)
        
        if lower_is_better:
            if change_pct < -0.05:
                return "▲"
            elif change_pct > 0.05:
                return "▼"
            else:
                return "▶"
        else:
            if change_pct > 0.05:
                return "▲"
            elif change_pct < -0.05:
                return "▼"
            else:
                return "▶"
    
    # Interpretation methods (from Excel messages - simplified for now)
    
    def _get_ci_interpretation(self, n, n1, n2) -> str:
        if n2 > n1 and n2 > n:
            return "▼ A empresa está a gastar mais com a sua operação face aos anos anteriores."
        elif n2 < n1 and n2 < n:
            return "▲ A empresa está a gastar menos com a sua operação face aos anos anteriores."
        else:
            return "▶ Os gastos com a operação mantiveram-se relativamente estáveis."
    
    def _get_vbp_interpretation(self, n, n1, n2) -> str:
        if n2 > n1 and n2 > n:
            return "▲ A empresa aumentou o volume total produzido e vendido, mostrando crescimento nas suas operações comerciais."
        elif n2 < n1 and n2 < n:
            return "▼ A empresa reduziu o volume total produzido e vendido, mostrando contração nas suas operações comerciais."
        else:
            return "▶ O volume produzido e vendido manteve-se estável."
    
    def _get_vab_interpretation(self, n, n1, n2) -> str:
        if n2 > n1 and n2 > n:
            return "▲ A empresa está a criar mais valor económico face aos anos anteriores."
        elif n2 < n1 and n2 < n:
            return "▼ A empresa está a criar menos valor económico face aos anos anteriores."
        else:
            return "▶ A criação de valor económico manteve-se estável."
    
    def _get_tc_interpretation(self, tc: float) -> str:
        if tc > 0:
            return "▲ A empresa está em crescimento."
        elif tc < 0:
            return "▼ A empresa está a regredir."
        else:
            return "▶ A empresa mantém estabilidade nas suas operações."
    
    def _get_ebe_interpretation(self, n, n1, n2) -> str:
        if n2 > n1 and n2 > n:
            return "▲ A empresa aumentou o lucro gerado diretamente pelas suas operações, mostrando maior eficiência na gestão operacional."
        elif n2 < n1 and n2 < n:
            return "▼ A empresa diminuiu o lucro gerado diretamente pelas suas operações, mostrando menor eficiência na gestão operacional."
        else:
            return "▶ O lucro operacional manteve-se estável."
    
    def _get_elp_interpretation(self, n, n1, n2) -> str:
        if n2 > n1 and n2 > n:
            return "▲ O excedente líquido melhorou face aos anos anteriores, revelando maior capacidade real de gerar dinheiro com as operações."
        elif n2 < n1 and n2 < n:
            return "▼ O excedente líquido piorou face aos anos anteriores, revelando menor capacidade real de gerar dinheiro com as operações."
        else:
            return "▶ O excedente líquido manteve-se estável."
    
    def _get_raf_interpretation(self, value: float) -> str:
        if value >= 0.5:
            return "▲ Excelente autonomia financeira. A empresa utiliza maioritariamente fundos próprios, revelando baixo risco financeiro."
        elif value >= 0.3333:
            return "▶ Autonomia financeira razoável, mas atenção ao equilíbrio entre capitais próprios e alheios."
        else:
            return "▼ Autonomia financeira baixa. A empresa depende demasiado de financiamento externo, o que aumenta o risco financeiro."
    
    def _get_re_interpretation(self, value: float) -> str:
        if value < 0.5:
            return "▲ Nível saudável de endividamento. A empresa mantém dívidas controladas, com risco financeiro reduzido."
        elif value <= 0.66:
            return "▶ Nível moderado de endividamento. Necessária atenção Á  gestão da dívida para evitar riscos futuros."
        else:
            return "▼ Elevado nível de endividamento. A empresa apresenta grande dependência de dívidas, aumentando o risco financeiro."
    
    def _get_rs_interpretation(self, value: float) -> str:
        if value >= 1:
            return "▲ Excelente solvabilidade. A empresa consegue facilmente cobrir as suas dívidas com recursos próprios."
        elif value >= 0.5:
            return "▶ Solvabilidade aceitável, mas pode existir alguma vulnerabilidade financeira."
        else:
            return "▼ Solvabilidade insuficiente. A empresa poderá enfrentar dificuldades financeiras para honrar as suas dívidas."
    
    def _get_rssr_interpretation(self, value: float) -> str:
        if value > 1.5:
            return "▲ Boa cobertura das dívidas pelo ativo. A empresa está muito segura para os credores."
        elif value >= 1:
            return "▶ Cobertura suficiente, mas deve ser acompanhada de perto."
        else:
            return "▼ Cobertura insuficiente. Ativo pode não ser suficiente para cobrir dívidas, situação de risco elevado."
    
    def _get_rde_interpretation(self, n, n1, n2) -> str:
        base = ""
        if n2 == 1:
            base = "▶ Recursos igualmente divididos entre capital próprio e dívida de curto prazo."
        elif n2 > 1:
            base = "▼ Dívida de curto prazo predomina sobre fundos próprios, maior risco financeiro."
        else:
            base = "▲ Fundos próprios predominam sobre a dívida de curto prazo, situação favorável financeiramente."
        
        if n2 > n1 and n2 > n:
            base += " Indicador aumentou face aos anos anteriores, ou seja, a empresa tem vindo a endividar-se."
        elif n2 < n1 and n2 < n:
            base += " Indicador diminuiu face aos anos anteriores, ou seja, a empresa tem vindo a diminuir a sua dívida."
        
        return base
    
    def _get_ref_interpretation(self, n, n1, n2) -> str:
        base = ""
        if n2 >= 1:
            base = "▲ A empresa tem financiamento estável para toda a sua atividade, o que é seguro e positivo."
        elif n2 >= 0.7:
            base = "▶ A empresa tem financiamento estável para a maior parte da atividade, mas deve monitorizar o financiamento de curto prazo."
        else:
            base = "▼ A empresa depende demasiado de empréstimos de curto prazo, aumentando o risco financeiro."
        
        return base
    
    def _get_rep_interpretation(self, n, n1, n2) -> str:
        if n2 == 1:
            return "▶ A dívida da empresa está equilibrada entre curto prazo e médio/longo prazo."
        elif n2 > 1:
            return "▼ A maior parte da dívida da empresa vence-se rapidamente (curto prazo), o que pode pressionar a tesouraria."
        else:
            return "▲ A maior parte da dívida da empresa vence-se num prazo longo, o que dá conforto financeiro."
    
    def _get_rcaflre_interpretation(self, n, n1, n2) -> str:
        if n2 > 1:
            return "▲ A empresa financia os seus investimentos de longo prazo com fundos próprios ou empréstimos de longo prazo, o que é positivo."
        elif n2 == 1:
            return "▶ O financiamento dos investimentos é justo, sem margem adicional, situação delicada."
        else:
            return "▼ A empresa não financia totalmente os investimentos de longo prazo com fundos próprios ou empréstimos de longo prazo, aumentando o risco financeiro."
    
    def _get_rcaflcp_interpretation(self, n, n1, n2) -> str:
        if n2 > 1:
            return "▲ A empresa financia os seus investimentos com dinheiro próprio, reduzindo o risco financeiro."
        elif n2 == 1:
            return "▶ A empresa financia os seus investimentos exclusivamente com dinheiro próprio, sem margem adicional."
        else:
            return "▼ A empresa financia os seus investimentos sobretudo com dívida externa, aumentando o risco financeiro."

# NEW CALCULATION METHODS TO ADD TO calculator.py
# These are the 34 additional methods needed for the 51 total metrics

    # ========== INDICADORES LONGO PRAZO (Additional 3) ==========
    
    def _calc_estrutura_endividamento(self) -> MetricValue:
        """
        REE = Passivo Corrente / Passivo Total
        Excel Row 22: =Balanço!E57/Balanço!E68
        """
        n = self.bs.year_n.total_passivo_corrente / self.bs.year_n.total_passivo if self.bs.year_n.total_passivo > 0 else 0
        n1 = self.bs.year_n1.total_passivo_corrente / self.bs.year_n1.total_passivo if self.bs.year_n1.total_passivo > 0 else 0
        n2 = self.bs.year_n2.total_passivo_corrente / self.bs.year_n2.total_passivo if self.bs.year_n2.total_passivo > 0 else 0
        
        return MetricValue(
            nome="RÁƒÂ¡cio de Estrutura de Endividamento (REE)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao="Indica a proporÁƒÂ§ÁƒÂ£o de dÁƒÂ­vidas de curto prazo no total do passivo. Valores elevados indicam maior pressão de pagamento no curto prazo."
        )
    
    def _calc_cobertura_gastos_financiamento(self) -> MetricValue:
        """
        RCGFRO = (Resultado Operacional + DepreciaÁƒÂ§ÁƒÂµes) / Gastos Financiamento
        Excel Row 23: =('DR'!E25+'DR'!K24)/'DR'!K25
        """
        ro_n = self.dr.year_n.resultado_antes_impostos + self.dr.year_n.juros_gastos_suportados
        ro_n1 = self.dr.year_n1.resultado_antes_impostos + self.dr.year_n1.juros_gastos_suportados
        ro_n2 = self.dr.year_n2.resultado_antes_impostos + self.dr.year_n2.juros_gastos_suportados
        
        dep_n = self.dr.year_n.gastos_depreciacoes_amortizacoes
        dep_n1 = self.dr.year_n1.gastos_depreciacoes_amortizacoes
        dep_n2 = self.dr.year_n2.gastos_depreciacoes_amortizacoes
        
        gf_n = abs(self.dr.year_n.juros_gastos_suportados)
        gf_n1 = abs(self.dr.year_n1.juros_gastos_suportados)
        gf_n2 = abs(self.dr.year_n2.juros_gastos_suportados)
        
        n = (ro_n + dep_n) / gf_n if gf_n > 0 else 0
        n1 = (ro_n1 + dep_n1) / gf_n1 if gf_n1 > 0 else 0
        n2 = (ro_n2 + dep_n2) / gf_n2 if gf_n2 > 0 else 0
        
        return MetricValue(
            nome="RÁƒÂ¡cio de Cobertura de Gastos de Financiamento (RCGFRO)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Mede a capacidade da empresa cobrir gastos financeiros com resultados operacionais. Valores >1 indicam boa cobertura."
        )
    
    def _calc_gastos_financiamento(self) -> MetricValue:
        """
        RGF = Gastos Financiamento / SubsÁƒÂ­dios
        Excel Row 24: ='DR'!K23/'DR'!K6
        """
        gf_n = abs(self.dr.year_n.juros_gastos_suportados)
        gf_n1 = abs(self.dr.year_n1.juros_gastos_suportados)
        gf_n2 = abs(self.dr.year_n2.juros_gastos_suportados)
        
        subs_n = self.dr.year_n.subsidios_exploracao
        subs_n1 = self.dr.year_n1.subsidios_exploracao
        subs_n2 = self.dr.year_n2.subsidios_exploracao
        
        n = gf_n / subs_n if subs_n > 0 else 0
        n1 = gf_n1 / subs_n1 if subs_n1 > 0 else 0
        n2 = gf_n2 / subs_n2 if subs_n2 > 0 else 0
        
        return MetricValue(
            nome="RÁƒÂ¡cio de Gastos de Financiamento (RGF)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao="Compara gastos financeiros com subsÁƒÂ­dios recebidos. Valores baixos são preferÁƒÂ­veis."
        )
    
    # ========== RÁƒÂCIOS DE ATIVIDADE CURTO PRAZO (6) ==========
    
    def _calc_rotacao_inventarios(self) -> MetricValue:
        """
        RI = CMVMC / Inventários (ENDING VALUES ONLY)
        Excel: ='Demonstração de Resultados'!E10/(Balanço!E18)
        FIXED: Uses ENDING values only (no averages)
        """
        # Use ENDING values only - no averages!
        n = self.dr.year_n.cmvmc / self.bs.year_n.inventarios if self.bs.year_n.inventarios > 0 else 0
        n1 = self.dr.year_n1.cmvmc / self.bs.year_n1.inventarios if self.bs.year_n1.inventarios > 0 else 0
        n2 = self.dr.year_n2.cmvmc / self.bs.year_n2.inventarios if self.bs.year_n2.inventarios > 0 else 0
        
        return MetricValue(
            nome="Rotação de Inventários (RI)",
            unidade="vezes/ano",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Número de vezes que o inventário roda por ano. Valores mais altos indicam melhor gestão de stocks."
        )
    
    def _calc_duracao_media_inventarios(self) -> MetricValue:
        """
        DMI = (Inventários / CMVMC) × 365 (ENDING VALUES ONLY)
        Excel: =(Balanço!E18/'Demonstração de Resultados'!E10)*365
        FIXED: Uses ENDING values only (no averages)
        """
        # Use ENDING values only - no averages!
        n = (self.bs.year_n.inventarios / self.dr.year_n.cmvmc) * 365 if self.dr.year_n.cmvmc > 0 else 0
        n1 = (self.bs.year_n1.inventarios / self.dr.year_n1.cmvmc) * 365 if self.dr.year_n1.cmvmc > 0 else 0
        n2 = (self.bs.year_n2.inventarios / self.dr.year_n2.cmvmc) * 365 if self.dr.year_n2.cmvmc > 0 else 0
        
        return MetricValue(
            nome="Duração Média de Inventários (DMI)",
            unidade="dias",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao="Número médio de dias que os produtos permanecem em stock. Valores menores indicam melhor rotação."
        )
    
    def _calc_prazo_medio_recebimento(self) -> MetricValue:
        """
        PMR = (Clientes / (Vendas × 1.23)) × 365 (ENDING VALUES ONLY)
        Excel: =(Balanço!E20/('Demonstração de Resultados'!E5*(1+0.23)))*365
        FIXED: Uses ENDING values only (no averages)
        """
        # Use ENDING values only - no averages!
        n = (self.bs.year_n.clientes / (self.dr.year_n.vendas_servicos_prestados * 1.23)) * 365 if self.dr.year_n.vendas_servicos_prestados > 0 else 0
        n1 = (self.bs.year_n1.clientes / (self.dr.year_n1.vendas_servicos_prestados * 1.23)) * 365 if self.dr.year_n1.vendas_servicos_prestados > 0 else 0
        n2 = (self.bs.year_n2.clientes / (self.dr.year_n2.vendas_servicos_prestados * 1.23)) * 365 if self.dr.year_n2.vendas_servicos_prestados > 0 else 0
        
        return MetricValue(
            nome="Prazo Médio de Recebimento (PMR)",
            unidade="dias",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao="Tempo médio para receber pagamentos de clientes. Valores menores indicam melhor gestão de crédito."
        )
    
    def _calc_prazo_medio_pagamento(self) -> MetricValue:
        """
        PMP = (Fornecedores / (CMVMC × 1.23)) × 356
        Excel: =(Balanço!E58/('DR'!E10*(1+0.23)))*356
        FIXED: Uses ENDING values only (no averages) and 356 days (not 365)
        """
        # Use ENDING values only - no averages!
        n = (self.bs.year_n.fornecedores / (self.dr.year_n.cmvmc * 1.23)) * 356 if self.dr.year_n.cmvmc > 0 else 0
        n1 = (self.bs.year_n1.fornecedores / (self.dr.year_n1.cmvmc * 1.23)) * 356 if self.dr.year_n1.cmvmc > 0 else 0
        n2 = (self.bs.year_n2.fornecedores / (self.dr.year_n2.cmvmc * 1.23)) * 356 if self.dr.year_n2.cmvmc > 0 else 0
        
        return MetricValue(
            nome="Prazo Médio de Pagamento (PMP)",
            unidade="dias",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Tempo médio para pagar fornecedores. Prazos maiores podem indicar melhor gestão de tesouraria."
        )
    
    def _calc_duracao_ciclo_operacional(self) -> MetricValue:
        """
        DCO = DMI + PMR
        Excel Row 30: =J27+J28
        """
        dmi = self._calc_duracao_media_inventarios()
        pmr = self._calc_prazo_medio_recebimento()
        
        return MetricValue(
            nome="DuraÁƒÂ§ÁƒÂ£o do Ciclo Operacional (DCO)",
            unidade="dias",
            year_n=dmi.year_n + pmr.year_n,
            year_n1=dmi.year_n1 + pmr.year_n1,
            year_n2=dmi.year_n2 + pmr.year_n2,
            tendencia=self._get_trend(dmi.year_n2 + pmr.year_n2, dmi.year_n1 + pmr.year_n1, lower_is_better=True),
            interpretacao="Tempo total do ciclo operacional desde compra atÁƒÂ© recebimento. Valores menores são preferÁƒÂ­veis."
        )
    
    def _calc_necessidades_fundo_maneio(self) -> MetricValue:
        """
        NFM = DCO - PMP
        Excel Row 31: =J30-J29
        """
        dco = self._calc_duracao_ciclo_operacional()
        pmp = self._calc_prazo_medio_pagamento()
        
        return MetricValue(
            nome="Necessidades de Fundo de Maneio (NFM)",
            unidade="dias",
            year_n=dco.year_n - pmp.year_n,
            year_n1=dco.year_n1 - pmp.year_n1,
            year_n2=dco.year_n2 - pmp.year_n2,
            tendencia=self._get_trend(dco.year_n2 - pmp.year_n2, dco.year_n1 - pmp.year_n1, lower_is_better=True),
            interpretacao="Dias de financiamento necessÁƒÂ¡rios para o ciclo operacional. Valores menores indicam menor necessidade de capital."
        )
    
    # ========== RENTABILIDADE (4) ==========
    
    def _calc_return_on_assets(self) -> MetricValue:
        """
        ROA = Resultado Operacional (EBIT) / Ativo Total
        Excel Row 34: ='Demonstração de Resultados'!E25/Balanço!E30
        Uses Year N point-in-time values (NO AVERAGE)
        """
        # Use EBIT (resultado operacional) directly (Year N only)
        n = self.dr.year_n.ebit / self.bs.year_n.total_ativo if self.bs.year_n.total_ativo > 0 else 0
        n1 = self.dr.year_n1.ebit / self.bs.year_n1.total_ativo if self.bs.year_n1.total_ativo > 0 else 0
        n2 = self.dr.year_n2.ebit / self.bs.year_n2.total_ativo if self.bs.year_n2.total_ativo > 0 else 0
        
        return MetricValue(
            nome="Return on Assets (ROA)",
            unidade="%",
            year_n=n * 100,
            year_n1=n1 * 100,
            year_n2=n2 * 100,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Rentabilidade dos ativos. Valores >3% são considerados bons. Indica eficiência na utilização dos ativos."
        )
    
    def _calc_return_on_equity(self) -> MetricValue:
        """
        ROE = Resultado Líquido / Capital Próprio
        Excel Row 35: ='Demonstração de Resultados'!E31/Balanço!E47
        Uses Year N point-in-time values (NO AVERAGE)
        """
        # Use Year N capital próprio only
        n = self.dr.year_n.resultado_liquido / self.bs.year_n.total_capital_proprio if self.bs.year_n.total_capital_proprio > 0 else 0
        n1 = self.dr.year_n1.resultado_liquido / self.bs.year_n1.total_capital_proprio if self.bs.year_n1.total_capital_proprio > 0 else 0
        n2 = self.dr.year_n2.resultado_liquido / self.bs.year_n2.total_capital_proprio if self.bs.year_n2.total_capital_proprio > 0 else 0
        
        return MetricValue(
            nome="Return on Equity (ROE)",
            unidade="%",
            year_n=n * 100,
            year_n1=n1 * 100,
            year_n2=n2 * 100,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Rentabilidade do capital próprio. Valores >5% são considerados bons. Indica retorno para os acionistas."
        )
    
    def _calc_rentabilidade_operacional_vendas(self) -> MetricValue:
        """
        ROV = Resultado Operacional (EBIT) / Vendas
        Excel Row 36: ='Demonstração de Resultados'!E25/'DR'!E5
        Uses EBIT (resultado operacional) directly
        """
        n = self.dr.year_n.ebit / self.dr.year_n.vendas_servicos_prestados if self.dr.year_n.vendas_servicos_prestados > 0 else 0
        n1 = self.dr.year_n1.ebit / self.dr.year_n1.vendas_servicos_prestados if self.dr.year_n1.vendas_servicos_prestados > 0 else 0
        n2 = self.dr.year_n2.ebit / self.dr.year_n2.vendas_servicos_prestados if self.dr.year_n2.vendas_servicos_prestados > 0 else 0
        
        return MetricValue(
            nome="Rentabilidade Operacional das Vendas (ROV)",
            unidade="%",
            year_n=n * 100,
            year_n1=n1 * 100,
            year_n2=n2 * 100,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Margem operacional. Indica quanto lucro operacional é gerado por cada euro de vendas."
        )
    
    def _calc_rentabilidade_liquida_vendas(self) -> MetricValue:
        """
        RLV = Resultado Líquido / Vendas
        Excel Row 44: ='DR'!E31/'DR'!E5
        """
        n = self.dr.year_n.resultado_liquido / self.dr.year_n.vendas_servicos_prestados if self.dr.year_n.vendas_servicos_prestados > 0 else 0
        n1 = self.dr.year_n1.resultado_liquido / self.dr.year_n1.vendas_servicos_prestados if self.dr.year_n1.vendas_servicos_prestados > 0 else 0
        n2 = self.dr.year_n2.resultado_liquido / self.dr.year_n2.vendas_servicos_prestados if self.dr.year_n2.vendas_servicos_prestados > 0 else 0
        
        return MetricValue(
            nome="Rentabilidade LÁƒÂ­quida das Vendas (RLV)",
            unidade="%",
            year_n=n * 100,
            year_n1=n1 * 100,
            year_n2=n2 * 100,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Margem lÁƒÂ­quida. Indica quanto lucro lÁƒÂ­quido ÁƒÂ© gerado por cada euro de vendas."
        )
    
    # ========== EFICIÁƒÅ NCIA (4) ==========
    
    def _calc_rotacao_ativo(self) -> MetricValue:
        """
        RAT = Vendas / Ativo Total
        Excel Row 27: ='Demonstração de Resultados'!E5/Balanço!E30
        Uses Year N point-in-time values (NO AVERAGE)
        """
        # Use Year N total_ativo only
        n = self.dr.year_n.vendas_servicos_prestados / self.bs.year_n.total_ativo if self.bs.year_n.total_ativo > 0 else 0
        n1 = self.dr.year_n1.vendas_servicos_prestados / self.bs.year_n1.total_ativo if self.bs.year_n1.total_ativo > 0 else 0
        n2 = self.dr.year_n2.vendas_servicos_prestados / self.bs.year_n2.total_ativo if self.bs.year_n2.total_ativo > 0 else 0
        
        return MetricValue(
            nome="Rotação do Ativo (RAT)",
            unidade="vezes",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Eficiência na utilização dos ativos para gerar vendas. Valores mais altos indicam melhor eficiência."
        )
    
    def _calc_rotacao_ativo_fixo(self) -> MetricValue:
        """
        RAFx = Vendas / (AFT + Ativos IntangÁƒÂ­veis) MÉDIO
        Excel Row 34: ='DR'!E5/(Balanço!E7+Balanço!E10)
        Excel uses Year N point-in-time values fixed assets between two years
        """
        aft_n = self.bs.year_n.ativos_fixos_tangiveis + self.bs.year_n.ativos_intangiveis
        aft_n1 = self.bs.year_n1.ativos_fixos_tangiveis + self.bs.year_n1.ativos_intangiveis
        aft_n2 = self.bs.year_n2.ativos_fixos_tangiveis + self.bs.year_n2.ativos_intangiveis
        
        # Year N: average of N and N-1
        aft_avg_n = (aft_n + aft_n1) / 2 if aft_n1 > 0 else aft_n
        n = self.dr.year_n.vendas_servicos_prestados / aft_avg_n if aft_avg_n > 0 else 0
        
        # Year N-1: average of N-1 and N-2
        aft_avg_n1 = (aft_n1 + aft_n2) / 2 if aft_n2 > 0 else aft_n1
        n1 = self.dr.year_n1.vendas_servicos_prestados / aft_avg_n1 if aft_avg_n1 > 0 else 0
        
        # Year N-2: use ending balance
        n2 = self.dr.year_n2.vendas_servicos_prestados / aft_n2 if aft_n2 > 0 else 0
        
        return MetricValue(
            nome="Rotação do Ativo Fixo (RAFx)",
            unidade="vezes",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Eficiência na utilização dos ativos fixos. Valores mais altos indicam melhor aproveitamento do investimento."
        )
    
    def _calc_produtividade_ativo(self) -> MetricValue:
        """
        PA = Vendas / Ativo Corrente MÉDIO
        Excel Row 35: ='DR'!E5/Balanço!E17
        Excel uses Year N point-in-time values current assets between two years
        """
        # Year N: average of N and N-1
        ac_avg_n = (self.bs.year_n.total_ativo_corrente + self.bs.year_n1.total_ativo_corrente) / 2 if self.bs.year_n1.total_ativo_corrente > 0 else self.bs.year_n.total_ativo_corrente
        n = self.dr.year_n.vendas_servicos_prestados / ac_avg_n if ac_avg_n > 0 else 0
        
        # Year N-1: average of N-1 and N-2
        ac_avg_n1 = (self.bs.year_n1.total_ativo_corrente + self.bs.year_n2.total_ativo_corrente) / 2 if self.bs.year_n2.total_ativo_corrente > 0 else self.bs.year_n1.total_ativo_corrente
        n1 = self.dr.year_n1.vendas_servicos_prestados / ac_avg_n1 if ac_avg_n1 > 0 else 0
        
        # Year N-2: use ending balance
        n2 = self.dr.year_n2.vendas_servicos_prestados / self.bs.year_n2.total_ativo_corrente if self.bs.year_n2.total_ativo_corrente > 0 else 0
        
        return MetricValue(
            nome="Produtividade do Ativo (PA)",
            unidade="vezes",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Produtividade do ativo corrente. Valores mais altos indicam melhor utilização do capital de giro."
        )
    
    def _calc_produtividade_capital_proprio(self) -> MetricValue:
        """
        PCP = Vendas / Capital Próprio
        Excel Row 36: ='DR'!E5/Balanço!E47
        Excel uses Year N point-in-time values (NO AVERAGE) between two years
        """
        # Year N: average of N and N-1
        cp_avg_n = (self.bs.year_n.total_capital_proprio + self.bs.year_n1.total_capital_proprio) / 2 if self.bs.year_n1.total_capital_proprio > 0 else self.bs.year_n.total_capital_proprio
        n = self.dr.year_n.vendas_servicos_prestados / cp_avg_n if cp_avg_n > 0 else 0
        
        # Year N-1: average of N-1 and N-2
        cp_avg_n1 = (self.bs.year_n1.total_capital_proprio + self.bs.year_n2.total_capital_proprio) / 2 if self.bs.year_n2.total_capital_proprio > 0 else self.bs.year_n1.total_capital_proprio
        n1 = self.dr.year_n1.vendas_servicos_prestados / cp_avg_n1 if cp_avg_n1 > 0 else 0
        
        # Year N-2: use ending balance
        n2 = self.dr.year_n2.vendas_servicos_prestados / self.bs.year_n2.total_capital_proprio if self.bs.year_n2.total_capital_proprio > 0 else 0
        
        return MetricValue(
            nome="Produtividade do Capital Próprio (PCP)",
            unidade="vezes",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Produtividade do capital prÁƒÂ³prio. Valores mais altos indicam melhor aproveitamento do capital dos sÁƒÂ³cios."
        )
    
    # ========== LIQUIDEZ (3) ==========
    
    def _calc_liquidez_geral(self) -> MetricValue:
        """
        LG = Ativo Corrente / Passivo Corrente
        Excel Row 37: =Balanço!E17/Balanço!E57
        """
        n = self.bs.year_n.total_ativo_corrente / self.bs.year_n.total_passivo_corrente if self.bs.year_n.total_passivo_corrente > 0 else 0
        n1 = self.bs.year_n1.total_ativo_corrente / self.bs.year_n1.total_passivo_corrente if self.bs.year_n1.total_passivo_corrente > 0 else 0
        n2 = self.bs.year_n2.total_ativo_corrente / self.bs.year_n2.total_passivo_corrente if self.bs.year_n2.total_passivo_corrente > 0 else 0
        
        return MetricValue(
            nome="Liquidez Geral (LG)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Capacidade de pagar dÁƒÂ­vidas de curto prazo. Valores >1 indicam boa liquidez. Benchmark: â≥Â¥1.0"
        )
    
    def _calc_liquidez_reduzida(self) -> MetricValue:
        """
        LR = (Ativo Corrente - InventÁƒÂ¡rios - Diferimentos) / Passivo Corrente
        Excel Row 38: =(Balanço!E17-Balanço!E18-Balanço!E19)/Balanço!E57
        """
        ac_liq_n = self.bs.year_n.total_ativo_corrente - self.bs.year_n.inventarios - self.bs.year_n.diferimentos_ativo
        ac_liq_n1 = self.bs.year_n1.total_ativo_corrente - self.bs.year_n1.inventarios - self.bs.year_n1.diferimentos_ativo
        ac_liq_n2 = self.bs.year_n2.total_ativo_corrente - self.bs.year_n2.inventarios - self.bs.year_n2.diferimentos_ativo
        
        n = ac_liq_n / self.bs.year_n.total_passivo_corrente if self.bs.year_n.total_passivo_corrente > 0 else 0
        n1 = ac_liq_n1 / self.bs.year_n1.total_passivo_corrente if self.bs.year_n1.total_passivo_corrente > 0 else 0
        n2 = ac_liq_n2 / self.bs.year_n2.total_passivo_corrente if self.bs.year_n2.total_passivo_corrente > 0 else 0
        
        return MetricValue(
            nome="Liquidez Reduzida (LR)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Liquidez excluindo inventÁƒÂ¡rios. Valores >0.8 são considerados bons. Benchmark: â≥Â¥0.8"
        )
    
    def _calc_liquidez_imediata(self) -> MetricValue:
        """
        LI = Caixa e DepÁƒÂ³sitos / Passivo Corrente
        Excel Row 39: =Balanço!E28/Balanço!E57
        """
        n = self.bs.year_n.caixa_depositos_bancarios / self.bs.year_n.total_passivo_corrente if self.bs.year_n.total_passivo_corrente > 0 else 0
        n1 = self.bs.year_n1.caixa_depositos_bancarios / self.bs.year_n1.total_passivo_corrente if self.bs.year_n1.total_passivo_corrente > 0 else 0
        n2 = self.bs.year_n2.caixa_depositos_bancarios / self.bs.year_n2.total_passivo_corrente if self.bs.year_n2.total_passivo_corrente > 0 else 0
        
        return MetricValue(
            nome="Liquidez Imediata (LI)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Liquidez apenas com disponibilidades imediatas. Valores >0.2 são considerados bons. Benchmark: â≥Â¥0.2"
        )
    
    # ========== RISCO (4) ==========
    
    def _calc_grau_alavanca_financeira(self) -> MetricValue:
        """
        GAF = Resultado Operacional / (Resultado Operacional - Gastos Financeiros)
        Excel Row 57: ='DR'!E25/'DR'!E29
        """
        ro_n = self.dr.year_n.resultado_antes_impostos + self.dr.year_n.juros_gastos_suportados
        ro_n1 = self.dr.year_n1.resultado_antes_impostos + self.dr.year_n1.juros_gastos_suportados
        ro_n2 = self.dr.year_n2.resultado_antes_impostos + self.dr.year_n2.juros_gastos_suportados
        
        rai_n = self.dr.year_n.resultado_antes_impostos
        rai_n1 = self.dr.year_n1.resultado_antes_impostos
        rai_n2 = self.dr.year_n2.resultado_antes_impostos
        
        n = ro_n / rai_n if rai_n != 0 else 0
        n1 = ro_n1 / rai_n1 if rai_n1 != 0 else 0
        n2 = ro_n2 / rai_n2 if rai_n2 != 0 else 0
        
        return MetricValue(
            nome="Grau de Alavanca Financeira (GAF)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao="Mede o risco financeiro. Valores prÁƒÂ³ximos de 1 indicam baixo risco, valores altos indicam alto risco financeiro."
        )
    
    def _calc_grau_alavanca_operacional(self) -> MetricValue:
        """
        GAO = (Vendas - Custos VariÁƒÂ¡veis) / Resultado Operacional
        Excel Row 56: =(Vendas - CMVMC) / RO
        """
        ro_n = self.dr.year_n.resultado_antes_impostos + self.dr.year_n.juros_gastos_suportados
        ro_n1 = self.dr.year_n1.resultado_antes_impostos + self.dr.year_n1.juros_gastos_suportados
        ro_n2 = self.dr.year_n2.resultado_antes_impostos + self.dr.year_n2.juros_gastos_suportados
        
        margem_n = self.dr.year_n.vendas_servicos_prestados - self.dr.year_n.cmvmc
        margem_n1 = self.dr.year_n1.vendas_servicos_prestados - self.dr.year_n1.cmvmc
        margem_n2 = self.dr.year_n2.vendas_servicos_prestados - self.dr.year_n2.cmvmc
        
        n = margem_n / ro_n if ro_n > 0 else 0
        n1 = margem_n1 / ro_n1 if ro_n1 > 0 else 0
        n2 = margem_n2 / ro_n2 if ro_n2 > 0 else 0
        
        return MetricValue(
            nome="Grau de Alavanca Operacional (GAO)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao="Mede o risco operacional. Valores mais altos indicam maior sensibilidade a variaÁƒÂ§ÁƒÂµes nas vendas."
        )
    
    def _calc_cobertura_juros(self) -> MetricValue:
        """
        CJ = Gastos Financeiros / (Financiamentos NC + Financiamentos C)
        Excel Row 53: ='DR'!K23/(Balanço!E52+Balanço!E61)
        """
        gf_n = abs(self.dr.year_n.juros_gastos_suportados)
        gf_n1 = abs(self.dr.year_n1.juros_gastos_suportados)
        gf_n2 = abs(self.dr.year_n2.juros_gastos_suportados)
        
        fin_n = self.bs.year_n.financiamentos_obtidos_nc + self.bs.year_n.financiamentos_obtidos_corrente
        fin_n1 = self.bs.year_n1.financiamentos_obtidos_nc + self.bs.year_n1.financiamentos_obtidos_corrente
        fin_n2 = self.bs.year_n2.financiamentos_obtidos_nc + self.bs.year_n2.financiamentos_obtidos_corrente
        
        n = gf_n / fin_n if fin_n > 0 else 0
        n1 = gf_n1 / fin_n1 if fin_n1 > 0 else 0
        n2 = gf_n2 / fin_n2 if fin_n2 > 0 else 0
        
        return MetricValue(
            nome="Cobertura de Juros (CJ)",
            unidade="ratio",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao="Taxa de juro implÁƒÂ­cita da dÁƒÂ­vida. Valores menores indicam melhores condiÁƒÂ§ÁƒÂµes de financiamento."
        )
    
    def _calc_indice_solidez_financeira(self) -> MetricValue:
        """
        ISF = Resultado Operacional / Ativo Total
        Excel Row 54: ='DR'!E25/Balanço!E30
        """
        ro_n = self.dr.year_n.resultado_antes_impostos + self.dr.year_n.juros_gastos_suportados
        ro_n1 = self.dr.year_n1.resultado_antes_impostos + self.dr.year_n1.juros_gastos_suportados
        ro_n2 = self.dr.year_n2.resultado_antes_impostos + self.dr.year_n2.juros_gastos_suportados
        
        n = ro_n / self.bs.year_n.total_ativo if self.bs.year_n.total_ativo > 0 else 0
        n1 = ro_n1 / self.bs.year_n1.total_ativo if self.bs.year_n1.total_ativo > 0 else 0
        n2 = ro_n2 / self.bs.year_n2.total_ativo if self.bs.year_n2.total_ativo > 0 else 0
        
        return MetricValue(
            nome="ÁƒÂndice de Solidez Financeira (ISF)",
            unidade="%",
            year_n=n * 100,
            year_n1=n1 * 100,
            year_n2=n2 * 100,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Solidez financeira global. Valores mais altos indicam maior capacidade de gerar resultados operacionais."
        )
    
    # ========== ANÁƒÂLISE DUPONT & COMPOSIÁƒâ€¡ÁƒÆ’O (5) ==========
    
    def _calc_margem_liquida(self) -> MetricValue:
        """
        ML = Resultado Líquido / Vendas (same as RLV)
        Excel Row 44: ='DR'!E31/'DR'!E5
        """
        return self._calc_rentabilidade_liquida_vendas()
    
    def _calc_rotacao_ativo_total(self) -> MetricValue:
        """
        RAT = Ativo Total / Capital Próprio
        Excel Row 52: =Balanço!E30/Balanço!E47
        """
        n = self.bs.year_n.total_ativo / self.bs.year_n.total_capital_proprio if self.bs.year_n.total_capital_proprio > 0 else 0
        n1 = self.bs.year_n1.total_ativo / self.bs.year_n1.total_capital_proprio if self.bs.year_n1.total_capital_proprio > 0 else 0
        n2 = self.bs.year_n2.total_ativo / self.bs.year_n2.total_capital_proprio if self.bs.year_n2.total_capital_proprio > 0 else 0
        
        return MetricValue(
            nome="Rotação do Ativo Total (RAT)",
            unidade="vezes",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Componente da anÁƒÂ¡lise DuPont. Indica quantas vezes o ativo ÁƒÂ© financiado pelo capital prÁƒÂ³prio."
        )
    
    def _calc_roe_dupont(self) -> MetricValue:
        """
        ROE DuPont = Margem LÁƒÂ­quida Áƒâ€” Rotação Ativo Áƒâ€” Multiplicador Capital
        Excel Row 49: =J50*J51*J52
        """
        ml = self._calc_margem_liquida()
        rat = self._calc_rotacao_ativo()
        mc = self._calc_multiplicador_capital()
        
        n = (ml.year_n / 100) * rat.year_n * mc.year_n
        n1 = (ml.year_n1 / 100) * rat.year_n1 * mc.year_n1
        n2 = (ml.year_n2 / 100) * rat.year_n2 * mc.year_n2
        
        return MetricValue(
            nome="ROE DuPont",
            unidade="%",
            year_n=n * 100,
            year_n1=n1 * 100,
            year_n2=n2 * 100,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Análise DuPont do ROE. DecomposiÁƒÂ§ÁƒÂ£o em margem, eficiência e alavancagem."
        )
    
    def _calc_multiplicador_capital(self) -> MetricValue:
        """
        MC = Ativo Total / Capital Próprio
        Excel Row 52: =Balanço!E30/Balanço!E47
        """
        n = self.bs.year_n.total_ativo / self.bs.year_n.total_capital_proprio if self.bs.year_n.total_capital_proprio > 0 else 0
        n1 = self.bs.year_n1.total_ativo / self.bs.year_n1.total_capital_proprio if self.bs.year_n1.total_capital_proprio > 0 else 0
        n2 = self.bs.year_n2.total_ativo / self.bs.year_n2.total_capital_proprio if self.bs.year_n2.total_capital_proprio > 0 else 0
        
        return MetricValue(
            nome="Multiplicador de Capital (MC)",
            unidade="vezes",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao="Alavancagem financeira. Valores mais altos indicam maior uso de dÁƒÂ­vida para financiar ativos."
        )
    
    def _calc_rentabilidade_ajustada(self) -> MetricValue:
        """
        Complex formula with tax adjustments
        Excel Row 45: =('DR'!E31+'DR'!K25*('DR'!E31/'DR'!E29))/Balanço!E30
        """
        rl_n = self.dr.year_n.resultado_liquido
        rl_n1 = self.dr.year_n1.resultado_liquido
        rl_n2 = self.dr.year_n2.resultado_liquido
        
        gf_n = abs(self.dr.year_n.juros_gastos_suportados)
        gf_n1 = abs(self.dr.year_n1.juros_gastos_suportados)
        gf_n2 = abs(self.dr.year_n2.juros_gastos_suportados)
        
        rai_n = self.dr.year_n.resultado_antes_impostos
        rai_n1 = self.dr.year_n1.resultado_antes_impostos
        rai_n2 = self.dr.year_n2.resultado_antes_impostos
        
        # Ajuste fiscal
        tax_adj_n = gf_n * (rl_n / rai_n) if rai_n != 0 else 0
        tax_adj_n1 = gf_n1 * (rl_n1 / rai_n1) if rai_n1 != 0 else 0
        tax_adj_n2 = gf_n2 * (rl_n2 / rai_n2) if rai_n2 != 0 else 0
        
        n = (rl_n + tax_adj_n) / self.bs.year_n.total_ativo if self.bs.year_n.total_ativo > 0 else 0
        n1 = (rl_n1 + tax_adj_n1) / self.bs.year_n1.total_ativo if self.bs.year_n1.total_ativo > 0 else 0
        n2 = (rl_n2 + tax_adj_n2) / self.bs.year_n2.total_ativo if self.bs.year_n2.total_ativo > 0 else 0
        
        return MetricValue(
            nome="Rentabilidade Ajustada",
            unidade="%",
            year_n=n * 100,
            year_n1=n1 * 100,
            year_n2=n2 * 100,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Rentabilidade ajustada por efeitos fiscais. Mede o retorno real considerando impostos."
        )
    
    # ========== MISSING METRICS (4 additional) ==========
    
    def _calc_rendibilidade_operacional_ativo(self) -> MetricValue:
        """
        #39 - Rendibilidade Operacional do Ativo (ROA Operacional)
        Formula: Resultado Operacional / Ativo Total
        Different from #34 (Return on Assets) which uses Net Income.
        This uses EBIT (operating profit before interest and taxes).
        """
        # Resultado Operacional = Resultado antes impostos + Juros Gastos
        ro_n = self.dr.year_n.resultado_antes_impostos + self.dr.year_n.juros_gastos_suportados
        ro_n1 = self.dr.year_n1.resultado_antes_impostos + self.dr.year_n1.juros_gastos_suportados
        ro_n2 = self.dr.year_n2.resultado_antes_impostos + self.dr.year_n2.juros_gastos_suportados
        
        n = self._safe_divide(ro_n, self.bs.year_n.total_ativo)
        n1 = self._safe_divide(ro_n1, self.bs.year_n1.total_ativo)
        n2 = self._safe_divide(ro_n2, self.bs.year_n2.total_ativo)
        
        return MetricValue(
            nome="Rendibilidade Operacional do Ativo (ROA Operacional)",
            unidade="%",
            year_n=n * 100,
            year_n1=n1 * 100,
            year_n2=n2 * 100,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Mede a eficiência operacional dos ativos, excluindo efeitos de financiamento e impostos. Benchmark: ≥ 5%"
        )
    
    def _calc_rendibilidade_capital_proprio(self) -> MetricValue:
        """
        #40 - Rendibilidade Capital Próprio (RCP)
        Formula: Resultado Líquido / Capital Próprio
        Different from #30 (Rotação do Capital Próprio) which uses Sales.
        This is a profitability ratio, similar to ROE.
        """
        n = self._safe_divide(self.dr.year_n.resultado_liquido, 
                              self.bs.year_n.total_capital_proprio)
        n1 = self._safe_divide(self.dr.year_n1.resultado_liquido, 
                               self.bs.year_n1.total_capital_proprio)
        n2 = self._safe_divide(self.dr.year_n2.resultado_liquido, 
                               self.bs.year_n2.total_capital_proprio)
        
        return MetricValue(
            nome="Rendibilidade Capital Próprio (RCP)",
            unidade="%",
            year_n=n * 100,
            year_n1=n1 * 100,
            year_n2=n2 * 100,
            tendencia=self._get_trend(n2, n1),
            interpretacao="Rentabilidade do capital próprio. Mede quanto lucro líquido é gerado por cada euro investido pelos acionistas. Benchmark: ≥ 10%"
        )
    
    def _calc_equacao_fundamental_rendibilidade(self) -> MetricValue:
        """
        #41 - Equação Fundamental da Rendibilidade (Dupont Identity)
        Formula: ROE = RLV × RA × LF
        Where:
        - RLV = Rendibilidade Líquida das Vendas (Net Margin)
        - RA = Rotação do Ativo (Asset Turnover)
        - LF = Leverage Financeiro (Financial Leverage)
        
        This is the fundamental Dupont equation decomposing ROE.
        """
        # RLV = Resultado Líquido / Vendas
        rlv_n = self._safe_divide(self.dr.year_n.resultado_liquido, 
                                  self.dr.year_n.vendas_servicos_prestados)
        rlv_n1 = self._safe_divide(self.dr.year_n1.resultado_liquido, 
                                   self.dr.year_n1.vendas_servicos_prestados)
        rlv_n2 = self._safe_divide(self.dr.year_n2.resultado_liquido, 
                                   self.dr.year_n2.vendas_servicos_prestados)
        
        # RA = Vendas / Ativo Total
        ra_n = self._safe_divide(self.dr.year_n.vendas_servicos_prestados, 
                                 self.bs.year_n.total_ativo)
        ra_n1 = self._safe_divide(self.dr.year_n1.vendas_servicos_prestados, 
                                  self.bs.year_n1.total_ativo)
        ra_n2 = self._safe_divide(self.dr.year_n2.vendas_servicos_prestados, 
                                  self.bs.year_n2.total_ativo)
        
        # LF = Ativo Total / Capital Próprio
        lf_n = self._safe_divide(self.bs.year_n.total_ativo, 
                                 self.bs.year_n.total_capital_proprio)
        lf_n1 = self._safe_divide(self.bs.year_n1.total_ativo, 
                                  self.bs.year_n1.total_capital_proprio)
        lf_n2 = self._safe_divide(self.bs.year_n2.total_ativo, 
                                  self.bs.year_n2.total_capital_proprio)
        
        # ROE = RLV × RA × LF
        n = rlv_n * ra_n * lf_n
        n1 = rlv_n1 * ra_n1 * lf_n1
        n2 = rlv_n2 * ra_n2 * lf_n2
        
        return MetricValue(
            nome="Equação Fundamental da Rendibilidade (Dupont)",
            unidade="%",
            year_n=n * 100,
            year_n1=n1 * 100,
            year_n2=n2 * 100,
            tendencia=self._get_trend(n2, n1),
            interpretacao=f"ROE decomposto: Margem Líquida × Rotação Ativo × Alavancagem. Year N: {rlv_n*100:.2f}% × {ra_n:.2f} × {lf_n:.2f} = {n*100:.2f}%"
        )
    
    def _calc_taxa_media_juros_capital_alheio(self) -> MetricValue:
        """
        #46 - Taxa Média de Juros de Capital Alheio
        Formula: Juros Gastos / (Financiamentos NC + Financiamentos C)
        Measures the average interest rate paid on borrowed capital.
        """
        # Total Financiamentos = Financiamentos Não Correntes + Financiamentos Correntes
        fin_n = (self.bs.year_n.financiamentos_obtidos_nc + 
                 self.bs.year_n.financiamentos_obtidos_corrente)
        fin_n1 = (self.bs.year_n1.financiamentos_obtidos_nc + 
                  self.bs.year_n1.financiamentos_obtidos_corrente)
        fin_n2 = (self.bs.year_n2.financiamentos_obtidos_nc + 
                  self.bs.year_n2.financiamentos_obtidos_corrente)
        
        # Juros Gastos
        juros_n = abs(self.dr.year_n.juros_gastos_suportados)
        juros_n1 = abs(self.dr.year_n1.juros_gastos_suportados)
        juros_n2 = abs(self.dr.year_n2.juros_gastos_suportados)
        
        # Taxa = Juros / Financiamentos
        n = self._safe_divide(juros_n, fin_n)
        n1 = self._safe_divide(juros_n1, fin_n1)
        n2 = self._safe_divide(juros_n2, fin_n2)
        
        return MetricValue(
            nome="Taxa Média de Juros de Capital Alheio",
            unidade="%",
            year_n=n * 100,
            year_n1=n1 * 100,
            year_n2=n2 * 100,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao=f"Taxa de juro média paga sobre financiamentos. Year N: {n*100:.2f}%. Comparar com taxa de mercado."
        )
    
    # ========== ADDITIONAL METRICS TO REACH 51/51 ==========
    
    def _calc_duracao_ciclo_financeiro(self) -> MetricValue:
        """
        #26 - Duração do Ciclo Financeiro (DCF)
        Formula: DCF = DCO - PMP
        Same as Necessidades de Fundo de Maneio but expressed differently in Excel.
        """
        dco = self._calc_duracao_ciclo_operacional()
        pmp = self._calc_prazo_medio_pagamento()
        
        n = dco.year_n - pmp.year_n
        n1 = dco.year_n1 - pmp.year_n1
        n2 = dco.year_n2 - pmp.year_n2
        
        return MetricValue(
            nome="Duração do Ciclo Financeiro (DCF)",
            unidade="dias",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao=f"Tempo médio que o capital fica imobilizado no ciclo operacional após deduzir crédito de fornecedores. Year N: {n:.0f} dias."
        )
    
    def _calc_rotacao_aplicacoes_fixas_liquidas_exploracao(self) -> MetricValue:
        """
        #28 - Rotação das Aplicações Fixas Líquidas de Exploração (RAFLE)
        Formula: RAFLE = Vendas / (AFT + Ativos Intangíveis) ENDING VALUES
        Excel: ='Demonstração de Resultados'!E5/(Balanço!E7+Balanço!E10)
        FIXED: Uses ENDING values only (no averages)
        """
        # Calculate fixed assets for each year - USE ENDING VALUES ONLY
        afl_n = self.bs.year_n.ativos_fixos_tangiveis + self.bs.year_n.ativos_intangiveis
        afl_n1 = self.bs.year_n1.ativos_fixos_tangiveis + self.bs.year_n1.ativos_intangiveis
        afl_n2 = self.bs.year_n2.ativos_fixos_tangiveis + self.bs.year_n2.ativos_intangiveis
        
        # Use ENDING values only - no averages!
        n = self._safe_divide(self.dr.year_n.vendas_servicos_prestados, afl_n)
        n1 = self._safe_divide(self.dr.year_n1.vendas_servicos_prestados, afl_n1)
        n2 = self._safe_divide(self.dr.year_n2.vendas_servicos_prestados, afl_n2)
        
        return MetricValue(
            nome="Rotação das Aplicações Fixas Líquidas de Exploração (RAFLE)",
            unidade="vezes",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao=f"Eficiência na utilização dos ativos fixos de exploração para gerar vendas. Year N: {n:.2f}x. Maior é melhor."
        )
    
    def _calc_rotacao_ativo_corrente(self) -> MetricValue:
        """
        #29 - Rotação do Ativo Corrente (RAC)
        Formula: RAC = Vendas / Ativo Corrente ENDING VALUES
        Excel: ='Demonstração de Resultados'!E5/Balanço!E17
        FIXED: Uses ENDING values only (no averages)
        """
        # Use ENDING values only - no averages!
        n = self._safe_divide(self.dr.year_n.vendas_servicos_prestados, self.bs.year_n.total_ativo_corrente)
        n1 = self._safe_divide(self.dr.year_n1.vendas_servicos_prestados, self.bs.year_n1.total_ativo_corrente)
        n2 = self._safe_divide(self.dr.year_n2.vendas_servicos_prestados, self.bs.year_n2.total_ativo_corrente)
        
        return MetricValue(
            nome="Rotação do Ativo Corrente (RAC)",
            unidade="vezes",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao=f"Quantas vezes o ativo corrente é renovado através das vendas. Year N: {n:.2f}x. Benchmark: ≥ 2.0"
        )
    
    def _calc_rotacao_capital_proprio_atividade(self) -> MetricValue:
        """
        #30 - Rotação do Capital Próprio - Atividade (RCP)
        Formula: RCP = Vendas / Capital Próprio ENDING VALUES
        Excel: ='Demonstração de Resultados'!E5/Balanço!E47
        FIXED: Uses ENDING values only (no averages)
        This is the ACTIVITY version (different from #40 which is profitability).
        """
        # Use ENDING values only - no averages!
        n = self._safe_divide(self.dr.year_n.vendas_servicos_prestados, self.bs.year_n.total_capital_proprio)
        n1 = self._safe_divide(self.dr.year_n1.vendas_servicos_prestados, self.bs.year_n1.total_capital_proprio)
        n2 = self._safe_divide(self.dr.year_n2.vendas_servicos_prestados, self.bs.year_n2.total_capital_proprio)
        
        return MetricValue(
            nome="Rotação do Capital Próprio (RCP) - Atividade",
            unidade="vezes",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao=f"Eficiência do capital próprio na geração de vendas. Year N: {n:.2f}x. Valores altos indicam boa utilização do equity."
        )
    
    def _calc_rotacao_ativo_medio_longo(self) -> MetricValue:
        """
        #30 - Rotação do Ativo (Médio/Longo Prazo)
        Formula: RAML = Vendas / Ativo Total
        Similar to RAT but categorized under medium/long-term activity.
        """
        n = self._safe_divide(self.dr.year_n.vendas_servicos_prestados, 
                              self.bs.year_n.total_ativo)
        n1 = self._safe_divide(self.dr.year_n1.vendas_servicos_prestados, 
                               self.bs.year_n1.total_ativo)
        n2 = self._safe_divide(self.dr.year_n2.vendas_servicos_prestados, 
                               self.bs.year_n2.total_ativo)
        
        return MetricValue(
            nome="Rotação do Ativo Total (RAML)",
            unidade="vezes",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao=f"Rotação global dos ativos (médio/longo prazo). Year N: {n:.2f}x. Benchmark: ≥ 1.0"
        )
    
    def _calc_leverage_financeiro(self) -> MetricValue:
        """
        #45b - Leverage Financeiro (LF) - Dupont Component
        Formula: LF = Ativo Total / Capital Próprio
        This is the leverage multiplier used in Dupont analysis.
        Similar to multiplicador_capital but used specifically in ROE decomposition.
        """
        n = self._safe_divide(self.bs.year_n.total_ativo, 
                              self.bs.year_n.total_capital_proprio)
        n1 = self._safe_divide(self.bs.year_n1.total_ativo, 
                               self.bs.year_n1.total_capital_proprio)
        n2 = self._safe_divide(self.bs.year_n2.total_ativo, 
                               self.bs.year_n2.total_capital_proprio)
        
        return MetricValue(
            nome="Leverage Financeiro (LF)",
            unidade="vezes",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao=f"Alavancagem financeira (Dupont). Year N: {n:.2f}x. Indica quanto de ativo é financiado por cada euro de capital próprio."
        )
    
    def _calc_grau_combinado_alavanca(self) -> MetricValue:
        """
        #50 - Grau Combinado de Alavanca (GCA)
        Formula: GCA = GAO × GAF
        Combines operating and financial leverage to show total leverage effect.
        """
        gao = self._calc_grau_alavanca_operacional()
        gaf = self._calc_grau_alavanca_financeira()
        
        n = gao.year_n * gaf.year_n
        n1 = gao.year_n1 * gaf.year_n1
        n2 = gao.year_n2 * gaf.year_n2
        
        return MetricValue(
            nome="Grau Combinado de Alavanca (GCA)",
            unidade="vezes",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1, lower_is_better=True),
            interpretacao=f"Alavanca combinada (operacional × financeira). Year N: {n:.2f}x. Mede sensibilidade total do resultado líquido às variações nas vendas."
        )
    
    def _calc_margem_seguranca(self) -> MetricValue:
        """
        #51 - Margem de Segurança (MSF)
        Formula: MSF = (Vendas - Ponto Crítico) / Vendas
        Where Ponto Crítico = Break-even point
        Simplified: Uses current margin as proxy for safety margin.
        """
        # Simplified calculation: Use operating margin as safety indicator
        # Full calculation would require detailed cost structure (fixed vs variable)
        ro_n = self.dr.year_n.resultado_antes_impostos + self.dr.year_n.juros_gastos_suportados
        ro_n1 = self.dr.year_n1.resultado_antes_impostos + self.dr.year_n1.juros_gastos_suportados
        ro_n2 = self.dr.year_n2.resultado_antes_impostos + self.dr.year_n2.juros_gastos_suportados
        
        # Margem de Segurança = Resultado Operacional / Vendas
        n = self._safe_divide(ro_n, self.dr.year_n.vendas_servicos_prestados)
        n1 = self._safe_divide(ro_n1, self.dr.year_n1.vendas_servicos_prestados)
        n2 = self._safe_divide(ro_n2, self.dr.year_n2.vendas_servicos_prestados)
        
        return MetricValue(
            nome="Margem de Segurança (MSF)",
            unidade="%",
            year_n=n * 100,
            year_n1=n1 * 100,
            year_n2=n2 * 100,
            tendencia=self._get_trend(n2, n1),
            interpretacao=f"Margem de segurança operacional. Year N: {n*100:.2f}%. Quanto as vendas podem cair antes de entrar em prejuízo operacional. Benchmark: ≥ 20%"
        )


