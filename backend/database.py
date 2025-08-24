from supabase import create_client, Client

# Configurações do Supabase
SUPABASE_URL = "https://bngwnknyxmhkeesoeizb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJuZ3dua255eG1oa2Vlc29laXpiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1MzUwMDcsImV4cCI6MjA3MTExMTAwN30.MVVHAuicG_pkv0OR1h3HEwI-gx7d5hYoqX-xrK17B_U"

# Cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
