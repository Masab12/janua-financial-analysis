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
    tolerance = 5000.0  # Tolerance for rounding differences (€5,000 for testing)
    
    # Check year N
    diff_n = abs(balanco.year_n.total_ativo - 
                 (balanco.year_n.total_passivo + balanco.year_n.total_capital_proprio))
    
    if diff_n > tolerance:
        logger.warning(f"Balance sheet year N doesn't balance. Difference: {diff_n}")
        raise BalanceSheetError(
            f"Balanço do ano N não está equilibrado. "
            f"Diferença: €{diff_n:.2f}. "
            f"Ativo: €{balanco.year_n.total_ativo:.2f}, "
            f"Passivo+CP: €{balanco.year_n.total_passivo + balanco.year_n.total_capital_proprio:.2f}"
        )
    
    # Check year N-1
    diff_n1 = abs(balanco.year_n1.total_ativo - 
                  (balanco.year_n1.total_passivo + balanco.year_n1.total_capital_proprio))
    
    if diff_n1 > tolerance:
        logger.warning(f"Balance sheet year N-1 doesn't balance. Difference: {diff_n1}")
        raise BalanceSheetError(
            f"Balanço do ano N-1 não está equilibrado. Diferença: €{diff_n1:.2f}"
        )
    
    # Check year N-2
    diff_n2 = abs(balanco.year_n2.total_ativo - 
                  (balanco.year_n2.total_passivo + balanco.year_n2.total_capital_proprio))
    
    if diff_n2 > tolerance:
        logger.warning(f"Balance sheet year N-2 doesn't balance. Difference: {diff_n2}")
        raise BalanceSheetError(
            f"Balanço do ano N-2 não está equilibrado. Diferença: €{diff_n2:.2f}"
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


def validate_all(balanco: BalanceSheet, demonstracao: IncomeStatement) -> Tuple[bool, str]:
    """
    Run all validation checks.
    Returns (success, message) tuple.
    """
    try:
        validate_balance_sheet(balanco)
        validate_positive_values(balanco)
        validate_income_statement(demonstracao)
        validate_reasonable_values(balanco, demonstracao)
        
        logger.info("All validation checks passed")
        return True, "Validação bem-sucedida"
        
    except (ValidationError, BalanceSheetError) as e:
        logger.error(f"Validation failed: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected validation error: {str(e)}")
        raise ValidationError(f"Erro inesperado na validação: {str(e)}")
