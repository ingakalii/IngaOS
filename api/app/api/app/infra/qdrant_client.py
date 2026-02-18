from qdrant_client import QdrantClient as Qdrant
from qdrant_client.http import models as rest

class QdrantClient:
    def __init__(self, url: str):
        # url is like "http://localhost:6333"
        # qdrant-client expects host param + prefer default grpc disabled for demo
        self.client = Qdrant(url=url)

    def create_collection_if_not_exists(self, name: str, vector_size: int):
        existing = [c.name for c in self.client.get_collections().collections]
        if name not in existing:
            self.client.recreate_collection(name=name, vectors_config=rest.VectorParams(size=vector_size, distance=rest.Distance.COSINE))

    def upsert(self, collection: str, items):
        # items: list of dict{ id, vector, payload } 
        points = []
        for it in items:
            points.append(rest.PointStruct(id=it["id"], vector=it["vector"], payload=it.get("payload")))
        self.client.upsert(collection_name=collection, points=points)

    def search(self, collection: str, vector, top_k: int = 5):
        hits = self.client.search(collection_name=collection, query_vector=vector, limit=top_k)
        return hits
