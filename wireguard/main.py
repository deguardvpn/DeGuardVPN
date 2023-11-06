import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DeGuardAPI", docs_url=None, redoc_url=None, openapi_url=None)

origins = ["*"]

security = HTTPBasic()


@app.get("/api/sync_configs")
async def sync_conf():
    os.system("su root ./update.sh")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)