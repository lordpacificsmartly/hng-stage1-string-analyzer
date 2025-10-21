from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
from .db import Base, engine, get_db
from . import models, schemas
from .service import StringService
from .nlp import parse_nl_query

Base.metadata.create_all(bind=engine)

app = FastAPI(title="String Analyzer Service", version="1.0.0")

def to_schema(rec: models.AnalyzedString) -> schemas.StringResponse:
    return schemas.StringResponse(
        id=rec.id,
        value=rec.value,
        properties=schemas.Properties(
            length=rec.length,
            is_palindrome=rec.is_palindrome,
            unique_characters=rec.unique_characters,
            word_count=rec.word_count,
            sha256_hash=rec.sha256_hash,
            character_frequency_map=rec.character_frequency_map,
        ),
        created_at=rec.created_at,
    )

@app.post("/strings", response_model=schemas.StringResponse, status_code=201)
def create_string(payload: schemas.AnalyzeRequest, db: Session = Depends(get_db)):
    rec = StringService.create_or_conflict(db, payload.value)
    return to_schema(rec)

@app.get("/strings", response_model=schemas.StringsListResponse)
def list_strings(
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None, ge=0),
    max_length: Optional[int] = Query(None, ge=0),
    word_count: Optional[int] = Query(None, ge=0),
    contains_character: Optional[str] = Query(None, min_length=1, max_length=1),
    db: Session = Depends(get_db),
):
    q = StringService.filter_query(db, is_palindrome=is_palindrome,
                                   min_length=min_length,
                                   max_length=max_length,
                                   word_count=word_count,
                                   contains_character=contains_character)
    rows = q.all()
    data = [to_schema(r) for r in rows]
    return schemas.StringsListResponse(
        data=data, count=len(data),
        filters_applied={k: v for k, v in {
            "is_palindrome": is_palindrome,
            "min_length": min_length,
            "max_length": max_length,
            "word_count": word_count,
            "contains_character": contains_character,
        }.items() if v is not None}
    )

@app.get("/strings/filter-by-natural-language", response_model=schemas.NaturalLanguageResponse)
def filter_by_nl(query: str, db: Session = Depends(get_db)):
    try:
        filters = parse_nl_query(query)
    except ValueError:
        raise HTTPException(status_code=400, detail="Unable to parse natural language query")
    q = StringService.filter_query(db, **filters)
    rows = q.all()
    data = [to_schema(r) for r in rows]
    return schemas.NaturalLanguageResponse(
        data=data, count=len(data),
        interpreted_query={"original": query, "parsed_filters": filters}
    )

@app.get("/strings/{string_value}", response_model=schemas.StringResponse)
def get_string(string_value: str, db: Session = Depends(get_db)):
    rec = StringService.get_by_value_or_404(db, string_value)
    return to_schema(rec)

@app.delete("/strings/{string_value}", status_code=204)
def delete_string(string_value: str, db: Session = Depends(get_db)):
    StringService.delete_by_value_or_404(db, string_value)
    return JSONResponse(status_code=204, content=None)
