from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud
from ..schemas import UserCreate,UserResponse,UserLogin
from .. import models
from ..security import create_access_token,get_current_user_id
router=APIRouter(prefix='/api/auth',tags=['Authentication'])
@router.post('/register',response_model=UserResponse)
def register(user:UserCreate,db:Session=Depends(get_db)):
    if crud.get_user_by_email(db,user.email): raise HTTPException(400,'Email already registered.')
    if crud.get_user_by_username(db,user.username): raise HTTPException(400,'Username already taken.')
    return crud.create_user(db,user.username,user.email,user.password)
@router.post('/login')
def login(user:UserLogin,db:Session=Depends(get_db)):
    existing=crud.get_user_by_email(db,user.email)
    if not existing or not crud.verify_password(user.password,existing.password_hash): raise HTTPException(401,'Invalid email or password.')
    return {'message':'Login successful','access_token':create_access_token({'sub':str(existing.id),'email':existing.email}),'token_type':'bearer','user':{'id':existing.id,'username':existing.username,'email':existing.email}}
@router.get('/me',response_model=UserResponse)
def me(user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if not user: raise HTTPException(404,'User not found.')
    return user
