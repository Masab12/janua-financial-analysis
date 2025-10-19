import { useState } from 'react';
import BalanceSheetForm from './components/forms/BalanceSheetForm';
import IncomeStatementForm from './components/forms/IncomeStatementForm';
import ResultsDisplay from './components/results/ResultsDisplay';
import Input from './components/common/Input';
import Button from './components/common/Button';
import Card from './components/common/Card';
import { createEmptyFinancialData } from './utils/dataStructures';
import { calculateFinancialMetrics } from './services/api';
import { dummyData } from './utils/dummyData'; // 🧪 TESTING ONLY - REMOVE BEFORE PRODUCTION

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [currentYear, setCurrentYear] = useState('year_n');
  // 🧪 AUTO-FILL WITH DUMMY DATA FOR TESTING - REMOVE BEFORE PRODUCTION
  const [financialData, setFinancialData] = useState(dummyData);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleEntityNameChange = (e) => {
    setFinancialData({
      ...financialData,
      nome_entidade: e.target.value,
    });
  };

  const handleBalanceSheetChange = (field, value) => {
    setFinancialData({
      ...financialData,
      balanco: {
        ...financialData.balanco,
        [currentYear]: {
          ...financialData.balanco[currentYear],
          [field]: value,
        },
      },
    });
  };

  const handleIncomeStatementChange = (field, value) => {
    setFinancialData({
      ...financialData,
      demonstracao_resultados: {
        ...financialData.demonstracao_resultados,
        [currentYear]: {
          ...financialData.demonstracao_resultados[currentYear],
          [field]: value,
        },
      },
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!financialData.nome_entidade.trim()) {
      setError('Por favor, insira o nome da entidade');
      return;
    }

    setLoading(true);
    setError(null);

    console.log('🚀 Submitting financial data...', financialData.nome_entidade);
    const result = await calculateFinancialMetrics(financialData);
    console.log('📊 API Result:', result);

    if (result.success) {
      console.log('✅ Calculation successful, setting results:', result.data);
      setResults(result.data);
      setCurrentStep(4);
      console.log('✅ Current step set to 4');
    } else {
      console.error('❌ Calculation failed:', result.error);
      setError(result.error);
    }

    setLoading(false);
  };

  const handleReset = () => {
    setFinancialData(createEmptyFinancialData());
    setResults(null);
    setCurrentStep(1);
    setCurrentYear('year_n');
    setError(null);
  };

  const steps = [
    { number: 1, title: 'Identificação' },
    { number: 2, title: 'Balanço' },
    { number: 3, title: 'Demonstração de Resultados' },
    { number: 4, title: 'Resultados' },
  ];

  const years = [
    { key: 'year_n', label: 'Ano N (Atual)' },
    { key: 'year_n1', label: 'Ano N-1' },
    { key: 'year_n2', label: 'Ano N-2' },
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-janua-navy text-white py-4 md:py-6 shadow-md">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <h1 className="text-xl md:text-2xl lg:text-3xl font-bold">JANUA Financial Analysis</h1>
              <p className="text-sm md:text-base text-gray-200 mt-1">Análise Financeira Empresarial</p>
            </div>
            <div className="flex-shrink-0 ml-4">
              <img 
                src="/logo_white.png" 
                alt="JANUA Logo" 
                className="h-12 md:h-16 lg:h-20 w-auto object-contain"
              />
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-4 md:py-8 flex-grow">
        {/* 🧪 TESTING MODE BANNER - REMOVE BEFORE PRODUCTION */}
        <div className="mb-4 bg-yellow-50 border-2 border-yellow-400 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-2xl">🧪</span>
              <div>
                <p className="font-bold text-yellow-900">Modo de Teste - Dados Pré-carregados</p>
                <p className="text-sm text-yellow-700">Os formulários estão preenchidos com dados dummy para facilitar os testes.</p>
              </div>
            </div>
            <Button
              onClick={() => {
                setFinancialData(createEmptyFinancialData());
                setCurrentStep(1);
                setResults(null);
              }}
              variant="secondary"
              className="bg-yellow-600 hover:bg-yellow-700 text-white"
            >
              Limpar Dados
            </Button>
          </div>
        </div>

        {currentStep < 4 && (
          <div className="mb-6 md:mb-8">
            <div className="flex items-center justify-between md:justify-center md:space-x-4 overflow-x-auto pb-2">
              {steps.map((step, index) => (
                <div key={step.number} className="flex items-center flex-shrink-0">
                  <div
                    className={`flex items-center justify-center w-8 h-8 md:w-10 md:h-10 rounded-full font-semibold text-sm md:text-base ${
                      currentStep >= step.number
                        ? 'bg-janua-navy text-white'
                        : 'bg-gray-300 text-gray-600'
                    }`}
                  >
                    {step.number}
                  </div>
                  <span
                    className={`ml-2 text-xs md:text-sm lg:inline ${
                      currentStep >= step.number ? 'text-janua-navy font-medium' : 'text-gray-500'
                    }`}
                  >
                    {step.title}
                  </span>
                  {index < steps.length - 1 && (
                    <div className="w-8 md:w-16 h-0.5 bg-gray-300 mx-1 md:mx-2"></div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {currentStep === 1 && (
            <Card title="Identificação da Entidade">
              <Input
                label="Nome da Entidade"
                name="nome_entidade"
                type="text"
                value={financialData.nome_entidade}
                onChange={handleEntityNameChange}
                required
              />
              <div className="mt-6">
                <Button
                  type="button"
                  onClick={() => setCurrentStep(2)}
                  fullWidth
                  disabled={!financialData.nome_entidade.trim()}
                >
                  Continuar
                </Button>
              </div>
            </Card>
          )}

          {currentStep === 2 && (
            <>
              <div className="mb-4 flex flex-wrap justify-center gap-2">
                {years.map((year) => (
                  <button
                    key={year.key}
                    type="button"
                    onClick={() => setCurrentYear(year.key)}
                    className={`px-3 md:px-4 py-2 rounded-lg font-medium text-sm md:text-base transition-all ${
                      currentYear === year.key
                        ? 'bg-janua-navy text-white'
                        : 'bg-white text-janua-navy border-2 border-janua-navy hover:bg-gray-50'
                    }`}
                  >
                    {year.label}
                  </button>
                ))}
              </div>

              <BalanceSheetForm
                data={financialData.balanco[currentYear]}
                onChange={handleBalanceSheetChange}
                year={currentYear}
              />

              <div className="mt-6 flex flex-col sm:flex-row gap-3 sm:gap-4">
                <Button type="button" onClick={() => setCurrentStep(1)} variant="secondary">
                  Voltar
                </Button>
                <Button type="button" onClick={() => setCurrentStep(3)} fullWidth>
                  Continuar
                </Button>
              </div>
            </>
          )}

          {currentStep === 3 && (
            <>
              <div className="mb-4 flex flex-wrap justify-center gap-2">
                {years.map((year) => (
                  <button
                    key={year.key}
                    type="button"
                    onClick={() => setCurrentYear(year.key)}
                    className={`px-3 md:px-4 py-2 rounded-lg font-medium text-sm md:text-base transition-all ${
                      currentYear === year.key
                        ? 'bg-janua-navy text-white'
                        : 'bg-white text-janua-navy border-2 border-janua-navy hover:bg-gray-50'
                    }`}
                  >
                    {year.label}
                  </button>
                ))}
              </div>

              <IncomeStatementForm
                data={financialData.demonstracao_resultados[currentYear]}
                onChange={handleIncomeStatementChange}
                year={currentYear}
              />

              <div className="mt-6 flex flex-col sm:flex-row gap-3 sm:gap-4">
                <Button type="button" onClick={() => setCurrentStep(2)} variant="secondary">
                  Voltar
                </Button>
                <Button type="submit" fullWidth disabled={loading}>
                  {loading ? 'A calcular...' : 'Calcular Análise'}
                </Button>
              </div>
            </>
          )}
        </form>

        {currentStep === 4 && results && (
          <>
            {console.log('🎨 Rendering ResultsDisplay with:', results)}
            <ResultsDisplay results={results} />
            <div className="mt-6">
              <Button type="button" onClick={handleReset} fullWidth>
                Nova Análise
              </Button>
            </div>
          </>
        )}
        
        {/* Debug info */}
        {currentStep === 4 && !results && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-800 font-medium">❌ Step 4 reached but no results available</p>
          </div>
        )}
      </main>

      <footer className="bg-janua-navy text-white py-6 mt-auto">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="text-center md:text-left mb-4 md:mb-0">
              <p className="text-sm md:text-base">© 2025 JANUA. Todos os direitos reservados.</p>
            </div>
            <div className="flex-shrink-0">
              <img 
                src="/logo_white.png" 
                alt="JANUA Logo" 
                className="h-8 md:h-10 w-auto object-contain opacity-80"
              />
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
