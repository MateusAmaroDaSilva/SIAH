import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { submitCadastro } from "../../api/api";
import "./cadastro.css";

function Cadastro() {
  const location = useLocation();
  const navigate = useNavigate();
  const [tempFile, setTempFile] = useState(null);
  const [erro, setErro] = useState(null);
  const [sucesso, setSucesso] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [nomeCompleto, setNomeCompleto] = useState("");
  const [cpf, setCpf] = useState("");
  const [rg, setRg] = useState("");
  const [dataNascimento, setDataNascimento] = useState("");
  const [genero, setGenero] = useState("");
  const [estadoCivil, setEstadoCivil] = useState("");
  const [nacionalidade, setNacionalidade] = useState("");
  const [naturalidade, setNaturalidade] = useState("");
  const [telefone, setTelefone] = useState("");
  const [telefoneSecundario, setTelefoneSecundario] = useState("");
  const [email, setEmail] = useState("");
  const [cep, setCep] = useState("");
  const [rua, setRua] = useState("");
  const [numero, setNumero] = useState("");
  const [complemento, setComplemento] = useState("");
  const [bairro, setBairro] = useState("");
  const [cidade, setCidade] = useState("");
  const [estado, setEstado] = useState("");
  const [hospital, setHospital] = useState("");
  const [medicoResponsavel, setMedicoResponsavel] = useState("");
  const [tipoSanguineo, setTipoSanguineo] = useState("");
  const [peso, setPeso] = useState("");
  const [altura, setAltura] = useState("");
  const [imc, setImc] = useState("");
  const [pressaoArterial, setPressaoArterial] = useState("");
  const [frequenciaCardiaca, setFrequenciaCardiaca] = useState("");
  const [alergias, setAlergias] = useState("");
  const [condicoesCronicas, setCondicoesCronicas] = useState("");
  const [cirurgias_anteriores, setCirurgias_Anteriores] = useState("");
  const [medicamentos, setMedicamentos] = useState("");
  const [historicoFamiliar, setHistoricoFamiliar] = useState("");
  const [observacoesMedicas, setObservacoesMedicas] = useState("");
  const [possuiPlano, setPossuiPlano] = useState(false);
  const [nomePlano, setNomePlano] = useState("");
  const [numeroCarteirinha, setNumeroCarteirinha] = useState("");
  const [validadeCarteirinha, setValidadeCarteirinha] = useState("");
  const [responsavelNome, setResponsavelNome] = useState("");
  const [responsavelParentesco, setResponsavelParentesco] = useState("");
  const [responsavelTelefone, setResponsavelTelefone] = useState("");
  const [cartaoSUS, setCartaoSUS] = useState("");
  const [cnh, setCnh] = useState("");

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const temp = params.get("temp_file");
    if (!temp) setErro("Parâmetro temp_file ausente.");
    else setTempFile(temp);
  }, [location]);

  useEffect(() => {
    if (peso && altura) {
      const calculo = (parseFloat(peso) / (parseFloat(altura) * parseFloat(altura))).toFixed(2);
      setImc(isNaN(calculo) ? "" : calculo);
    }
  }, [peso, altura]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!tempFile) {
      setErro("Arquivo temporário ausente.");
      return;
    }
  
    setCarregando(true);
    setErro(null);
    setSucesso(null);
  
    try {
      const payload = {
        nome: nomeCompleto,
        cpf,
        email,
        embedding_path: "temp/path", 
        temp_file: tempFile,         
        rg,
        data_nascimento: dataNascimento,
        genero,
        estado_civil: estadoCivil,
        nacionalidade,
        naturalidade,
        telefone,
        telefone_secundario: telefoneSecundario,
        cep,
        rua,
        numero,
        complemento,
        bairro,
        cidade,
        estado,
        hospital_vinculado: hospital,
        medico_responsavel: medicoResponsavel,
        tipo_sanguineo: tipoSanguineo,
        peso: peso || 0,
        altura: altura || 0,
        imc: imc || 0,
        pressao_arterial: pressaoArterial,
        frequencia_cardiaca: frequenciaCardiaca,
        alergias,
        condicoes_cronicas: condicoesCronicas,
        cirurgias_anteriores,
        medicamentos_em_uso: medicamentos,
        historico_familiar: historicoFamiliar,
        observacoes_medicas: observacoesMedicas,
        possui_plano_saude: possuiPlano,
        nome_plano: nomePlano,
        numero_carteirinha: numeroCarteirinha,
        validade_carteirinha: validadeCarteirinha,
        nome_responsavel: responsavelNome,
        parentesco: responsavelParentesco,
        telefone_responsavel: responsavelTelefone,
        cartao_sus: cartaoSUS,
        cnh,
      };
      const response = await submitCadastro(payload);
      setSucesso("Usuário cadastrado com sucesso!");
      console.log("Resposta do backend:", response.data);
      navigate(`/informacoes/${cpf}`);
    } catch (err) {
      console.error("Erro no cadastro:", err.response?.data || err.message);
      if (err.response?.data?.detail) {
        console.error("Detalhe do erro do backend:", err.response.data.detail);
        setErro(err.response.data.detail);
      } else {
        setErro(err.message || "Erro ao cadastrar usuário.");
      }
    } finally {
      setCarregando(false);
    }
  };
  

  return (
    <div className="container">
      <h2>Cadastro de Paciente</h2>
      {erro && <p className="error">{erro.toString()}</p>}
      {sucesso && <p className="success">{sucesso}</p>}

      <form onSubmit={handleSubmit}>
        <h3>Dados Pessoais</h3>
        <label>Nome Completo *</label>
        <input value={nomeCompleto} onChange={(e) => setNomeCompleto(e.target.value)} required />
        <label>CPF *</label>
        <input value={cpf} onChange={(e) => setCpf(e.target.value)} required />
        <label>RG</label>
        <input value={rg} onChange={(e) => setRg(e.target.value)} />
        <label>Data de Nascimento *</label>
        <input type="date" value={dataNascimento} onChange={(e) => setDataNascimento(e.target.value)} required />
        <label>Gênero</label>
        <input value={genero} onChange={(e) => setGenero(e.target.value)} />
        <label>Estado Civil</label>
        <input value={estadoCivil} onChange={(e) => setEstadoCivil(e.target.value)} />
        <label>Nacionalidade</label>
        <input value={nacionalidade} onChange={(e) => setNacionalidade(e.target.value)} />
        <label>Naturalidade</label>
        <input value={naturalidade} onChange={(e) => setNaturalidade(e.target.value)} />
        <label>Telefone</label>
        <input value={telefone} onChange={(e) => setTelefone(e.target.value)} />
        <label>Telefone Secundário</label>
        <input value={telefoneSecundario} onChange={(e) => setTelefoneSecundario(e.target.value)} />
        <label>E-mail</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <h3>Endereço</h3>
        <label>CEP</label>
        <input value={cep} onChange={(e) => setCep(e.target.value)} />
        <label>Rua</label>
        <input value={rua} onChange={(e) => setRua(e.target.value)} />
        <label>Número</label>
        <input value={numero} onChange={(e) => setNumero(e.target.value)} />
        <label>Complemento</label>
        <input value={complemento} onChange={(e) => setComplemento(e.target.value)} />
        <label>Bairro</label>
        <input value={bairro} onChange={(e) => setBairro(e.target.value)} />
        <label>Cidade</label>
        <input value={cidade} onChange={(e) => setCidade(e.target.value)} />
        <label>Estado</label>
        <input value={estado} onChange={(e) => setEstado(e.target.value)} />
        <h3>Informações Médicas</h3>
        <label>Hospital Vinculado *</label>
        <input value={hospital} onChange={(e) => setHospital(e.target.value)} required />
        <label>Médico Responsável *</label>
        <input value={medicoResponsavel} onChange={(e) => setMedicoResponsavel(e.target.value)} required />
        <label>Tipo Sanguíneo</label>
        <input value={tipoSanguineo} onChange={(e) => setTipoSanguineo(e.target.value)} />
        <label>Peso (kg)</label>
        <input type="number" value={peso} onChange={(e) => setPeso(e.target.value)} />
        <label>Altura (m)</label>
        <input type="number" step="0.01" value={altura} onChange={(e) => setAltura(e.target.value)} />
        <label>IMC</label>
        <input value={imc} readOnly />
        <label>Pressão Arterial</label>
        <input value={pressaoArterial} onChange={(e) => setPressaoArterial(e.target.value)} />
        <label>Frequência Cardíaca</label>
        <input value={frequenciaCardiaca} onChange={(e) => setFrequenciaCardiaca(e.target.value)} />
        <label>Alergias</label>
        <textarea value={alergias} onChange={(e) => setAlergias(e.target.value)} />
        <label>Condições Crônicas</label>
        <textarea value={condicoesCronicas} onChange={(e) => setCondicoesCronicas(e.target.value)} />
        <label>Cirurgias Anteriores</label>
        <textarea value={cirurgias_anteriores} onChange={(e) => setCirurgias_Anteriores(e.target.value)} />
        <label>Medicamentos em Uso</label>
        <textarea value={medicamentos} onChange={(e) => setMedicamentos(e.target.value)} />
        <label>Histórico Familiar</label>
        <textarea value={historicoFamiliar} onChange={(e) => setHistoricoFamiliar(e.target.value)} />
        <label>Observações Médicas</label>
        <textarea value={observacoesMedicas} onChange={(e) => setObservacoesMedicas(e.target.value)} />
        <h3>Plano de Saúde</h3>
        <label>
          <input type="checkbox" checked={possuiPlano} onChange={(e) => setPossuiPlano(e.target.checked)} />
          Possui plano de saúde
        </label>
        {possuiPlano && (
          <>
            <label>Nome do Plano</label>
            <input value={nomePlano} onChange={(e) => setNomePlano(e.target.value)} />
            <label>Número da Carteirinha</label>
            <input value={numeroCarteirinha} onChange={(e) => setNumeroCarteirinha(e.target.value)} />
            <label>Validade da Carteirinha</label>
            <input type="date" value={validadeCarteirinha} onChange={(e) => setValidadeCarteirinha(e.target.value)} />
          </>
        )}
        <h3>Responsável</h3>
        <label>Nome do Responsável</label>
        <input value={responsavelNome} onChange={(e) => setResponsavelNome(e.target.value)} />
        <label>Parentesco</label>
        <input value={responsavelParentesco} onChange={(e) => setResponsavelParentesco(e.target.value)} />
        <label>Telefone do Responsável</label>
        <input value={responsavelTelefone} onChange={(e) => setResponsavelTelefone(e.target.value)} />
        <h3>Documentos</h3>
        <label>Cartão SUS</label>
        <input value={cartaoSUS} onChange={(e) => setCartaoSUS(e.target.value)} />
        <label>CNH</label>
        <input value={cnh} onChange={(e) => setCnh(e.target.value)} />

        <button type="submit" disabled={carregando}>
          {carregando ? "Cadastrando..." : "Cadastrar"}
        </button>
      </form>
    </div>
  );
}

export default Cadastro;
