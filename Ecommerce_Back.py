from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta

app = FastAPI()

# In-memory DB
# In-memory DB

books_db = {
    1: {"id": 1, "title": "Clean Code", "author": "Robert Martin", "available": True},
    2: {"id": 2, "title": "Introduction to Algorithms", "author": "Cormen", "available": True},
    3: {"id": 3, "title": "Python Crash Course", "author": "Eric Matthes", "available": True},
    4: {"id": 4, "title": "Deep Learning", "author": "Ian Goodfellow", "available": True},
    5: {"id": 5, "title": "Artificial Intelligence", "author": "Stuart Russell", "available": True},
    6: {"id": 6, "title": "Data Structures in Python", "author": "Narasimha Karumanchi", "available": True},
    7: {"id": 7, "title": "Java Programming", "author": "Herbert Schildt", "available": True},
    8: {"id": 8, "title": "Operating Systems", "author": "Galvin", "available": True},
    9: {"id": 9, "title": "Computer Networks", "author": "Kurose", "available": True},
    10: {"id": 10, "title": "DBMS Concepts", "author": "Silberschatz", "available": True},
    11: {"id": 11, "title": "Machine Learning Basics", "author": "Tom Mitchell", "available": True},
    12: {"id": 12, "title": "React JS Guide", "author": "Maximilian", "available": True},
    13: {"id": 13, "title": "Flask Web Dev", "author": "Miguel Grinberg", "available": True},
    14: {"id": 14, "title": "System Design", "author": "Alex Xu", "available": True},
    15: {"id": 15, "title": "Competitive Programming", "author": "Steven Halim", "available": True}
}

users_db = {
    101: {"id": 101, "name": "Kiran"},
    102: {"id": 102, "name": "Rahul"},
    103: {"id": 103, "name": "Anjali"},
    104: {"id": 104, "name": "Sneha"},
    105: {"id": 105, "name": "Arjun"},
    106: {"id": 106, "name": "Priya"},
    107: {"id": 107, "name": "Vikram"},
    108: {"id": 108, "name": "Pooja"},
    109: {"id": 109, "name": "Ravi"},
    110: {"id": 110, "name": "Neha"},
    111: {"id": 111, "name": "Suresh"},
    112: {"id": 112, "name": "Meena"},
    113: {"id": 113, "name": "Karthik"},
    114: {"id": 114, "name": "Divya"},
    115: {"id": 115, "name": "Naveen"}
}

transactions_db = {}

# MODELS
class Book(BaseModel):
    id: int
    title: str
    author: str
    available: bool = True

class User(BaseModel):
    id: int
    name: str

class Issue(BaseModel):
    book_id: int
    user_id: int

# ---------------- BOOK APIs ----------------

@app.post("/books")
def add_book(book: Book):
    if book.id in books_db:
        raise HTTPException(400, "Book exists")
    books_db[book.id] = book.dict()
    return {"msg": "Book added"}

@app.get("/books")
def get_books():
    return list(books_db.values())

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    if book_id not in books_db:
        raise HTTPException(404, "Not found")
    books_db[book_id] = book.dict()
    return {"msg": "Updated"}

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    if book_id not in books_db:
        raise HTTPException(404, "Not found")
    del books_db[book_id]
    return {"msg": "Deleted"}

# ---------------- USER APIs ----------------

@app.post("/users")
def add_user(user: User):
    if user.id in users_db:
        raise HTTPException(400, "User exists")
    users_db[user.id] = user.dict()
    return {"msg": "User added"}

@app.get("/users")
def get_users():
    return list(users_db.values())

# ---------------- ISSUE BOOK ----------------

@app.post("/issue")
def issue_book(data: Issue):
    if data.book_id not in books_db:
        raise HTTPException(404, "Book not found")

    if not books_db[data.book_id]["available"]:
        raise HTTPException(400, "Book already issued")

    issue_date = datetime.now()
    due_date = issue_date + timedelta(days=7)

    transactions_db[data.book_id] = {
        "user_id": data.user_id,
        "issue_date": issue_date,
        "due_date": due_date,
        "returned": False
    }

    books_db[data.book_id]["available"] = False

    return {"msg": "Book issued"}

# ---------------- RETURN BOOK ----------------

@app.put("/return/{book_id}")
def return_book(book_id: int):
    if book_id not in transactions_db:
        raise HTTPException(404, "No record")

    txn = transactions_db[book_id]
    txn["returned"] = True

    return_date = datetime.now()
    due_date = txn["due_date"]

    fine = 0
    if return_date > due_date:
        days = (return_date - due_date).days
        fine = days * 5

    books_db[book_id]["available"] = True

    return {
        "msg": "Returned",
        "fine": fine
    }

# ---------------- TRANSACTIONS ----------------

@app.get("/transactions")
def get_transactions():
    return transactions_db