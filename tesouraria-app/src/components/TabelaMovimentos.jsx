import React from 'react';

export default function TabelaMovimentos({ movimentos, onRemoveMovimento }) {
  if (movimentos.length === 0) {
    return (
      <div className="tabela-container">
        <h2>Histórico de Movimentos</h2>
        <p className="empty-message">Nenhum movimento registrado ainda.</p>
      </div>
    );
  }

  const formatDate = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleDateString('pt-PT', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="tabela-container">
      <h2>Histórico de Movimentos</h2>
      <table className="tabela-movimentos">
        <thead>
          <tr>
            <th>Data</th>
            <th>Tipo</th>
            <th>Descrição</th>
            <th>Categoria</th>
            <th>Valor</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {movimentos.map(movimento => (
            <tr key={movimento.id}>
              <td>{formatDate(movimento.data)}</td>
              <td>
                <span className={`badge ${movimento.tipo}`}>
                  {movimento.tipo === 'entrada' ? 'Entrada' : 'Saída'}
                </span>
              </td>
              <td>{movimento.descricao}</td>
              <td>{movimento.categoria || '-'}</td>
              <td className={movimento.tipo}>
                € {parseFloat(movimento.valor).toFixed(2)}
              </td>
              <td>
                <button
                  className="btn-delete"
                  onClick={() => onRemoveMovimento(movimento.id)}
                  title="Remover movimento"
                >
                  ✕
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
