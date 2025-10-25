"""
Validation utilities for financial data.
Checks that the data makes sense before we try to calculate anything.
"""

from typing import Tuple
from app.models.balance_sheet import BalanceSheet
from app.models.income_statement import IncomeStatement
from app.exceptions import ValidationError, BalanceSheetError
from app.config import settings
from app.logger import get_logger

logger = get_logger(__name__)


def validate_balance_sheet(balanco: BalanceSheet) -> bool:
    """
    Check if the balance sheet actually balances.
    Basic accounting equation: Assets = Liabilities + Equity
    
    We allow a tolerance for rounding differences in manually entered/test data.
    """
    tolerance = 1000.0  # Reduced tolerance for better accuracy (€1,000)
    
    # Check year N
    assets_n = balanco.year_n.total_ativo
    liabilities_equity_n = balanco.year_n.total_passivo + balanco.year_n.total_capital_proprio
    diff_n = abs(assets_n - liabilities_equity_n)
    
    if diff_n > tolerance:
        logger.warning(f"Balance sheet year N doesn't balance. Difference: {diff_n}")
        raise BalanceSheetError(
            f"REGRA VIOLADA: Total do Ativo = Total do Passivo + Capital Próprio (Ano N)\n"
            f"Diferença encontrada: €{diff_n:.2f}\n"
            f"Total do Ativo (Ano N): €{assets_n:,.2f}\n"
            f"Total do Passivo + Capital Próprio (Ano N): €{liabilities_equity_n:,.2f}\n"
            f"Verifique se todos os valores foram inseridos corretamente."
        )
    
    # Check year N-1
    assets_n1 = balanco.year_n1.total_ativo
    liabilities_equity_n1 = balanco.year_n1.total_passivo + balanco.year_n1.total_capital_proprio
    diff_n1 = abs(assets_n1 - liabilities_equity_n1)
    
    if diff_n1 > tolerance:
        logger.warning(f"Balance sheet year N-1 doesn't balance. Difference: {diff_n1}")
        raise BalanceSheetError(
            f"REGRA VIOLADA: Total do Ativo = Total do Passivo + Capital Próprio (Ano N-1)\n"
            f"Diferença encontrada: €{diff_n1:.2f}\n"
            f"Total do Ativo (Ano N-1): €{assets_n1:,.2f}\n"
            f"Total do Passivo + Capital Próprio (Ano N-1): €{liabilities_equity_n1:,.2f}"
        )
    
    # Check year N-2
    assets_n2 = balanco.year_n2.total_ativo
    liabilities_equity_n2 = balanco.year_n2.total_passivo + balanco.year_n2.total_capital_proprio
    diff_n2 = abs(assets_n2 - liabilities_equity_n2)
    
    if diff_n2 > tolerance:
        logger.warning(f"Balance sheet year N-2 doesn't balance. Difference: {diff_n2}")
        raise BalanceSheetError(
            f"REGRA VIOLADA: Total do Ativo = Total do Passivo + Capital Próprio (Ano N-2)\n"
            f"Diferença encontrada: €{diff_n2:.2f}\n"
            f"Total do Ativo (Ano N-2): €{assets_n2:,.2f}\n"
            f"Total do Passivo + Capital Próprio (Ano N-2): €{liabilities_equity_n2:,.2f}"
        )
    
    logger.debug("Balance sheet validation passed for all years")
    return True


def validate_positive_values(balanco: BalanceSheet) -> bool:
    """
    Check that certain values are positive.
    Things like total assets, equity should never be negative in normal cases.
    """
    
    # Check year N
    if balanco.year_n.total_ativo <= 0:
        raise ValidationError("Total do Ativo do ano N deve ser positivo")
    
    if balanco.year_n.total_capital_proprio < 0:
        logger.warning("Negative equity detected in year N - company might be insolvent")
        # Don't raise error - negative equity is possible (just bad)
    
    # Check year N-1
    if balanco.year_n1.total_ativo <= 0:
        raise ValidationError("Total do Ativo do ano N-1 deve ser positivo")
    
    # Check year N-2
    if balanco.year_n2.total_ativo <= 0:
        raise ValidationError("Total do Ativo do ano N-2 deve ser positivo")
    
    return True


def validate_income_statement(demonstracao: IncomeStatement) -> bool:
    """
    Check income statement for obvious errors.
    Revenue should typically be positive, but we allow edge cases.
    """
    
    # Check if revenue is present for at least one year
    total_revenue = (
        demonstracao.year_n.vendas_servicos_prestados +
        demonstracao.year_n1.vendas_servicos_prestados +
        demonstracao.year_n2.vendas_servicos_prestados
    )
    
    if total_revenue <= 0:
        logger.warning("No revenue detected in any year")
        raise ValidationError(
            "A empresa deve ter receitas em pelo menos um dos anos analisados"
        )
    
    return True


