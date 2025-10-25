"""
Validation helper functions to provide better error messages
"""

from typing import Dict, List, Any
from pydantic import ValidationError as PydanticValidationError

def format_pydantic_errors(validation_error: PydanticValidationError) -> str:
    """
    Convert Pydantic validation errors into user-friendly Portuguese messages
    """
    error_messages = []
    field_translations = {
        'company_info': 'Informações da Empresa',
        'nome_empresa': 'Nome da Empresa',
        'setor_atividade': 'Setor de Atividade',
        'objetivo_empresa': 'Objetivo da Empresa',
        'email_empresario': 'Email do Empresário',
        'balanco': 'Balanço',
        'demonstracao_resultados': 'Demonstração de Resultados',
        'year_n': 'Ano N (Atual)',
        'year_n1': 'Ano N-1',
        'year_n2': 'Ano N-2',
        'ativos_fixos_tangiveis': 'Ativos Fixos Tangíveis',
        'inventarios': 'Inventários',
        'clientes': 'Clientes',
        'fornecedores': 'Fornecedores',
        'capital_realizado': 'Capital Realizado',
        'resultado_liquido_periodo': 'Resultado Líquido do Período',
        'vendas_servicos_prestados': 'Vendas e Serviços Prestados',
        'cmvmc': 'Custo das Mercadorias Vendidas e Matérias Consumidas',
        'gastos_pessoal': 'Gastos com Pessoal',
    }
    
    for error in validation_error.errors():
        field_path_raw = " -> ".join(str(x) for x in error['loc'])
        # Translate field names to Portuguese
        field_parts = [field_translations.get(part, part) for part in error['loc']]
        field_path = " -> ".join(str(x) for x in field_parts)
        
        error_type = error['type']
        error_msg = error['msg']
        
        # Translate common error types to Portuguese
        if error_type == 'type_error.float':
            user_message = f"O campo '{field_path}' deve ser um número. Verifique se usou vírgula (,) ou ponto (.) como separador decimal e não inseriu texto."
        elif error_type == 'value_error.missing':
            user_message = f"O campo obrigatório '{field_path}' não foi preenchido."
        elif error_type == 'type_error.str':
            user_message = f"O campo '{field_path}' deve ser texto."
        elif error_type == 'value_error.email':
            user_message = f"O email no campo '{field_path}' não tem um formato válido. Use o formato: exemplo@empresa.com"
        elif 'min_length' in error_type:
            min_length = error.get('ctx', {}).get('limit_value', 1)
            user_message = f"O campo '{field_path}' deve ter pelo menos {min_length} caracteres."
        elif 'max_length' in error_type:
            max_length = error.get('ctx', {}).get('limit_value', 200)
            user_message = f"O campo '{field_path}' não pode ter mais de {max_length} caracteres."
        elif 'value_error' in error_type:
            user_message = f"Valor inválido no campo '{field_path}'. Verifique o formato dos dados inseridos."
        else:
            # Fallback to original message with better context
            user_message = f"Erro no campo '{field_path}': {error_msg}"
        
        error_messages.append(user_message)
    
    # Group similar errors and provide helpful tips
    tips = []
    if any('número' in msg for msg in error_messages):
        tips.append("💡 Para números decimais, use vírgula (,) ou ponto (.) como separador decimal")
    if any('obrigatório' in msg for msg in error_messages):
        tips.append("💡 Certifique-se de que preencheu todos os campos obrigatórios")
    if any('email' in msg for msg in error_messages):
        tips.append("💡 O email deve ter o formato: nome@empresa.com")
    
    result = "❌ ERRO DE VALIDAÇÃO DOS DADOS:\n\n" + "\n".join(f"• {msg}" for msg in error_messages)
    
    if tips:
        result += "\n\n📋 DICAS PARA CORRIGIR:\n" + "\n".join(tips)
    
    return result

def validate_financial_data_format(data: Dict[str, Any]) -> List[str]:
    """
    Additional validation for common financial data issues
    """
    issues = []
    
    # Check if company info exists
    if not data.get('company_info'):
        issues.append("Informações da empresa em falta. Preencha pelo menos o nome da empresa.")
    
    # Check if balance sheet data exists
    if not data.get('balanco'):
        issues.append("Dados do balanço em falta.")
    
    # Check if income statement data exists  
    if not data.get('demonstracao_resultados'):
        issues.append("Dados da demonstração de resultados em falta.")
    
    # Check for common field issues
    if data.get('balanco'):
        for year in ['year_n', 'year_n1', 'year_n2']:
            year_data = data['balanco'].get(year, {})
            if not isinstance(year_data, dict):
                issues.append(f"Dados do balanço para {year} estão em formato incorreto.")
    
    if data.get('demonstracao_resultados'):
        for year in ['year_n', 'year_n1', 'year_n2']:
            year_data = data['demonstracao_resultados'].get(year, {})
            if not isinstance(year_data, dict):
                issues.append(f"Dados da demonstração de resultados para {year} estão em formato incorreto.")
    
    return issues

def create_detailed_error_response(error: Exception) -> str:
    """
    Create a detailed, user-friendly error message
    """
    if isinstance(error, PydanticValidationError):
        return format_pydantic_errors(error)
    
    error_str = str(error)
    
    # Common error patterns and their translations
    if "422" in error_str or "validation" in error_str.lower():
        return (
            "ERRO DE VALIDAÇÃO DOS DADOS:\n\n"
            "Os dados inseridos não estão no formato correto. Verifique:\n"
            "• Se todos os campos numéricos contêm apenas números\n"
            "• Se usou vírgula (,) ou ponto (.) como separador decimal\n"
            "• Se o nome da empresa foi preenchido\n"
            "• Se os valores do balanço estão equilibrados\n\n"
            f"Erro técnico: {error_str}"
        )
    
    return f"Erro inesperado: {error_str}"