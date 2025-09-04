import requests
import json
import random

BASE_URL = "http://localhost:8000"

def clear_all_books():
    """Helper function to clear all books from the database."""
    response = requests.get(f"{BASE_URL}/books/")
    for book in response.json():
        requests.delete(f"{BASE_URL}/books/{book['book_id']}")
        print(f"Deleted book with serial number {book['book_id']}")

    print(f"All books deleted. Current books in library:{requests.get(f'{BASE_URL}/books/').json()}")

def print_response(response):
    """Helper function to print the status code and JSON response."""
    print(f"Status Code: {response.status_code}")
    try:
        print("Response JSON:")
        if response.content:
            print(json.dumps(response.json(), indent=4))
    except json.JSONDecodeError:
        print("Response content (not JSON):")
        print(response.text)
    print("-" * 20)


# Clear all books at the start (for clean testing)
clear_all_books() # Uncomment this line if you want to start with an empty database each time

# 1. Add a new book
print("--- 1. Adding a new book ---")
new_book_data = {
    "book_id": random.randint(100000, 999999),
    "title": "The Lord of the Rings",
    "author": "J.R.R. Tolkien"
}
response = requests.post(f"{BASE_URL}/books/", json=new_book_data)
print_response(response)
added_book_serial = new_book_data['book_id']

# Add another book
new_book_data_2 = {
    "book_id": random.randint(100000, 999999),
    "title": "1984",
    "author": "George Orwell"
}
response = requests.post(f"{BASE_URL}/books/", json=new_book_data_2)
print_response(response)


# 2. Get all books
print("--- 2. Getting all books ---")
response = requests.get(f"{BASE_URL}/books/")
print_response(response)

# 3. Borrow a book
print(f"--- 3. Borrowing book with serial number {added_book_serial} ---")
borrow_data = {"borrower_card_number": 111222}
response = requests.patch(f"{BASE_URL}/books/{added_book_serial}/borrow", json=borrow_data)
print_response(response)

# 4. Get all books to see the change
print("--- 4. Getting all books to see the updated status ---")
response = requests.get(f"{BASE_URL}/books/")
print_response(response)

# 5. Return a book
print(f"--- 5. Returning book with serial number {added_book_serial} ---")
response = requests.patch(f"{BASE_URL}/books/{added_book_serial}/return")
print_response(response)

# 6. Get all books to see the final status
print("--- 6. Getting all books to see the final status ---")
response = requests.get(f"{BASE_URL}/books/")
print_response(response)

# 7. Delete a book
print(f"--- 7. Deleting book with serial number {added_book_serial} ---")
response = requests.delete(f"{BASE_URL}/books/{added_book_serial}")
print_response(response)

# 8. Get all books to confirm deletion
print("--- 8. Getting all books to confirm deletion ---")
response = requests.get(f"{BASE_URL}/books/")
print_response(response)