def validate_reasonable_values(balanco: BalanceSheet, demonstracao: IncomeStatement) -> bool:
    """
    Sanity check - make sure values aren't absurdly large.
    Prevents issues with data entry errors (like adding extra zeros).
    """
    
    max_value = settings.max_financial_value
    
    # Check balance sheet
    if balanco.year_n.total_ativo > max_value:
        raise ValidationError(
            f"Valor do Ativo parece demasiado alto: €{balanco.year_n.total_ativo:,.0f}. "
            f"Verifique se não adicionou zeros a mais."
        )
    
    # Check revenue
    if demonstracao.year_n.vendas_servicos_prestados > max_value:
        raise ValidationError(
            f"Valor de Vendas parece demasiado alto: €{demonstracao.year_n.vendas_servicos_prestados:,.0f}. "
            f"Verifique se não adicionou zeros a mais."
        )
    
    return True


def validate_net_result_consistency(balanco: BalanceSheet, demonstracao: IncomeStatement) -> bool:
    """
    Check that Net Result for the Period matches between Balance Sheet and Income Statement.
    This is a critical accounting validation as per client requirements.
    """
    
    # Check year N
    bs_result_n = balanco.year_n.resultado_liquido_periodo
    is_result_n = demonstracao.year_n.resultado_liquido
    
    if abs(bs_result_n - is_result_n) > 1.0:  # Allow €1 tolerance for rounding
        raise ValidationError(
            f"REGRA VIOLADA: Resultado Líquido deve ser igual no Balanço e na Demonstração de Resultados (Ano N)\n"
            f"Resultado Líquido no Balanço (Ano N): €{bs_result_n:,.2f}\n"
            f"Resultado Líquido na Demonstração de Resultados (Ano N): €{is_result_n:,.2f}\n"
            f"Diferença: €{abs(bs_result_n - is_result_n):.2f}\n"
            f"Verifique se inseriu o mesmo valor nos dois locais."
        )
    
    # Check year N-1
    bs_result_n1 = balanco.year_n1.resultado_liquido_periodo
    is_result_n1 = demonstracao.year_n1.resultado_liquido
    
    if abs(bs_result_n1 - is_result_n1) > 1.0:
        raise ValidationError(
            f"REGRA VIOLADA: Resultado Líquido deve ser igual no Balanço e na Demonstração de Resultados (Ano N-1)\n"
            f"Resultado Líquido no Balanço (Ano N-1): €{bs_result_n1:,.2f}\n"
            f"Resultado Líquido na Demonstração de Resultados (Ano N-1): €{is_result_n1:,.2f}\n"
            f"Diferença: €{abs(bs_result_n1 - is_result_n1):.2f}"
        )
    
    # Check year N-2
    bs_result_n2 = balanco.year_n2.resultado_liquido_periodo
    is_result_n2 = demonstracao.year_n2.resultado_liquido
    
    if abs(bs_result_n2 - is_result_n2) > 1.0:
        raise ValidationError(
            f"REGRA VIOLADA: Resultado Líquido deve ser igual no Balanço e na Demonstração de Resultados (Ano N-2)\n"
            f"Resultado Líquido no Balanço (Ano N-2): €{bs_result_n2:,.2f}\n"
            f"Resultado Líquido na Demonstração de Resultados (Ano N-2): €{is_result_n2:,.2f}\n"
            f"Diferença: €{abs(bs_result_n2 - is_result_n2):.2f}"
        )
    
    logger.debug("Net result consistency validation passed for all years")
    return True


def validate_on_request_only(balanco: BalanceSheet, demonstracao: IncomeStatement) -> Tuple[bool, str]:
    """
    Run all validation checks ONLY when explicitly called by API endpoints.
    This prevents validation errors from appearing on app load.
    
    Returns (success, message) tuple.
    """
    try:
        # Only validate if we have actual data (not just default zeros)
        has_balance_data = (
            balanco.year_n.total_ativo > 0 or 
            balanco.year_n1.total_ativo > 0 or 
            balanco.year_n2.total_ativo > 0
        )
        
        has_income_data = (
            demonstracao.year_n.vendas_servicos_prestados != 0 or
            demonstracao.year_n1.vendas_servicos_prestados != 0 or
            demonstracao.year_n2.vendas_servicos_prestados != 0
        )
        
        # If no real data, skip validation (this prevents errors on app load)
        if not has_balance_data and not has_income_data:
            logger.debug("No financial data provided, skipping validation")
            return True, "Nenhum dado fornecido para validação"
        
        # Run all validation checks
        validate_balance_sheet(balanco)
        validate_positive_values(balanco)
        validate_income_statement(demonstracao)
        validate_net_result_consistency(balanco, demonstracao)
        validate_reasonable_values(balanco, demonstracao)
        
        logger.info("All validation checks passed")
        return True, "Validação bem-sucedida"
        
    except (ValidationError, BalanceSheetError) as e:
        logger.error(f"Validation failed: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected validation error: {str(e)}")
        raise ValidationError(f"Erro inesperado na validação: {str(e)}")


def validate_all(balanco: BalanceSheet, demonstracao: IncomeStatement) -> Tuple[bool, str]:
    """
    Legacy function - now redirects to validate_on_request_only.
    Maintained for backward compatibility.
    """
    return validate_on_request_only(balanco, demonstracao)
