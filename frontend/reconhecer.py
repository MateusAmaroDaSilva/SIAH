import cv2
import mediapipe as mp
import numpy as np
import base64
import requests

API_URL = "http://127.0.0.1:8000"

cap = cv2.VideoCapture(0)
mp_face_detection = mp.solutions.face_detection

print("Olhe para a câmera. Pressione 'Q' para sair.")

with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as fd:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = fd.process(rgb)

        nome = "Desconhecido"
        cor = (0, 0, 255)  # vermelho por padrão

        if results.detections:
            det = results.detections[0]
            bbox = det.location_data.relative_bounding_box
            h, w = frame.shape[:2]
            x1 = max(0, int(bbox.xmin * w) - 20)
            y1 = max(0, int(bbox.ymin * h) - 20)
            x2 = min(w, int((bbox.xmin + bbox.width) * w) + 20)
            y2 = min(h, int((bbox.ymin + bbox.height) * h) + 20)

            cv2.rectangle(frame, (x1, y1), (x2, y2), cor, 2)

            face = frame[y1:y2, x1:x2]
            if face.size > 0:
                face_resized = cv2.resize(face, (200, 200))
                face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)
                embedding = face_rgb.flatten().astype(np.float32)
                embedding_b64 = base64.b64encode(embedding.tobytes()).decode('utf-8')

                # Enviar para API
                response = requests.post(f"{API_URL}/recognize/", json={"embedding": embedding_b64})
                if response.status_code == 200:
                    data = response.json()
                    nome = data.get("name", "Desconhecido")
                    if nome != "Desconhecido":
                        cor = (0, 255, 0)

        cv2.putText(frame, nome, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, cor, 2)
        cv2.imshow("Reconhecimento Facial", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
