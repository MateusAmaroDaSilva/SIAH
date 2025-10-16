import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import "./informacoes.css"; // importa o CSS

function Informacoes() {
  const { cpf } = useParams();
  const [usuario, setUsuario] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await axios.get(`http://127.0.0.1:8000/tela_informacoes/${cpf}`);
        setUsuario(res.data);
      } catch (err) {
        setUsuario({ error: "Usuário não encontrado" });
      }
    };
    fetchUser();
  }, [cpf]);

  if (!usuario) return <p className="loading">Carregando...</p>;
  if (usuario.error) return <p className="error">{usuario.error}</p>;

  return (
    <div className="container">
      <h2>Informações do Usuário</h2>
      <p><strong>Nome:</strong> {usuario.nome}</p>
      <p><strong>Email:</strong> {usuario.email}</p>
      <p><strong>CPF:</strong> {usuario.cpf}</p>
    </div>
  );
}

export default Informacoes;
