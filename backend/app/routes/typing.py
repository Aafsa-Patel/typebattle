from fastapi import APIRouter
import random
router=APIRouter(prefix='/api/typing',tags=['Typing'])
PASSAGES=['The quick brown fox jumps over the lazy dog.','Practice makes progress and regular typing improves your speed.','Programming becomes easier when you practice consistently.','Type accurately first and gradually increase your speed.','Fast and accurate typing is a useful skill for everyone.']
@router.get('/passage')
def get_typing_passage():
 p=random.choice(PASSAGES);return {'passage':p,'length':len(p)}
