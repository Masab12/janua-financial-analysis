# API Documentation

## JANUA Financial Analysis API

Complete REST API for analyzing Portuguese company financial statements. Calculates 17 different financial ratios using Portuguese/European accounting standards.

---

## Base URL

```
http://localhost:8000  (development)
https://api.janua.pt  (production - when deployed)
```

---

## Authentication

Currently no authentication required. This is a private API for JANUA's website only.

In production, we'll add API keys or JWT tokens for security.

---

## Endpoints

### 1. Health Check

Check if the API is alive and responding.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "janua-financial-api",
  "version": "1.0.0"
}
```

---

### 2. Calculate Financial Metrics

Main endpoint that does all the financial analysis calculations.

**Endpoint:** `POST /api/calculate`

**Request Body:**

You need to send 3 years of data: N (most recent), N-1, and N-2.

```json
{
  "nome_entidade": "My Company Ltd",
  "data_analise": "2025-12-31",
  "balanco": {
    "year_n": {
      "ativos_fixos_tangiveis": 100000,
      "inventarios": 20000,
      "clientes": 30000,
      "caixa_depositos_bancarios": 10000,
      "capital_realizado": 50000,
      "reservas_legais": 10000,
      "resultado_liquido_periodo": 10000,
      "financiamentos_obtidos_nao_corrente": 40000,
      "fornecedores": 30000,
      "financiamentos_obtidos_corrente": 10000
      // ... all other balance sheet fields
    },
    "year_n1": { /* same structure as year_n */ },
    "year_n2": { /* same structure as year_n */ }
  },
  "demonstracao_resultados": {
    "year_n": {
      "vendas_servicos_prestados": 200000,
      "cmvmc": 80000,
      "fornecimentos_servicos_externos": 40000,
      "gastos_pessoal": 50000,
      "gastos_depreciacao_amortizacao": 10000
      // ... all other income statement fields
    },
    "year_n1": { /* same structure */ },
    "year_n2": { /* same structure */ }
  }
}
```

**Success Response (200):**

```json
{
  "timestamp": "2024-10-18T01:30:00",
  "empresa": "My Company Ltd",
  "success": true,
  "message": "Cálculo realizado com sucesso",
  "metrics": {
    "consumos_intermedios": {
      "nome": "Consumos intermédios (CI)",
      "unidade": "€",
      "year_n": 120000,
      "year_n1": 110000,
      "year_n2": 100000,
      "tendencia": "▲",
      "interpretacao": "A empresa está a gastar menos com a sua operação..."
    },
    "racio_autonomia_financeira": {
      "nome": "Rácio de Autonomia Financeira (RAF)",
      "unidade": "ratio",
      "year_n": 0.5000,
      "year_n1": 0.4800,
      "year_n2": 0.4500,
      "tendencia": "▲",
      "interpretacao": "Excelente autonomia financeira. A empresa utiliza..."
    }
    // ... all 17 metrics
  }
}
```

**Error Responses:**

**400 Bad Request** - Invalid input data
```json
{
  "error": "Dados inválidos: Total do Ativo do ano N deve ser positivo",
  "type": "validation_error"
}
```

**422 Unprocessable Entity** - Calculation error or unbalanced balance sheet
```json
{
  "error": "Erro no cálculo: Balanço não está equilibrado",
  "type": "balance_sheet_error"
}
```

**500 Internal Server Error** - Something went wrong on our end
```json
{
  "error": "Erro interno do servidor. Por favor, tente novamente mais tarde.",
  "type": "internal_error"
}
```

---

## All Calculated Metrics

The API returns these 17 financial ratios:

### Production Metrics
1. **CI** - Consumos Intermédios (Intermediate Consumption)
2. **VBP** - Valor Bruto de Produção (Gross Production Value)
3. **VAB** - Valor Acrescentado Bruto (Gross Value Added)
4. **TC** - Taxa de Crescimento (Growth Rate)
5. **EBE** - Excedente Bruto de Exploração (Gross Operating Surplus)
6. **ELP** - Excedente Líquido de Produção (Net Operating Surplus)

### Balance Sheet Ratios
7. **RAF** - Rácio de Autonomia Financeira (Financial Autonomy Ratio)
8. **RE** - Rácio de Endividamento (Debt Ratio)
9. **RS** - Rácio de Solvabilidade (Solvency Ratio)
10. **RSSR** - Rácio de Solvabilidade em Sentido Restrito (Restricted Solvency)

### Long-Term Indicators
11. **RDE** - Rácio de Estrutura (Capital Structure Ratio)
12. **REF** - Rácio de Estabilidade de Financiamento (Financing Stability)
13. **REP** - Rácio de Estrutura do Passivo (Liability Structure)
14. **RCAFLRE** - Cobertura de Aplicações Fixas por Recursos Estáveis
15. **RCAFLCP** - Cobertura de Aplicações Fixas por Capital Próprio

Plus:
- **Resumo Balanço Funcional** - Functional balance sheet summary
- **Ativo Económico** - Economic assets

---

## Validation Rules

The API validates your data before calculating. Here's what gets checked:

### Balance Sheet Must Balance
```
Total Ativo = Total Passivo + Total Capital Próprio
```
We allow a tolerance of €0.01 for rounding.

### Positive Values Required
- Total Assets must be positive (> 0)
- Negative equity is allowed (company might be in trouble) but gets logged

### Revenue Check
- At least one year must have revenue > 0
- Zero revenue across all 3 years gets rejected

### Sanity Check
- Values can't exceed 1 trillion (prevents data entry errors like extra zeros)

---

## Trend Arrows Explained

Each metric includes a trend indicator:

- **▲** Going up by more than 5%
- **▼** Going down by more than 5%
- **►** Stable (within 5%)

For some metrics (like debt ratios), "going down" is good, so we flip the arrows.

---

## Rate Limits

Currently no rate limits during MVP phase.

In production we'll add:
- 100 requests per minute per IP
- 1000 requests per day per API key

---

## Interactive Documentation

Visit `/docs` when the server is running to see interactive API documentation powered by Swagger UI.

You can try out all endpoints right in your browser.

---

## Example: Complete Request

Here's a full working example you can copy-paste:

```python
import requests

