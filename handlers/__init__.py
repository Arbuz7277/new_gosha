import os
import importlib
import logging

logger = logging.getLogger(__name__)

def register_all(bot):
    current_dir = os.path.dirname(__file__)
    loaded = 0
    errors = 0

    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                rel_path = os.path.relpath(os.path.join(root, file), current_dir)
                module_name = rel_path.replace('.py', '').replace(os.sep, '.')

                try:
                    module = importlib.import_module(f"handlers.{module_name}")

                    if hasattr(module, 'register'):
                        module.register(bot)
                        loaded += 1
                        logger.info(f"Loaded: {module_name}")
                    else:
                        logger.warning(f"Not found register() in {module_name}")

                except Exception as e:
                    errors += 1
                    logger.error(f"Error in {module_name}: {type(e).__name__}: {e}")
    logger.info(f"Total: loaded {loaded}, errors {errors}")


__all__ = ['register_all']