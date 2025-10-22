from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.models.financial_data import InputData, CalculationResult
from app.services.calculator import FinancialCalculator
from app.services.pdf_generator import FinancialPDFGenerator
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

@router.post("/generate-pdf")
async def generate_pdf(data: InputData):
    """
    Generate PDF report with financial analysis summary.
    
    Returns a PDF file with the 8 key indicators matching the Relatório format.
    """
    logger.info(f"PDF generation request for: {data.nome_entidade}")
    
    try:
        # Validate and calculate
        validate_all(data.balanco, data.demonstracao_resultados)
        
        calculator = FinancialCalculator(
            balanco=data.balanco,
            demonstracao=data.demonstracao_resultados
        )
        
        metrics = calculator.calculate_all()
        logger.debug("Calculations completed for PDF")
        
        # Convert metrics to dict format
        metrics_dict = {}
        for field_name, field_value in metrics.__dict__.items():
            if hasattr(field_value, '__dict__'):
                metrics_dict[field_name] = field_value.__dict__
            else:
                metrics_dict[field_name] = field_value
        
        # Generate PDF with proper data including computed properties
        balance_sheet_data = {
            **data.balanco.year_n.__dict__,
            'total_ativo': data.balanco.year_n.total_ativo,
            'total_passivo': data.balanco.year_n.total_passivo,
            'total_capital_proprio': data.balanco.year_n.total_capital_proprio,
            'total_ativo_corrente': data.balanco.year_n.total_ativo_corrente,
            'total_passivo_corrente': data.balanco.year_n.total_passivo_corrente,
        }
        
        income_statement_data = {
            **data.demonstracao_resultados.year_n.__dict__
        }
        
        pdf_generator = FinancialPDFGenerator()
        pdf_buffer = pdf_generator.generate_report(
            empresa_nome=data.nome_entidade,
            metrics=metrics_dict,
            balance_sheet=balance_sheet_data,
            income_statement=income_statement_data
        )
        
        logger.info(f"PDF generated successfully for: {data.nome_entidade}")
        
        # Return PDF as streaming response
        filename = f"relatorio_{data.nome_entidade.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except Exception as e:
        logger.error(f"PDF generation error: {str(e)}", exc_info=True)
        raise CalculationError(f"Erro ao gerar PDF: {str(e)}")


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
            "generate-pdf": "POST /api/generate-pdf - Gerar relatório PDF",
            "health": "GET /api/health - Verificar saúde do serviço",
            "docs": "GET /docs - Documentação interativa da API"
        }
    }
