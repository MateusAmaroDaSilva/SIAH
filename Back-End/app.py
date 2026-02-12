import uuid
from fastapi import FastAPI, HTTPException, Query, Form, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from supabase import create_client, Client
import base64
import numpy as np
from numpy.linalg import norm
import json
from fastapi.middleware.cors import CORSMiddleware

SUPABASE_URL = "https://bngwnknyxmhkeesoeizb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJuZ3dua255eG1oa2Vlc29laXpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1MzUwMDcsImV4cCI6MjA3MTExMTAwN30.MVVHAuicG_pkv0OR1h3HEwI-gx7d5hYoqX-xrK17B_U" 
SIMILARITY_THRESHOLD = 0.85 
EMBEDDINGS_DIR = "faces"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
app = FastAPI(title="API de Reconhecimento Facial")

origins = [
    "http://localhost:5174", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def normalize_vector(vec: np.ndarray) -> np.ndarray:
    norm_value = np.linalg.norm(vec)
    if norm_value == 0:
        return vec
    return vec / norm_value

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (norm(v1) * norm(v2))

class UserCreate(BaseModel):
    nome: str
    email: str
    cpf: str
    embedding_path: str

class UserResponse(BaseModel):
    nome: str
    email: str
    cpf: str
    images: list[str] = []

class RecognizeRequest(BaseModel):
    embeddings: list[str] 

class RecognizeResponse(BaseModel):
    nome: str
    email: str | None = None
    cpf: str | None = None
    similarity: float

@app.post("/cadastro/")
def cadastro_temporario(
    nome: str = Form(...),
    cpf: str = Form(...),
    rg: str = Form(""),
    data_nascimento: str = Form(""),
    genero: str = Form(""),
    estado_civil: str = Form(""),
    nacionalidade: str = Form(""),
    naturalidade: str = Form(""),
    telefone: str = Form(""),
    telefone_secundario: str = Form(""),
    email: str = Form(...),
    cep: str = Form(""),
    rua: str = Form(""),
    numero: str = Form(""),
    complemento: str = Form(""),
    bairro: str = Form(""),
    cidade: str = Form(""),
    estado: str = Form(""),
    hospital_vinculado: str = Form(""),
    medico_responsavel: str = Form(""),
    tipo_sanguineo: str = Form(""),
    peso: str = Form(""),
    altura: str = Form(""),
    imc: str = Form(""),
    pressao_arterial: str = Form(""),
    frequencia_cardiaca: str = Form(""),
    alergias: str = Form(""),
    condicoes_cronicas: str = Form(""),
    cirurgias_anteriores: str = Form(""),
    medicamentos_em_uso: str = Form(""),
    historico_familiar: str = Form(""),
    observacoes_medicas: str = Form(""),
    possui_plano_saude: bool = Form(False),
    nome_plano: str = Form(""),
    numero_carteirinha: str = Form(""),
    validade_carteirinha: str = Form(""),
    nome_responsavel: str = Form(""),
    parentesco: str = Form(""),
    telefone_responsavel: str = Form(""),
    cartao_sus: str = Form(""),
    cnh: str = Form(""),
    temp_file: str = Form(...),
):
    return {
        "nome": nome,
        "cpf": cpf,
        "rg": rg,
        "data_nascimento": data_nascimento,
        "genero": genero,
        "estado_civil": estado_civil,
        "nacionalidade": nacionalidade,
        "naturalidade": naturalidade,
        "telefone": telefone,
        "telefone_secundario": telefone_secundario,
        "email": email,
        "cep": cep,
        "rua": rua,
        "numero": numero,
        "complemento": complemento,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado,
        "hospital_vinculado": hospital_vinculado,
        "medico_responsavel": medico_responsavel,
        "tipo_sanguineo": tipo_sanguineo,
        "peso": peso,
        "altura": altura,
        "imc": imc,
        "pressao_arterial": pressao_arterial,
        "frequencia_cardiaca": frequencia_cardiaca,
        "alergias": alergias,
        "condicoes_cronicas": condicoes_cronicas,
        "cirurgias_anteriores": cirurgias_anteriores,
        "medicamentos_em_uso": medicamentos_em_uso,
        "historico_familiar": historico_familiar,
        "observacoes_medicas": observacoes_medicas,
        "possui_plano_saude": possui_plano_saude,
        "nome_plano": nome_plano,
        "numero_carteirinha": numero_carteirinha,
        "validade_carteirinha": validade_carteirinha,
        "nome_responsavel": nome_responsavel,
        "parentesco": parentesco,
        "telefone_responsavel": telefone_responsavel,
        "cartao_sus": cartao_sus,
        "cnh": cnh,
        "temp_file": temp_file
}

@app.post("/process-embedding/")
async def process_embedding(request: Request):
    try:
        body = await request.json()
        embeddings_b64 = body.get("embeddings")
        images_b64 = body.get("images")

        if not embeddings_b64 or not images_b64:
            raise HTTPException(status_code=400, detail="Embeddings ou imagens ausentes.")

        input_embeddings = [
            normalize_vector(np.frombuffer(base64.b64decode(e), dtype=np.float32))
            for e in embeddings_b64
        ]

        usuarios = supabase.table("usuarios").select("*").execute().data or []

        if not usuarios:
            return salvar_temporarios(embeddings_b64, images_b64)

        best_match = None
        best_similarity = -1

        for u in usuarios:
            user_folder = u["embedding_path"]
            files = supabase.storage.from_("faces").list(user_folder) or []
            for file_info in files:
                if not file_info['name'].endswith(".bin"):
                    continue
                embedding_bytes = supabase.storage.from_("faces").download(f"{user_folder}{file_info['name']}")
                user_vec = normalize_vector(np.frombuffer(embedding_bytes, dtype=np.float32))
                for input_vec in input_embeddings:
                    sim = float(np.dot(input_vec, user_vec))
                    if sim > best_similarity:
                        best_similarity = sim
                        best_match = u

        if best_similarity >= SIMILARITY_THRESHOLD:
             return {
                "status": "reconhecido",
                "usuario": {
                    "nome": best_match.get("nome"),
                    "cpf": best_match.get("cpf"),
                    "rg": best_match.get("rg"),
                    "data_nascimento": best_match.get("data_nascimento"),
                    "genero": best_match.get("genero"),
                    "estado_civil": best_match.get("estado_civil"),
                    "nacionalidade": best_match.get("nacionalidade"),
                    "naturalidade": best_match.get("naturalidade"),
                    "telefone": best_match.get("telefone"),
                    "telefone_secundario": best_match.get("telefone_secundario"),
                    "email": best_match.get("email"),
                    "cep": best_match.get("cep"),
                    "rua": best_match.get("rua"),
                    "numero": best_match.get("numero"),
                    "complemento": best_match.get("complemento"),
                    "bairro": best_match.get("bairro"),
                    "cidade": best_match.get("cidade"),
                    "estado": best_match.get("estado"),
                    "hospital_vinculado": best_match.get("hospital_vinculado"),
                    "medico_responsavel": best_match.get("medico_responsavel"),
                    "tipo_sanguineo": best_match.get("tipo_sanguineo"),
                    "peso": best_match.get("peso"),
                    "altura": best_match.get("altura"),
                    "imc": best_match.get("imc"),
                    "pressao_arterial": best_match.get("pressao_arterial"),
                    "frequencia_cardiaca": best_match.get("frequencia_cardiaca"),
                    "alergias": best_match.get("alergias"),
                    "condicoes_cronicas": best_match.get("condicoes_cronicas"),
                    "cirurgias_anteriores": best_match.get("cirurgias_anteriores"),
                    "medicamentos_em_uso": best_match.get("medicamentos_em_uso"),
                    "historico_familiar": best_match.get("historico_familiar"),
                    "observacoes_medicas": best_match.get("observacoes_medicas"),
                    "possui_plano_saude": best_match.get("possui_plano_saude"),
                    "nome_plano": best_match.get("nome_plano"),
                    "numero_carteirinha": best_match.get("numero_carteirinha"),
                    "validade_carteirinha": best_match.get("validade_carteirinha"),
                    "nome_responsavel": best_match.get("nome_responsavel"),
                    "parentesco": best_match.get("parentesco"),
                    "telefone_responsavel": best_match.get("telefone_responsavel"),
                    "cartao_sus": best_match.get("cartao_sus"),
                    "cnh": best_match.get("cnh"),
                    "embedding_path": best_match.get("embedding_path"),
                    "images": best_match.get("images", []),
                    "similarity": best_similarity
                }
            }

        return salvar_temporarios(embeddings_b64, images_b64)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def salvar_temporarios(embeddings_b64, images_b64):
    temp_id = str(uuid.uuid4())
    embeddings_paths = []
    images_paths = []

    for idx, emb_b64 in enumerate(embeddings_b64, start=1):
        path = f"{temp_id}/embedding_{idx}.bin"
        supabase.storage.from_("faces").upload(path, base64.b64decode(emb_b64))
        embeddings_paths.append(path)

    for idx, img_b64 in enumerate(images_b64, start=1):
        path = f"{temp_id}/image_{idx}.jpg"
        supabase.storage.from_("faces").upload(path, base64.b64decode(img_b64))
        images_paths.append(path)

    return {"status": "desconhecido", "temp_id": temp_id, "embeddings_paths": embeddings_paths, "images_paths": images_paths}

@app.post("/users/", response_model=UserResponse)
def Criar_Usuario(
    nome: str = Form(...),
    cpf: str = Form(...),
    rg: str = Form(""),
    data_nascimento: str = Form(""),
    genero: str = Form(""),
    estado_civil: str = Form(""),
    nacionalidade: str = Form(""),
    naturalidade: str = Form(""),
    telefone: str = Form(""),
    telefone_secundario: str = Form(""),
    email: str = Form(...),
    cep: str = Form(""),
    rua: str = Form(""),
    numero: str = Form(""),
    complemento: str = Form(""),
    bairro: str = Form(""),
    cidade: str = Form(""),
    estado: str = Form(""),
    hospital_vinculado: str = Form(""),
    medico_responsavel: str = Form(""),
    tipo_sanguineo: str = Form(""),
    peso: str = Form(""),
    altura: str = Form(""),
    imc: str = Form(""),
    pressao_arterial: str = Form(""),
    frequencia_cardiaca: str = Form(""),
    alergias: str = Form(""),
    condicoes_cronicas: str = Form(""),
    cirurgias_anteriores: str = Form(""),
    medicamentos_em_uso: str = Form(""),
    historico_familiar: str = Form(""),
    observacoes_medicas: str = Form(""),
    possui_plano_saude: bool = Form(False),
    nome_plano: str = Form(""),
    numero_carteirinha: str = Form(""),
    validade_carteirinha: str = Form(""),
    nome_responsavel: str = Form(""),
    parentesco: str = Form(""),
    telefone_responsavel: str = Form(""),
    cartao_sus: str = Form(""),
    cnh: str = Form(""),
    temp_file: str = Form(...),
):
    try:
        existing = supabase.from_("usuarios").select("*").eq("cpf", cpf).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="Usuário já cadastrado")
        user_folder = f"{cpf}/"
        files_in_temp = supabase.storage.from_("faces").list(temp_file) or []

        image_paths = []
        embedding_list = []

        for file_info in files_in_temp:
            source_path = f"{temp_file}/{file_info['name']}"
            final_path = f"{user_folder}{file_info['name']}"
            data = supabase.storage.from_("faces").download(source_path)
            supabase.storage.from_("faces").upload(final_path, data)

            if file_info['name'].lower().endswith(('.jpg', '.jpeg', '.png')):
                image_paths.append(final_path)
            if file_info['name'].endswith('.bin'):
                emb_vector = np.frombuffer(data, dtype=np.float32)
                # embedding_list.append(emb_vector)

        # if files_in_temp:
        #     paths_to_remove = [f"{temp_file}/{f['name']}" for f in files_in_temp]
        #     supabase.storage.from_("faces").remove(paths_to_remove)
        # try:
        #     supabase.storage.from_("faces").remove([temp_file])
        # except:
        #     pass

        supabase.from_("usuarios").insert({
                    "nome": nome,
                    "cpf": cpf,
                    "rg": rg,
                    "data_nascimento": data_nascimento,
                    "genero": genero,
                    "estado_civil": estado_civil,
                    "nacionalidade": nacionalidade,
                    "naturalidade": naturalidade,
                    "telefone": telefone,
                    "telefone_secundario": telefone_secundario,
                    "email": email,
                    "cep": cep,
                    "rua": rua,
                    "numero": numero,
                    "complemento": complemento,
                    "bairro": bairro,
                    "cidade": cidade,
                    "estado": estado,
                    "hospital_vinculado": hospital_vinculado,
                    "medico_responsavel": medico_responsavel,
                    "tipo_sanguineo": tipo_sanguineo,
                    "peso": peso,
                    "altura": altura,
                    "imc": imc,
                    "pressao_arterial": pressao_arterial,
                    "frequencia_cardiaca": frequencia_cardiaca,
                    "alergias": alergias,
                    "condicoes_cronicas": condicoes_cronicas,
                    "cirurgias_anteriores": cirurgias_anteriores,
                    "medicamentos_em_uso": medicamentos_em_uso,
                    "historico_familiar": historico_familiar,
                    "observacoes_medicas": observacoes_medicas,
                    "possui_plano_saude": possui_plano_saude,
                    "nome_plano": nome_plano,
                    "numero_carteirinha": numero_carteirinha,
                    "validade_carteirinha": validade_carteirinha,
                    "nome_responsavel": nome_responsavel,
                    "parentesco": parentesco,
                    "telefone_responsavel": telefone_responsavel,
                    "cartao_sus": cartao_sus,
                    "cnh": cnh,
                    "embedding_path": user_folder,
                    "images": image_paths,
                    "embeddings": json.dumps(embedding_list)
        }).execute()

        return {
            "nome": nome,
            "cpf": cpf,
            "rg": rg,
            "data_nascimento": data_nascimento,
            "genero": genero,
            "estado_civil": estado_civil,
            "nacionalidade": nacionalidade,
            "naturalidade": naturalidade,
            "telefone": telefone,
            "telefone_secundario": telefone_secundario,
            "email": email,
            "cep": cep,
            "rua": rua,
            "numero": numero,
            "complemento": complemento,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado,
            "hospital_vinculado": hospital_vinculado,
            "medico_responsavel": medico_responsavel,
            "tipo_sanguineo": tipo_sanguineo,
            "peso": peso,
            "altura": altura,
            "imc": imc,
            "pressao_arterial": pressao_arterial,
            "frequencia_cardiaca": frequencia_cardiaca,
            "alergias": alergias,
            "condicoes_cronicas": condicoes_cronicas,
            "cirurgias_anteriores": cirurgias_anteriores,
            "medicamentos_em_uso": medicamentos_em_uso,
            "historico_familiar": historico_familiar,
            "observacoes_medicas": observacoes_medicas,
            "possui_plano_saude": possui_plano_saude,
            "nome_plano": nome_plano,
            "numero_carteirinha": numero_carteirinha,
            "validade_carteirinha": validade_carteirinha,
            "nome_responsavel": nome_responsavel,
            "parentesco": parentesco,
            "telefone_responsavel": telefone_responsavel,
            "cartao_sus": cartao_sus,
            "cnh": cnh,
            "images": image_paths
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(e)}")

