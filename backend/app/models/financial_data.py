from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.balance_sheet import BalanceSheet
from app.models.income_statement import IncomeStatement

class InputData(BaseModel):
    """Complete input data structure"""
    nome_entidade: str = Field(..., min_length=1, max_length=200, description="Nome da entidade/empresa")
    data_analise: Optional[str] = Field(default=None, description="Data da análise (opcional)")
    balanco: BalanceSheet
    demonstracao_resultados: IncomeStatement


class MetricValue(BaseModel):
    """Single metric with values for 3 years and trend"""
    nome: str
    unidade: str  # "€", "%", "ratio", "dias"
    year_n: float
    year_n1: float
    year_n2: float
    tendencia: str  # "▲", "▼", "►"
    interpretacao: Optional[str] = None


class PerformanceMetrics(BaseModel):
    """
    ALL 51 performance metrics as per Excel 'Performance' sheet.
    Based on exact Excel formulas extracted from rows 3-59.
    """
    
    # ========== DIMENSÃO / PRODUÇÃO (6 metrics) ==========
    consumos_intermedios: MetricValue  # Row 3: CI = CMVMC + FSE
    valor_bruto_producao: MetricValue  # Row 4: VBP = Vendas + Var.Inv + Trab.Próprios + Subsídios
    valor_acrescentado_bruto: MetricValue  # Row 5: VAB = VBP - CI
    taxa_crescimento: MetricValue  # Row 6: TC = (VAB_N - VAB_N-1) / VAB_N-1
    excedente_bruto_exploracao: MetricValue  # Row 7: EBE = VAB - Gastos Pessoal
    excedente_liquido_producao: MetricValue  # Row 8: ELP = EBE - Depreciações
    
    # ========== RÁCIOS DO BALANÇO (4 metrics) ==========
    racio_autonomia_financeira: MetricValue  # Row 10: RAF = CP / Ativo Total
    racio_endividamento: MetricValue  # Row 11: RE = Passivo / Ativo Total
    racio_solvabilidade: MetricValue  # Row 12: RS = CP / Passivo
    racio_solvabilidade_restrito: MetricValue  # Row 13: RSSR = Ativo / Passivo
    
    # ========== RESUMO BALANÇO FUNCIONAL (2 metrics) ==========
    resumo_balanco_funcional: dict  # Row 14: Status Bom/Médio/Mau
    ativo_economico: MetricValue  # Row 15: AE = Ativo NC + NFM
    
    # ========== INDICADORES LONGO PRAZO (8 metrics) ==========
    racio_estrutura: MetricValue  # Row 17: RDE = Passivo NC / CP
    racio_estabilidade_financiamento: MetricValue  # Row 18: REF = (CP + PNC) / ANC
    racio_estrutura_passivo: MetricValue  # Row 19: REP = Passivo NC / Passivo Total
    racio_cobertura_aplicacoes_fixas_recursos: MetricValue  # Row 20: RCAFLRE
    racio_cobertura_aplicacoes_fixas_capital: MetricValue  # Row 21: RCAFLCP = CP / ANC
    racio_estrutura_endividamento: MetricValue  # Row 22: REE = PC / Passivo Total
    racio_cobertura_gastos_financiamento: MetricValue  # Row 23: RCGFRO = (RO + Dep) / GF
    racio_gastos_financiamento: MetricValue  # Row 24: RGF = GF / Subsídios
    
    # ========== RÁCIOS DE ATIVIDADE CURTO PRAZO (6 metrics) ==========
    rotacao_inventarios: MetricValue  # Row 21: RI = CMVMC / Inventários
    duracao_media_inventarios: MetricValue  # Row 22: DMI = (Inv / CMVMC) × 365
    prazo_medio_recebimento: MetricValue  # Row 23: PMR = (Clientes / Vendas×1.23) × 365
    prazo_medio_pagamento: MetricValue  # Row 24: PMP = (Forn / CMVMC×1.23) × 365
    duracao_ciclo_operacional: MetricValue  # Row 25: DCO = DMI + PMR
    duracao_ciclo_financeiro: MetricValue  # Row 26: DCF = DCO - PMP (same as NFM in days)
    
    # ========== RÁCIOS DE ATIVIDADE MÉDIO/LONGO PRAZO (4 metrics) ==========
    rotacao_aplicacoes_fixas_liquidas_exploracao: MetricValue  # Row 27: RAFLE = Vendas / AFL Exploração
    rotacao_ativo_corrente: MetricValue  # Row 28: RAC = Vendas / Ativo Corrente
    rotacao_capital_proprio_atividade: MetricValue  # Row 29: RCP = Vendas / CP (activity)
    rotacao_ativo_medio_longo: MetricValue  # Row 30: RAML = Vendas / Ativo Total
    
    # ========== RENTABILIDADE (7 metrics) ==========
    return_on_assets: MetricValue  # Row 34: ROA = RL / Ativo (Net Income based)
    return_on_equity: MetricValue  # Row 35: ROE = RL / CP
    rentabilidade_operacional_vendas: MetricValue  # Row 36: ROV = RO / Vendas
    rentabilidade_liquida_vendas: MetricValue  # Row 37: RLV = RL / Vendas
    rendibilidade_operacional_ativo: MetricValue  # Row 39: ROA Operacional = RO / Ativo (EBIT based)
    rendibilidade_capital_proprio: MetricValue  # Row 40: RCP = RL / CP (profitability)
    equacao_fundamental_rendibilidade: MetricValue  # Row 41: Dupont = RLV × RA × LF
    
    # ========== EFICIÊNCIA (4 metrics) ==========
    rotacao_ativo: MetricValue  # Row 33: RAT = Vendas / Ativo
    rotacao_ativo_fixo: MetricValue  # Row 34: RAFx = Vendas / (AFT + AI)
    produtividade_ativo: MetricValue  # Row 35: PA = Vendas / Ativo Corrente
    produtividade_capital_proprio: MetricValue  # Row 36: PCP = Vendas / CP
    
    # ========== LIQUIDEZ (3 metrics) ==========
    liquidez_geral: MetricValue  # Row 31: LG = AC / PC
    liquidez_reduzida: MetricValue  # Row 32: LR = (AC - Inv - Dif) / PC
    liquidez_imediata: MetricValue  # Row 33: LI = Caixa / PC
    
    # ========== RISCO (4 metrics) ==========
    grau_alavanca_financeira: MetricValue  # Row 49: GAF = RO / (RO - GF)
    grau_alavanca_operacional: MetricValue  # Row 48: GAO = (Vendas - CV) / RO
    cobertura_juros: MetricValue  # Row 50: CJ = RO / Juros
    indice_solidez_financeira: MetricValue  # Row 51: ISF = CP / Ativo
    
    # ========== ANÁLISE DUPONT & ALAVANCAS (8 metrics) ==========
    margem_liquida: MetricValue  # Row 43: ML = RL / Vendas (duplicate RLV)
    rotacao_ativo_total: MetricValue  # Row 44: RAT = Vendas / Ativo
    roe_dupont: MetricValue  # Row 42: ROE = ML × RAT × Mult.Capital
    multiplicador_capital: MetricValue  # Row 45: MC = Ativo / CP (Leverage)
    leverage_financeiro: MetricValue  # Row 45b: LF = Ativo / CP (Dupont leverage component)
    rentabilidade_ajustada: MetricValue  # Row 47: RA with tax adjustments
    taxa_media_juros_capital_alheio: MetricValue  # Row 46: Taxa Juros = Juros / Financiamentos
    grau_combinado_alavanca: MetricValue  # Row 50: GCA = GAO × GAF
    margem_seguranca: MetricValue  # Row 51: MSF = (Vendas - Ponto Crítico) / Vendas


class CalculationResult(BaseModel):
    """Complete calculation result"""
    timestamp: datetime
    empresa: str
    metrics: PerformanceMetrics
    success: bool
    message: str
