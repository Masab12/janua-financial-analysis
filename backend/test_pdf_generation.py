"""
Test PDF generation with dummy data to verify:
1. Total do Ativo and Total do Passivo show correct values (not 0,00 €)
2. PDF format matches the Relatório format
3. Logo is properly included
"""

from app.models.balance_sheet import BalanceSheet, BalanceSheetYear
from app.models.income_statement import IncomeStatement, IncomeStatementYear
from app.services.calculator import FinancialCalculator
from app.services.pdf_generator import FinancialPDFGenerator

def create_test_data():
    """Create simple test data"""
    
    # Balance Sheet - Year N
    bs_year_n = BalanceSheetYear(
        # Ativo Não Corrente
        ativos_fixos_tangiveis=150000,
        ativos_intangiveis=5000,
        investimentos_financeiros=3000,
        outros_ativos_nao_correntes=2000,
        
        # Ativo Corrente
        inventarios=25000,
        clientes=20000,
        estado_outros_entes_publicos_ativo=2000,
        outras_contas_receber=3000,
        caixa_depositos_bancarios=30000,
        
        # Capital Próprio
        capital_realizado=50000,
        reservas_legais=5000,
        outras_reservas=10000,
        resultados_transitados=20000,
        resultado_liquido_periodo=14000,
        
        # Passivo Não Corrente
        provisoes_nc=2000,
        financiamentos_obtidos_nc=70000,
        
        # Passivo Corrente
        fornecedores=40000,
        estado_outros_entes_publicos_passivo=10000,
        financiamentos_obtidos_corrente=15000,
        outras_contas_pagar_corrente=4000,
    )
    
    # Balance Sheet - Year N-1 (simplified)
    bs_year_n1 = BalanceSheetYear(
        ativos_fixos_tangiveis=155000,
        ativos_intangiveis=4000,
        investimentos_financeiros=3000,
        outros_ativos_nao_correntes=2000,
        inventarios=23000,
        clientes=22000,
        estado_outros_entes_publicos_ativo=2500,
        outras_contas_receber=3000,
        caixa_depositos_bancarios=32000,
        capital_realizado=50000,
        reservas_legais=5000,
        outras_reservas=10000,
        resultados_transitados=22000,
        resultado_liquido_periodo=12400,
        provisoes_nc=2000,
        financiamentos_obtidos_nc=68000,
        fornecedores=43000,
        estado_outros_entes_publicos_passivo=10000,
        financiamentos_obtidos_corrente=18000,
        outras_contas_pagar_corrente=6100,
    )
    
    # Balance Sheet - Year N-2 (simplified)
    bs_year_n2 = BalanceSheetYear(
        ativos_fixos_tangiveis=170000,
        ativos_intangiveis=4000,
        investimentos_financeiros=3000,
        outros_ativos_nao_correntes=2000,
        inventarios=20000,
        clientes=26000,
        estado_outros_entes_publicos_ativo=3000,
        outras_contas_receber=4000,
        caixa_depositos_bancarios=38000,
        capital_realizado=50000,
        reservas_legais=5000,
        outras_reservas=12000,
        resultados_transitados=25000,
        resultado_liquido_periodo=10000,
        provisoes_nc=3000,
        financiamentos_obtidos_nc=77000,
        fornecedores=45000,
        estado_outros_entes_publicos_passivo=10000,
        financiamentos_obtidos_corrente=20000,
        outras_contas_pagar_corrente=13000,
    )
    
    balance_sheet = BalanceSheet(
        year_n=bs_year_n,
        year_n1=bs_year_n1,
        year_n2=bs_year_n2
    )
    
    # Income Statement - Year N
    dr_year_n = IncomeStatementYear(
        vendas_servicos_prestados=410000,
        subsidios_exploracao=2000,
        variacao_inventarios_producao=1000,
        outros_rendimentos_ganhos=3000,
        cmvmc=250000,
        fornecimentos_servicos_externos=60000,
        gastos_pessoal=70000,
        imparidade_dividas_receber=500,
        outros_gastos_perdas=3000,
        gastos_depreciacoes_amortizacoes=10000,
        juros_rendimentos_obtidos=500,
        juros_gastos_suportados=4000,
        imposto_rendimento=5000,
    )
    
    # Income Statement - Year N-1
    dr_year_n1 = IncomeStatementYear(
        vendas_servicos_prestados=395000,
        subsidios_exploracao=1500,
        variacao_inventarios_producao=800,
        outros_rendimentos_ganhos=2000,
        cmvmc=245000,
        fornecimentos_servicos_externos=55000,
        gastos_pessoal=68000,
        imparidade_dividas_receber=400,
        outros_gastos_perdas=2000,
        gastos_depreciacoes_amortizacoes=9000,
        juros_rendimentos_obtidos=300,
        juros_gastos_suportados=3800,
        imposto_rendimento=4000,
    )
    
    # Income Statement - Year N-2
    dr_year_n2 = IncomeStatementYear(
        vendas_servicos_prestados=380000,
        subsidios_exploracao=1200,
        variacao_inventarios_producao=600,
        outros_rendimentos_ganhos=2000,
        cmvmc=240000,
        fornecimentos_servicos_externos=52000,
        gastos_pessoal=65000,
        imparidade_dividas_receber=300,
        outros_gastos_perdas=2000,
        gastos_depreciacoes_amortizacoes=8000,
        juros_rendimentos_obtidos=200,
        juros_gastos_suportados=3500,
        imposto_rendimento=3200,
    )
    
    income_statement = IncomeStatement(
        year_n=dr_year_n,
        year_n1=dr_year_n1,
        year_n2=dr_year_n2
    )
    
    return balance_sheet, income_statement


