from pydantic import BaseModel, Field


class SearchBookInput(BaseModel):
    book_name: str = Field(min_length=1)


class CheckAvailabilityInput(BaseModel):
    book_id: int = Field(gt=0)


class BorrowBookInput(BaseModel):
    book_id: int = Field(gt=0)


class DeleteBookInput(BaseModel):
    book_id: int = Field(gt=0)