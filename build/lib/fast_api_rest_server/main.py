from fastapi import FastAPI
from configs.config import octa_config, common_config
from endpoints.routers import router as poll_router
# from models.dbmodel import Base
# from db.session import engine
# from db.session import engine
# from models.dbmodel import Base


# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(poll_router, prefix="/sqlparser", tags=["sqlparser"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=common_config['api_host_address'], port=common_config['api_host_port'])