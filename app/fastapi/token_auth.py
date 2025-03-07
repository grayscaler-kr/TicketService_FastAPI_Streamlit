import jwt
from datetime import datetime, timedelta
from typing import Dict

# 비밀 키와 알고리즘 설정
SECRET_KEY = "test1234dkagh1."
ALGORITHM = "HS256"

# JWT 생성 함수
def create_access_token(data: Dict[str, str], expires_delta: timedelta = timedelta(hours=1)) -> str:
    expiration = datetime.now() + expires_delta  # 토큰 유효기간 설정
    to_encode = data.copy()
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# JWT 디코드 함수
def decode_access_token(token: str) -> Dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError("Token expired")
    except jwt.JWTError:
        raise jwt.JWTError("Invalid token")
