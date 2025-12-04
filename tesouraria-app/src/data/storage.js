// Gestão de dados local com localStorage
const STORAGE_KEY = 'tesouraria_data';

const getDefaultData = () => ({
  movimentos: [],
  contas: [
    { id: 1, nome: 'Santander', saldo: 0 },
    { id: 2, nome: 'NovoBanco', saldo: 0 },
    { id: 3, nome: 'Revolut', saldo: 0 },
    { id: 4, nome: 'Cartão', saldo: 0 }
  ],
  projetos: [
    { id: 1, nome: 'Imobiliária' },
    { id: 2, nome: 'Go Linke' },
    { id: 3, nome: 'Pessoal' },
    { id: 4, nome: 'Casa' }
  ],
  pessoas: [
    { id: 1, nome: 'Calixto' },
    { id: 2, nome: 'Ivone' },
    { id: 3, nome: 'Sandro' },
    { id: 4, nome: 'Vera' }
  ],
  categorias: [
    { id: 1, nome: 'Rendas', tipo: 'entrada' },
    { id: 2, nome: 'Faturação', tipo: 'entrada' },
    { id: 3, nome: 'Pessoal', tipo: 'saida' },
    { id: 4, nome: 'Telecom', tipo: 'saida' },
    { id: 5, nome: 'Eletricidade', tipo: 'saida' },
    { id: 6, nome: 'Combustível', tipo: 'saida' }
  ]
});

export const loadData = () => {
  const stored = localStorage.getItem(STORAGE_KEY);
  return stored ? JSON.parse(stored) : getDefaultData();
};

export const saveData = (data) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
};

export const addMovimento = (movimento) => {
  const data = loadData();
  const novoMov = {
    id: Date.now(),
    ...movimento,
    createdAt: new Date().toISOString()
  };
  data.movimentos.unshift(novoMov);

  // Atualiza saldo da conta
  if (movimento.contaId) {
    const conta = data.contas.find(c => c.id === movimento.contaId);
    if (conta) {
      conta.saldo = parseFloat(conta.saldo) + parseFloat(movimento.valor);
    }
  }

  saveData(data);
  return novoMov;
};

export const deleteMovimento = (id) => {
  const data = loadData();
  const mov = data.movimentos.find(m => m.id === id);

  if (mov && mov.contaId) {
    const conta = data.contas.find(c => c.id === mov.contaId);
    if (conta) {
      conta.saldo = parseFloat(conta.saldo) - parseFloat(mov.valor);
    }
  }

  data.movimentos = data.movimentos.filter(m => m.id !== id);
  saveData(data);
};

export const updateMovimento = (id, updates) => {
  const data = loadData();
  const index = data.movimentos.findIndex(m => m.id === id);
  if (index !== -1) {
    data.movimentos[index] = { ...data.movimentos[index], ...updates };
    saveData(data);
  }
};

export const exportToJSON = () => {
  const data = loadData();
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `tesouraria_${new Date().toISOString().split('T')[0]}.json`;
  a.click();
};

export const importFromJSON = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        saveData(data);
        resolve(data);
      } catch (error) {
        reject(error);
      }
    };
    reader.readAsText(file);
  });
};
