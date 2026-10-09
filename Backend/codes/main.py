from fastapi import FastAPI

from codes.api.auth.customer_auth_api import (
    router as auth_router,
)
from codes.api.organizations.organization_api import (
    router as organization_router,
)
from codes.api.admin.technician_verification_api import (
    router as technician_verification_router,
)

app = FastAPI(
    title="Prudence AI",
    version="0.1.0",
)


app.include_router(organization_router)
app.include_router(auth_router)
app.include_router(technician_verification_router)


@app.get("/")
def read_root():
    return {
        "message": "Prudence AI backend is running",
    }
