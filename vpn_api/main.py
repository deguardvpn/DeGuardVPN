import secrets
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
from starlette import status
import config
from fastapi import Response
from api.configs_controller.config_router import router as config_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="DeGuardAPI", docs_url=None, redoc_url=None, openapi_url=None)

origins = [
  "https://app.dev.deguard.io",
  "https://app.deguard.io",
  "http://app.dev.deguard.io",
  "http://app.deguard.io"
  "https://deguard.io"
]

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, config.SWAGGER_LOGIN)
    correct_password = secrets.compare_digest(credentials.password, config.SWAGGER_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/api/docs")
async def get_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")


@app.get("/api/openapi.json")
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title="FastAPI", version="0.1.0", routes=app.routes)


@app.get('/get_logs')
def get_logs():
    with open('logfile.log', 'r') as f:
        logs = f.read()

    return Response(content=logs, media_type='text')


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(config_router)
