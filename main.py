from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

import firebase_admin
from firebase_admin import credentials, auth

import pyrebase

from models import SignUpSchema, LoginSchema


app = FastAPI(
    title="FastAPI with Firebase",
    description="A simple example of a FastAPI API with Firebase",
    version="0.1.0",
    docs_url="/",
    redoc_url="/redoc",
)

# Firebase Config
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    
# Firebase App Config
firebaseConfig = {
  "apiKey": "",
  "authDomain": "",
  "projectId": "",
  "storageBucket": "",
  "messagingSenderId": "",
  "appId": "",
  "databaseURL": ""
}
    
firebase = pyrebase.initialize_app(firebaseConfig)



# Create User
@app.post("/signup")
def create_account(user_data: SignUpSchema):
    email = user_data.email
    password = user_data.password
    
    try:
        user = auth.create_user(email=email, password=password)
        
        return JSONResponse(content={"message": f"Account Created successfully for user {user.uid}"}, status_code=status.HTTP_201_CREATED)
    except auth.EmailAlreadyExistsError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {email} already exists",
        )


# Login User and create JTW Access Token
@app.post("/login")
def login_user(user_data: LoginSchema):
    email = user_data.email
    password = user_data.password
    
    try:
        user = firebase.auth().sign_in_with_email_and_password(email=email, password=password)
        
        token = user['idToken']
        
        return JSONResponse(content={"token": token}, status_code=status.HTTP_200_OK)
    
    except auth.Error as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {email} or password is incorrect",
        )


# Validate JTW Access Token
@app.post("/ping")
def validate_token(request: Request):
    headers = request.headers
    
    jwt = headers.get('authorization')
    
    user = auth.verify_id_token(jwt)
    
    return user['user_id']