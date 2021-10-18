import json
import jwt

from fastapi import FastAPI, Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

with open("menu.json", "r") as read_file: 
    data = json.load(read_file)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def authenticate_user(username: str, password: str):
    # user = await User.get(username=username)
    if username != "asdf":
        return False 
    if password != "asdf":
        return False
    return True 

@app.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    token = jwt.encode({"username":form_data.username, "password": form_data.password}, "Raflie's Signature")

    return {'access_token' : token, 'token_type' : 'bearer'}

@app.get('/')
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "Raflie's Signature", algorithms=['HS256'])

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )
    return payload

@app.get('/menu')
async def read_all_menu(token: str = Depends(oauth2_scheme)):
    return data['menu']

@app.get('/menu/{item_id}') 
async def read_menu(item_id:int, token: str = Depends(oauth2_scheme)): 
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.post('/menu/{item_name}')
async def add_menu(item_name:str, token: str = Depends(oauth2_scheme)):
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

@app.put('/menu/{item_id}')
async def update_menu(item_id:int, item_name:str, token: str = Depends(oauth2_scheme)):
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

@app.delete('/menu/{item_id}')
async def delete_menu(item_id:int, token: str = Depends(oauth2_scheme)):
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