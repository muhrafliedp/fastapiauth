import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

with open("menu.json", "r") as read_file: 
    data = json.load(read_file)
app = FastAPI()

@app.get('/menu')
async def read_all_menu():
    return data['menu']

@app.get('/menu/{item_id}') 
async def read_menu(item_id:int): 
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
    )

@app.post('/menu/{item_name}')
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

@app.put('/menu/{item_id}')
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

@app.delete('/menu/{item_id}')
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