from fastapi import FastAPI
app= FastAPI(title="Portfolio api", version='1.0.0')


@app.get('/')
async def root():
    return {"message":"Hello world"}
 