from fastapi import FastAPI
from services import router


app = FastAPI()

if __name__ == "__main__":
    import uvicorn
    app.include_router(router=router)

    uvicorn.run(app=app, host='0.0.0.0', port=8000)