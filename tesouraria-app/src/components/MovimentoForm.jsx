import React, { useState } from 'react';

export default function MovimentoForm({ onAddMovimento }) {
  const [formData, setFormData] = useState({
    tipo: 'entrada',
    descricao: '',
    valor: '',
    categoria: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!formData.descricao || !formData.valor) {
      alert('Por favor, preencha todos os campos obrigatórios');
      return;
    }

    onAddMovimento(formData);
    
    // Limpar formulário
    setFormData({
      tipo: 'entrada',
      descricao: '',
      valor: '',
      categoria: ''
    });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <form className="movimento-form" onSubmit={handleSubmit}>
      <h2>Novo Movimento</h2>
      
      <div className="form-group">
        <label>Tipo:</label>
        <select name="tipo" value={formData.tipo} onChange={handleChange}>
          <option value="entrada">Entrada</option>
          <option value="saida">Saída</option>
        </select>
      </div>

      <div className="form-group">
        <label>Descrição:</label>
        <input
          type="text"
          name="descricao"
          value={formData.descricao}
          onChange={handleChange}
          placeholder="Ex: Venda de produto"
          required
        />
      </div>

      <div className="form-group">
        <label>Valor (€):</label>
        <input
          type="number"
          name="valor"
          value={formData.valor}
          onChange={handleChange}
          placeholder="0.00"
          step="0.01"
          min="0"
          required
        />
      </div>

      <div className="form-group">
        <label>Categoria:</label>
        <input
          type="text"
          name="categoria"
          value={formData.categoria}
          onChange={handleChange}
          placeholder="Ex: Vendas, Despesas"
        />
      </div>

      <button type="submit" className="btn-submit">
        Adicionar Movimento
      </button>
    </form>
  );
}
