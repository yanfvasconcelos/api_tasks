from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.controllers import task_controller, user_controller

app = FastAPI()

origins = ['http://localhost:5500', 'http://127.0.0.1:5500', 'http://localhost:5500/public/', 'mongodb://localhost:27023']

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'], expose_headers=['Access-Control-Allow-Origin'])

app.include_router(task_controller.router, prefix=task_controller.prefix)
app.include_router(user_controller.router, prefix=user_controller.prefix)