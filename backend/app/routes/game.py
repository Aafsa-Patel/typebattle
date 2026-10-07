from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from ..database import get_db
from .. import models
from ..security import get_current_user_id
router=APIRouter(tags=['Game'])
class BattleCreate(BaseModel):
 mode:str=Field(pattern='^(easy|medium|hard)$');wpm:float=Field(ge=0,le=1000);accuracy:float=Field(ge=0,le=100);score:int=Field(ge=0);won:bool;time_taken:int=Field(ge=0,le=3600)
@router.post('/api/battle/result')
def save_battle(result:BattleCreate,user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
 row=models.BattleResult(user_id=user_id,**result.model_dump());db.add(row);db.commit();db.refresh(row);return {'message':'Battle result saved','id':row.id}
@router.get('/api/leaderboard')
def leaderboard(db:Session=Depends(get_db)):
 from sqlalchemy import func
 rows=db.query(models.User.id,models.User.username,func.max(models.PracticeResult.wpm).label('wpm'),func.max(models.PracticeResult.accuracy).label('accuracy')).join(models.PracticeResult,models.User.id==models.PracticeResult.user_id).group_by(models.User.id,models.User.username).order_by(func.max(models.PracticeResult.wpm).desc()).limit(50).all()
 return {'leaderboard':[{'user_id':r.id,'username':r.username,'wpm':r.wpm or 0,'accuracy':r.accuracy or 0} for r in rows]}
@router.get('/api/profile')
def profile(user_id:int=Depends(get_current_user_id),db:Session=Depends(get_db)):
 from sqlalchemy import func
 practices=db.query(models.PracticeResult).filter(models.PracticeResult.user_id==user_id).order_by(models.PracticeResult.created_at.desc()).limit(10).all()
 best_wpm=db.query(func.max(models.PracticeResult.wpm)).filter(models.PracticeResult.user_id==user_id).scalar() or 0
 best_acc=db.query(func.max(models.PracticeResult.accuracy)).filter(models.PracticeResult.user_id==user_id).scalar() or 0
 count=db.query(func.count(models.PracticeResult.id)).filter(models.PracticeResult.user_id==user_id).scalar() or 0
 wins=db.query(func.count(models.BattleResult.id)).filter(models.BattleResult.user_id==user_id,models.BattleResult.won==True).scalar() or 0
 return {'best_wpm':best_wpm,'best_accuracy':best_acc,'practice_count':count,'battles_won':wins,'recent_practice':[{'id':r.id,'wpm':r.wpm,'accuracy':r.accuracy,'errors':r.errors,'time_taken':r.time_taken,'created_at':r.created_at} for r in practices]}
