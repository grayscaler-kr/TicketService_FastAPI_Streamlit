# fastapi-app/models.py
from pydantic import BaseModel, Field, field_validator
import re

class UserRequest(BaseModel):
    username: str = Field(..., min_length=5, max_length=20)  # ID 길이 제한 (5~20자)
    password: str = Field(..., min_length=8, max_length=30)  # 비밀번호 길이 제한 (8~30자)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if not v.isalnum():  # 영문+숫자로만 이루어져야 함
            raise ValueError("ID는 영문과 숫자로만 이루어져야 합니다.")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not any(c.isdigit() for c in v):
            raise ValueError("비밀번호는 최소 1개 이상의 숫자를 포함해야 합니다.")
        if not any(c.isalpha() for c in v):
            raise ValueError("비밀번호는 최소 1개 이상의 영문자를 포함해야 합니다.")
        if " " in v:
            raise ValueError("비밀번호는 공백을 포함할 수 없습니다.")
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/|`~]', v):
            raise ValueError("비밀번호는 최소 1개 이상의 특수문자를 포함해야 합니다.")
        return v
