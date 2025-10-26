"""Document embedding using OpenAI API."""
from typing import List, Dict
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
import time

load_dotenv()

logger = logging.getLogger(__name__)


class DocumentEmbedder:
    """Generate embeddings for semantic search."""

    def __init__(self):
        """Initialize OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key.startswith("sk-your"):
            raise ValueError("OPENAI_API_KEY not configured in .env file")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
        self.dimensions = int(os.getenv("EMBEDDING_DIMENSION", "3072"))

        logger.info(f"Initialized embedder with model: {self.model}, dimensions: {self.dimensions}")

    def embed_requirements(self, requirements: List[Dict]) -> List[Dict]:
        """
        Add embeddings to requirement dicts.

        Args:
            requirements: List of requirement dicts from SRDParser

        Returns:
            Same list with 'statement_embedding' field added
        """
        logger.info(f"Generating embeddings for {len(requirements)} requirements...")

        # Extract texts to embed
        texts = []
        for req in requirements:
            # Combine title and statement for better semantic representation
            text = f"{req.get('title', '')} {req.get('statement', '')}"
            texts.append(text.strip())

        # Generate embeddings in batches
        embeddings = self._batch_embed(texts)

        # Add embeddings to requirements
        for req, embedding in zip(requirements, embeddings):
            req['statement_embedding'] = embedding

        logger.info(f"✓ Generated {len(embeddings)} embeddings")
        return requirements

    def embed_sections(self, sections: List[Dict]) -> List[Dict]:
        """
        Add embeddings to section dicts.

        Args:
            sections: List of section dicts from PDDParser/DDDParser

        Returns:
            Same list with 'content_embedding' field added
        """
        logger.info(f"Generating embeddings for {len(sections)} sections...")

        # Extract texts to embed
        texts = []
        for sec in sections:
            # Use content if available, otherwise title
            text = sec.get('content', sec.get('title', ''))
            # Limit text length to avoid token limits (approximately 8000 tokens = 32000 chars)
            if len(text) > 32000:
                text = text[:32000]
            texts.append(text.strip())

        # Generate embeddings in batches
        embeddings = self._batch_embed(texts)

        # Add embeddings to sections
        for sec, embedding in zip(sections, embeddings):
            sec['content_embedding'] = embedding

        logger.info(f"✓ Generated {len(embeddings)} embeddings")
        return sections

    def _batch_embed(
        self,
        texts: List[str],
        batch_size: int = 100
    ) -> List[List[float]]:
        """
        Batch embed texts with OpenAI API.

        Args:
            texts: List of text strings
            batch_size: Max texts per API call

        Returns:
            List of embedding vectors
        """
        all_embeddings = []
        total_batches = (len(texts) + batch_size - 1) // batch_size

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            batch_num = (i // batch_size) + 1

            try:
                logger.info(f"  Processing batch {batch_num}/{total_batches} ({len(batch)} texts)")

                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch,
                    dimensions=self.dimensions
                )

                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)

                logger.info(f"  ✓ Batch {batch_num}/{total_batches} complete")

                # Rate limiting: sleep briefly between batches
                if batch_num < total_batches:
                    time.sleep(0.5)

            except Exception as e:
                logger.error(f"  ✗ Batch {batch_num}/{total_batches} failed: {e}")
                # Fallback: zero vectors
                logger.warning(f"  Using zero vectors for batch {batch_num}")
                all_embeddings.extend([[0.0] * self.dimensions] * len(batch))

        return all_embeddings

    def embed_text(self, text: str) -> List[float]:
        """
        Embed a single text string.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=[text],
                dimensions=self.dimensions
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to embed text: {e}")
            return [0.0] * self.dimensions


if __name__ == "__main__":
    # Test the embedder
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    print("=== Testing DocumentEmbedder ===\n")

    try:
        embedder = DocumentEmbedder()

        # Test single text embedding
        print("Testing single text embedding...")
        test_text = "The MOSAR technology shall allow repair and update of modular spacecraft"
        embedding = embedder.embed_text(test_text)

        print(f"✓ Generated embedding with {len(embedding)} dimensions")
        print(f"  First 5 values: {embedding[:5]}")

        # Test batch embedding with sample requirements
        print("\nTesting batch embedding...")
        sample_reqs = [
            {
                "id": "FuncR_S101",
                "title": "Satellite repair",
                "statement": "The system shall allow repair of satellites"
            },
            {
                "id": "FuncR_S102",
                "title": "Module replacement",
                "statement": "The system shall enable module replacement"
            }
        ]

        embedded_reqs = embedder.embed_requirements(sample_reqs)

        print(f"✓ Embedded {len(embedded_reqs)} requirements")
        for req in embedded_reqs:
            print(f"  {req['id']}: {len(req['statement_embedding'])} dimensions")

        print("\n✅ Embedder test complete!")

    except Exception as e:
        print(f"\n❌ Embedder test failed: {e}")
