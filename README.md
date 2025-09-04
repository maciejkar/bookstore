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

## Prerequisites

*   Docker
*   Docker Compose

## Getting Started

1.  **Create a `.env` file** in the root directory of the project with the following content:

    ```
    POSTGRES_USER=user
    POSTGRES_PASSWORD=password
    POSTGRES_DB=bookstore
    DATABASE_URL=postgresql://user:password@db:5432/bookstore
    ```

2.  **Run the application** using Docker Compose:

    ```bash
    docker-compose up --build
    ```

The API will be available at `http://localhost:8000`.

## API Endpoints

*   `POST /books/` - Add a new book
*   `GET /books/` - Get a list of all books
*   `DELETE /books/{book_id}` - Delete a book by its serial number
*   `PUT /books/{book_id}/borrow` - Borrow a book
*   `PUT /books/{book_id}/return` - Return a book
