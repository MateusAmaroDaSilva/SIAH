import axios from "axios";

const API_BASE = "http://localhost:8000";

export const submitCadastro = async ({ nome, email, cpf, temp_file }) => {
  const formData = new FormData();
  formData.append("nome", nome);
  formData.append("email", email);
  formData.append("cpf", cpf);
  formData.append("temp_file", temp_file);
  return await axios.post(`${API_BASE}/users/`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};
