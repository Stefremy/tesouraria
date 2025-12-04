import React from 'react';

export default function Dashboard({ movimentos }) {
  // Calcular totais
  const totalEntradas = movimentos
    .filter(m => m.tipo === 'entrada')
    .reduce((sum, m) => sum + parseFloat(m.valor || 0), 0);

  const totalSaidas = movimentos
    .filter(m => m.tipo === 'saida')
    .reduce((sum, m) => sum + parseFloat(m.valor || 0), 0);

  const saldo = totalEntradas - totalSaidas;

  return (
    <div className="dashboard">
      <div className="card">
        <h3>Entradas</h3>
        <p className="valor entrada">€ {totalEntradas.toFixed(2)}</p>
      </div>
      <div className="card">
        <h3>Saídas</h3>
        <p className="valor saida">€ {totalSaidas.toFixed(2)}</p>
      </div>
      <div className="card">
        <h3>Saldo</h3>
        <p className={`valor ${saldo >= 0 ? 'entrada' : 'saida'}`}>
          € {saldo.toFixed(2)}
        </p>
      </div>
    </div>
  );
}
