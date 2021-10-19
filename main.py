import json
import jwt

from fastapi import FastAPI, Depends, HTTPException, Request, status 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

with open("menu.json", "r") as read_file: 
    data = json.load(read_file)

app = FastAPI()

JWT_SECRET = "Raflie's Signature"

USER_PAYLOAD = {
    "username": "asdf", 
    "password": "asdf"
    }
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="You don't have access here because your token is invalid or expired.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = jwt.decode(jwtoken, JWT_SECRET, algorithms=['HS256'])
        except:
            payload = None
        if payload == USER_PAYLOAD:
            isTokenValid = True
        return isTokenValid

async def authenticate_user(username: str, password: str):
    if username != "asdf":
        return False 
    if password != "asdf":
        return False
    return True 

# ~~~ UNPROTECTED ~~~ #

@app.get('/')
async def get_user():
    return USER_PAYLOAD

@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )
    payload = {
        "username": form_data.username, 
        "password": form_data.password
    }
    token = jwt.encode(payload, JWT_SECRET)

    return {'access_token' : token, 'token_type' : 'bearer'}

# ~~~ PROTECTED ~~~ #

@app.get('/menu', dependencies=[Depends(JWTBearer())])
async def read_all_menu():
    return data['menu']

@app.get('/menu/{item_id}', dependencies=[Depends(JWTBearer())]) 
async def read_menu(item_id:int): 
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.post('/menu/{item_name}', dependencies=[Depends(JWTBearer())])
async def add_menu(item_name:str):
    id=1
    if(len(data['menu'])>0):
        id=data['menu'][len(data['menu'])-1]['id']+1
    updated={'id':id, 'name':item_name}
    data['menu'].append(dict(updated))
    
    read_file.close()
    with open("menu.json", "w") as write_file:
        json.dump(data, write_file, indent=4)
    write_file.close()

    return(updated)
    raise HTTPException(
        status_code=500, detail=f'Data Gagal Diperbarui'
    )

@app.put('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def update_menu(item_id:int, item_name:str):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            menu_item['name'] = item_name
            
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data, write_file, indent=4)
            write_file.close()

            return{"message":"Menu Item Berhasil Diubah"} 

    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.delete('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def delete_menu(item_id:int):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            data['menu'].remove(menu_item)

            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data, write_file, indent=4)
            write_file.close()

            return{"message":"Data Menu Tersebut Berhasil Dihapus"}

    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )