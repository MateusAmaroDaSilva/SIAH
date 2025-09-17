import uuid
from fastapi import FastAPI, HTTPException, Query, Form
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from pydantic import BaseModel
from supabase import create_client, Client
import base64
import numpy as np
from fastapi import FastAPI, HTTPException, Request  
import os
from numpy.linalg import norm

SUPABASE_URL = "https://bngwnknyxmhkeesoeizb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJuZ3dua255eG1oa2Vlc29laXpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1MzUwMDcsImV4cCI6MjA3MTExMTAwN30.MVVHAuicG_pkv0OR1h3HEwI-gx7d5hYoqX-xrK17B_U"
SIMILARITY_THRESHOLD = 0.6

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
app = FastAPI(title="API de Reconhecimento Facial")

SIMILARITY_THRESHOLD = 0.80 
EMBEDDINGS_DIR = "embeddings"

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
    embedding: str  

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
            <p>Temp File: {temp_file}</p>
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

        download_bytes = supabase.storage.from_("faces").download(f"{temp_file}/embedding.bin")
        new_path = f"{cpf}/embedding.bin"

        supabase.storage.from_("faces").upload(new_path, download_bytes)

        supabase.storage.from_("faces").remove([f"{temp_file}/embedding.bin"])

        supabase.from_("usuarios").insert({
            "nome": nome,
            "email": email,
            "cpf": cpf,
            "embedding_path": new_path
        }).execute()

        return {"nome": nome, "email": email, "cpf": cpf}

    except Exception as e:
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

@app.post("/recognize/", response_model=RecognizeResponse)
def recognize_user(request: RecognizeRequest):
    try:
        input_vec = np.frombuffer(base64.b64decode(request.embedding), dtype=np.float32)
        res = supabase.from_("usuarios").select("*").execute()

        best_match = {"nome": "Desconhecido", "email": None, "cpf": None, "similarity": 0.0}

        for u in res.data:
            try:
                embedding_path = u["embedding_path"]
                embedding_bytes = supabase.storage.from_("faces").download(embedding_path)
                user_vec = np.frombuffer(embedding_bytes, dtype=np.float32)

                sim = cosine_similarity(input_vec, user_vec)
                if sim > best_match["similarity"]:
                    best_match = {
                        "nome": u["nome"],
                        "email": u["email"],
                        "cpf": u["cpf"],
                        "similarity": float(sim)
                    }
            except Exception as e:
                print(f"Erro ao processar embedding de {u['cpf']}: {e}")

        if best_match["similarity"] >= SIMILARITY_THRESHOLD:
            return best_match
        else:
            return {"nome": "Desconhecido", "email": None, "cpf": None, "similarity": 0.0}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao reconhecer usuário: {str(e)}")

@app.post("/process-embedding/")
async def process_embedding(request: Request):
    try:
        body = await request.json()
        embedding_b64 = body.get("embedding")

        if not embedding_b64:
            raise HTTPException(status_code=400, detail="Embedding não fornecido.")

        input_vec = np.frombuffer(base64.b64decode(embedding_b64), dtype=np.float32)
        input_vec = normalize_vector(input_vec)
        print("[INFO] Novo embedding recebido e normalizado.")

        response = supabase.table("usuarios").select("*").execute()
        usuarios = response.data or []

        if not usuarios:
            print("[WARN] Nenhum usuário cadastrado.")
            return salvar_novo_usuario(embedding_b64)

        best_match = None
        best_similarity = -1

        print(f"[INFO] Comparando com {len(usuarios)} usuários cadastrados...")

        for u in usuarios:
            try:
                embedding_bytes = supabase.storage.from_("faces").download(u["embedding_path"])
                user_vec = np.frombuffer(embedding_bytes, dtype=np.float32)
                user_vec = normalize_vector(user_vec)

                sim = float(np.dot(input_vec, user_vec))
                print(f"[DEBUG] Comparando CPF {u['cpf']} -> Similaridade: {sim:.4f}")

                if sim > best_similarity:
                    best_similarity = sim
                    best_match = u
            except Exception as e:
                print(f"[ERROR] Falha ao processar embedding de {u['cpf']}: {e}")
                continue

        if best_similarity >= SIMILARITY_THRESHOLD:
            print(f"[INFO] Usuário reconhecido: {best_match['nome']} "
                  f"(CPF: {best_match['cpf']}) - Similaridade: {best_similarity:.4f}")
            return {
                "status": "reconhecido",
                "usuario": {
                    "nome": best_match["nome"],
                    "cpf": best_match["cpf"],
                    "email": best_match["email"],
                    "similarity": best_similarity
                }
            }

        print(f"[WARN] Nenhum usuário reconhecido. Maior similaridade: {best_similarity:.4f}")
        return salvar_novo_usuario(embedding_b64)

    except Exception as e:
        print(f"[ERROR] Falha ao processar embedding: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def salvar_novo_usuario(embedding_b64: str):
    temp_id = str(uuid.uuid4())
    caminho_temp = f"{temp_id}/embedding.bin"

    try:
        supabase.storage.from_("faces").upload(caminho_temp, base64.b64decode(embedding_b64))
        print(f"[INFO] Usuário desconhecido - Embedding salvo em {caminho_temp}")
    except Exception as e:
        print(f"[ERROR] Falha ao salvar embedding temporário: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao salvar embedding: {e}")

    return {
        "status": "desconhecido",
        "redirect": f"/cadastro/?temp_file={temp_id}"
    }


@app.get("/tela_informacoes/{cpf}", response_class=HTMLResponse)
async def tela_informacoes(cpf: str):
    try:
        response = supabase.table("usuarios").select("*").eq("cpf", cpf).execute()

        if not response.data:
            return HTMLResponse(f"<h2>Usuário com CPF {cpf} não encontrado.</h2>", status_code=404)

        usuario = response.data[0]

        return f"""
        <html>
            <head>
                <title>Informações do Usuário</title>
            </head>
            <body>
                <h2>Usuário reconhecido com sucesso!</h2>
                <p><strong>Nome:</strong> {usuario['nome']}</p>
                <p><strong>Email:</strong> {usuario['email']}</p>
                <p><strong>CPF:</strong> {usuario['cpf']}</p>
                <p><strong>Embedding salvo em:</strong> {usuario['embedding_path']}</p>
            </body>
        </html>
        """

    except Exception as e:
        return HTMLResponse(f"<h2>Erro ao carregar informações: {str(e)}</h2>", status_code=500)
