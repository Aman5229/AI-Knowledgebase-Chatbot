class ChunkingService:

    @staticmethod
    def split_text(
        text: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> list[str]:

        chunks = []

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk = text[start:end]

            if chunk:
                chunks.append(chunk)

            start = end - chunk_overlap

        return chunks