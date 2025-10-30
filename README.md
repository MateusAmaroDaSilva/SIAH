<div align="center">

#  SIAH - Sistema Integrado de Atendimento Hospitalar

### API de Reconhecimento Facial para Gestão de Pacientes

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)

[Funcionalidades](#-funcionalidades) • [Instalação](#-instalação) • [Uso](#️-uso) • [API](#-endpoints-da-api) • [Contribuir](#-contribuindo)

</div>

---

## Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Configuração](#️-configuração)
- [Uso](#️-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Endpoints da API](#-endpoints-da-api)
- [Front-end](#-front-end)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)
- [Contato](#-contato)

---

## Sobre o Projeto

O **SIAH** é uma solução moderna e escalável para gerenciamento de pacientes em ambientes hospitalares, utilizando tecnologia de reconhecimento facial para identificação rápida e segura.

A API foi desenvolvida com **FastAPI** e integra-se ao **Supabase** para armazenamento de dados e arquivos, proporcionando:

- ✅ **Cadastro de pacientes** com imagens faciais e embeddings
- ✅ **Reconhecimento facial automático** via comparação de vetores de similaridade
- ✅ **Armazenamento seguro** de dados clínicos e pessoais
- ✅ **Consulta rápida** de informações por CPF
- ✅ **Interface moderna** em React para interação com o sistema

---

## Funcionalidades

### Backend (API)
- Cadastro seguro de pacientes com validação de dados
- Reconhecimento facial com threshold de similaridade configurável
- Armazenamento de embeddings faciais no Supabase
- Busca de pacientes por CPF
- Listagem completa de usuários cadastrados
- Upload e gerenciamento de imagens faciais

### Frontend
- Captura de imagens via webcam
- Formulário de cadastro intuitivo
- Interface de reconhecimento facial em tempo real
- Visualização detalhada de informações do paciente
- Design moderno e responsivo

---

## Tecnologias

### Backend
- **[Python 3.10+](https://www.python.org/)** - Linguagem de programação
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e rápido
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI
- **[Supabase](https://supabase.com/)** - Backend as a Service (BaaS)
- **[NumPy](https://numpy.org/)** - Processamento de arrays e vetores
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Validação de dados

### Frontend
- **[React](https://reactjs.org/)** - Biblioteca JavaScript para UI
- **[Vite](https://vitejs.dev/)** - Build tool e dev server
- **[Supabase Client](https://supabase.com/docs/reference/javascript/introduction)** - Cliente JavaScript

---

## Requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.10 ou superior** - [Download aqui](https://www.python.org/downloads/)
- **pip** (geralmente já vem com o Python)
- **Node.js 16+** e **npm** - [Download aqui](https://nodejs.org/)
- **Conta no Supabase** - [Criar conta gratuita](https://supabase.com/)

---

## Instalação

### 1️. Clone o repositório

```bash
git clone https://github.com/SEU-USUARIO/SIAH.git
cd SIAH
```
### 2️. Configuração do Backend

```bash
# Acesse o diretório da API
cd Back-End

# Instale as dependências
pip install -r requirements.txt
```

### 3️. Configuração do Frontend

```bash
# Acesse o diretório do frontend
cd ../Front-end

# Instale as dependências
npm install
```

---

## Configuração

### Backend - Variáveis de Ambiente

Crie um arquivo `.env` na pasta `backend/` com as seguintes variáveis:

```env
SUPABASE_URL=https://SEU-PROJETO.supabase.co
SUPABASE_KEY=SEU_SUPABASE_KEY
SIMILARITY_THRESHOLD=0.85
```

> **Nota:** Obtenha suas credenciais do Supabase em: [Dashboard do Supabase](https://app.supabase.com/) → Settings → API

### Configuração do Supabase

1. Crie uma tabela `pacientes` no Supabase com a seguinte estrutura:
   - `id` (uuid, primary key)
   - `nome` (text)
   - `email` (text)
   - `cpf` (text, unique)
   - `embedding_path` (text)
   - `images` (text[])
   - `created_at` (timestamp)

2. Configure o Storage Bucket para armazenar as imagens faciais

---

##  Uso

### Iniciando o Backend

```bash
cd backend
uvicorn main:app --reload
```

A API estará disponível em: **http://localhost:8000**

**Documentação interativa (Swagger UI):** http://localhost:8000/docs

### Iniciando o Frontend

```bash
cd Front-end
npm run dev
```

O frontend estará disponível em: **http://localhost:5174**

---

## 📁 Estrutura do Projeto

```
SIAH/
├── backend/
│   ├── main.py                  # Arquivo principal da API
│   ├── requirements.txt         # Dependências do Python
│   ├── embeddings/              # Pasta local de vetores faciais (opcional)
│   ├── .env                     # Configurações do Supabase
│   └── .gitignore
│
└── Front-end/
    ├── src/
    │   ├── components/          # Componentes React
    │   ├── pages/               # Páginas da aplicação
    │   ├── services/            # Serviços e APIs
    │   └── App.jsx              # Componente principal
    ├── package.json
    ├── vite.config.js
    └── .gitignore
```

---

## 🔗 Endpoints da API

### 🧍‍♂️ `POST /cadastro/`

Cadastra um novo paciente com dados pessoais e imagens faciais.

**Parâmetros (Form Data):**
- `nome` (string) - Nome completo do paciente
- `email` (string) - Email do paciente
- `cpf` (string) - CPF do paciente (apenas números)
- `temp_file` (string) - ID temporário das imagens

**Exemplo de Resposta:**
```json
{
  "nome": "Mateus Amaro",
  "email": "mateus@siah.com",
  "cpf": "12345678900",
  "images": ["12345678900/image_1.jpg"]
}
```

---

### `POST /process-embedding/`

Processa embeddings faciais e tenta reconhecer o paciente.

**Fluxo:**
- ✅ Similaridade ≥ 0.85 → Paciente reconhecido
- ❌ Similaridade < 0.85 → Salva como temporário

**Corpo da Requisição:**
```json
{
  "embeddings": ["AAA..."],
  "images": ["BBB..."]
}
```

**Resposta (Reconhecido):**
```json
{
  "status": "reconhecido",
  "usuario": {
    "nome": "Maria Silva",
    "cpf": "98765432100",
    "email": "maria@siah.com",
    "similarity": 0.91
  }
}
```

**Resposta (Não Reconhecido):**
```json
{
  "status": "desconhecido",
  "temp_id": "b02f1f10-321b-11ee-89ab-0242ac110002"
}
```

---

###  `GET /users/`

Lista todos os pacientes cadastrados no sistema.

**Exemplo de Resposta:**
```json
[
  {
    "nome": "Mateus Amaro",
    "email": "mateus@siah.com",
    "cpf": "12345678900",
    "images": ["12345678900/image_1.jpg"]
  }
]
```

---

### `GET /tela_informacoes/{cpf}`

Retorna informações completas de um paciente específico.

**Exemplo:**
```
GET http://localhost:8000/tela_informacoes/12345678900
```

**Resposta:**
```json
{
  "nome": "Mateus Amaro",
  "email": "mateus@siah.com",
  "cpf": "12345678900",
  "embedding_path": "12345678900/",
  "images": ["12345678900/image_1.jpg"]
}
```

---

## Front-end

O frontend foi desenvolvido com **React + Vite** e oferece uma interface moderna e intuitiva.

### Páginas Principais

1. **📸 Cadastro Facial**
   - Captura de imagens via webcam
   - Formulário com nome, CPF e email
   - Envio para `/cadastro/`

2. **🔍 Reconhecimento Facial**
   - Captura em tempo real
   - Processamento de embeddings
   - Envio para `/process-embedding/`

3. **📋 Informações do Paciente**
   - Busca por CPF
   - Exibição de dados completos
   - Consulta via `/tela_informacoes/{cpf}`

### Executando o Frontend

```bash
cd Front-end
npm install
npm run dev
```

Acesse: **http://localhost:5174**

---

## Contribuindo

Contribuições são sempre bem-vindas! Siga os passos abaixo:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Diretrizes

- Mantenha o código limpo e bem documentado
- Siga as convenções de código do projeto
- Adicione testes quando aplicável
- Atualize a documentação conforme necessário

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📞 Contato

**Equipe Treenity**

**Desenvolvido por:**

**Mateus Amaro**
- 💼 LinkedIn: https://www.linkedin.com/in/mateus-amaro-da-silva-613910227/

**Vitor Henrique**
- 💼 LinkedIn: https://www.linkedin.com/in/vitor-araujo-5a4910227/

**Vinicius Santana**
- 💼 LinkedIn: https://www.linkedin.com/in/vin%C3%ADcius-santana-b169b8268/

**Thiago Gabriel**
- 💼 LinkedIn: https://www.linkedin.com/in/thiago-cruz-97228b286/

**Daniel Lopez**
- 💼 LinkedIn: https://www.linkedin.com/in/daniel-ferreira-lopes/

<br>
  
- 🌐 Website: [Treenity.com.br](https://treenity.com.br)

---

<div align="center">

Sistema Integrado de Atendimento Hospitalar

</div>
