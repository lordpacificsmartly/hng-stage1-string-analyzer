from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON, Index
from sqlalchemy.sql import func
from .db import Base


class AnalyzedString(Base):
    __tablename__ = "analyzed_strings"

    id = Column(String(64), primary_key=True, index=True)  # SHA-256
    value = Column(String, unique=True, nullable=False, index=True)

    length = Column(Integer, nullable=False)
    is_palindrome = Column(Boolean, nullable=False)
    unique_characters = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)
    sha256_hash = Column(String(64), nullable=False)
    character_frequency_map = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("ix_len", "length"),
        Index("ix_pal", "is_palindrome"),
        Index("ix_wc", "word_count"),
    )
