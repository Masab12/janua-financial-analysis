from pydantic import BaseModel, Field, validator
from typing import Union
import re

def parse_portuguese_number(value: Union[str, int, float]) -> float:
    """
    Parse Portuguese number format (handles commas as decimal separators)
    """
    if value is None or value == "":
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        # Remove spaces and handle empty strings
        value = value.strip()
        if value == "" or value == "-":
            return 0.0
        
        # Handle Portuguese format: 1.234.567,89 or simple comma format: 1234,89
        # If there are multiple dots and one comma, assume Portuguese format
        if value.count('.') > 1 and value.count(',') == 1:
            # Portuguese format: 1.234.567,89
            value = value.replace('.', '').replace(',', '.')
        elif value.count(',') > 1 and value.count('.') == 1:
            # US format with commas: 1,234,567.89
            value = value.replace(',', '')
        elif ',' in value and '.' in value:
            # Determine which is decimal separator by position
            comma_pos = value.rfind(',')
            dot_pos = value.rfind('.')
            if comma_pos > dot_pos:
                # Comma is decimal separator: 1.234,89
                value = value.replace('.', '').replace(',', '.')
            else:
                # Dot is decimal separator: 1,234.89
                value = value.replace(',', '')
        elif ',' in value and '.' not in value:
            # Only comma, assume decimal separator: 1234,89
            value = value.replace(',', '.')
        
        # Remove any remaining non-numeric characters except dots and minus
        value = re.sub(r'[^\d.-]', '', value)
        
        try:
            return float(value)
        except ValueError:
            return 0.0
    
    return 0.0

class IncomeStatementYear(BaseModel):
    """
    Demonstração de Resultados para um único ano.
    Based on Excel 'Demonstração de Resultados' sheet.
    """
    
    vendas_servicos_prestados: float = Field(default=0.0)
    subsidios_exploracao: float = Field(default=0.0)
    ganhos_perdas_subsidiarias: float = Field(default=0.0)
    variacao_inventarios_producao: float = Field(default=0.0)
    trabalhos_propria_entidade: float = Field(default=0.0)
    cmvmc: float = Field(default=0.0)  # Custo das Mercadorias Vendidas e Matérias Consumidas
    fornecimentos_servicos_externos: float = Field(default=0.0)
    gastos_pessoal: float = Field(default=0.0)
    imparidade_inventarios: float = Field(default=0.0)
    imparidade_dividas_receber: float = Field(default=0.0)
    provisoes: float = Field(default=0.0)
    imparidade_investimentos_nao_depreciaveis: float = Field(default=0.0)
    aumentos_reducoes_justo_valor: float = Field(default=0.0)
    outros_rendimentos_ganhos: float = Field(default=0.0)
    outros_gastos_perdas: float = Field(default=0.0)
    gastos_depreciacoes_amortizacoes: float = Field(default=0.0)
    juros_rendimentos_obtidos: float = Field(default=0.0)
    juros_gastos_suportados: float = Field(default=0.0)
    imposto_rendimento: float = Field(default=0.0)
    
    # Validators for Portuguese number format
    @validator('*', pre=True)
    def parse_numbers(cls, v):
        """Parse Portuguese number formats for all numeric fields"""
        return parse_portuguese_number(v)
    
    @property
    def ebitda(self) -> float:
        """
        EBITDA calculation based on Excel logic.
        This is derived from the income statement items.
        """
        return (
            self.vendas_servicos_prestados +
            self.subsidios_exploracao +
            self.ganhos_perdas_subsidiarias +
            self.variacao_inventarios_producao +
            self.trabalhos_propria_entidade -
            self.cmvmc -
            self.fornecimentos_servicos_externos -
            self.gastos_pessoal -
            self.imparidade_inventarios -
            self.imparidade_dividas_receber -
            self.provisoes -
            self.imparidade_investimentos_nao_depreciaveis +
            self.aumentos_reducoes_justo_valor +
            self.outros_rendimentos_ganhos -
            self.outros_gastos_perdas
        )
    
    @property
    def ebit(self) -> float:
        """EBIT = EBITDA - Depreciações"""
        return self.ebitda - self.gastos_depreciacoes_amortizacoes
    
    @property
    def resultado_antes_impostos(self) -> float:
        """Resultado antes de impostos"""
        return (
            self.ebit +
            self.juros_rendimentos_obtidos -
            self.juros_gastos_suportados
        )
    
    @property
    def resultado_liquido(self) -> float:
        """Resultado líquido do período"""
        return self.resultado_antes_impostos - self.imposto_rendimento


class IncomeStatement(BaseModel):
    """Demonstração de Resultados completa para os 3 anos"""
    year_n: IncomeStatementYear
    year_n1: IncomeStatementYear
    year_n2: IncomeStatementYear
