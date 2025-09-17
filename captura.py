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
EMBEDDING_SEND_INTERVAL = 2

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def recognize_face(face_embedding_b64):
    try:
        resp = requests.post(
            f"{API_URL}/process-embedding/",
            json={"embedding": face_embedding_b64},
            allow_redirects=False,
            timeout=5
        )

        if resp.status_code == 303:
            return {"status": "desconhecido"}

        if resp.status_code == 200:
            data = resp.json()

            if data.get("status") == "reconhecido":
                return {
                    "status": "reconhecido",
                    "nome": data["usuario"]["nome"],
                    "cpf": data["usuario"]["cpf"],
                    "email": data["usuario"]["email"],
                    "similarity": data["usuario"]["similarity"]
                }
            else:
                return {"status": "desconhecido"}

        return {"status": "erro"}

    except Exception as e:
        print("Erro ao chamar API:", e)
        return {"status": "erro"}

def start_recognition():
    embedding_enviado = False 
    cap = cv2.VideoCapture(0)
    mp_face_detection = mp.solutions.face_detection

    recognized = False
    current_name = "DESCONHECIDO"
    last_embedding_b64 = None
    last_api_call_time = 0
    last_response = {}

    start_time = time.time()

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as fd:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao acessar a câmera.")
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
                    embedding = embedding / np.linalg.norm(embedding)
                    embedding_b64 = base64.b64encode(embedding.tobytes()).decode('utf-8')
                    last_embedding_b64 = embedding_b64

                    if not recognized and not embedding_enviado:
                        embedding_enviado = True
                        response = recognize_face(embedding_b64)

                        if response and "nome" in response and response["nome"] != "Desconhecido":
                            recognized = True
                            current_name = response["nome"]
                            print(f"Usuário reconhecido: {current_name} ({response.get('cpf')})")
                            webbrowser.open(f"{API_URL}/tela_informacoes/{response.get('cpf')}")

            color = (0, 0, 255) if current_name == "DESCONHECIDO" else (0, 255, 0)
            cv2.putText(frame, current_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
            cv2.imshow("Reconhecimento Facial", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Interrompido pelo usuário.")
                break

            if time.time() - start_time > RECOGNITION_TIME:
                print("Tempo limite atingido.")
                break

    cap.release()
    cv2.destroyAllWindows()

    if not recognized and last_embedding_b64:
        temp_folder_id = str(uuid.uuid4())
        upload_path = f"{temp_folder_id}/embedding.bin"
        try:
            print(f"Enviando embedding para Supabase no caminho: {upload_path}")
            supabase.storage.from_("faces").upload(upload_path, base64.b64decode(last_embedding_b64))
            print("Upload Supabase realizado com sucesso.")

            cadastro_url = f"{API_URL}/cadastro/?temp_file={temp_folder_id}"
            print(f"Abrindo tela de cadastro: {cadastro_url}")
            webbrowser.open(cadastro_url)

        except Exception as e:
            print("Erro ao salvar embedding no Supabase:", e)

if __name__ == "__main__":
    print("Certifique-se de que a API está rodando antes de executar este script!")
    start_recognition()