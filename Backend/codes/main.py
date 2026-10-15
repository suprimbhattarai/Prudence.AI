from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from codes.api.auth.customer_auth_api import (
    router as auth_router,
)
from codes.api.organizations.organization_api import (
    router as organization_router,
)
from codes.api.admin.technician_verification_api import (
    router as technician_verification_router,
)
from codes.api.support.conversation_api import (
    router as conversation_router,
)

from codes.api.support.message_api import (
    router as message_router,
)

app = FastAPI(
    title="Prudence AI",
    version="0.1.0",
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Authorization",
        "Content-Type",
    ],
)

# Register API routers
app.include_router(organization_router)
app.include_router(auth_router)
app.include_router(technician_verification_router)
app.include_router(conversation_router)
app.include_router(message_router)

@app.get("/")
def read_root():
    return {
        "message": "Prudence AI backend is running",
    }
