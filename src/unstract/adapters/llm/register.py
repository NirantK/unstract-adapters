import logging
import os
from importlib import import_module
from typing import Any

from unstract.adapters.constants import Common
from unstract.adapters.llm.llm_adapter import LLMAdapter
from unstract.adapters.registry import AdapterRegistry

logger = logging.getLogger(__name__)


class LLMRegistry(AdapterRegistry):
    @staticmethod
    def register_adapters(adapters: dict[str, Any]) -> None:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        package = "unstract.adapters.llm"

        for adapter in os.listdir(current_directory):
            adapter_path = os.path.join(
                current_directory, adapter, Common.SRC_FOLDER
            )
            # Check if the item is a directory and not a
            # special directory like _pycache__
            if os.path.isdir(adapter_path) and not adapter.startswith("__"):
                LLMRegistry.__build_adapter_list(adapter, package, adapters)
        if len(adapters) == 0:
            logger.warning("No llm adapter found.")

    @staticmethod
    def __build_adapter_list(
        adapter: str, package: str, adapters: dict[str, Any]
    ) -> None:
        try:
            full_module_path = f"{package}.{adapter}.{Common.SRC_FOLDER}"
            module = import_module(full_module_path)
            metadata = getattr(module, Common.METADATA, {})
            if metadata.get("is_active", False):
                adapter_class: LLMAdapter = metadata[Common.ADAPTER]
                adapter_id = adapter_class.get_id()
                if not adapter_id or (adapter_id in adapters):
                    logger.warning(f"Duplicate Id : {adapter_id}")
                else:
                    adapters[adapter_id] = {
                        Common.MODULE: module,
                        Common.METADATA: metadata,
                    }
        except ModuleNotFoundError as exception:
            logger.error(f"Error while importing llm adapters : {exception}")
