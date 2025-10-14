from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from supabase import create_client
import uuid
import base64
import numpy as np

SUPABASE_URL = "https://bngwnknyxmhkeesoeizb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJuZ3dua255eG1oa2Vlc29laXpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1MzUwMDcsImV4cCI6MjA3MTExMTAwN30.MVVHAuicG_pkv0OR1h3HEwI-gx7d5hYoqX-xrK17B_U" 
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

SIMILARITY_THRESHOLD = 0.85
app = FastAPI()

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

@app.get("/cadastro/", response_class=HTMLResponse)
async def cadastro_form(temp_file: str):
    html_content = f"""
    <html>
        <head><title>Cadastro de Usuário</title></head>
        <body>
            <h2>Cadastro de Usuário</h2>
            <form action="/cadastro/" method="post">
                Nome: <input type="text" name="nome" required><br>
                Email: <input type="email" name="email" required><br>
                CPF: <input type="text" name="cpf" required><br>
                <input type="hidden" name="temp_file" value="{temp_file}">
                <input type="submit" value="Cadastrar">
            </form>
        </body>
    </html>
    """
    return html_content

@app.post("/cadastro/")
async def cadastro_submit(
    nome: str = Form(...),
    email: str = Form(...),
    cpf: str = Form(...),
    temp_file: str = Form(...)
):
    try:
        files = supabase.storage.from_("faces").list(path=temp_file)
        embedding_file = next((f for f in files if f["name"] == "embedding.bin"), None)
        if not embedding_file:
            return HTMLResponse(f"Embedding não encontrado na pasta: {temp_file}", status_code=400)
        embedding_data = supabase.storage.from_("faces").download(f"{temp_file}/embedding.bin")
        upload_path = f"{cpf}/embedding.bin"
        supabase.storage.from_("faces").upload(upload_path, embedding_data)
        supabase.storage.from_("faces").remove(f"{temp_file}/embedding.bin")
        data = {
            "nome": nome,
            "email": email,
            "cpf": cpf,
            "embedding_path": upload_path
        }
        supabase.table("usuarios").insert(data).execute()
        return RedirectResponse(url=f"/tela_informacoes/{nome}", status_code=303)
    except Exception as e:
        return HTMLResponse(f"Erro no cadastro: {str(e)}", status_code=500)

@app.get("/tela_informacoes/{nome}", response_class=HTMLResponse)
async def tela_informacoes(nome: str):
    return f"""
    <html>
        <head><title>Informações</title></head>
        <body>
            <h2>Usuário {nome} cadastrado com sucesso!</h2>
        </body>
    </html>
    """

from pydantic import BaseModel

class RecognizeRequest(BaseModel):
    embedding: str

@app.post("/process-embedding/")
async def process_embedding(request: RecognizeRequest):
    try:
        input_vec = np.frombuffer(base64.b64decode(request.embedding), dtype=np.float32)
        res = supabase.table("usuarios").select("*").execute()
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
            return JSONResponse(best_match)
        else:
            temp_id = str(uuid.uuid4())
            temp_path = f"{temp_id}/embedding.bin"
            supabase.storage.from_("faces").upload(temp_path, base64.b64decode(request.embedding))
            return RedirectResponse(url=f"/cadastro/?temp_file={temp_id}", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")
