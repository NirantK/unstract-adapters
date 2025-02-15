import logging
import os
from typing import Union

from llama_index import (
    ServiceContext,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.vector_stores.types import BasePydanticVectorStore, VectorStore
from unstract.adapters.exceptions import AdapterError
from unstract.adapters.vectordb.constants import VectorDbConstants

logger = logging.getLogger(__name__)


class VectorDBHelper:
    @staticmethod
    def test_vector_db_instance(
        vector_store: Union[VectorStore, BasePydanticVectorStore, None]
    ) -> bool:
        try:
            if vector_store is None:
                return False

            # For custom embedding args will be:
            #     embed_model - InstructorEmbeddings(embed_batch_size=2)
            #     chunk_size - 512
            #     llm=None
            service_context = ServiceContext.from_defaults(
                llm=None, embed_model=None
            )

            storage_context = StorageContext.from_defaults(
                vector_store=vector_store
            )
            local_path = f"{os.path.dirname(__file__)}/samples/"
            index = VectorStoreIndex.from_documents(
                documents=SimpleDirectoryReader(local_path).load_data(),
                storage_context=storage_context,
                service_context=service_context,
            )
            query_engine = index.as_query_engine()

            response = query_engine.query("What did the author learn?")
            if response is not None:
                return True
        except Exception as e:
            logger.error(f"Error occured while testing adapter {e}")
            raise AdapterError(str(e))

    @staticmethod
    def get_collection_name(
        collection_name_prefix: str,
        embedding_dimension: int,
    ) -> str:
        """
        Notes:
            This function constructs the collection / table name to store the
            documents in the vector db.
            If user supplies this field in the config metadata then system
            would pick that and append it as prefix to embedding type.
            If this does not come as user setting, then system looks for it
            in the get_vector_db() argument and append it to embedding type
            If it is not there in both places then system appends
            "unstract_vector_db" as prefix to embedding type.
            If embedding type is not passed in get_vector_db() as arg,
            then system ignores appending that
        Args:
            collection_name_prefix (str): the prefix to be added. If this is
                    not passed in, then the default DEFAULT_VECTOR_DB_NAME
                    will be picked up for prefixing
            embedding_dimension (str): this will be suffixed.
                    If this value is not passed in,
                    then only collection_name_prefix will be returned
                Eg. collection_name_prefix -> mock_org
                    embedding_dimension -> 1536
                    return value -> mock_org_unstract_1536

                    collection_name_prefix -> No value
                    embedding_type -> No value
                    return value -> unstract_vector_db

        """
        vector_db_collection_name: str = (
            VectorDbConstants.DEFAULT_VECTOR_DB_NAME
        )
        if (
            collection_name_prefix is not None
            and embedding_dimension is not None
        ):
            vector_db_collection_name = (
                collection_name_prefix
                + "_"
                + VectorDbConstants.DEFAULT_VECTOR_DB_NAME
                + "_"
                + str(embedding_dimension)
            )
        logger.info(f"Vector DB name: {vector_db_collection_name}")
        return vector_db_collection_name