def main():
    print("=" * 80)
    print("TESTING PDF GENERATION")
    print("=" * 80)
    print()
    
    # Create test data
    balance_sheet, income_statement = create_test_data()
    
    # Verify balance sheet totals are calculated correctly
    print("✓ Balance Sheet Year N:")
    print(f"  Total Ativo: €{balance_sheet.year_n.total_ativo:,.2f}")
    print(f"  Total Passivo: €{balance_sheet.year_n.total_passivo:,.2f}")
    print(f"  Total Capital Próprio: €{balance_sheet.year_n.total_capital_proprio:,.2f}")
    print()
    
    # Calculate all metrics
    print("✓ Calculating metrics...")
    calculator = FinancialCalculator(balance_sheet, income_statement)
    results = calculator.calculate_all()
    print("  Metrics calculated successfully!")
    print()
    
    # Convert metrics to dict format
    metrics_dict = {}
    for field_name, field_value in results.__dict__.items():
        if hasattr(field_value, '__dict__'):
            metrics_dict[field_name] = field_value.__dict__
        else:
            metrics_dict[field_name] = field_value
    
    # Prepare balance sheet data with computed properties
    balance_sheet_data = {
        **balance_sheet.year_n.__dict__,
        'total_ativo': balance_sheet.year_n.total_ativo,
        'total_passivo': balance_sheet.year_n.total_passivo,
        'total_capital_proprio': balance_sheet.year_n.total_capital_proprio,
        'total_ativo_corrente': balance_sheet.year_n.total_ativo_corrente,
        'total_passivo_corrente': balance_sheet.year_n.total_passivo_corrente,
    }
    
    income_statement_data = {
        **income_statement.year_n.__dict__
    }
    
    print("✓ Generating PDF...")
    pdf_generator = FinancialPDFGenerator()
    pdf_buffer = pdf_generator.generate_report(
        empresa_nome="Empresa Teste JANUA",
        metrics=metrics_dict,
        balance_sheet=balance_sheet_data,
        income_statement=income_statement_data
    )
    
    # Save PDF to file
    output_file = "test_relatorio_janua.pdf"
    with open(output_file, 'wb') as f:
        f.write(pdf_buffer.read())
    
    print(f"  PDF saved to: {output_file}")
    print()
    
    print("=" * 80)
    print("✅ SUCCESS! PDF generated successfully")
    print("=" * 80)
    print()
    print("📋 VERIFICATION CHECKLIST:")
    print("  ✓ Total do Ativo should show: 240 000,00 €")
    print("  ✓ Total do Passivo should show: 141 000,00 €")
    print("  ✓ Faturação should show: 410 000,00 €")
    print("  ✓ Logo should be displayed (or placeholder)")
    print("  ✓ Format should match Relatório PDF")
    print()
    print(f"👉 Open {output_file} to verify!")
    print()


if __name__ == "__main__":
    main()
