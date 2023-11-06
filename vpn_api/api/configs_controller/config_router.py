from fastapi import APIRouter, Depends, Response, HTTPException
from api.auth import api_key_auth, oauth2_scheme
from api.configs_controller import config_crud as crud

router = APIRouter(
    prefix='/api/config',
    tags=["Config Controller"]
)


@router.post('/create/{user_id}')
def create_user_config_from_user_id(user_id: str, api_key: str = Depends(oauth2_scheme)):
    if not api_key_auth(api_key):
        raise HTTPException(status_code=401, detail=f"Incorrect api token {api_key}")
    else:
        user_config = crud.create_user_config(user_id)

        return Response(content=user_config, media_type='text')

# @router.delete('/{user_id}')
# def delete_config_by_user_id(user_id: str, db: Session = Depends(get_db), api_key: str = Depends(oauth2_scheme)):
#     if not api_key_auth(api_key):
#         raise HTTPException(status_code=401, detail=f"Incorrect api token {api_key}")
#     else:
#         result = crud.delete_user_config_by_user_id(db, user_id)
#         if not result:
#             raise HTTPException(status_code=400, detail='Some thing wrong')