import os
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

SECRET_KEY=os.getenv('JWT_SECRET_KEY','typebattle-development-secret-change-me')
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES=60
bearer=HTTPBearer(auto_error=False)

def create_access_token(data:dict):
    payload=data.copy();payload['exp']=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

def get_current_user_id(credentials:HTTPAuthorizationCredentials=Depends(bearer)):
    if not credentials: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Please log in first.')
    try:
        payload=jwt.decode(credentials.credentials,SECRET_KEY,algorithms=[ALGORITHM])
        user_id=int(payload.get('sub'))
    except (JWTError,TypeError,ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Your session has expired. Please log in again.')
    return user_id
