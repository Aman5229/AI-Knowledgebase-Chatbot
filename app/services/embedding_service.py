from sentence_transformers import SentenceTransformer

class EmbeddingService:
  model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

  @staticmethod
  def create_embedding(text: str) -> list[float]:
    embedding = EmbeddingService.model.encode(text)

    return embedding.tolist()