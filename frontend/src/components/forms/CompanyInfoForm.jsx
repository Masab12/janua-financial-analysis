import Input from '../common/Input';
import Card from '../common/Card';
import DummyDataButtonSmall from '../common/DummyDataButtonSmall';

function CompanyInfoForm({ data, onChange, onFillDummyData }) {
  const handleChange = (field) => (e) => {
    onChange(field, e.target.value);
  };

  return (
    <Card 
      title="Informações da Empresa"
      action={onFillDummyData && (
        <DummyDataButtonSmall onFillData={onFillDummyData} />
      )}
    >
      <div className="space-y-4">
        <Input
          label="Nome da Empresa *"
          name="nome_empresa"
          type="text"
          value={data.nome_empresa || ''}
          onChange={handleChange('nome_empresa')}
          required
          placeholder="Digite o nome da empresa"
        />

        <Input
          label="Setor de Atividade"
          name="setor_atividade"
          type="text"
          value={data.setor_atividade || ''}
          onChange={handleChange('setor_atividade')}
          placeholder="Ex: Tecnologia, Comércio, Serviços..."
        />

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Objetivo do Relatório
          </label>
          <textarea
            name="objetivo_relatorio"
            value={data.objetivo_relatorio || ''}
            onChange={handleChange('objetivo_relatorio')}
            placeholder="Descreva o objetivo desta análise financeira..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-janua-navy focus:border-transparent resize-none"
            rows={3}
          />
        </div>

        <Input
          label="Email do Empresário"
          name="email_empresario"
          type="email"
          value={data.email_empresario || ''}
          onChange={handleChange('email_empresario')}
          placeholder="exemplo@empresa.com"
        />

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mt-4">
          <p className="text-sm text-blue-800">
            <strong>Nota:</strong> Estas informações serão incluídas no relatório PDF gerado. 
            Apenas o nome da empresa é obrigatório.
          </p>
        </div>
      </div>
    </Card>
  );
}

export default CompanyInfoForm;