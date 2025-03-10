from pydantic import BaseModel

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