@app.get("/users/", response_model=list[dict])
def Lista_Usuarios():
    res = supabase.from_("usuarios").select("*").execute()
    return [
        {
            "nome": u.get("nome"),
            "cpf": u.get("cpf"),
            "rg": u.get("rg"),
            "data_nascimento": u.get("data_nascimento"),
            "genero": u.get("genero"),
            "estado_civil": u.get("estado_civil"),
            "nacionalidade": u.get("nacionalidade"),
            "naturalidade": u.get("naturalidade"),
            "telefone": u.get("telefone"),
            "telefone_secundario": u.get("telefone_secundario"),
            "email": u.get("email"),
            "cep": u.get("cep"),
            "rua": u.get("rua"),
            "numero": u.get("numero"),
            "complemento": u.get("complemento"),
            "bairro": u.get("bairro"),
            "cidade": u.get("cidade"),
            "estado": u.get("estado"),
            "hospital_vinculado": u.get("hospital_vinculado"),
            "medico_responsavel": u.get("medico_responsavel"),
            "tipo_sanguineo": u.get("tipo_sanguineo"),
            "peso": u.get("peso"),
            "altura": u.get("altura"),
            "imc": u.get("imc"),
            "pressao_arterial": u.get("pressao_arterial"),
            "frequencia_cardiaca": u.get("frequencia_cardiaca"),
            "alergias": u.get("alergias"),
            "condicoes_cronicas": u.get("condicoes_cronicas"),
            "cirurgias_anteriores": u.get("cirurgias_anteriores"),
            "medicamentos_em_uso": u.get("medicamentos_em_uso"),
            "historico_familiar": u.get("historico_familiar"),
            "observacoes_medicas": u.get("observacoes_medicas"),
            "possui_plano_saude": u.get("possui_plano_saude"),
            "nome_plano": u.get("nome_plano"),
            "numero_carteirinha": u.get("numero_carteirinha"),
            "validade_carteirinha": u.get("validade_carteirinha"),
            "nome_responsavel": u.get("nome_responsavel"),
            "parentesco": u.get("parentesco"),
            "telefone_responsavel": u.get("telefone_responsavel"),
            "cartao_sus": u.get("cartao_sus"),
            "cnh": u.get("cnh"),
            "embedding_path": u.get("embedding_path"),
            "images": u.get("images", []),
            "embeddings": u.get("embeddings", [])
        }
        for u in res.data
    ]

