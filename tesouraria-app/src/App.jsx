import { useState, useEffect } from 'react';
import { Calendar, TrendingUp, DollarSign, FileText, Plus, Download, Upload, Trash2 } from 'lucide-react';
import { format, parseISO } from 'date-fns';
import { pt } from 'date-fns/locale';
import { loadData, addMovimento, deleteMovimento, exportToJSON, importFromJSON } from './data/storage';

function App() {
  const [data, setData] = useState(loadData());
  const [showModal, setShowModal] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [ivaFilterProject, setIvaFilterProject] = useState('total');
  const [saldoFilterProject, setSaldoFilterProject] = useState('total');
  const [entradasFilterProject, setEntradasFilterProject] = useState('total');
  const [movimentosFilterProject, setMovimentosFilterProject] = useState('total');
  const [form, setForm] = useState({
    data: format(new Date(), 'yyyy-MM-dd'),
    descricao: '',
    valor: '',
    contaId: '',
    projetoId: '',
    pessoaId: '',
    categoriaId: '',
    iva: 0,
    irc: 0,
    pago: true
  });

  const refreshData = () => setData(loadData());

  const handleSubmit = (e) => {
    e.preventDefault();

    const movimento = {
      ...form,
      valor: parseFloat(form.valor),
      iva: parseFloat(form.iva || 0),
      irc: parseFloat(form.irc || 0),
      contaId: parseInt(form.contaId) || null,
      projetoId: parseInt(form.projetoId) || null,
      pessoaId: parseInt(form.pessoaId) || null,
      categoriaId: parseInt(form.categoriaId) || null
    };

    addMovimento(movimento);
    refreshData();
    setShowModal(false);
    setForm({
      data: format(new Date(), 'yyyy-MM-dd'),
      descricao: '',
      valor: '',
      contaId: '',
      projetoId: '',
      pessoaId: '',
      categoriaId: '',
      iva: 0,
      irc: 0,
      pago: true
    });
  };

  const handleDelete = (id) => {
    if (confirm('Eliminar este movimento?')) {
      deleteMovimento(id);
      refreshData();
    }
  };

  const handleImport = (e) => {
    const file = e.target.files[0];
    if (file) {
      importFromJSON(file).then(() => {
        refreshData();
        alert('Dados importados com sucesso!');
      }).catch(() => {
        alert('Erro ao importar ficheiro');
      });
    }
  };

  // Calcular totais
  const entradas = entradasFilterProject === 'total'
    ? data.movimentos.filter(m => m.valor > 0).reduce((sum, m) => sum + m.valor, 0)
    : data.movimentos.filter(m => m.valor > 0 && m.projetoId === parseInt(entradasFilterProject)).reduce((sum, m) => sum + m.valor, 0);

  const saidas = data.movimentos
    .filter(m => m.valor < 0)
    .reduce((sum, m) => sum + Math.abs(m.valor), 0);

  const saldoTotal = saldoFilterProject === 'total'
    ? data.contas.reduce((sum, c) => sum + parseFloat(c.saldo), 0)
    : data.movimentos
        .filter(m => m.projetoId === parseInt(saldoFilterProject))
        .reduce((sum, m) => sum + parseFloat(m.valor || 0), 0);

  const totalMovimentos = movimentosFilterProject === 'total'
    ? data.movimentos.length
    : data.movimentos.filter(m => m.projetoId === parseInt(movimentosFilterProject)).length;

  // Calcular IVA por projeto ou total
  const ivaPagar = ivaFilterProject === 'total'
    ? data.movimentos.reduce((sum, m) => sum + (m.iva || 0), 0)
    : data.movimentos
        .filter(m => m.projetoId === parseInt(ivaFilterProject))
        .reduce((sum, m) => sum + (m.iva || 0), 0);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">

        {/* HEADER */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              💰 Tesouraria Pessoal
            </h1>
            <p className="text-gray-600 mt-1">
              {format(new Date(), "EEEE, d 'de' MMMM 'de' yyyy", { locale: pt })}
            </p>
          </div>

          <div className="flex gap-3">
            <button
              onClick={exportToJSON}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-3 rounded-xl font-semibold flex items-center gap-2 shadow-lg transition-all"
            >
              <Download size={20} /> Exportar
            </button>

            <label className="bg-orange-600 hover:bg-orange-700 text-white px-4 py-3 rounded-xl font-semibold flex items-center gap-2 shadow-lg transition-all cursor-pointer">
              <Upload size={20} /> Importar
              <input type="file" accept=".json" onChange={handleImport} className="hidden" />
            </label>

            <button
              onClick={() => setShowModal(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-semibold flex items-center gap-2 shadow-lg transition-all"
            >
              <Plus size={20} /> Novo Movimento
            </button>
          </div>
        </div>

        {/* DASHBOARD CARDS */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-8 shadow-xl">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-3">
                <DollarSign className="text-green-500 w-8 h-8" />
                <h3 className="font-semibold text-gray-700">Saldo Total</h3>
              </div>
              <select
                value={saldoFilterProject}
                onChange={(e) => setSaldoFilterProject(e.target.value)}
                className="text-xs px-2 py-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              >
                <option value="total">Total</option>
                {data.projetos.map(p => (
                  <option key={p.id} value={p.id}>{p.nome}</option>
                ))}
              </select>
            </div>
            <p className="text-3xl font-bold text-green-600">€{saldoTotal.toFixed(2)}</p>
            {saldoFilterProject !== 'total' && (
              <p className="text-xs text-gray-500 mt-2">
                {data.projetos.find(p => p.id === parseInt(saldoFilterProject))?.nome}
              </p>
            )}
          </div>

          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-8 shadow-xl">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-3">
                <TrendingUp className="text-blue-500 w-8 h-8" />
                <h3 className="font-semibold text-gray-700">Entradas</h3>
              </div>
              <select
                value={entradasFilterProject}
                onChange={(e) => setEntradasFilterProject(e.target.value)}
                className="text-xs px-2 py-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="total">Total</option>
                {data.projetos.map(p => (
                  <option key={p.id} value={p.id}>{p.nome}</option>
                ))}
              </select>
            </div>
            <p className="text-3xl font-bold text-blue-600">+€{entradas.toFixed(2)}</p>
            {entradasFilterProject !== 'total' && (
              <p className="text-xs text-gray-500 mt-2">
                {data.projetos.find(p => p.id === parseInt(entradasFilterProject))?.nome}
              </p>
            )}
          </div>

          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-8 shadow-xl">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-3">
                <FileText className="text-orange-500 w-8 h-8" />
                <h3 className="font-semibold text-gray-700">IVA a Pagar</h3>
              </div>
              <select
                value={ivaFilterProject}
                onChange={(e) => setIvaFilterProject(e.target.value)}
                className="text-xs px-2 py-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              >
                <option value="total">Total</option>
                {data.projetos.map(p => (
                  <option key={p.id} value={p.id}>{p.nome}</option>
                ))}
              </select>
            </div>
            <p className="text-3xl font-bold text-orange-600">€{ivaPagar.toFixed(2)}</p>
            {ivaFilterProject !== 'total' && (
              <p className="text-xs text-gray-500 mt-2">
                {data.projetos.find(p => p.id === parseInt(ivaFilterProject))?.nome}
              </p>
            )}
          </div>

          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-8 shadow-xl">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-3">
                <Calendar className="text-red-500 w-8 h-8" />
                <h3 className="font-semibold text-gray-700">Movimentos</h3>
              </div>
              <select
                value={movimentosFilterProject}
                onChange={(e) => setMovimentosFilterProject(e.target.value)}
                className="text-xs px-2 py-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              >
                <option value="total">Total</option>
                {data.projetos.map(p => (
                  <option key={p.id} value={p.id}>{p.nome}</option>
                ))}
              </select>
            </div>
            <p className="text-3xl font-bold text-red-600">{totalMovimentos}</p>
            {movimentosFilterProject !== 'total' && (
              <p className="text-xs text-gray-500 mt-2">
                {data.projetos.find(p => p.id === parseInt(movimentosFilterProject))?.nome}
              </p>
            )}
          </div>
        </div>

        {/* SALDOS CONTAS */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-8 shadow-xl">
            <h3 className="text-xl font-bold mb-6 text-gray-800">💳 Saldos por Conta</h3>
            <div className="space-y-3">
              {data.contas.map(conta => (
                <div key={conta.id} className="flex justify-between items-center p-4 bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl">
                  <span className="font-semibold text-gray-800">{conta.nome}</span>
                  <span className={`font-bold ${conta.saldo >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    €{Math.abs(conta.saldo).toFixed(2)}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* ÚLTIMOS MOVIMENTOS */}
          <div className="bg-white/80 backdrop-blur-xl rounded-2xl p-8 shadow-xl">
            <h3 className="text-xl font-bold mb-6 text-gray-800">📊 Últimos Movimentos</h3>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {data.movimentos.slice(0, 10).map(mov => {
                const projeto = data.projetos.find(p => p.id === mov.projetoId);
                const pessoa = data.pessoas.find(p => p.id === mov.pessoaId);
                const conta = data.contas.find(c => c.id === mov.contaId);

                return (
                  <div key={mov.id} className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl hover:shadow-md transition-all group">
                    <div className="flex-1">
                      <p className="font-semibold text-gray-800">{mov.descricao}</p>
                      <p className="text-sm text-gray-500">
                        {projeto?.nome} • {pessoa?.nome || '-'} • {conta?.nome}
                      </p>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="text-right">
                        <p className={`font-bold text-lg ${mov.valor >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                          €{Math.abs(mov.valor).toFixed(2)}
                        </p>
                        <p className="text-xs text-gray-500">
                          {format(parseISO(mov.data), 'dd/MM/yyyy')}
                        </p>
                      </div>
                      <button
                        onClick={() => handleDelete(mov.id)}
                        className="opacity-0 group-hover:opacity-100 transition-opacity text-red-500 hover:text-red-700"
                      >
                        <Trash2 size={18} />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* MODAL NOVO MOVIMENTO */}
        {showModal && (
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-2xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
              <h2 className="text-2xl font-bold mb-6 text-gray-800">➕ Novo Movimento</h2>

              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Data</label>
                    <input
                      type="date"
                      value={form.data}
                      onChange={(e) => setForm({ ...form, data: e.target.value })}
                      required
                      className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Valor €</label>
                    <input
                      type="number"
                      step="0.01"
                      value={form.valor}
                      onChange={(e) => setForm({ ...form, valor: e.target.value })}
                      placeholder="1500.00"
                      required
                      className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Descrição</label>
                  <input
                    type="text"
                    value={form.descricao}
                    onChange={(e) => setForm({ ...form, descricao: e.target.value })}
                    placeholder="Ex: Renda Taipas+Trofa"
                    required
                    className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Conta</label>
                    <select
                      value={form.contaId}
                      onChange={(e) => setForm({ ...form, contaId: e.target.value })}
                      className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="">Selecionar...</option>
                      {data.contas.map(c => (
                        <option key={c.id} value={c.id}>{c.nome}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Projeto</label>
                    <select
                      value={form.projetoId}
                      onChange={(e) => setForm({ ...form, projetoId: e.target.value })}
                      className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="">Selecionar...</option>
                      {data.projetos.map(p => (
                        <option key={p.id} value={p.id}>{p.nome}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">Pessoa</label>
                    <select
                      value={form.pessoaId}
                      onChange={(e) => setForm({ ...form, pessoaId: e.target.value })}
                      className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="">Nenhuma</option>
                      {data.pessoas.map(p => (
                        <option key={p.id} value={p.id}>{p.nome}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Categoria</label>
                    <select
                      value={form.categoriaId}
                      onChange={(e) => setForm({ ...form, categoriaId: e.target.value })}
                      className="w-full p-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="">Selecionar...</option>
                      {data.categorias.map(c => (
                        <option key={c.id} value={c.id}>{c.nome} ({c.tipo})</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">IVA €</label>
                    <input
                      type="number"
                      step="0.01"
                      value={form.iva}
                      onChange={(e) => setForm({ ...form, iva: e.target.value })}
                      placeholder="0.00"
                      className="w-full p-3 border border-gray-200 rounded-xl"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">IRC €</label>
                    <input
                      type="number"
                      step="0.01"
                      value={form.irc}
                      onChange={(e) => setForm({ ...form, irc: e.target.value })}
                      placeholder="0.00"
                      className="w-full p-3 border border-gray-200 rounded-xl"
                    />
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={form.pago}
                    onChange={(e) => setForm({ ...form, pago: e.target.checked })}
                    className="w-5 h-5"
                  />
                  <label className="text-sm font-medium">Movimento pago</label>
                </div>

                <div className="flex gap-4 pt-4">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 py-3 rounded-xl font-semibold transition-all"
                  >
                    Cancelar
                  </button>
                  <button
                    type="submit"
                    className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl font-semibold shadow-lg transition-all"
                  >
                    Adicionar
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
