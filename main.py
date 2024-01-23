from ai_devs_api_client import get_auth_token, post_response
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


api = F'127.0.0.1:45324/ownapi'
token = get_auth_token('ownapi')
post_response(api, 