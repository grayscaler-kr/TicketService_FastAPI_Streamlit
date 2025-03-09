from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db_sample import BUYER_DB

app = FastAPI()

# 데이터 모델 정의
class ReservationRequest(BaseModel):
    name: str
    phone: str
    birth_date: str
    ticket: str
    zone: str
    num_people: int
    total_price: int

class DuplicateCheckRequest(BaseModel):
    name: str
    phone: str
    birth_date: str

# 중복 신청 확인 API
@app.post("/check_duplicate")
def check_duplicate(request: DuplicateCheckRequest):
    if (request.name in BUYER_DB["name"] and 
        request.phone in BUYER_DB["phone"] and 
        request.birth_date in BUYER_DB["birth_date"]):
        return {"duplicate": True}
    return {"duplicate": False}

# 예약 신청 API
@app.post("/reserve_ticket")
def reserve_ticket(request: ReservationRequest):
    BUYER_DB["name"].append(request.name)
    BUYER_DB["phone"].append(request.phone)
    BUYER_DB["birth_date"].append(request.birth_date)
    BUYER_DB["ticket_name"].append(request.ticket)
    return {"message": "예약이 완료되었습니다!"}
