"""
Custom exceptions for the API.
Makes it easier to handle specific error cases with proper HTTP status codes.
"""

from fastapi import HTTPException, status


class CalculationError(HTTPException):
    """
    Raised when something goes wrong during financial calculations.
    Usually means the input data has issues.
    """
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Erro no cálculo: {detail}"
        )


class ValidationError(HTTPException):
    """
    Raised when input data doesn't pass validation.
    For example: negative values where they shouldn't be, or missing required fields.
    """
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dados inválidos: {detail}"
        )


class BalanceSheetError(HTTPException):
    """
    Raised when balance sheet doesn't balance.
    Assets must equal Liabilities + Equity, basic accounting rule.
    """
    def __init__(self, detail: str = "Balanço não está equilibrado. Ativo deve ser igual a Passivo + Capital Próprio."):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )
