# __init__.py
from aiogram import Router, types

# Импорт всех роутеров
from .start import router as start_rt

main_router = Router()
main_router.include_router(start_rt)

pass