data = {
    "nome_entidade": "JANUA Exemplo",
    "balanco": {
        "year_n": {
            "ativos_fixos_tangiveis": 100000,
            "propriedades_investimento": 0,
            "trespasse": 0,
            "ativos_intangiveis": 0,
            "ativos_biologicos": 0,
            "participacoes_financeiras": 0,
            "accionistas": 0,
            "outros_ativos_financeiros": 0,
            "ativos_nao_correntes_detidos_venda": 0,
            "inventarios": 20000,
            "ativos_biologicos_correntes": 0,
            "clientes": 30000,
            "estado_outros_entes_publicos": 0,
            "accionistas_corrente": 0,
            "outras_contas_receber": 0,
            "diferimentos": 0,
            "ativos_financeiros_detidos_negociacao": 0,
            "outros_ativos_financeiros_correntes": 0,
            "caixa_depositos_bancarios": 10000,
            "capital_realizado": 50000,
            "accoes_quotas_proprias": 0,
            "outros_instrumentos_capital_proprio": 0,
            "premios_emissao": 0,
            "reservas_legais": 10000,
            "outras_reservas": 0,
            "resultados_transitados": 10000,
            "excedentes_revalorizacao": 0,
            "outras_variacoes_capital_proprio": 0,
            "resultado_liquido_periodo": 10000,
            "dividendos_antecipados": 0,
            "provisoes": 0,
            "financiamentos_obtidos_nao_corrente": 40000,
            "responsabilidades_beneficios_pos_emprego": 0,
            "passivos_diferidos": 0,
            "outras_contas_pagar_nao_corrente": 0,
            "fornecedores": 30000,
            "adiantamentos_clientes": 0,
            "estado_outros_entes_publicos_corrente": 0,
            "accionistas_passivo_corrente": 0,
            "financiamentos_obtidos_corrente": 10000,
            "outras_contas_pagar_corrente": 0,
            "passivos_detidos_venda": 0,
            "diferimentos_passivo": 0
        },
        # Add year_n1 and year_n2 with similar data...
    },
    "demonstracao_resultados": {
        "year_n": {
            "vendas_servicos_prestados": 200000,
            "subsidios_exploracao": 0,
            "variacao_inventarios_producao": 0,
            "trabalhos_propria_entidade": 0,
            "cmvmc": 80000,
            "fornecimentos_servicos_externos": 40000,
            "gastos_pessoal": 50000,
            "imparidade_inventarios": 0,
            "imparidade_dividas_receber": 0,
            "provisoes": 0,
            "imparidade_investimentos_nao_depreciaveis": 0,
            "aumentos_diminuicoes_justo_valor": 0,
            "outros_rendimentos_ganhos": 5000,
            "outros_gastos_perdas": 0,
            "reversoes_depreciacao_amortizacao": 0,
            "gastos_depreciacao_amortizacao": 10000,
            "juros_rendimentos_similares_obtidos": 0,
            "juros_gastos_similares_suportados": 5000,
            "resultado_antes_impostos": 10000,
            "imposto_rendimento_periodo": 0
        },
        # Add year_n1 and year_n2...
    }
}

response = requests.post("http://localhost:8000/api/calculate", json=data)
print(response.json())
```

---

