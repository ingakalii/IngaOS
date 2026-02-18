from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, texts):
        if isinstance(texts, str):
            return self.model.encode(texts)
        return self.model.encode(texts)
