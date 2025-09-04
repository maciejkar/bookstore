from sqlalchemy import Column, Integer, String, Boolean, DateTime, CheckConstraint
from .database import Base

class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    is_borrowed = Column(Boolean, default=False, nullable=False)
    borrowed_date = Column(DateTime, nullable=True)
    borrower_card_number = Column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint('book_id >= 100000 AND book_id <= 999999', name='book_id_6_digits'),
        CheckConstraint('borrower_card_number >= 100000 AND borrower_card_number <= 999999', name='borrower_card_number_6_digits'),
    )
