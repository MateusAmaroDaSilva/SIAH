from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
import base64
import numpy as np

# Configurações do Supabase
SUPABASE_URL = "https://bngwnknyxmhkeesoeizb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJuZ3dua255eG1oa2Vlc29laXpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1MzUwMDcsImV4cCI6MjA3MTExMTAwN30.MVVHAuicG_pkv0OR1h3HEwI-gx7d5hYoqX-xrK17B_U"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Limite de similaridade
SIMILARITY_THRESHOLD = 0.6

app = FastAPI(title="API de Reconhecimento Facial")

# Schemas
class UserCreate(BaseModel):
    name: str
    email: str
    embedding: str  # embedding codificado em base64

class UserResponse(BaseModel):
    name: str
    email: str

class RecognizeRequest(BaseModel):
    embedding: str

# Função de similaridade
def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# Criar usuário
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate):
    # Verifica se usuário já existe
    existing = supabase.from_("users").select("*").eq("email", user.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    
    supabase.from_("users").insert({
        "name": user.name,
        "email": user.email,
        "embedding": user.embedding
    }).execute()
    
    return {"name": user.name, "email": user.email}

# Listar usuários
@app.get("/users/", response_model=list[UserResponse])
def list_users():
    res = supabase.from_("users").select("*").execute()
    users = [{"name": u["name"], "email": u["email"]} for u in res.data]
    return users

# Reconhecer usuário pelo embedding
@app.post("/recognize/")
def recognize_user(request: RecognizeRequest):
    input_vec = np.frombuffer(base64.b64decode(request.embedding), dtype=np.float32)
    
    res = supabase.from_("users").select("*").execute()
    for u in res.data:
        user_vec = np.frombuffer(base64.b64decode(u["embedding"]), dtype=np.float32)
        sim = cosine_similarity(input_vec, user_vec)
        if sim > SIMILARITY_THRESHOLD:
            return {"name": u["name"], "email": u["email"], "similarity": float(sim)}
    
    return {"name": "Desconhecido", "similarity": 0.0}
