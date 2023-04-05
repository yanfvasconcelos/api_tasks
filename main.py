from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.controllers import task_controller, user_controller

app = FastAPI()

origins = ['http://localhost:5500',
           'http://127.0.0.1:5500',
           'https://api-tasks-tau.vercel.app']

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

# Rotas e Controllers
app.include_router(task_controller.router,
                   prefix=task_controller.prefix)
app.include_router(user_controller.router,
                   prefix=user_controller.prefix)