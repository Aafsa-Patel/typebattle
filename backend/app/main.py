from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from .database import engine,Base
from . import models
from .routes.auth import router as auth_router
from .routes.practice import router as practice_router
from .routes.typing import router as typing_router
from .routes.game import router as game_router
app=FastAPI(title='TypeBattle API',description='Typing practice and battle backend',version='2.0.0')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:5173','http://127.0.0.1:5173'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
Base.metadata.create_all(bind=engine)
app.include_router(auth_router);app.include_router(practice_router);app.include_router(typing_router);app.include_router(game_router)
@app.get('/')
def root(): return {'message':'TypeBattle API is running'}
@app.get('/database-test')
def database_test():
 try:
  with engine.connect() as c:c.execute(text('SELECT 1'))
  return {'status':'success','message':'Database connected successfully!'}
 except Exception as e:return {'status':'error','message':str(e)}
