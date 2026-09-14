from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from application.use_cases import analyzeText, analyzeBatch


app = FastAPI(
  title="Text Analyzer API",
  description="API для анализа текста",
  version="1.0.0"
)


class AnalysisRequest(BaseModel):
  text: str


class BatchRequest(BaseModel):
  texts: list[str]


@app.get("/")
def root():
  return {
    "message": "Text Analyzer API работает"
  }


@app.post("/analyze")
def analyze(request: AnalysisRequest):
  try:
    result = analyzeText(request.text)

    return result

  except ValueError as error:
    raise HTTPException(
      status_code=400,
      detail=str(error)
    )

  except Exception:
    raise HTTPException(
      status_code=500,
      detail="Внутренняя ошибка сервера"
    )


@app.post("/analyze-batch")
def analyze_batch(request: BatchRequest):
  try:
    result = analyzeBatch(request.texts)

    return result

  except ValueError as error:
    raise HTTPException(
      status_code=400,
      detail=str(error)
    )

  except Exception:
    raise HTTPException(
      status_code=500,
      detail="Внутренняя ошибка сервера"
    )
