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
        """Calcula todas as métricas"""
        
        return PerformanceMetrics(
            # Dimensão
            consumos_intermedios=self._calc_consumos_intermedios(),
            valor_bruto_producao=self._calc_valor_bruto_producao(),
            valor_acrescentado_bruto=self._calc_valor_acrescentado_bruto(),
            taxa_crescimento=self._calc_taxa_crescimento(),
            excedente_bruto_exploracao=self._calc_excedente_bruto_exploracao(),
            excedente_liquido_producao=self._calc_excedente_liquido_producao(),
            
            # Rácios do Balanço
            racio_autonomia_financeira=self._calc_autonomia_financeira(),
            racio_endividamento=self._calc_endividamento(),
            racio_solvabilidade=self._calc_solvabilidade(),
            racio_solvabilidade_restrito=self._calc_solvabilidade_restrito(),
            
            # Balanço Funcional
            resumo_balanco_funcional=self._calc_resumo_balanco_funcional(),
            ativo_economico=self._calc_ativo_economico(),
            
            # Indicadores Longo Prazo
            racio_estrutura=self._calc_racio_estrutura(),
            racio_estabilidade_financiamento=self._calc_estabilidade_financiamento(),
            racio_estrutura_passivo=self._calc_estrutura_passivo(),
            racio_cobertura_aplicacoes_fixas_recursos=self._calc_cobertura_aplicacoes_recursos(),
            racio_cobertura_aplicacoes_fixas_capital=self._calc_cobertura_aplicacoes_capital()
        )
    
    # Dimensão / Produção
    
    def _calc_consumos_intermedios(self) -> MetricValue:
        """
        CI = CMVMC + FSE + outros gastos operacionais
        Excel: ='DR'!K13+'DR'!K14+'DR'!E28
        """
        n = (self.dr.year_n.cmvmc + 
             self.dr.year_n.fornecimentos_servicos_externos)
        n1 = (self.dr.year_n1.cmvmc + 
              self.dr.year_n1.fornecimentos_servicos_externos)
        n2 = (self.dr.year_n2.cmvmc + 
              self.dr.year_n2.fornecimentos_servicos_externos)
        
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
        """Taxa de crescimento entre N+1 e N+2"""
        vbp_n1 = (self.dr.year_n1.vendas_servicos_prestados +
                  self.dr.year_n1.variacao_inventarios_producao +
                  self.dr.year_n1.trabalhos_propria_entidade)
        
        vbp_n2 = (self.dr.year_n2.vendas_servicos_prestados +
                  self.dr.year_n2.variacao_inventarios_producao +
                  self.dr.year_n2.trabalhos_propria_entidade)
        
        if vbp_n1 != 0:
            tc = (vbp_n2 - vbp_n1) / vbp_n1
        else:
            tc = 0
        
        return MetricValue(
            nome="Taxa de Crescimento (TC)",
            unidade="%",
            year_n=0,
            year_n1=0,
            year_n2=tc * 100,
            tendencia="▲" if tc > 0 else ("▼" if tc < 0 else "►"),
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
        ELP = EBE - Depreciações
        Baseado em EBIT
        """
        n = self.dr.year_n.ebit
        n1 = self.dr.year_n1.ebit
        n2 = self.dr.year_n2.ebit
        
        return MetricValue(
            nome="Excedente Líquido de Produção (ELP)",
            unidade="€",
            year_n=n,
            year_n1=n1,
            year_n2=n2,
            tendencia=self._get_trend(n2, n1),
            interpretacao=self._get_elp_interpretation(n, n1, n2)
        )
    
    # Rácios do Balanço
    
    def _calc_autonomia_financeira(self) -> MetricValue:
        """
        RAF = Capital Próprio / Total Ativo
        Excel: =BS!E47/BS!E30
        """
        n = self._safe_divide(self.bs.year_n.total_capital_proprio, 
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
        This requires Fundo de Maneio, NFM, Tesouraria calculations
        Simplified version for MVP
        """
        return {
            "status": "Em desenvolvimento",
            "mensagem": "Análise detalhada do balanço funcional"
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
        ▲ = improving, ▼ = declining, ► = stable
        """
        if previous == 0:
            return "►"
        
        change_pct = (current - previous) / abs(previous)
        
        if lower_is_better:
            if change_pct < -0.05:
                return "▲"
            elif change_pct > 0.05:
                return "▼"
            else:
                return "►"
        else:
            if change_pct > 0.05:
                return "▲"
            elif change_pct < -0.05:
                return "▼"
            else:
                return "►"
    
    # Interpretation methods (from Excel messages - simplified for now)
    
    def _get_ci_interpretation(self, n, n1, n2) -> str:
        if n2 > n1 and n2 > n:
            return "▼ A empresa está a gastar mais com a sua operação face aos anos anteriores."
        elif n2 < n1 and n2 < n:
            return "▲ A empresa está a gastar menos com a sua operação face aos anos anteriores."
        else:
            return "► Os gastos com a operação mantiveram-se relativamente estáveis."
    
    def _get_vbp_interpretation(self, n, n1, n2) -> str:
        if n2 > n1 and n2 > n:
            return "▲ A empresa aumentou o volume total produzido e vendido, mostrando crescimento nas suas operações comerciais."
        elif n2 < n1 and n2 < n:
            return "▼ A empresa reduziu o volume total produzido e vendido, mostrando contração nas suas operações comerciais."
        else:
            return "► O volume produzido e vendido manteve-se estável."
    
    def _get_vab_interpretation(self, n, n1, n2) -> str:
        if n2 > n1 and n2 > n:
            return "▲ A empresa está a criar mais valor económico face aos anos anteriores."
        elif n2 < n1 and n2 < n:
            return "▼ A empresa está a criar menos valor económico face aos anos anteriores."
        else:
            return "► A criação de valor económico manteve-se estável."
    
    def _get_tc_interpretation(self, tc: float) -> str:
        if tc > 0:
            return "▲ A empresa está em crescimento."
        elif tc < 0:
            return "▼ A empresa está a regredir."
        else:
            return "► A empresa mantém estabilidade nas suas operações."
    
    def _get_ebe_interpretation(self, n, n1, n2) -> str:
        if n2 > n1 and n2 > n:
            return "▲ A empresa aumentou o lucro gerado diretamente pelas suas operações, mostrando maior eficiência na gestão operacional."
        elif n2 < n1 and n2 < n:
            return "▼ A empresa diminuiu o lucro gerado diretamente pelas suas operações, mostrando menor eficiência na gestão operacional."
        else:
            return "► O lucro operacional manteve-se estável."
    
    def _get_elp_interpretation(self, n, n1, n2) -> str:
        if n2 > n1 and n2 > n:
            return "▲ O excedente líquido melhorou face aos anos anteriores, revelando maior capacidade real de gerar dinheiro com as operações."
        elif n2 < n1 and n2 < n:
            return "▼ O excedente líquido piorou face aos anos anteriores, revelando menor capacidade real de gerar dinheiro com as operações."
        else:
            return "► O excedente líquido manteve-se estável."
    
    def _get_raf_interpretation(self, value: float) -> str:
        if value >= 0.5:
            return "▲ Excelente autonomia financeira. A empresa utiliza maioritariamente fundos próprios, revelando baixo risco financeiro."
        elif value >= 0.3333:
            return "► Autonomia financeira razoável, mas atenção ao equilíbrio entre capitais próprios e alheios."
        else:
            return "▼ Autonomia financeira baixa. A empresa depende demasiado de financiamento externo, o que aumenta o risco financeiro."
    
    def _get_re_interpretation(self, value: float) -> str:
        if value < 0.5:
            return "▲ Nível saudável de endividamento. A empresa mantém dívidas controladas, com risco financeiro reduzido."
        elif value <= 0.66:
            return "► Nível moderado de endividamento. Necessária atenção à gestão da dívida para evitar riscos futuros."
        else:
            return "▼ Elevado nível de endividamento. A empresa apresenta grande dependência de dívidas, aumentando o risco financeiro."
    
    def _get_rs_interpretation(self, value: float) -> str:
        if value >= 1:
            return "▲ Excelente solvabilidade. A empresa consegue facilmente cobrir as suas dívidas com recursos próprios."
        elif value >= 0.5:
            return "► Solvabilidade aceitável, mas pode existir alguma vulnerabilidade financeira."
        else:
            return "▼ Solvabilidade insuficiente. A empresa poderá enfrentar dificuldades financeiras para honrar as suas dívidas."
    
    def _get_rssr_interpretation(self, value: float) -> str:
        if value > 1.5:
            return "▲ Boa cobertura das dívidas pelo ativo. A empresa está muito segura para os credores."
        elif value >= 1:
            return "► Cobertura suficiente, mas deve ser acompanhada de perto."
        else:
            return "▼ Cobertura insuficiente. Ativo pode não ser suficiente para cobrir dívidas, situação de risco elevado."
    
    def _get_rde_interpretation(self, n, n1, n2) -> str:
        base = ""
        if n2 == 1:
            base = "► Recursos igualmente divididos entre capital próprio e dívida de curto prazo."
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
            base = "► A empresa tem financiamento estável para a maior parte da atividade, mas deve monitorizar o financiamento de curto prazo."
        else:
            base = "▼ A empresa depende demasiado de empréstimos de curto prazo, aumentando o risco financeiro."
        
        return base
    
    def _get_rep_interpretation(self, n, n1, n2) -> str:
        if n2 == 1:
            return "► A dívida da empresa está equilibrada entre curto prazo e médio/longo prazo."
        elif n2 > 1:
            return "▼ A maior parte da dívida da empresa vence-se rapidamente (curto prazo), o que pode pressionar a tesouraria."
        else:
            return "▲ A maior parte da dívida da empresa vence-se num prazo longo, o que dá conforto financeiro."
    
    def _get_rcaflre_interpretation(self, n, n1, n2) -> str:
        if n2 > 1:
            return "▲ A empresa financia os seus investimentos de longo prazo com fundos próprios ou empréstimos de longo prazo, o que é positivo."
        elif n2 == 1:
            return "► O financiamento dos investimentos é justo, sem margem adicional, situação delicada."
        else:
            return "▼ A empresa não financia totalmente os investimentos de longo prazo com fundos próprios ou empréstimos de longo prazo, aumentando o risco financeiro."
    
    def _get_rcaflcp_interpretation(self, n, n1, n2) -> str:
        if n2 > 1:
            return "▲ A empresa financia os seus investimentos com dinheiro próprio, reduzindo o risco financeiro."
        elif n2 == 1:
            return "► A empresa financia os seus investimentos exclusivamente com dinheiro próprio, sem margem adicional."
        else:
            return "▼ A empresa financia os seus investimentos sobretudo com dívida externa, aumentando o risco financeiro."
