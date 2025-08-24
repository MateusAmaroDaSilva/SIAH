import numpy as np
import base64

def embedding_from_base64(b64_string):
    bytes_data = base64.b64decode(b64_string)
    return np.frombuffer(bytes_data, dtype=np.float32)

def embedding_to_base64(embedding):
    return base64.b64encode(embedding.tobytes()).decode('utf-8')

def cosine_similarity(v1, v2):
    if v1.shape != v2.shape:
        return 0
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
