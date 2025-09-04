import pytest
import requests
import random
import os

BASE_URL = os.environ.get("BASE_URL", "http://app:8000")

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Clear all books before and after tests."""
    clear_all_books()
    yield
    clear_all_books()

def clear_all_books():
    """Helper function to clear all books from the database."""
    response = requests.get(f"{BASE_URL}/books/")
    if response.status_code == 200:
        for book in response.json():
            requests.delete(f"{BASE_URL}/books/{book['book_id']}")

def create_book_payload():
    """Helper function to create a unique book payload."""
    return {
        "book_id": random.randint(100000, 999999),
        "title": "Test Book",
        "author": "Test Author"
    }

def test_create_book():
    """Test creating a new book."""
    payload = create_book_payload()
    response = requests.post(f"{BASE_URL}/books/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["book_id"] == payload["book_id"]
    assert data["title"] == payload["title"]
    assert data["author"] == payload["author"]
    assert not data["is_borrowed"]

def test_create_existing_book():
    """Test creating a book that already exists."""
    payload = create_book_payload()
    requests.post(f"{BASE_URL}/books/", json=payload)
    response = requests.post(f"{BASE_URL}/books/", json=payload)
    assert response.status_code == 400

def test_get_all_books():
    """Test getting all books."""
    payload = create_book_payload()
    requests.post(f"{BASE_URL}/books/", json=payload)
    response = requests.get(f"{BASE_URL}/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1

def test_delete_book():
    """Test deleting a book."""
    payload = create_book_payload()
    post_response = requests.post(f"{BASE_URL}/books/", json=payload)
    book_id = post_response.json()["book_id"]
    
    delete_response = requests.delete(f"{BASE_URL}/books/{book_id}")
    assert delete_response.status_code == 204
    
    get_response = requests.get(f"{BASE_URL}/books/")
    assert not any(book['book_id'] == book_id for book in get_response.json())

def test_delete_non_existent_book():
    """Test deleting a non-existent book."""
    response = requests.delete(f"{BASE_URL}/books/{random.randint(100000, 999999)}")
    assert response.status_code == 404

def test_borrow_book():
    """Test borrowing a book."""
    payload = create_book_payload()
    post_response = requests.post(f"{BASE_URL}/books/", json=payload)
    book_id = post_response.json()["book_id"]
    
    borrow_payload = {"borrower_card_number": random.randint(100000, 999999)}
    borrow_response = requests.patch(f"{BASE_URL}/books/{book_id}/borrow", json=borrow_payload)
    assert borrow_response.status_code == 200
    data = borrow_response.json()
    assert data["is_borrowed"]
    assert data["borrower_card_number"] == borrow_payload["borrower_card_number"]

def test_borrow_non_existent_book():
    """Test borrowing a non-existent book."""
    borrow_payload = {"borrower_card_number": random.randint(100000, 999999)}
    response = requests.patch(f"{BASE_URL}/books/{random.randint(100000, 999999)}/borrow", json=borrow_payload)
    assert response.status_code == 404

def test_borrow_already_borrowed_book():
    """Test borrowing a book that is already borrowed."""
    payload = create_book_payload()
    post_response = requests.post(f"{BASE_URL}/books/", json=payload)
    book_id = post_response.json()["book_id"]
    
    borrow_payload = {"borrower_card_number": random.randint(100000, 999999)}
    requests.patch(f"{BASE_URL}/books/{book_id}/borrow", json=borrow_payload)
    
    error_response = requests.patch(f"{BASE_URL}/books/{book_id}/borrow", json=borrow_payload)
    assert error_response.status_code == 400

def test_return_book():
    """Test returning a book."""
    payload = create_book_payload()
    post_response = requests.post(f"{BASE_URL}/books/", json=payload)
    book_id = post_response.json()["book_id"]
    
    borrow_payload = {"borrower_card_number": random.randint(100000, 999999)}
    requests.patch(f"{BASE_URL}/books/{book_id}/borrow", json=borrow_payload)
    
    return_response = requests.patch(f"{BASE_URL}/books/{book_id}/return")
    assert return_response.status_code == 200
    data = return_response.json()
    assert not data["is_borrowed"]
    assert data["borrower_card_number"] is None

def test_return_non_existent_book():
    """Test returning a non-existent book."""
    response = requests.patch(f"{BASE_URL}/books/{random.randint(100000, 999999)}/return")
    assert response.status_code == 404

def test_return_not_borrowed_book():
    """Test returning a book that is not borrowed."""
    payload = create_book_payload()
    post_response = requests.post(f"{BASE_URL}/books/", json=payload)
    book_id = post_response.json()["book_id"]
    
    error_response = requests.patch(f"{BASE_URL}/books/{book_id}/return")
    assert error_response.status_code == 400