@app.get("/tela_informacoes/{cpf}")
async def tela_informacoes(cpf: str):
    try:
        response = supabase.table("usuarios").select("*").eq("cpf", cpf).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail=f"Usuário com CPF {cpf} não encontrado.")

        usuario = response.data[0]

        return {
            "nome": usuario.get("nome", ""),
            "cpf": usuario.get("cpf", ""),
            "rg": usuario.get("rg", ""),
            "dataNascimento": usuario.get("data_nascimento", ""),
            "genero": usuario.get("genero", ""),
            "estadoCivil": usuario.get("estado_civil", ""),
            "nacionalidade": usuario.get("nacionalidade", ""),
            "naturalidade": usuario.get("naturalidade", ""),
            "telefone": usuario.get("telefone", ""),
            "telefoneSecundario": usuario.get("telefone_secundario", ""),
            "email": usuario.get("email", ""),
            "cep": usuario.get("cep", ""),
            "rua": usuario.get("rua", ""),
            "numero": usuario.get("numero", ""),
            "complemento": usuario.get("complemento", ""),
            "bairro": usuario.get("bairro", ""),
            "cidade": usuario.get("cidade", ""),
            "estado": usuario.get("estado", ""),
            "hospital": usuario.get("hospital_vinculado", ""),
            "medicoResponsavel": usuario.get("medico_responsavel", ""),
            "tipoSanguineo": usuario.get("tipo_sanguineo", ""),
            "peso": usuario.get("peso", ""),
            "altura": usuario.get("altura", ""),
            "imc": usuario.get("imc", ""),
            "pressaoArterial": usuario.get("pressao_arterial", ""),
            "frequenciaCardiaca": usuario.get("frequencia_cardiaca", ""),
            "alergias": usuario.get("alergias", ""),
            "condicoesCronicas": usuario.get("condicoes_cronicas", ""),
            "cirurgias_anteriores": usuario.get("cirurgias_anteriores", ""),
            "medicamentos": usuario.get("medicamentos_em_uso", ""),
            "historicoFamiliar": usuario.get("historico_familiar", ""),
            "observacoesMedicas": usuario.get("observacoes_medicas", ""),
            "possuiPlano": usuario.get("possui_plano_saude", False),
            "nomePlano": usuario.get("nome_plano", ""),
            "numeroCarteirinha": usuario.get("numero_carteirinha", ""),
            "validadeCarteirinha": usuario.get("validade_carteirinha", ""),
            "responsavelNome": usuario.get("nome_responsavel", ""),
            "responsavelParentesco": usuario.get("parentesco", ""),
            "responsavelTelefone": usuario.get("telefone_responsavel", ""),
            "cartaoSUS": usuario.get("cartao_sus", ""),
            "cnh": usuario.get("cnh", ""),
            "embedding_path": usuario.get("embedding_path", None),
            "images": usuario.get("images", [])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar informações: {str(e)}")