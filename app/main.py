from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from typing import List
from datetime import datetime, timezone
import time
import traceback
import logging

from . import models, schemas
from .database import SessionLocal, engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/app/logs/bookstore.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Simple retry logic for database connection 
for i in range(5):  
    try:
        logger.info(f"Attempting to connect to database... (attempt {i+1}/5)")
        models.Base.metadata.create_all(bind=engine)
        logger.info("Database connection established successfully!")
        break
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        logger.error(f"Full error: {traceback.format_exc()}")
        if i == 4:  # Last attempt
            logger.critical("Failed to connect to database after 5 attempts")
            raise e
        logger.info(f"Retrying in {2**i} seconds...")
        time.sleep(2**i)  # Exponential backoff

app = FastAPI(
    title="Library API",
    description="API for managing library books.",
    version="1.0.0",
)

# Dependency to get DB session
def get_db():
    """Dependency that provides a database session.

    Yields:
        Session: Database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/", response_model=schemas.Book, status_code=201, summary="Add a new book to library")
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Add a new book to the library collection.
    
    Args:
        book (schemas.BookCreate): Object containing book details with keys: 
                                 book_id (6 digits), title (string), author (string).
        db (Session): Database session.

    Raises:
        HTTPException: If book with same book_id already exists.

    Returns:
        schemas.Book: The newly created book record.
    """
    try:
        logger.info(f"Attempting to create book: {book.model_dump()}")
        
        # Check if book already exists
        db_book = db.query(models.Book).filter(models.Book.book_id == book.book_id).first()
        if db_book:
            logger.warning(f"Book with ID {book.book_id} already exists")
            raise HTTPException(status_code=400, detail="Book with this book_id already exists.")
        
        new_book = models.Book(**book.model_dump())
        
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        logger.info(f"Book created successfully: {new_book.book_id}")
        return new_book
    
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error: {e}")
        raise HTTPException(status_code=400, detail="Database constraint violation")
    except OperationalError as e:
        db.rollback()
        logger.error(f"Database operational error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error creating book: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/books/", response_model=List[schemas.Book], summary="Get all books in bookstore")
def get_all_books(db: Session = Depends(get_db)):
    """Retrieves a list of all books in the library collection.
    
    Args:
        db (Session): Database session.
        
    Returns:
        List[schemas.Book]: List of all books in the library.
    """
    try:
        logger.info("Retrieving all books")
        return db.query(models.Book).all()
    except Exception as e:
        logger.error(f"Failed to retrieve books: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve books")

@app.delete("/books/{book_id}", status_code=204, summary="Delete a book")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Deletes a book from the collection by its ID.
    
    Args:
        book_id (int): ID of the book to delete.
        db (Session): Database session.
        
    Raises:
        HTTPException: If book with given ID does not exist.
        
    Returns:
        None
    """
    try:
        logger.info(f"Attempting to delete book with ID: {book_id}")
        db_book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
        if not db_book:
            logger.warning(f"Book with ID {book_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Book not found.")
        
        db.delete(db_book)
        db.commit()
        logger.info(f"Book with ID {book_id} deleted successfully.")
        return
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete book")

@app.patch("/books/{book_id}/borrow", response_model=schemas.Book, summary="Borrow a book")
def borrow_book(book_id: int, borrow_request: schemas.BorrowRequest, db: Session = Depends(get_db)):
    """Marks a book as borrowed by a library card holder.
    
    Args:
        book_id (int): ID of the book to borrow.
        borrow_request (schemas.BorrowRequest): Object containing borrower_card_number (int).
        db (Session): Database session.
        
    Raises:
        HTTPException: If book with given ID does not exist or is already borrowed.
        
    Returns:
        schemas.Book: The updated book record.
    """
    try:
        logger.info(f"Attempting to borrow book with ID: {book_id}")
        db_book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
        if not db_book:
            logger.warning(f"Book with ID {book_id} not found for borrowing")
            raise HTTPException(status_code=404, detail="Book not found.")
        if db_book.is_borrowed:
            logger.warning(f"Book with ID {book_id} is already borrowed")
            raise HTTPException(status_code=400, detail="Book is already borrowed.")
            
        db_book.is_borrowed = True
        db_book.borrower_card_number = borrow_request.borrower_card_number
        db_book.borrowed_date = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(db_book)
        logger.info(f"Book with ID {book_id} borrowed successfully by card number {borrow_request.borrower_card_number}")
        return db_book
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to borrow book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to borrow book")

@app.patch("/books/{book_id}/return", response_model=schemas.Book, summary="Return a book")
def return_book(book_id: int, db: Session = Depends(get_db)):
    """Marks a book as returned and available.
    
    Args:
        book_id (int): ID of the book to return.
        db (Session): Database session.
        
    Raises:
        HTTPException: If book with given ID does not exist or is not currently borrowed.
        
    Returns:
        schemas.Book: The updated book record.
    """
    try:
        logger.info(f"Attempting to return book with ID: {book_id}")
        db_book = db.query(models.Book).filter(models.Book.book_id == book_id).first()
        if not db_book:
            logger.warning(f"Book with ID {book_id} not found for return")
            raise HTTPException(status_code=404, detail="Book not found.")
        if not db_book.is_borrowed:
            logger.warning(f"Book with ID {book_id} is not currently borrowed")
            raise HTTPException(status_code=400, detail="Book is not currently borrowed.")
            
        db_book.is_borrowed = False
        db_book.borrower_card_number = None 
        db_book.borrowed_date = None
        
        db.commit()
        db.refresh(db_book)
        logger.info(f"Book with ID {book_id} returned successfully")
        return db_book
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to return book {book_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to return book")

@app.get("/", summary="Health check")
def health_check():
    """Simple health check endpoint."""
    logger.info("Health check endpoint called")
    return {"status": "healthy", "message": "Library API is running"}
