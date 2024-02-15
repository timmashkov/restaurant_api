import uvicorn
from api import router as main_router
from fastapi import FastAPI


app = FastAPI(
    title='Ylab Menu Api',
    description='API для работы с Меню, Подменю и Блюдом',
    version='4.0.0',
)

app.include_router(router=main_router, tags=['api'])

if __name__ == '__main__':
    uvicorn.run('runner:app', reload=True)
