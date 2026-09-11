import hashlib
import importlib

from app import logger, MODULES, FAILED_TO_LOAD_MODULES, PLUGINS_PATH


def load_plugins():
    for file in PLUGINS_PATH.rglob("*.py"):
        if file.name.startswith("_"):
            continue

        module_name = ".".join(file.with_suffix("").parts)

        try:
            module = importlib.import_module(module_name)

            if hasattr(module, "__module__"):
                meta = module.__module__
                # 8 char static ID from the filename
                meta["_id"] = hashlib.sha256(file.stem.encode()).hexdigest()[:8]
                # Update Modules Data
                MODULES[meta["_id"]] = meta

                logger.info(f"[+] Loaded {module_name}")

        except Exception as e:
            msg = f"[!] Failed to load {module_name} - Error: {e}"
            logger.error(msg)
            FAILED_TO_LOAD_MODULES.append(msg)
