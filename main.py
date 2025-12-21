from typing import Union
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

app= FastAPI()

#1 모델 정의

app = FastAPI()

#1. 모델정의
class Item(BaseModel):
    name: str
    price : float
    is_offer : Union[bool, None] = None

#2. 가짜 데이터베이스 (서버끄면 사라짐)
fake_items_db = {
    1:{"name":"기본 아이템", "price" : 1000.0, "is_offer": False}
}

#Read 조회
@app.get("/item/{item_id}")
def read_item(item_id:int):
    return fake_items_db.get(item_id, {"message":"아이템이 없습니다."})

#Create 생성
@app.post("/items/{item_id}")
def create_item(item_id:int, item:Item):
    if item_id in fake_items_db:
        return{"error":"이미 존재하는 ID입니다"}

    #db에 저장
    fake_items_db[item_id] = item.dict()
    return {"message":"저장 성공", "item": item}

#Update 수정
@app.put("/items/{item_id}")
def update_item(item_id:int, item:Item):
    if item_id not in fake_items_db:
        return {"error":"수정할 아이템이 없습니다."}

    #db 내용 덮어쓰기
    fake_items_db[item_id]=item.dict()
    return {"message":"수정 성공", "item": item}

#Delete 삭제
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in fake_items_db:
        return {"error": "삭제할 아이템이 없습니다."}
    
    #DB에서 삭제
    del fake_items_db[item_id]
    return {"message": "삭제 성공"}

#File 업로드
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename" :file.filename,
    "content_type": file.content_type}