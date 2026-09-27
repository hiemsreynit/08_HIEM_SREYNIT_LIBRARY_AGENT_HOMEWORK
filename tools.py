from schemas import (
    SearchBookInput,
    CheckAvailabilityInput,
    BorrowBookInput,
    DeleteBookInput,
)

books = [
    {
        "id": 1,
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "available": True,
    },
    {
        "id": 2,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "available": False,
    },
    {
        "id": 3,
        "title": "JavaScript: The Good Parts",
        "author": "Douglas Crockford",
        "available": True,
    },
    {
        "id": 4,
        "title": "Learning React",
        "author": "Alex Banks",
        "available": True,
    },
]


def search_book(input_data: SearchBookInput):
    keyword = input_data.book_name.lower()

    results = []

    for book in books:
        if keyword in book["title"].lower():
            results.append({
                "id": book["id"],
                "title": book["title"],
                "author": book["author"],
            })

    if not results:
        return {
            "success": False,
            "message": f"No books found for '{input_data.book_name}'.",
            "books": [],
        }

    return {
        "success": True,
        "books": results,
    }


def check_availability(input_data: CheckAvailabilityInput):
    for book in books:
        if book["id"] == input_data.book_id:
            return {
                "success": True,
                "book_id": book["id"],
                "title": book["title"],
                "available": book["available"],
            }

    return {
        "success": False,
        "message": f"Book with ID {input_data.book_id} was not found.",
    }


def borrow_book(input_data: BorrowBookInput):
    for book in books:
        if book["id"] == input_data.book_id:

            if not book["available"]:
                return {
                    "success": False,
                    "error_code": "BOOK_UNAVAILABLE",
                    "message": f"'{book['title']}' is currently unavailable.",
                }

            book["available"] = False

            return {
                "success": True,
                "message": f"You successfully borrowed '{book['title']}'.",
            }

    return {
        "success": False,
        "message": f"Book with ID {input_data.book_id} was not found.",
    }


def delete_book(input_data: DeleteBookInput):
    for book in books:
        if book["id"] == input_data.book_id:
            books.remove(book)

            return {
                "success": True,
                "message": f"Book '{book['title']}' was deleted.",
            }

    return {
        "success": False,
        "message": f"Book with ID {input_data.book_id} was not found.",
    }

input_data = SearchBookInput(book_name="Python")
result = search_book(input_data)

print(result)