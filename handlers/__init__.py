from .start import router as start_router
from .name import router as name_router
from .admin import router as admin_router
from .phone import router as phone_router
from .gift_choice import router as gift_router
from .subscription import router as sub_router
from .broadcast import router as broadcast_router
from .user_reply import router as reply_router
from .user_message_handler import router as mes_router

routers = [start_router,
           name_router,
           admin_router,
           phone_router,
           gift_router,
           sub_router,
           broadcast_router,
           reply_router,
           mes_router]
