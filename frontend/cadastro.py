from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from supabase import create_client
import requests

API_URL = "http://127.0.0.1:8000"
SUPABASE_URL = "https://bngwnknyxmhkeesoeizb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJuZ3dua255eG1oa2Vlc29laXpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1MzUwMDcsImV4cCI6MjA3MTExMTAwN30.MVVHAuicG_pkv0OR1h3HEwI-gx7d5hYoqX-xrK17B_U"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.get("/cadastro/", response_class=HTMLResponse)
async def cadastro_form(temp_file: str):
    html_content = f"""
    <html>
        <head><title>Cadastro de Usuário</title></head>
        <body>
            <h2>Cadastro de Usuário</h2>
            <form action="/cadastro/" method="post">
                Nome: <input type="text" name="name" required><br>
                Email: <input type="email" name="email" required><br>
                <input type="hidden" name="temp_file" value="{temp_file}">
                <input type="submit" value="Cadastrar">
            </form>
        </body>
    </html>
    """
    return html_content

@app.post("/cadastro/")
async def cadastro_submit(
    name: str = Form(...),
    email: str = Form(...),
    temp_file: str = Form(...)
):
    try:
        # 1️⃣ Listar arquivos na pasta temporária
        files = supabase.storage.from_("faces").list(path=temp_file)
        embedding_file = next((f for f in files if f['name'] == "embedding.bin"), None)

        if not embedding_file:
            return HTMLResponse(f"❌ Embedding não encontrado na pasta: {temp_file}", status_code=400)

        # 2️⃣ Baixar o arquivo embedding.bin
        embedding_data = supabase.storage.from_("faces").download(f"{temp_file}/embedding.bin")
        # embedding_data já é bytes, sem precisar de .read()

        # 3️⃣ Fazer upload na pasta definitiva (nome do usuário)
        upload_path = f"{name}/embedding.bin"
        supabase.storage.from_("faces").upload(upload_path, embedding_data)
        print(f"✅ Embedding movido para: {upload_path}")

        # 4️⃣ Deletar o arquivo da pasta temporária
        supabase.storage.from_("faces").remove(f"{temp_file}/embedding.bin")
        print(f"🗑 Embedding temporário removido: {temp_file}/embedding.bin")

        # 5️⃣ Enviar dados para API
        data = {"name": name, "email": email, "embedding": upload_path}
        response = requests.post(f"{API_URL}/users/", json=data)

        if response.status_code == 200:
            return RedirectResponse(url=f"/tela_informacoes/{name}", status_code=303)
        else:
            return HTMLResponse(f"Erro ao cadastrar: {response.json()}", status_code=400)

    except Exception as e:
        return HTMLResponse(f"❌ Erro no cadastro: {str(e)}", status_code=500)
