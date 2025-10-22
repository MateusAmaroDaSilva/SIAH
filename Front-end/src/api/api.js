import axios from "axios";

const API_BASE = "http://localhost:8000";

export const submitCadastro = async (data) => {
  const formData = new FormData();
  const camposObrigatorios = [
    "nome",
    "cpf",
    "email",
    "embedding_path",
    "hospital_vinculado",
    "medico_responsavel",
    "rg",
    "data_nascimento",
    "genero",
    "estado_civil",
    "nacionalidade",
    "naturalidade",
    "telefone",
    "telefone_secundario",
    "cep",
    "rua",
    "numero",
    "complemento",
    "bairro",
    "cidade",
    "estado",
    "tipo_sanguineo",
    "peso",
    "altura",
    "imc",
    "pressao_arterial",
    "frequencia_cardiaca",
    "alergias",
    "condicoes_cronicas",
    "cirurgias_anteriores",
    "medicamentos_em_uso",
    "historico_familiar",
    "observacoes_medicas",
    "possui_plano_saude",
    "nome_plano",
    "numero_carteirinha",
    "validade_carteirinha",
    "nome_responsavel",
    "parentesco",
    "telefone_responsavel",
    "cartao_sus",
    "cnh",
    "temp_file",
  ];

  for (const key of camposObrigatorios) {
    if (data[key] === undefined || data[key] === null || data[key] === "") {
      throw new Error(`Campo obrigatório "${key}" não preenchido.`);
    }
    if (["peso", "altura", "imc"].includes(key)) {
      formData.append(key, parseFloat(data[key]));
    } else if (key === "possui_plano_saude") {
      formData.append(key, data[key] ? "true" : "false");
    } else {
      formData.append(key, data[key]);
    }
  }

  try {
    const response = await axios.post(`${API_BASE}/users/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response;
  } catch (err) {
    console.error("Erro no submitCadastro:", err.response?.data || err.message);
    if (err.response?.data?.detail) {
      console.error("Detalhe do erro do backend:", err.response.data.detail);
    }
    throw err;
  }
};
