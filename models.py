from pydantic import BaseModel


class SignUpSchema(BaseModel):
    email: str
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "sample@example.com",
                "password": "samplepass123"
            }
        }
    
    
class LoginSchema(BaseModel):
    email: str
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "sample@example.com",
                "password": "samplepass123"
            }
        }