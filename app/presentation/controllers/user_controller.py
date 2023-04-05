from fastapi import APIRouter

router = APIRouter()
prefix = '/usuarios'

print('user controller ok')
@router.get('/')
def todos_usuarios():
    return []