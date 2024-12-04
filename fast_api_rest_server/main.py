from fastapi import FastAPI
from configs.config import common_config
from endpoints.routers import router as poll_router


app = FastAPI()

app.include_router(poll_router, prefix="/marketing_server", tags=["marketing_server"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host=common_config["api_host_address"], port=common_config["api_host_port"]
    )
