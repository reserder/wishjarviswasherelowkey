import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

class AegisMemory:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL)
        self.collections = ["personal_life_os", "amora_business_ops", "forge_codebase", "muse_brand"]
        self._ensure_collections()

    def _ensure_collections(self):
        try:
            existing = [c.name for c in self.client.get_collections().collections]
            for col in self.collections:
                if col not in existing:
                    self.client.recreate_collection(
                        collection_name=col,
                        vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
                    )
        except Exception as e:
            print(f"Warning: Could not connect to Qdrant at {QDRANT_URL}. Memory features may be limited. Error: {e}")

    def add_memory(self, collection: str, text: str, metadata: dict = None):
        # In a real implementation, we would embed the text here
        # For now, we scaffold the interface
        pass

    def search_memory(self, collection: str, query: str, limit: int = 5):
        # In a real implementation, we would embed the query and search Qdrant
        pass

memory_db = AegisMemory()
