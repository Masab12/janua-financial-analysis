from fastapi import APIRouter, HTTPException
from app.models.financial_data import InputData, CalculationResult
from app.models.balance_sheet import BalanceSheet
from app.models.income_statement import IncomeStatement
from app.services.calculator import FinancialCalculator
from datetime import datetime

router = APIRouter()

@router.post("/calculate", response_model=CalculationResult)
async def calculate_metrics(data: InputData):
    """
    Endpoint principal para cálculo das métricas financeiras.
    Recebe dados do balanço e demonstração de resultados para 3 anos.
    Retorna todos os indicadores e interpretações.
    """
    try:
        # Create calculator instance
        calculator = FinancialCalculator(
            balanco=data.balanco,
            demonstracao=data.demonstracao_resultados
        )
        
        # Calculate all metrics
        metrics = calculator.calculate_all()
        
        # Build result
        result = CalculationResult(
            timestamp=datetime.now(),
            empresa=data.nome_entidade,
            metrics=metrics,
            success=True,
            message="Cálculo realizado com sucesso"
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao calcular métricas: {str(e)}"
        )

@router.get("/test")
async def test_endpoint():
    """Endpoint de teste para verificar se a API está funcional"""
    return {
        "status": "ok",
        "message": "API está funcional",
        "endpoints": [
            "/api/calculate - POST - Calcular métricas financeiras",
            "/api/test - GET - Testar API"
        ]
    }
