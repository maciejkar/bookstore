from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# --- Base Schemas --- #
class BookBase(BaseModel):
    book_id: int = Field(..., ge=100000, le=999999, description="The unique 6-digit book_id.")
    title: str
    author: str

# --- Schemas for Creating/Updating --- #
class BookCreate(BookBase):
    pass

class BorrowRequest(BaseModel):
    borrower_card_number: int = Field(..., ge=100000, le=999999, description="The 6-digit library card number of the borrower.")

# --- Schemas for API Responses --- #
class Book(BookBase):
    # book_id: int
    is_borrowed: bool
    borrowed_date: Optional[datetime] = None
    borrower_card_number: Optional[int] = None

    class Config:
        from_attributes = True
