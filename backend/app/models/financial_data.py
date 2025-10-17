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
    All performance metrics as per Excel 'Performance' sheet.
    Based on actual Excel formulas extracted.
    """
    
    # Dimensão / Produção
    consumos_intermedios: MetricValue  # CI
    valor_bruto_producao: MetricValue  # VBP
    valor_acrescentado_bruto: MetricValue  # VAB
    taxa_crescimento: MetricValue  # TC
    excedente_bruto_exploracao: MetricValue  # EBE
    excedente_liquido_producao: MetricValue  # ELP
    
    # Rácios do Balanço
    racio_autonomia_financeira: MetricValue  # RAF
    racio_endividamento: MetricValue  # RE
    racio_solvabilidade: MetricValue  # RS
    racio_solvabilidade_restrito: MetricValue  # RSSR
    
    # Resumo Balanço Funcional
    resumo_balanco_funcional: dict  # Status: Bom/Médio/Fraco
    ativo_economico: MetricValue
    
    # Indicadores Longo Prazo
    racio_estrutura: MetricValue  # RDE
    racio_estabilidade_financiamento: MetricValue  # REF
    racio_estrutura_passivo: MetricValue  # REP
    racio_cobertura_aplicacoes_fixas_recursos: MetricValue  # RCAFLRE
    racio_cobertura_aplicacoes_fixas_capital: MetricValue  # RCAFLCP


class CalculationResult(BaseModel):
    """Complete calculation result"""
    timestamp: datetime
    empresa: str
    metrics: PerformanceMetrics
    success: bool
    message: str
