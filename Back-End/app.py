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
SUPABASE_KEY = "SEU_SUPABASE_KEY_AQUI"  
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
def cadastro_react(
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    temp_file: str = Form(...)
):
    return create_user(nome, email, cpf, temp_file)

@app.post("/users/", response_model=UserResponse)
def create_user(nome: str = Form(...), email: str = Form(...), cpf: str = Form(...), temp_file: str = Form(...)):
    try:
        existing = supabase.from_("usuarios").select("*").eq("cpf", cpf).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="Usuário já cadastrado")
        
        user_folder = f"{cpf}/"
        files_in_temp = supabase.storage.from_("faces").list(temp_file) or []

        image_paths = []
        for file_info in files_in_temp:
            source_path = f"{temp_file}/{file_info['name']}"
            final_path = f"{user_folder}{file_info['name']}"
            data = supabase.storage.from_("faces").download(source_path)
            supabase.storage.from_("faces").upload(final_path, data)

            if file_info['name'].lower().endswith(('.jpg','.jpeg','.png')):
                image_paths.append(final_path)

        if files_in_temp:
            paths_to_remove = [f"{temp_file}/{f['name']}" for f in files_in_temp]
            supabase.storage.from_("faces").remove(paths_to_remove)
        try:
            supabase.storage.from_("faces").remove([temp_file])
        except:
            pass

        supabase.from_("usuarios").insert({
            "nome": nome,
            "email": email,
            "cpf": cpf,
            "embedding_path": user_folder,
            "images": image_paths  
        }).execute()

        return {"nome": nome, "email": email, "cpf": cpf, "images": image_paths}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(e)}")

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
                emb_vector = np.frombuffer(data, dtype=np.float32).tolist()
                embedding_list.append(emb_vector)
        if files_in_temp:
            paths_to_remove = [f"{temp_file}/{f['name']}" for f in files_in_temp]
            supabase.storage.from_("faces").remove(paths_to_remove)
        try:
            supabase.storage.from_("faces").remove([temp_file])
        except:
            pass

        supabase.from_("usuarios").insert({
        "nome": nome,
        "email": email,
        "cpf": cpf,
        "embedding_path": user_folder,
        "images": image_paths,
        "embeddings": json.dumps(embedding_list)  
    }).execute()

        return {"nome": nome, "email": email, "cpf": cpf, "images": image_paths}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(e)}")

@app.get("/users/", response_model=list[UserResponse])
def list_users():
    res = supabase.from_("usuarios").select("*").execute()
    return [{"nome": u["nome"], "email": u["email"], "cpf": u["cpf"], "images": u.get("images", [])} for u in res.data]

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
                    "nome": best_match["nome"],
                    "cpf": best_match["cpf"],
                    "email": best_match["email"],
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

@app.get("/tela_informacoes/{cpf}")
async def tela_informacoes(cpf: str):
    try:
        response = supabase.table("usuarios").select("*").eq("cpf", cpf).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail=f"Usuário com CPF {cpf} não encontrado.")

        usuario = response.data[0]

        return {
            "nome": usuario['nome'],
            "email": usuario['email'],
            "cpf": usuario['cpf'],
            "embedding_path": usuario.get('embedding_path', None),
            "images": usuario.get('images', [])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar informações: {str(e)}")

