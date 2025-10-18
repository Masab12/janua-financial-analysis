from fastapi import APIRouter
from app.models.financial_data import InputData, CalculationResult
from app.services.calculator import FinancialCalculator
from app.validators import validate_all
from app.exceptions import CalculationError
from app.logger import get_logger
from datetime import datetime

router = APIRouter()
logger = get_logger(__name__)


@router.post("/calculate", response_model=CalculationResult)
async def calculate_metrics(data: InputData):
    """
    Main endpoint for financial analysis calculations.
    
    Accepts:
        - Company name
        - Balance sheet data (3 years)
        - Income statement data (3 years)
    
    Returns:
        - All 17 Portuguese financial ratios
        - Trend indicators
        - Portuguese interpretations
    
    The calculations match the client's Excel file exactly.
    """
    logger.info(f"Calculation request received for: {data.nome_entidade}")
    
    try:
        # Validate input data first
        validate_all(data.balanco, data.demonstracao_resultados)
        logger.debug("Input validation passed")
        
        # Create calculator and run calculations
        calculator = FinancialCalculator(
            balanco=data.balanco,
            demonstracao=data.demonstracao_resultados
        )
        
        logger.debug("Running calculations...")
        metrics = calculator.calculate_all()
        logger.debug("Calculations completed successfully")
        
        # Build response
        result = CalculationResult(
            timestamp=datetime.now(),
            empresa=data.nome_entidade,
            metrics=metrics,
            success=True,
            message="Cálculo realizado com sucesso"
        )
        
        logger.info(f"Calculation successful for: {data.nome_entidade}")
        return result
        
    except (ValueError, ZeroDivisionError) as e:
        logger.error(f"Calculation error: {str(e)}")
        raise CalculationError(
            f"Não foi possível calcular as métricas. Verifique os dados inseridos. Erro: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error during calculation: {str(e)}", exc_info=True)
        raise CalculationError(f"Erro inesperado: {str(e)}")

@router.get("/test")
async def test_endpoint():
    """
    Simple test endpoint to verify the API is responding.
    Used during development and for basic connectivity checks.
    """
    logger.debug("Test endpoint called")
    return {
        "status": "ok",
        "message": "API está funcional e pronta para receber dados",
        "available_endpoints": {
            "calculate": "POST /api/calculate - Calcular métricas financeiras",
            "health": "GET /api/health - Verificar saúde do serviço",
            "docs": "GET /docs - Documentação interativa da API"
        }
    }
