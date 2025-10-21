from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models
from .utils import analyze_string

class StringService:
    @staticmethod
    def create_or_conflict(db: Session, value: str) -> models.AnalyzedString:
        existing = db.query(models.AnalyzedString).filter_by(value=value).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="String already exists")

        props = analyze_string(value)
        record = models.AnalyzedString(
            id=props["sha256_hash"],
            value=value,
            length=props["length"],
            is_palindrome=props["is_palindrome"],
            unique_characters=props["unique_characters"],
            word_count=props["word_count"],
            sha256_hash=props["sha256_hash"],
            character_frequency_map=props["character_frequency_map"],
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_by_value_or_404(db: Session, value: str) -> models.AnalyzedString:
        rec = db.query(models.AnalyzedString).filter_by(value=value).first()
        if not rec:
            raise HTTPException(status_code=404, detail="String not found")
        return rec

    @staticmethod
    def delete_by_value_or_404(db: Session, value: str) -> None:
        rec = db.query(models.AnalyzedString).filter_by(value=value).first()
        if not rec:
            raise HTTPException(status_code=404, detail="String not found")
        db.delete(rec)
        db.commit()

    @staticmethod
    def filter_query(db: Session, *, is_palindrome=None, min_length=None, max_length=None, word_count=None, contains_character=None):
        q = db.query(models.AnalyzedString)
        if is_palindrome is not None:
            q = q.filter(models.AnalyzedString.is_palindrome == is_palindrome)
        if min_length is not None:
            q = q.filter(models.AnalyzedString.length >= min_length)
        if max_length is not None:
            q = q.filter(models.AnalyzedString.length <= max_length)
        if word_count is not None:
            q = q.filter(models.AnalyzedString.word_count == word_count)
        if contains_character is not None:
            q = q.filter(models.AnalyzedString.value.like(f"%{contains_character}%"))
        return q.order_by(models.AnalyzedString.created_at.desc())
