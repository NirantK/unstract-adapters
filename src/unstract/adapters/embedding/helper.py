import logging
from typing import Any, Optional

from llama_index.core.embeddings.base import BaseEmbedding
from unstract.adapters.exceptions import AdapterError

logger = logging.getLogger(__name__)


class EmbeddingConstants:
    DEFAULT_EMBED_BATCH_SIZE = 10
    EMBED_BATCH_SIZE = "embed_batch_size"


class EmbeddingHelper:
    @staticmethod
    def get_embedding_batch_size(config: dict[str, Any]) -> int:
        if config.get(EmbeddingConstants.EMBED_BATCH_SIZE) is None:
            embedding_batch_size = EmbeddingConstants.DEFAULT_EMBED_BATCH_SIZE
        else:
            embedding_batch_size = int(
                config.get(
                    EmbeddingConstants.EMBED_BATCH_SIZE,
                    EmbeddingConstants.DEFAULT_EMBED_BATCH_SIZE,
                )
            )
        return embedding_batch_size

    @staticmethod
    def test_embedding_instance(embedding: Optional[BaseEmbedding]) -> bool:
        try:
            if embedding is None:
                return False
            response = embedding._get_text_embedding("This is a test")
            if response is not None:
                return True
        except Exception as e:
            logger.error(f"Error occured while testing adapter {e}")
            raise AdapterError(str(e))
