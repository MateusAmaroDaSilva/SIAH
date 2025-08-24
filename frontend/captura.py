import cv2
import mediapipe as mp
import numpy as np
import base64
import requests
import webbrowser
import uuid
import time
from supabase import create_client, Client

API_URL = "http://127.0.0.1:8000"
SUPABASE_URL = "https://bngwnknyxmhkeesoeizb.supabase.co"
SUPABASE_KEY = "SEU_SUPABASE_KEY_AQUI"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

RECOGNITION_TIME = 20  

cap = cv2.VideoCapture(0)
mp_face_detection = mp.solutions.face_detection
start_time = time.time()
recognized = False
current_name = "DESCONHECIDO"
temp_folder_id = None
last_embedding_b64 = None

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as fd:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Erro ao acessar a câmera.")
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = fd.process(rgb)

        if results.detections:
            det = results.detections[0]
            bbox = det.location_data.relative_bounding_box
            h, w = frame.shape[:2]
            x1 = max(0, int(bbox.xmin * w) - 20)
            y1 = max(0, int(bbox.ymin * h) - 20)
            x2 = min(w, int((bbox.xmin + bbox.width) * w) + 20)
            y2 = min(h, int((bbox.ymin + bbox.height) * h) + 20)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            face = frame[y1:y2, x1:x2]
            if face.size > 0:
                face_resized = cv2.resize(face, (200, 200))
                face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
                embedding = face_rgb.flatten().astype(np.float32)
                embedding_b64 = base64.b64encode(embedding.tobytes()).decode('utf-8')

                last_embedding_b64 = embedding_b64

                if not recognized:
                    try:
                        response = requests.post(f"{API_URL}/recognize/", json={"embedding": embedding_b64})
                        data = response.json()
                        if data.get("name") and data.get("name") != "Desconhecido":
                            recognized = True
                            current_name = data["name"]
                            print(f"✅ Usuário reconhecido: {current_name}")
                            break
                    except Exception as e:
                        print(" Erro ao chamar API de reconhecimento:", e)

        color = (0, 0, 255) if current_name == "DESCONHECIDO" else (0, 255, 0)
        cv2.putText(frame, current_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
        cv2.imshow("Reconhecimento Facial", frame)

        if time.time() - start_time > RECOGNITION_TIME:
            print("Tempo limite atingido.")
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Interrompido pelo usuário.")
            break

cap.release()
cv2.destroyAllWindows()

if not recognized and last_embedding_b64:
    temp_folder_id = str(uuid.uuid4())
    upload_path = f"{temp_folder_id}/embedding.bin"

    try:
        print(f"📤 Enviando embedding para Supabase no caminho: {upload_path}")
        response = supabase.storage.from_("faces").upload(
            upload_path,
            base64.b64decode(last_embedding_b64)
        )
        print("🔎 Upload Supabase retorno:", response)

        # Redireciona para cadastro web
        print(f"🌐 Redirecionando para cadastro web...")
        webbrowser.open(f"http://127.0.0.1:8000/cadastro/?temp_file={temp_folder_id}")

    except Exception as e:
        print("Erro ao salvar embedding no Supabase:", e)
else:
    print("⚠ Nenhum embedding salvo. Não será feito redirecionamento.")
