from pydantic import BaseModel, Field
from typing import Optional

class BalanceSheetYear(BaseModel):
    """
    Estrutura do Balanço para um único ano.
    Based on Excel file 'Balanço' sheet structure.
    """
    
    # Ativo Não Corrente
    ativos_fixos_tangiveis: float = Field(default=0.0, ge=0)
    propriedades_investimento: float = Field(default=0.0, ge=0)
    goodwill: float = Field(default=0.0, ge=0)
    ativos_intangiveis: float = Field(default=0.0, ge=0)
    investimentos_financeiros: float = Field(default=0.0, ge=0)
    acionistas_socios_nc: float = Field(default=0.0, ge=0)
    outros_ativos_financeiros: float = Field(default=0.0, ge=0)
    ativos_impostos_diferidos: float = Field(default=0.0, ge=0)
    outros_ativos_nao_correntes: float = Field(default=0.0, ge=0)
    
    # Ativo Corrente
    inventarios: float = Field(default=0.0, ge=0)
    clientes: float = Field(default=0.0, ge=0)
    adiantamentos_fornecedores: float = Field(default=0.0, ge=0)
    estado_outros_entes_publicos_ativo: float = Field(default=0.0, ge=0)
    acionistas_socios_corrente: float = Field(default=0.0, ge=0)
    outras_contas_receber: float = Field(default=0.0, ge=0)
    diferimentos_ativo: float = Field(default=0.0, ge=0)
    ativos_financeiros_correntes: float = Field(default=0.0, ge=0)
    outros_ativos_correntes: float = Field(default=0.0, ge=0)
    caixa_depositos_bancarios: float = Field(default=0.0, ge=0)
    
    # Capital Próprio
    capital_realizado: float = Field(default=0.0)
    acoes_quotas_proprias: float = Field(default=0.0)
    outros_instrumentos_capital_proprio: float = Field(default=0.0)
    premios_emissao: float = Field(default=0.0)
    reservas_legais: float = Field(default=0.0)
    outras_reservas: float = Field(default=0.0)
    resultados_transitados: float = Field(default=0.0)
    ajustamentos_ativos_financeiros: float = Field(default=0.0)
    excedentes_revalorizacao: float = Field(default=0.0)
    outras_variacoes_capital_proprio: float = Field(default=0.0)
    resultado_liquido_periodo: float = Field(default=0.0)
    interesses_minoritarios: float = Field(default=0.0)
    
    # Passivo Não Corrente
    provisoes_nc: float = Field(default=0.0, ge=0)
    financiamentos_obtidos_nc: float = Field(default=0.0, ge=0)
    responsabilidades_beneficios_pos_emprego: float = Field(default=0.0, ge=0)
    passivos_impostos_diferidos: float = Field(default=0.0, ge=0)
    outras_contas_pagar_nc: float = Field(default=0.0, ge=0)
    outros_passivos_nao_correntes: float = Field(default=0.0, ge=0)
    
    # Passivo Corrente
    fornecedores: float = Field(default=0.0, ge=0)
    adiantamentos_clientes: float = Field(default=0.0, ge=0)
    estado_outros_entes_publicos_passivo: float = Field(default=0.0, ge=0)
    acionistas_socios_passivo: float = Field(default=0.0, ge=0)
    financiamentos_obtidos_corrente: float = Field(default=0.0, ge=0)
    outras_contas_pagar_corrente: float = Field(default=0.0, ge=0)
    diferimentos_passivo: float = Field(default=0.0, ge=0)
    outros_passivos_correntes: float = Field(default=0.0, ge=0)
    
    @property
    def total_ativo_nao_corrente(self) -> float:
        """Total de Ativos Não Correntes"""
        return (
            self.ativos_fixos_tangiveis +
            self.propriedades_investimento +
            self.goodwill +
            self.ativos_intangiveis +
            self.investimentos_financeiros +
            self.acionistas_socios_nc +
            self.outros_ativos_financeiros +
            self.ativos_impostos_diferidos +
            self.outros_ativos_nao_correntes
        )
    
    @property
    def total_ativo_corrente(self) -> float:
        """Total de Ativos Correntes"""
        return (
            self.inventarios +
            self.clientes +
            self.adiantamentos_fornecedores +
            self.estado_outros_entes_publicos_ativo +
            self.acionistas_socios_corrente +
            self.outras_contas_receber +
            self.diferimentos_ativo +
            self.ativos_financeiros_correntes +
            self.outros_ativos_correntes +
            self.caixa_depositos_bancarios
        )
    
    @property
    def total_ativo(self) -> float:
        """Total do Ativo"""
        return self.total_ativo_nao_corrente + self.total_ativo_corrente
    
    @property
    def total_capital_proprio(self) -> float:
        """Total do Capital Próprio"""
        return (
            self.capital_realizado +
            self.acoes_quotas_proprias +
            self.outros_instrumentos_capital_proprio +
            self.premios_emissao +
            self.reservas_legais +
            self.outras_reservas +
            self.resultados_transitados +
            self.ajustamentos_ativos_financeiros +
            self.excedentes_revalorizacao +
            self.outras_variacoes_capital_proprio +
            self.resultado_liquido_periodo +
            self.interesses_minoritarios
        )
    
    @property
    def total_passivo_nao_corrente(self) -> float:
        """Total do Passivo Não Corrente"""
        return (
            self.provisoes_nc +
            self.financiamentos_obtidos_nc +
            self.responsabilidades_beneficios_pos_emprego +
            self.passivos_impostos_diferidos +
            self.outras_contas_pagar_nc +
            self.outros_passivos_nao_correntes
        )
    
    @property
    def total_passivo_corrente(self) -> float:
        """Total do Passivo Corrente"""
        return (
            self.fornecedores +
            self.adiantamentos_clientes +
            self.estado_outros_entes_publicos_passivo +
            self.acionistas_socios_passivo +
            self.financiamentos_obtidos_corrente +
            self.outras_contas_pagar_corrente +
            self.diferimentos_passivo +
            self.outros_passivos_correntes
        )
    
    @property
    def total_passivo(self) -> float:
        """Total do Passivo"""
        return self.total_passivo_nao_corrente + self.total_passivo_corrente


class BalanceSheet(BaseModel):
    """Balanço completo para os 3 anos (N, N+1, N+2)"""
    year_n: BalanceSheetYear
    year_n1: BalanceSheetYear
    year_n2: BalanceSheetYear
