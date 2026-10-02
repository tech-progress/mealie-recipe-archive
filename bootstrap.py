import os

from sqlalchemy import select

from mealie.core.security import hash_password
from mealie.core.security.hasher import get_hasher
from mealie.db.db_setup import session_context
from mealie.db.init_db import main
from mealie.db.models.users.users import User


main()
with session_context() as session:
    default_user = session.scalar(select(User).where(User.email == "changeme@example.com"))
    if default_user is not None and get_hasher().verify("MyPassword", default_user.password):
        default_user.email = os.environ["MEALIE_ADMIN_EMAIL"].lower()
        default_user.password = hash_password(os.environ["MEALIE_ADMIN_PASSWORD"])
        default_user.full_name = "Archive Administrator"
        session.commit()
    unsafe_user = session.scalar(select(User).where(User.email == "changeme@example.com"))
    if unsafe_user is not None and get_hasher().verify("MyPassword", unsafe_user.password):
        raise RuntimeError("Default administrator still active; refusing to listen")
