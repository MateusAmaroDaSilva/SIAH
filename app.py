import uuid
from fastapi import FastAPI, HTTPException, Query, Form, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from supabase import create_client, Client
import base64
import numpy as np
from numpy.linalg import norm

SUPABASE_URL = "https://bngwnknyxmhkeesoeizb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJuZ3dua255eG1oa2Vlc29laXpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1MzUwMDcsImV4cCI6MjA3MTExMTAwN30.MVVHAuicG_pkv0OR1h3HEwI-gx7d5hYoqX-xrK17B_U"
SIMILARITY_THRESHOLD = 0.85 
EMBEDDINGS_DIR = "faces"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
app = FastAPI(title="API de Reconhecimento Facial")

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

class RecognizeRequest(BaseModel):
    embeddings: list[str] 

class RecognizeResponse(BaseModel):
    nome: str
    email: str | None = None
    cpf: str | None = None
    similarity: float

@app.get("/cadastro/", response_class=HTMLResponse)
def cadastro(temp_file: str = Query(..., description="Arquivo temporário com embedding")):
    html_content = f"""
    <html>
        <head><title>Cadastro Usuário</title></head>
        <body>
            <h2>Usuário não reconhecido</h2>
            <p>Arquivo temporário: {temp_file}</p>
            <p>Preencha o cadastro para registrar sua face.</p>
            <form action="/users/" method="post">
                Nome: <input type="text" name="nome" required><br>
                Email: <input type="email" name="email" required><br>
                CPF: <input type="text" name="cpf" required><br>
                <input type="hidden" name="temp_file" value="{temp_file}">
                <input type="submit" value="Cadastrar">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/users/", response_model=UserResponse)
def create_user(
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    temp_file: str = Form(...)
):
    try:
        existing = supabase.from_("usuarios").select("*").eq("cpf", cpf).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="Usuário já cadastrado")
        
        user_folder = f"{cpf}/"

        files_in_temp = supabase.storage.from_("faces").list(temp_file) or []
        
        if files_in_temp:
            paths_to_remove = [f"{temp_file}/{f['name']}" for f in files_in_temp]
            supabase.storage.from_("faces").remove(paths_to_remove)
            print(f"[INFO] Todos os arquivos da pasta temporária {temp_file} foram removidos.")
        else:
            print(f"[INFO] Nenhum arquivo na pasta temporária {temp_file}. Já está vazia.")

        for i, file_info in enumerate(files_in_temp, start=1):
            file_name = file_info['name']

            source_path = f"{temp_file}/{file_name}"
            final_path = f"{user_folder}embedding_{i}.bin"

            print(f"[INFO] Movendo {source_path} para {final_path}")

            embedding_data = supabase.storage.from_("faces").download(source_path)

            supabase.storage.from_("faces").upload(final_path, embedding_data)

        files_in_temp = supabase.storage.from_("faces").list(temp_file)
        if files_in_temp:
            paths_to_remove = [f"{temp_file}/{f['name']}" for f in files_in_temp]
            supabase.storage.from_("faces").remove(paths_to_remove)
            print(f"[INFO] Arquivos temporários removidos: {paths_to_remove}")

        try:
            supabase.storage.from_("faces").remove([temp_file])
            print(f"[INFO] Pasta temporária {temp_file} removida com sucesso.")
        except Exception as e:
            print(f"[WARN] Falha ao remover pasta temporária {temp_file}: {e}")

        supabase.from_("usuarios").insert({
            "nome": nome,
            "email": email,
            "cpf": cpf,
            "embedding_path": user_folder
        }).execute()

        print(f"[INFO] Usuário {nome} cadastrado com sucesso e embeddings movidos!")

        return {"nome": nome, "email": email, "cpf": cpf}

    except Exception as e:
        print(f"[ERROR] Falha ao criar usuário: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(e)}")

@app.get("/users/", response_model=list[UserResponse])
def list_users():
    res = supabase.from_("usuarios").select("*").execute()
    return [
        {
            "nome": u["nome"],
            "email": u["email"],
            "cpf": u["cpf"]
        } for u in res.data
    ]

@app.post("/process-embedding/")
async def process_embedding(request: Request):
    try:
        body = await request.json()
        embeddings_b64 = body.get("embeddings")

        if not embeddings_b64 or not isinstance(embeddings_b64, list):
            raise HTTPException(status_code=400, detail="Lista de embeddings não fornecida ou inválida.")
        
        input_embeddings = [
            normalize_vector(np.frombuffer(base64.b64decode(e), dtype=np.float32))
            for e in embeddings_b64
        ]
        print(f"[INFO] Recebidos {len(input_embeddings)} embeddings para reconhecimento.")

        response = supabase.table("usuarios").select("*").execute()
        usuarios = response.data or []

        if not usuarios:
            print("[WARN] Nenhum usuário cadastrado. Salvando na pasta temporária...")
            return salvar_embeddings_temporarios(embeddings_b64)

        best_match = None
        best_similarity = -1

        for u in usuarios:
            user_folder = u["embedding_path"]
            files = supabase.storage.from_("faces").list(user_folder)

            for file_info in files:
                file_name = file_info["name"]
                embedding_bytes = supabase.storage.from_("faces").download(f"{user_folder}{file_name}")
                user_vec = normalize_vector(np.frombuffer(embedding_bytes, dtype=np.float32))

                for input_vec in input_embeddings:
                    sim = float(np.dot(input_vec, user_vec))
                    if sim > best_similarity:
                        best_similarity = sim
                        best_match = u

                    print(f"[DEBUG] Comparando {u['cpf']} ({file_name}) -> Similaridade: {sim:.4f}")

        if best_similarity >= SIMILARITY_THRESHOLD:
            print(f"[INFO] Usuário reconhecido: {best_match['nome']} (CPF: {best_match['cpf']}) - Similaridade: {best_similarity:.4f}")
            return {
                "status": "reconhecido",
                "usuario": {
                    "nome": best_match["nome"],
                    "cpf": best_match["cpf"],
                    "email": best_match["email"],
                    "similarity": best_similarity
                }
            }
            
        print(f"[WARN] Nenhum usuário reconhecido. Similaridade máxima: {best_similarity:.4f}")
        return salvar_embeddings_temporarios(embeddings_b64)

    except Exception as e:
        print(f"[ERROR] Falha ao processar embeddings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def salvar_embeddings_temporarios(embeddings_b64):
    try:
        temp_id = str(uuid.uuid4())

        for idx, emb_b64 in enumerate(embeddings_b64, start=1):
            file_path = f"{temp_id}/embedding_{idx}.bin"
            supabase.storage.from_("faces").upload(file_path, base64.b64decode(emb_b64))

        print(f"[INFO] Embeddings salvos na pasta temporária: {temp_id}")

        return {
            "status": "desconhecido",
            "temp_id": temp_id
        }

    except Exception as e:
        print(f"[ERROR] Falha ao salvar embeddings temporários: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tela_informacoes/{cpf}", response_class=HTMLResponse)
async def tela_informacoes(cpf: str):
    try:
        response = supabase.table("usuarios").select("*").eq("cpf", cpf).execute()

        if not response.data:
            return HTMLResponse(f"<h2>Usuário com CPF {cpf} não encontrado.</h2>", status_code=404)

        usuario = response.data[0]

        return f"""
        <html>
            <head><title>Informações do Usuário</title></head>
            <body>
                <h2>Usuário reconhecido com sucesso!</h2>
                <p><strong>Nome:</strong> {usuario['nome']}</p>
                <p><strong>Email:</strong> {usuario['email']}</p>
                <p><strong>CPF:</strong> {usuario['cpf']}</p>
                <p><strong>Pasta de Embeddings:</strong> {usuario['embedding_path']}</p>
            </body>
        </html>
        """

    except Exception as e:
        return HTMLResponse(f"<h2>Erro ao carregar informações: {str(e)}</h2>", status_code=500)
