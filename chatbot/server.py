from fastapi import FastAPI
from .indexing import get_faq_index
from .schemas import Query


index = get_faq_index()
engine = index.as_query_engine()
app = FastAPI()

@app.post('/')
async def index(request: Query):
    result = engine.query(request.question)
    return result
