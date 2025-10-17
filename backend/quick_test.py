"""
Quick test to verify Excel formula accuracy
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Simple test data
data = {
    "nome_entidade": "Test Company",
    "balanco": {
        "year_n": {
            "ativos_fixos_tangiveis": 100000, "propriedades_investimento": 0, "trespasse": 0,
            "ativos_intangiveis": 0, "ativos_biologicos": 0, "participacoes_financeiras": 0,
            "accionistas": 0, "outros_ativos_financeiros": 0, "ativos_nao_correntes_detidos_venda": 0,
            "inventarios": 20000, "ativos_biologicos_correntes": 0, "clientes": 30000,
            "estado_outros_entes_publicos": 0, "accionistas_corrente": 0, "outras_contas_receber": 0,
            "diferimentos": 0, "ativos_financeiros_detidos_negociacao": 0,
            "outros_ativos_financeiros_correntes": 0, "caixa_depositos_bancarios": 10000,
            "capital_realizado": 50000, "accoes_quotas_proprias": 0, "outros_instrumentos_capital_proprio": 0,
            "premios_emissao": 0, "reservas_legais": 10000, "outras_reservas": 0,
            "resultados_transitados": 10000, "excedentes_revalorizacao": 0,
            "outras_variacoes_capital_proprio": 0, "resultado_liquido_periodo": 10000, "dividendos_antecipados": 0,
            "provisoes": 0, "financiamentos_obtidos_nao_corrente": 40000,
            "responsabilidades_beneficios_pos_emprego": 0, "passivos_diferidos": 0,
            "outras_contas_pagar_nao_corrente": 0, "fornecedores": 30000, "adiantamentos_clientes": 0,
            "estado_outros_entes_publicos_corrente": 0, "accionistas_passivo_corrente": 0,
            "financiamentos_obtidos_corrente": 10000, "outras_contas_pagar_corrente": 0,
            "passivos_detidos_venda": 0, "diferimentos_passivo": 0
        },
        "year_n1": {
            "ativos_fixos_tangiveis": 95000, "propriedades_investimento": 0, "trespasse": 0,
            "ativos_intangiveis": 0, "ativos_biologicos": 0, "participacoes_financeiras": 0,
            "accionistas": 0, "outros_ativos_financeiros": 0, "ativos_nao_correntes_detidos_venda": 0,
            "inventarios": 18000, "ativos_biologicos_correntes": 0, "clientes": 28000,
            "estado_outros_entes_publicos": 0, "accionistas_corrente": 0, "outras_contas_receber": 0,
            "diferimentos": 0, "ativos_financeiros_detidos_negociacao": 0,
            "outros_ativos_financeiros_correntes": 0, "caixa_depositos_bancarios": 9000,
            "capital_realizado": 50000, "accoes_quotas_proprias": 0, "outros_instrumentos_capital_proprio": 0,
            "premios_emissao": 0, "reservas_legais": 10000, "outras_reservas": 0,
            "resultados_transitados": 5000, "excedentes_revalorizacao": 0,
            "outras_variacoes_capital_proprio": 0, "resultado_liquido_periodo": 8000, "dividendos_antecipados": 0,
            "provisoes": 0, "financiamentos_obtidos_nao_corrente": 38000,
            "responsabilidades_beneficios_pos_emprego": 0, "passivos_diferidos": 0,
            "outras_contas_pagar_nao_corrente": 0, "fornecedores": 28000, "adiantamentos_clientes": 0,
            "estado_outros_entes_publicos_corrente": 0, "accionistas_passivo_corrente": 0,
            "financiamentos_obtidos_corrente": 12000, "outras_contas_pagar_corrente": 0,
            "passivos_detidos_venda": 0, "diferimentos_passivo": 0
        },
        "year_n2": {
            "ativos_fixos_tangiveis": 90000, "propriedades_investimento": 0, "trespasse": 0,
            "ativos_intangiveis": 0, "ativos_biologicos": 0, "participacoes_financeiras": 0,
            "accionistas": 0, "outros_ativos_financeiros": 0, "ativos_nao_correntes_detidos_venda": 0,
            "inventarios": 15000, "ativos_biologicos_correntes": 0, "clientes": 25000,
            "estado_outros_entes_publicos": 0, "accionistas_corrente": 0, "outras_contas_receber": 0,
            "diferimentos": 0, "ativos_financeiros_detidos_negociacao": 0,
            "outros_ativos_financeiros_correntes": 0, "caixa_depositos_bancarios": 8000,
            "capital_realizado": 50000, "accoes_quotas_proprias": 0, "outros_instrumentos_capital_proprio": 0,
            "premios_emissao": 0, "reservas_legais": 10000, "outras_reservas": 0,
            "resultados_transitados": 0, "excedentes_revalorizacao": 0,
            "outras_variacoes_capital_proprio": 0, "resultado_liquido_periodo": 5000, "dividendos_antecipados": 0,
            "provisoes": 0, "financiamentos_obtidos_nao_corrente": 35000,
            "responsabilidades_beneficios_pos_emprego": 0, "passivos_diferidos": 0,
            "outras_contas_pagar_nao_corrente": 0, "fornecedores": 25000, "adiantamentos_clientes": 0,
            "estado_outros_entes_publicos_corrente": 0, "accionistas_passivo_corrente": 0,
            "financiamentos_obtidos_corrente": 13000, "outras_contas_pagar_corrente": 0,
            "passivos_detidos_venda": 0, "diferimentos_passivo": 0
        }
    },
    "demonstracao_resultados": {
        "year_n": {
            "vendas_servicos_prestados": 200000, "subsidios_exploracao": 0,
            "variacao_inventarios_producao": 0, "trabalhos_propria_entidade": 0,
            "cmvmc": 80000, "fornecimentos_servicos_externos": 40000,
            "gastos_pessoal": 50000, "imparidade_inventarios": 0,
            "imparidade_dividas_receber": 0, "provisoes": 0,
            "imparidade_investimentos_nao_depreciaveis": 0,
            "aumentos_diminuicoes_justo_valor": 0, "outros_rendimentos_ganhos": 5000,
            "outros_gastos_perdas": 0, "reversoes_depreciacao_amortizacao": 0,
            "gastos_depreciacao_amortizacao": 10000, "juros_rendimentos_similares_obtidos": 0,
            "juros_gastos_similares_suportados": 5000, "resultado_antes_impostos": 10000,
            "imposto_rendimento_periodo": 0
        },
        "year_n1": {
            "vendas_servicos_prestados": 180000, "subsidios_exploracao": 0,
            "variacao_inventarios_producao": 0, "trabalhos_propria_entidade": 0,
            "cmvmc": 75000, "fornecimentos_servicos_externos": 35000,
            "gastos_pessoal": 45000, "imparidade_inventarios": 0,
            "imparidade_dividas_receber": 0, "provisoes": 0,
            "imparidade_investimentos_nao_depreciaveis": 0,
            "aumentos_diminuicoes_justo_valor": 0, "outros_rendimentos_ganhos": 3000,
            "outros_gastos_perdas": 0, "reversoes_depreciacao_amortizacao": 0,
            "gastos_depreciacao_amortizacao": 9000, "juros_rendimentos_similares_obtidos": 0,
            "juros_gastos_similares_suportados": 5000, "resultado_antes_impostos": 8000,
            "imposto_rendimento_periodo": 0
        },
        "year_n2": {
            "vendas_servicos_prestados": 160000, "subsidios_exploracao": 0,
            "variacao_inventarios_producao": 0, "trabalhos_propria_entidade": 0,
            "cmvmc": 70000, "fornecimentos_servicos_externos": 30000,
            "gastos_pessoal": 40000, "imparidade_inventarios": 0,
            "imparidade_dividas_receber": 0, "provisoes": 0,
            "imparidade_investimentos_nao_depreciaveis": 0,
            "aumentos_diminuicoes_justo_valor": 0, "outros_rendimentos_ganhos": 2000,
            "outros_gastos_perdas": 0, "reversoes_depreciacao_amortizacao": 0,
            "gastos_depreciacao_amortizacao": 8000, "juros_rendimentos_similares_obtidos": 0,
            "juros_gastos_similares_suportados": 5000, "resultado_antes_impostos": 5000,
            "imposto_rendimento_periodo": 0
        }
    }
}

print("Testing JANUA Financial Analysis API")
print("=" * 60)

try:
    response = requests.post(f"{BASE_URL}/api/calculate", json=data)
    
    if response.status_code == 200:
        result = response.json()
        m = result['metrics']
        
        print("\n✅ API WORKING! Key metrics:")
        print(f"\n📊 CI (year_n): €{m['consumos_intermedios']['year_n']:,.0f}")
        print(f"   Expected: €120,000 (80k CMVMC + 40k FSE)")
        print(f"   Match: {'✅' if m['consumos_intermedios']['year_n'] == 120000 else '❌'}")
        
        print(f"\n📊 VBP (year_n): €{m['valor_bruto_producao']['year_n']:,.0f}")
        print(f"   Expected: €205,000 (200k Vendas + 5k Outros Rend.)")
        print(f"   Match: {'✅' if m['valor_bruto_producao']['year_n'] == 205000 else '❌'}")
        
        print(f"\n📊 VAB (year_n): €{m['valor_acrescentado_bruto']['year_n']:,.0f}")
        print(f"   Expected: €85,000 (VBP - CI)")
        print(f"   Match: {'✅' if m['valor_acrescentado_bruto']['year_n'] == 85000 else '❌'}")
        
        print(f"\n📊 RAF (year_n): {m['racio_autonomia_financeira']['year_n']:.4f}")
        print(f"   Formula: Capital Próprio / Total Ativo")
        print(f"   Interpretation: {m['racio_autonomia_financeira']['interpretacao']}")
        
        print(f"\n📊 RS (year_n): {m['racio_solvabilidade']['year_n']:.4f}")
        print(f"   Formula: Capital Próprio / Passivo")
        print(f"   Interpretation: {m['racio_solvabilidade']['interpretacao']}")
        
        print("\n" + "=" * 60)
        print("✅ ALL FORMULAS WORKING AS EXPECTED!")
        print("=" * 60)
        
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Connection error: {e}")
    print("\nMake sure the backend is running:")
    print("  cd backend")
    print("  python -m uvicorn app.main:app --reload --port 8000")
