# Bookstore API

This is a simple API for a library information system. The API is used by library employees to track and update the status of books owned by the library.

## Features

*   Add a new book
*   Delete a book
*   Get a list of all books
*   Update book status: borrowed / available

## Tech Stack

*   Python
*   FastAPI
*   PostgreSQL
*   Docker

## Project Structure

```
.
├── app/
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database session management
│   ├── models.py         # SQLAlchemy models
│   └── schemas.py        # Pydantic schemas
├── tests/
│   └── test_api.py       # API tests
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
└── example_usage.py      # Script to demonstrate API usage
```

## Getting Started

### With Docker (Recommended)

1.  **Create a `.env` file** in the root directory of the project with the following content:

    ```
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_DB=bookstore
    DATABASE_URL=postgresql://user:password@db:5432/bookstore
    ```

2.  **Run the application** using Docker Compose:

    ```bash
    docker compose up --build
    ```

The API will be available at `http://localhost:8000`.

### Without Docker

1.  **Install PostgreSQL** and create a database.

2.  **Create a `.env` file** with your database credentials:

    ```
    POSTGRES_USER=<your_postgres_user>
    POSTGRES_PASSWORD=<your_postgres_password>
    POSTGRES_DB=<your_database_name>
    DATABASE_URL=postgresql://<your_postgres_user>:<your_postgres_password>@localhost:5432/<your_database_name>
    ```

3.  **Install Python dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application**:

    ```bash
    uvicorn app.main:app --reload
    ```

The API will be available at `http://localhost:8000`.

## Running Tests

There are two ways to run the tests:

### With Docker Compose (Recommended)

This is the easiest and recommended way to run the tests, as it ensures the testing environment is identical to the production environment.

1.  Make sure the application is running via `docker compose up`.
2.  In a separate terminal, run the following command:

    ```bash
    docker compose run test
    ```

### Locally

You can also run the tests on your local machine.

1.  Make sure the application is running locally (see [Without Docker](#without-docker)).
2.  Set the `BASE_URL` environment variable to point to your local server:

    ```bash
    export BASE_URL="http://localhost:8000"
    ```

3.  Run pytest:

    ```bash
    pytest
    ```

## API Endpoints

### `POST /books/`

Add a new book to the library collection.

*   **Request Body:**

    ```json
    {
      "book_id": 123456,
      "title": "The Hitchhiker's Guide to the Galaxy",
      "author": "Douglas Adams"
    }
    ```

*   **Response (201 Created):**

    ```json
    {
      "book_id": 123456,
      "title": "The Hitchhiker's Guide to the Galaxy",
      "author": "Douglas Adams",
      "is_borrowed": false,
      "borrowed_date": null,
      "borrower_card_number": null
    }
    ```

### `GET /books/`

Retrieves a list of all books in the library.

*   **Response (200 OK):**

    ```json
    [
      {
        "book_id": 123456,
        "title": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "is_borrowed": false,
        "borrowed_date": null,
        "borrower_card_number": null
      }
    ]
    ```

### `DELETE /books/{book_id}`

Deletes a book from the collection by its ID.

*   **Response (204 No Content)**

### `PATCH /books/{book_id}/borrow`

Marks a book as borrowed by a library card holder.

*   **Request Body:**

    ```json
    {
      "borrower_card_number": 111222
    }
    ```

*   **Response (200 OK):**

    ```json
    {
      "book_id": 123456,
      "title": "The Hitchhiker's Guide to the Galaxy",
      "author": "Douglas Adams",
      "is_borrowed": true,
      "borrowed_date": "2025-09-04T10:00:00.000Z",
      "borrower_card_number": 111222
    }
    ```

### `PATCH /books/{book_id}/return`

Marks a book as returned and available.

*   **Response (200 OK):**

    ```json
    {
      "book_id": 123456,
      "title": "The Hitchhiker's Guide to the Galaxy",
      "author": "Douglas Adams",
      "is_borrowed": false,
      "borrowed_date": null,
      "borrower_card_number": null
    }
    ```

## Example Usage

The `example_usage.py` script demonstrates how to interact with the API.

To run the script, first ensure the API is running. Then, execute the following command:

```bash
python example_usage.py
```

The script will:
1.  Add new books.
2.  Borrow a book.
3.  Return a book.
4.  Delete a book.