import socket
from uuid import UUID

import uvicorn

from fastapi import HTTPException, Request
from starlette.responses import JSONResponse

from mealie.app import app
from mealie.core.dependencies.dependencies import get_current_user
from mealie.db.db_setup import session_context
from mealie.db.models.recipe.recipe import RecipeModel
from mealie.db.models.users.users import User


@app.get("/api/template-source", tags=["Corresponding Source"])
async def template_source():
    return {
        "recipeSource": "https://github.com/tech-progress/mealie-recipe-archive/tree/v1.0.2",
        "upstreamSource": "https://github.com/mealie-recipes/mealie/tree/v3.28.0",
        "notices": "https://github.com/tech-progress/mealie-recipe-archive/blob/v1.0.2/THIRD_PARTY_NOTICES.md",
        "licenseScope": "Owner-authored recipe code: MIT. Upstream Mealie: AGPL-3.0-only. Component licenses and corresponding-source obligations remain applicable.",
    }


app.routes.insert(0, app.routes.pop())


@app.middleware("http")
async def corresponding_source_offer(request: Request, call_next):
    response = await call_next(request)
    response.headers["Link"] = '</api/template-source>; rel="describedby"; title="Corresponding source and license notices"'
    return response


@app.middleware("http")
async def private_archive_media(request: Request, call_next):
    if request.url.path.startswith("/api/media/"):
        authorization = request.headers.get("authorization", "")
        token = authorization[7:] if authorization.lower().startswith("bearer ") else request.cookies.get("mealie.access_token", "")
        with session_context() as session:
            try:
                user = await get_current_user(token, session)
            except HTTPException:
                return JSONResponse({"detail": "Authentication required"}, status_code=401)
            parts = request.url.path.split("/")
            if len(parts) >= 5 and parts[3] == "recipes":
                try:
                    recipe = session.get(RecipeModel, UUID(parts[4]))
                except ValueError:
                    return JSONResponse({"detail": "Not found"}, status_code=404)
                if recipe is None or str(recipe.group_id) != str(user.group_id):
                    return JSONResponse({"detail": "Not found"}, status_code=404)
            if len(parts) >= 5 and parts[3] == "users":
                try:
                    account = session.get(User, UUID(parts[4]))
                except ValueError:
                    return JSONResponse({"detail": "Not found"}, status_code=404)
                if account is None or str(account.group_id) != str(user.group_id):
                    return JSONResponse({"detail": "Not found"}, status_code=404)
    return await call_next(request)


if __name__ == "__main__":
    with socket.create_server(("::", 9000), family=socket.AF_INET6, dualstack_ipv6=True) as listener:
        uvicorn.run(app, fd=listener.fileno(), proxy_headers=True, forwarded_allow_ips="*")
