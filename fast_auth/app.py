from fastapi import FastAPI

from fast_auth.views import router as auth_routes
 
app = FastAPI()

app.include_router(auth_routes)

