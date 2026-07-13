from aiogram import Router

from start import router as start_router
from states import router as states_router
from commands import router as commands_router
from common import router as common_router

handlers_router = Router()

handlers_router.include_routers(
    start_router,
    states_router,
    commands_router,
    common_router
)