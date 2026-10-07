from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from ..database import get_db
from .. import models
from ..security import get_current_user_id
router=APIRouter(prefix='/api/practice',tags=['Practice'])
class PracticeResultCreate(BaseModel):
    passage:str=Field(min_length=1,max_length=5000);wpm:float=Field(ge=0,le=1000);accuracy:float=Field(ge=0,le=100);errors:int=Field(ge=0);time_taken:int=Field(ge=0,le=3600)
@router.post('/result')
def save(result:PracticeResultCreate,user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    row=models.PracticeResult(user_id=user_id,**result.model_dump());db.add(row);db.commit();db.refresh(row);return {'message':'Practice result saved successfully','result':{'id':row.id,'wpm':row.wpm,'accuracy':row.accuracy,'errors':row.errors,'time_taken':row.time_taken}}
@router.get('/history')
def history(user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
    rows=db.query(models.PracticeResult).filter(models.PracticeResult.user_id==user_id).order_by(models.PracticeResult.created_at.desc()).limit(20).all()
    return {'results':[{'id':r.id,'wpm':r.wpm,'accuracy':r.accuracy,'errors':r.errors,'time_taken':r.time_taken,'created_at':r.created_at} for r in rows]}
