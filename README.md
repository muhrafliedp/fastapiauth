# Fast API Authentication 

Hasil Deploy : `https://fast-api-muhrafliedp.herokuapp.com/docs`

**Proses Authentication** pada Authorize dilakukan dengan memasukkan *Token*.

_Jika menginginkan Proses Authentication pada Authorize dengan **memasukkan username dan password**, ada pada main.py hasil commit kedua._

Token didapat dari `POST Generate Token`, dengan memasukkan username dan password yang sesuai. Jika tidak sesuai, token tidak akan keluar. Adapun, username dan password yang sesuai didapat dari `GET Get User`, yaitu username : “asdf”, password : “asdf”.
Token yang dimasukkan mempengaruhi hak akses dari semua Endpoints _Proses_ Menu. 

* Apabila melakukan Authentication dengan memasukkan token pada Authorize, maka hasil Response semua Endpoints akan mengeluarkan pesan detail : “Not Authenticated”. 

* Namun, apabila token yang dimasukkan salah ( bukanlah milik user “asdf” ), maka hasil Response semua Endpoints akan mengeluarkan pesan detail : “You don't have access here because your token is invalid or expired."

* Sedangkan, jika token yang dimasukkan benar, maka semua Endpoints akan dapat menjalankan fungsinya dengan tepat.

# Proses Implementasi Endpoints
**METDHOD**|**ROUTE**|**FUNCTIONALITY**|**STATUS**
:-----:|:-----:|:-----:|:-----:
_GET_|`/`|Mendapatkan username dan password user|_Unprotected_
_POST_|`/token/`|Men-generate token dari username dan password yang dimasukkan|_Unprotected_
_GET_|`/menu/`|Mendapatkan seluruh daftar menu|_Protected_
_GET_|`/menu/{item_id}/`|Mendapatkan 1 menu tertentu berdasarkan id item|_Protected_
_PUT_|`/menu/{item_id}/`|Mengubah 1 menu tertentu berdasarkan id item|_Protected_
_DELETE_|`/menu/{item_id}/`|Menghapus 1 menu tertentu berdasarkan id item|_Protected_
_POST_|`/menu/{item_name}/`|Menambah 1 menu berdasarkan nama item|_Protected_

# How to Run This Project
* Install Python
* Git clone project ini dengan `git clone https://github.com/muhrafliedp/fastapiauth.git`
* Buat virtual environment dengan `Pipenv` atau `virtualenv`, kemudian aktifkan
* Install seluruh requirements dengan `pip install -r requirements.txt`
* Terakhir, jalankan API dengan `uvicorn main:app --reload`, dan lihatlah hasilnya pada browser anda `http://127.0.0.1:8000/docs`
* Atau jika ingin langsung menjalankan pada Heroku, silakan buka linknya pada `https://fast-api-muhrafliedp.herokuapp.com/docs`
