from supabase import create_client, Client

# Configurações do Supabase
SUPABASE_URL = "https://bngwnknyxmhkeesoeizb.supabase.co"
SUPABASE_KEY = "SEU_SUPABASE_KEY_AQUI"

# Cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
