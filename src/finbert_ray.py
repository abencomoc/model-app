from ray import serve
from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel, Field

app = FastAPI()

# Create a Pydantic model for request validation
class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=512, description="Text to analyze for sentiment") # BERT models have a limit of 512 tokens

# Create a Pydantic model for response validation
class SentimentResponse(BaseModel):
    sentiment: str
    score: float

@serve.deployment
@serve.ingress(app)
class Finbert:
    def __init__(self):
        # Load model
        self.model = pipeline("text-classification", model="ProsusAI/finbert")

    @app.post("/", response_model=SentimentResponse)
    def analyze(self, request: SentimentRequest):
        # Run inference
        model_output = self.model(request.text)

        # Post-process output
        result = model_output[0]

        return SentimentResponse(
            sentiment=result["label"],
            score=result["score"]
        )

finbertapp = Finbert.bind()
