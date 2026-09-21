import time
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from application.use_cases import analyzeText, analyzeBatch


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('api')


app = FastAPI(
  title='Text Analyzer API',
  description='API для анализа текста',
  version='1.0.0'
)

MAX_BODY_SIZE = 100_000


@app.middleware('http')
async def logRequests(request: Request, call_next):
  """Логирует запросы и считает время ответа."""
  startTime = time.time()

  contentLength = request.headers.get('content-length')
  if contentLength and int(contentLength) > MAX_BODY_SIZE:
    return JSONResponse(
      status_code=413,
      content={'detail': 'Тело запроса слишком большое'}
    )

  response = await call_next(request)

  durationMs = (time.time() - startTime) * 1000
  logger.info(f'{request.method} {request.url.path} -> {response.status_code} ({durationMs:.1f} ms)')
  response.headers['X-Process-Time-Ms'] = f'{durationMs:.1f}'

  return response


class AnalysisRequest(BaseModel):
  """Запрос на анализ одного текста."""
  text: str


class BatchRequest(BaseModel):
  """Запрос на анализ массива текстов."""
  texts: list[str]


class StatsResponse(BaseModel):
  """Статистика текста."""
  sentence_count: int
  word_count: int
  syllable_count: int
  avg_sentence_length: float
  avg_word_syllables: float


class AnalysisResponse(BaseModel):
  """Ответ с результатами анализа."""
  language: str
  flesch_index: float
  flesch_kincaid: float
  interpretation: str
  polarity: str
  subjectivity: float
  lexical_diversity: float
  rare_word_density: float
  stats: StatsResponse


def resultToResponse(result):
  """Преобразует AnalysisResult в словарь для ответа API."""
  return {
    'language': result.language.name.lower(),
    'flesch_index': result.flesch_index,
    'flesch_kincaid': result.flesch_kincaid,
    'interpretation': result.interpretation,
    'polarity': result.polarity.value,
    'subjectivity': result.subjectivity,
    'lexical_diversity': result.lexical_diversity,
    'rare_word_density': result.rare_word_density,
    'stats': {
      'sentence_count': result.stats.sentence_count,
      'word_count': result.stats.word_count,
      'syllable_count': result.stats.syllable_count,
      'avg_sentence_length': result.stats.avg_sentence_length,
      'avg_word_syllables': result.stats.avg_word_syllables
    }
  }


app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/')
def root():
  """Отдаёт главную HTML-страницу."""
  return FileResponse('static/index.html')


@app.post('/analyze', response_model=AnalysisResponse)
def analyze(request: AnalysisRequest):
  """Анализирует один текст."""
  try:
    result = analyzeText(request.text)
    return resultToResponse(result)
  except ValueError as error:
    raise HTTPException(status_code=400, detail=str(error))
  except Exception:
    raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')


@app.post('/analyze-batch', response_model=list[AnalysisResponse])
def analyze_batch(request: BatchRequest):
  """Анализирует массив текстов."""
  try:
    results = analyzeBatch(request.texts)
    return [resultToResponse(r) for r in results]
  except ValueError as error:
    raise HTTPException(status_code=400, detail=str(error))
  except Exception:
    raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')
