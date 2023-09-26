from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
async def root(request: Request):
    client_host = request.client.host
    return {"message": client_host}
