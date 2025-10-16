import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { submitCadastro } from "../../api/api";
import "./cadastro.css"; 

function Cadastro() {
  const location = useLocation();
  const navigate = useNavigate();

  const [tempFile, setTempFile] = useState(null);
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [cpf, setCpf] = useState("");
  const [erro, setErro] = useState(null);
  const [sucesso, setSucesso] = useState(null);
  const [carregando, setCarregando] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const temp = params.get("temp_file");
    if (!temp) setErro("Parâmetro temp_file ausente.");
    else setTempFile(temp);
  }, [location]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!tempFile) return setErro("Arquivo temporário ausente.");

    setCarregando(true);
    setErro(null);
    setSucesso(null);

    try {
      const response = await submitCadastro({ nome, email, cpf, temp_file: tempFile });

      if (response.status === 200 || response.status === 201) {
        setSucesso("Usuário cadastrado com sucesso!");
        navigate(`/informacoes/${cpf}`);
      } else {
        setErro("Erro desconhecido ao cadastrar usuário.");
      }
    } catch (err) {
      console.error(err);
      setErro(err.response?.data?.detail || "Erro ao cadastrar usuário ou conexão com o servidor.");
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="container">
      <h2>Cadastro de Usuário</h2>
      {erro && <p className="error">{erro.toString()}</p>}
      {sucesso && <p className="success">{sucesso}</p>}

      <form onSubmit={handleSubmit}>
        <label>Nome:</label>
        <input type="text" value={nome} onChange={(e) => setNome(e.target.value)} required />

        <label>Email:</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />

        <label>CPF:</label>
        <input type="text" value={cpf} onChange={(e) => setCpf(e.target.value)} required />

        <button type="submit" disabled={carregando}>
          {carregando ? "Cadastrando..." : "Cadastrar"}
        </button>
      </form>
    </div>
  );
}

export default Cadastro;
