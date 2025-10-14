import cv2
import mediapipe as mp
import numpy as np
import base64
import requests
import webbrowser
import time
import uuid
from supabase import create_client, Client

API_URL = "http://127.0.0.1:8000"
SUPABASE_URL = "https://bngwnknyxmhkeesoeizb.supabase.co"
SUPABASE_KEY = "SEU_SUPABASE_KEY_AQUI"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

POSES = [
    "Olhe para frente",
    "Vire a cabeça para a esquerda",
    "Vire a cabeça para a direita",
    "Aproxime-se da câmera",
    "Afaste-se da câmera"
]

CAPTURE_DELAY = 1.0 
POSE_HOLD_TIME = 3.0 

def capture_embedding(frame, bbox):
    x1, y1, x2, y2 = bbox
    face = frame[y1:y2, x1:x2]
    if face.size > 0:
        face_resized = cv2.resize(face, (200, 200))
        face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
        embedding = face_rgb.flatten().astype(np.float32)
        embedding = embedding / np.linalg.norm(embedding)
        return base64.b64encode(embedding.tobytes()).decode('utf-8')
    return None

def capture_image(frame, bbox):
    x1, y1, x2, y2 = bbox
    face = frame[y1:y2, x1:x2]
    if face.size > 0:
        _, buffer = cv2.imencode(".jpg", face)
        return base64.b64encode(buffer).decode('utf-8')
    return None

def start_recognition():
    cap = cv2.VideoCapture(0)
    mp_face_detection = mp.solutions.face_detection

    collected_embeddings = []
    collected_images = []
    pose_index = 0
    pose_start_time = time.time()
    box_color = (255, 255, 255)
    capturing = False
    capture_time = 0

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as fd:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERRO] Não foi possível acessar a câmera.")
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = fd.process(rgb)
            instruction = POSES[pose_index] if pose_index < len(POSES) else "Captura finalizada!"
            cv2.putText(frame, instruction, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

            if results.detections:
                det = results.detections[0]
                bbox = det.location_data.relative_bounding_box
                h, w = frame.shape[:2]
                x1 = max(0, int(bbox.xmin * w) - 20)
                y1 = max(0, int(bbox.ymin * h) - 20)
                x2 = min(w, int((bbox.xmin + bbox.width) * w) + 20)
                y2 = min(h, int((bbox.ymin + bbox.height) * h) + 20)

                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)

                if not capturing and (time.time() - pose_start_time >= POSE_HOLD_TIME) and pose_index < len(POSES):
                    embedding_b64 = capture_embedding(frame, (x1, y1, x2, y2))
                    image_b64 = capture_image(frame, (x1, y1, x2, y2))

                    if embedding_b64 and image_b64:
                        collected_embeddings.append(embedding_b64)
                        collected_images.append(image_b64)
                        print(f"[CAPTURA] Embedding e imagem da pose {POSES[pose_index]} salvos.")
                        box_color = (0, 255, 0)
                        capturing = True
                        capture_time = time.time()

            if capturing and (time.time() - capture_time >= CAPTURE_DELAY):
                capturing = False
                box_color = (255, 255, 255)
                pose_index += 1
                pose_start_time = time.time()
                if pose_index >= len(POSES):
                    print("[INFO] Todas as capturas concluídas.")
                    break

            cv2.imshow("Reconhecimento Facial", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[INFO] Interrompido pelo usuário.")
                break

    cap.release()
    cv2.destroyAllWindows()

    if collected_embeddings:
        print(f"[INFO] Enviando {len(collected_embeddings)} embeddings e imagens para a API...")
    
    response = requests.post(
        f"{API_URL}/process-embedding/",
        json={
            "embeddings": collected_embeddings,
            "images": collected_images
        }
    )

    if response.status_code == 200:
        data = response.json()
        temp_id = None  

        if data.get("status") == "reconhecido":
            print(f"Usuário reconhecido: {data['usuario']['nome']} (CPF: {data['usuario']['cpf']})")
            webbrowser.open(f"{API_URL}/tela_informacoes/{data['usuario']['cpf']}")
        else:
            temp_id = data.get("temp_id")
            if temp_id:
                redirect_url = f"{API_URL}/cadastro/?temp_file={temp_id}"
                print("[INFO] Usuário não reconhecido. Redirecionando para cadastro...")
                webbrowser.open(redirect_url)
    else:
        print(f"[ERRO] Falha na resposta da API: {response.status_code}")

if __name__ == "__main__":
    print("Certifique-se de que a API está rodando antes de executar este script!")
    start_recognition()
