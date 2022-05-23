# Importing Required Libraries
from fastapi import Depends, FastAPI,Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict
from classifier.model import Model,get_model

# instantiate an app
app = FastAPI()

# Create a templates object that you can re-use later
templates = Jinja2Templates(directory="templates")

# Mount a StaticFiles() instance in a specific path.
app.mount("/static", StaticFiles(directory="static"), name="static")


class SentimentResponse(BaseModel):
    probabilities: Dict[str, float]
    sentiment: str
    confidence: float


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )



@app.post("/predict", response_model=SentimentResponse)
async def predict(request: Request,text: str = Form(...), model: Model = Depends(get_model)):
    sentiment, confidence, probabilities = model.predict(text)

    result = SentimentResponse(
        sentiment=sentiment, confidence=confidence, probabilities=probabilities
    )

    return templates.TemplateResponse("index.html", {"request": request,"result": result})
    
