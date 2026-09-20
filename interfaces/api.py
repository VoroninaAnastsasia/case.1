import time
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from application.use_cases import analyzeText, analyzeBatch


# Логирование запросов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")


app = FastAPI(
  title="Text Analyzer API",
  description="API для анализа текста",
  version="1.0.0"
)


# CORS - чтобы браузер разрешал запросы с других адресов
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)


# Максимальный размер тела запроса в байтах (100 КБ)
MAX_BODY_SIZE = 100_000


@app.middleware("http")
async def logRequests(request: Request, call_next):
  startTime = time.time()

  # Проверяем размер тела запроса
  contentLength = request.headers.get("content-length")
  if contentLength and int(contentLength) > MAX_BODY_SIZE:
    return JSONResponse(
      status_code=413,
      content={"detail": "Тело запроса слишком большое"}
    )

  # Передаём запрос дальше
  response = await call_next(request)

  # Считаем время
  durationMs = (time.time() - startTime) * 1000
  logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({durationMs:.1f} ms)")

  # Добавляем заголовок со временем ответа
  response.headers["X-Process-Time-Ms"] = f"{durationMs:.1f}"

  return response


class AnalysisRequest(BaseModel):
  text: str


class BatchRequest(BaseModel):
  texts: list[str]

class StatsResponse(BaseModel):
  sentence_count: int
  word_count: int
  syllable_count: int
  avg_sentence_length: float
  avg_word_syllables: float


class AnalysisResponse(BaseModel):
  language: int
  flesch_index: float
  flesch_kincaid: float
  interpretation: str
  polarity: str
  subjectivity: float
  lexical_diversity: float
  rare_word_density: float
  stats: StatsResponse

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
  return FileResponse("static/index.html")


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest):
  try:
    result = analyzeText(request.text)

    return result

  except ValueError as error:
    raise HTTPException(status_code=400,
                        detail="Текст не подходит для анализа")

  except Exception:
    raise HTTPException(status_code=500,detail="Внутренняя ошибка сервера")


@app.post("/analyze-batch", response_model=list[AnalysisResponse])
def analyze_batch(request: BatchRequest):
  try:
    result = analyzeBatch(request.texts)

    return result

  except ValueError as error:
    raise HTTPException(status_code=400,
                        detail="Текст не подходит для анализа")

  except Exception:
    raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")
