import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { submitCadastro } from "../../api/api";
import "./cadastro.css";

function Cadastro() {
  const location = useLocation();
  const navigate = useNavigate();
  const [tempFile, setTempFile] = useState(null);
  const [fotoFrontal, setFotoFrontal] = useState(null);
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
    if (tempFile) {
      const supabaseBaseUrl =
        "https://bngwnknyxmhkeesoeizb.supabase.co/storage/v1/object/public/faces";
      const imageUrl = `${supabaseBaseUrl}/${tempFile}/image_1.jpg`;
      setFotoFrontal(imageUrl);
    }
  }, [tempFile]);

  useEffect(() => {
    if (peso && altura) {
      const calculo = (parseFloat(peso) / (parseFloat(altura) * parseFloat(altura))).toFixed(2);
      setImc(isNaN(calculo) ? "" : calculo);
    }
  }, [peso, altura]);

  const onlyNumbers = (value) => value.replace(/\D/g, "");

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
        rg,
        data_nascimento: dataNascimento,
        genero,
        estado_civil: estadoCivil,
        nacionalidade,
        naturalidade,
        telefone,
        telefone_secundario: telefoneSecundario,
        email,
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
        temp_file: tempFile,
        embedding_path: `faces/${tempFile}/embedding.json` 
      };      
  
      const response = await submitCadastro(payload);
      setSucesso("Usuário cadastrado com sucesso!");
      navigate(`/informacoes/${cpf}`);
    } catch (err) {
      console.error(err);
      setErro(err.response?.data?.detail || "Erro ao cadastrar usuário.");
    } finally {
      setCarregando(false);
    }
  };

  return (
    <div className="container">
      <h2>Cadastro de Paciente</h2>
      {erro && <p className="error">{erro}</p>}
      {sucesso && <p className="success">{sucesso}</p>}

      {fotoFrontal && (
        <div className="foto-preview">
          <h3>Foto capturada</h3>
          <img src={fotoFrontal} alt="Foto frontal" className="foto-usuario"/>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <h3>Dados Pessoais</h3>
        <label>Nome Completo *</label>
        <input value={nomeCompleto} onChange={(e) => setNomeCompleto(e.target.value)} required />

        <label>CPF *</label>
        <input value={cpf} onChange={(e) => setCpf(onlyNumbers(e.target.value))} maxLength={11} required />

        <label>RG</label>
        <input value={rg} onChange={(e) => setRg(onlyNumbers(e.target.value))} />

        <label>Data de Nascimento *</label>
        <input type="date" value={dataNascimento} onChange={(e) => setDataNascimento(e.target.value)} required />

        <label>Gênero</label>
        <select value={genero} onChange={(e) => setGenero(e.target.value)}>
          <option value="">Selecione</option>
          <option value="masculino">Masculino</option>
          <option value="feminino">Feminino</option>
          <option value="outro">Outro</option>
          <option value="nao-informar">Prefiro não informar</option>
        </select>

        <label>Estado Civil</label>
        <select value={estadoCivil} onChange={(e) => setEstadoCivil(e.target.value)}>
          <option value="">Selecione</option>
          <option value="solteiro">Solteiro(a)</option>
          <option value="casado">Casado(a)</option>
          <option value="divorciado">Divorciado(a)</option>
          <option value="viuvo">Viúvo(a)</option>
          <option value="uniao-estavel">União Estável</option>
        </select>

        <label>Nacionalidade</label>
        <input value={nacionalidade} onChange={(e) => setNacionalidade(e.target.value)} />

        <label>Naturalidade</label>
        <input value={naturalidade} onChange={(e) => setNaturalidade(e.target.value)} />

        <label>Telefone</label>
        <input value={telefone} onChange={(e) => setTelefone(onlyNumbers(e.target.value))} maxLength={11} />

        <label>Telefone Secundário</label>
        <input value={telefoneSecundario} onChange={(e) => setTelefoneSecundario(onlyNumbers(e.target.value))} maxLength={11} />

        <label>E-mail</label>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} />

        <h3>Endereço</h3>
        <label>CEP</label>
        <input value={cep} onChange={(e) => setCep(onlyNumbers(e.target.value))} maxLength={8} />

        <label>Rua</label>
        <input value={rua} onChange={(e) => setRua(e.target.value)} />

        <label>Número</label>
        <input value={numero} onChange={(e) => setNumero(onlyNumbers(e.target.value))} />

        <label>Complemento</label>
        <input value={complemento} onChange={(e) => setComplemento(e.target.value)} />

        <label>Bairro</label>
        <input value={bairro} onChange={(e) => setBairro(e.target.value)} />

        <label>Cidade</label>
        <input value={cidade} onChange={(e) => setCidade(e.target.value)} />

        <label>Estado</label>
        <select value={estado} onChange={(e) => setEstado(e.target.value)}>
          <option value="">Selecione</option>
          <option value="AC">Acre</option>
          <option value="AL">Alagoas</option>
          <option value="AP">Amapá</option>
          <option value="AM">Amazonas</option>
          <option value="BA">Bahia</option>
          <option value="CE">Ceará</option>
          <option value="DF">Distrito Federal</option>
          <option value="ES">Espírito Santo</option>
          <option value="GO">Goiás</option>
          <option value="MA">Maranhão</option>
          <option value="MT">Mato Grosso</option>
          <option value="MS">Mato Grosso do Sul</option>
          <option value="MG">Minas Gerais</option>
          <option value="PA">Pará</option>
          <option value="PB">Paraíba</option>
          <option value="PR">Paraná</option>
          <option value="PE">Pernambuco</option>
          <option value="PI">Piauí</option>
          <option value="RJ">Rio de Janeiro</option>
          <option value="RN">Rio Grande do Norte</option>
          <option value="RS">Rio Grande do Sul</option>
          <option value="RO">Rondônia</option>
          <option value="RR">Roraima</option>
          <option value="SC">Santa Catarina</option>
          <option value="SP">São Paulo</option>
          <option value="SE">Sergipe</option>
          <option value="TO">Tocantins</option>
        </select>
        <h3>Informações Médicas</h3>

        <label>Hospital Vinculado *</label>
        <input value={hospital} onChange={(e) => setHospital(e.target.value)} required />

        <label>Médico Responsável *</label>
        <input value={medicoResponsavel} onChange={(e) => setMedicoResponsavel(e.target.value)} required />

        <label>Tipo Sanguíneo</label>
        <select value={tipoSanguineo} onChange={(e) => setTipoSanguineo(e.target.value)}>
          <option value="">Selecione</option>
          <option value="A+">A+</option>
          <option value="A-">A-</option>
          <option value="B+">B+</option>
          <option value="B-">B-</option>
          <option value="AB+">AB+</option>
          <option value="AB-">AB-</option>
          <option value="O+">O+</option>
          <option value="O-">O-</option>
        </select>

        <label>Peso (kg)</label>
        <input type="number" value={peso} onChange={(e) => setPeso(e.target.value)} min="0" step="0.1" />

        <label>Altura (m)</label>
        <input type="number" step="0.01" value={altura} onChange={(e) => setAltura(e.target.value)} min="0" />

        <label>IMC</label>
        <input value={imc} readOnly />

        <label>Pressão Arterial</label>
        <input value={pressaoArterial} onChange={(e) => setPressaoArterial(e.target.value)} />

        <label>Frequência Cardíaca</label>
        <input type="number" value={frequenciaCardiaca} onChange={(e) => setFrequenciaCardiaca(e.target.value)} min="0" />

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
            <input value={numeroCarteirinha} onChange={(e) => setNumeroCarteirinha(onlyNumbers(e.target.value))} />

            <label>Validade da Carteirinha</label>
            <input type="date" value={validadeCarteirinha} onChange={(e) => setValidadeCarteirinha(e.target.value)} />
          </>
        )}
        <h3>Responsável</h3>
        <label>Nome do Responsável</label>
        <input value={responsavelNome} onChange={(e) => setResponsavelNome(e.target.value)} />
        <label>Parentesco</label>
        <select value={responsavelParentesco} onChange={(e) => setResponsavelParentesco(e.target.value)}>
          <option value="">Selecione</option>
          <option value="pai">Pai</option>
          <option value="mae">Mãe</option>
          <option value="irmao">Irmão(a)</option>
          <option value="conjuge">Cônjuge</option>
          <option value="outro">Outro</option>
        </select>
        <label>Telefone do Responsável</label>
        <input value={responsavelTelefone} onChange={(e) => setResponsavelTelefone(onlyNumbers(e.target.value))} maxLength={11} />
        <h3>Documentos</h3>
        <label>Cartão SUS</label>
        <input value={cartaoSUS} onChange={(e) => setCartaoSUS(onlyNumbers(e.target.value))} />
        <label>CNH</label>
        <input value={cnh} onChange={(e) => setCnh(onlyNumbers(e.target.value))} />
        <button type="submit" disabled={carregando}>
          {carregando ? "Cadastrando..." : "Cadastrar"}
        </button>
      </form>
    </div>
  );
}

export default Cadastro;