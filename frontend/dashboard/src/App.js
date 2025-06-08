import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  Legend
} from "recharts";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

function App() {
  const [rapport, setRapport] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:8000/ventes/rapport")
      .then(response => setRapport(response.data))
      .catch(error => console.error("Erreur de chargement :", error));
  }, []);

  if (!rapport) return <div style={{ padding: "2rem" }}>Chargement...</div>;

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>📊 Tableau de bord – Performances</h1>

      <section style={{ marginBottom: "2rem" }}>
        <h2>💰 Total des ventes : {rapport.total_ventes.toFixed(2)} $</h2>
      </section>

      <section style={{ marginBottom: "2rem" }}>
        <h2>📦 Produits les plus vendus</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={rapport.produits}>
            <CartesianGrid stroke="#ccc" />
            <XAxis dataKey="nom" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="quantite" fill="#8884d8" name="Quantités vendues" />
          </BarChart>
        </ResponsiveContainer>
      </section>

      <section style={{ marginBottom: "2rem" }}>
        <h2>🔴 Produits en rupture de stock</h2>
        <p>Ce sont les produits avec une quantité en stock égale à 0.</p>
        <ul>
          {rapport.ruptures.length === 0 ? (
            <li>Aucun produit en rupture ✅</li>
          ) : (
            rapport.ruptures.map((p, i) => (
              <li key={i}>🔴 {p.nom} ({p.categorie})</li>
            ))
          )}
        </ul>
      </section>

      <section style={{ marginBottom: "2rem" }}>
        <h2>🟡 Produits en surstock</h2>
        <p>Ce sont les produits dont le stock est supérieur à 50 unités (seuil configurable).</p>
        <ul>
          {rapport.surstocks.length === 0 ? (
            <li>Aucun produit en surstock</li>
          ) : (
            rapport.surstocks.map((p, i) => (
              <li key={i}>🟡 {p.nom} — {p.stock} unités</li>
            ))
          )}
        </ul>
      </section>

      <section style={{ marginBottom: "2rem" }}>
        <h2>🏪 Ventes par magasin</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={rapport.ventes_par_magasin}
              dataKey="total"
              nameKey="magasin"
              cx="50%"
              cy="50%"
              outerRadius={100}
              label
            >
              {rapport.ventes_par_magasin.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </section>

      <section>
        <h2>📈 Tendance journalière des ventes</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={rapport.tendance_journaliere}>
            <XAxis dataKey="jour" />
            <YAxis />
            <CartesianGrid strokeDasharray="3 3" />
            <Tooltip />
            <Line type="monotone" dataKey="total" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </section>
    </div>
  );
}

export default App;
