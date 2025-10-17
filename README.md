# JANUA Financial Analysis Platform

## What's This All About?

- Input your balance sheet and income statement (3 years of data)
- Get instant financial analysis with Portuguese ratios and metrics
- Download a professional PDF report
- Embed it right into their Squarespace website

**Current Status:** Backend generic setup done for now, along with calculation models and analysis done and api tested, along with mapping all formulas from "Performance" sheet into the calculations 
**Version:** 1.0.0 (MVP)

## Tech Stack

**Backend:**
- Python 3.10+ 
- FastAPI 
- Pydantic 
- ReportLab (for PDF generation)

**Frontend:**
- React.js with Tailwind CSS
- React Hook Form
- Axios for API calls

**Hosting:**
- Frontend on Vercel 
- Backend on Render or Railway 

## Getting Started

A simple guide to run this excel to web app mvp locally:

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

That's it! The API runs on http://localhost:8000

You can check http://localhost:8000/docs to see all the endpoints.

### Frontend (Coming Soon)

```bash
cd frontend
npm install
npm run dev
```

## The Portuguese Ratios We Calculate

I am using **Portuguese/European accounting ratios** as client suggested. The client's Excel uses specific formulas that match Portuguese financial analysis standards as well so every calculation is according to the columns/rows in the excel.

### Production & Size Metrics
- **CI** (Consumos Intermédios) - How much the company spends on operations
- **VBP** (Valor Bruto de Produção) - Total production value  
- **VAB** (Valor Acrescentado Bruto) - Value the company actually creates
- **TC** (Taxa de Crescimento) - Growth rate
- **EBE** (Excedente Bruto de Exploração) - Operating profit
- **ELP** (Excedente Líquido de Produção) - Net operating profit

### Balance Sheet Ratios
- **RAF** (Rácio de Autonomia Financeira) - How independent the company is financially
- **RE** (Rácio de Endividamento) - Debt level
- **RS** (Rácio de Solvabilidade) - Can they pay their debts?
- **RSSR** (Rácio de Solvabilidade em Sentido Restrito) - Asset coverage of debts

### Long-Term Indicators
- **RDE** (Rácio de Estrutura) - Capital structure
- **REF** (Rácio de Estabilidade de Financiamento) - Financing stability
- **REP** (Rácio de Estrutura do Passivo) - Liability structure
- **RCAFLRE** - Coverage of fixed assets by stable resources
- **RCAFLCP** - Coverage of fixed assets by equity

All of these come with trend arrows (▲▼►) and Portuguese interpretations that explain what the numbers actually mean.

### Why Portuguese Ratios?

The client specifically uses European/Portuguese accounting standards, which are different from US GAAP or IFRS. I extracted the exact formulas from their Excel file to make sure everything matches 100%. 

## API Endpoints

Pretty straightforward:

- `POST /api/calculate` - Send in your financial data, get back all the metrics
- `POST /api/generate-pdf` - Same thing but as a PDF
- `GET /api/health` - Just checking if the server's alive

Check `/docs` when the server is running to play with the API interactively.

## Testing

I created a test file as well to test ratio/calculations:

```bash

# Quick validation test
python quick_test.py
```

The test verify that our calculations match the Excel formulas exactly.


Under Development by Masab Farooque(P_Scribbles) 
October 2025
