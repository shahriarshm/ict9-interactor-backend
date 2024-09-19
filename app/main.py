from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import (
    discount_codes,
    users,
    hosts,
    campaigns,
    widget_templates,
    widgets,
    host_users,
)
from app.db import engine
from app.models import base

app = FastAPI(title="Interactor")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
base.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(hosts.router, prefix="/api/v1/hosts", tags=["hosts"])
app.include_router(campaigns.router, prefix="/api/v1/campaigns", tags=["campaigns"])
app.include_router(
    discount_codes.router, prefix="/api/v1/discount-codes", tags=["discount_codes"]
)
app.include_router(
    widget_templates.router,
    prefix="/api/v1/widget-templates",
    tags=["widget_templates"],
)
app.include_router(widgets.router, prefix="/api/v1/widgets", tags=["widgets"])
app.include_router(host_users.router, prefix="/api/v1/host-users", tags=["host_users"])


@app.get("/")
async def root():
    return {"message": "Hello World"}
