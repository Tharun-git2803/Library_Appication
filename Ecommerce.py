import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:8000"

st.title("📚 Library Management System")

menu = st.sidebar.selectbox("Menu", [
    "Add Book", "View Books",
    "Add User", "Issue Book",
    "Return Book", "Transactions"
])

# ---------------- ADD BOOK ----------------
if menu == "Add Book":
    st.subheader("Add Book")

    id = st.number_input("Book ID", step=1)
    title = st.text_input("Title")
    author = st.text_input("Author")

    if st.button("Add"):
        res = requests.post(f"{API}/books", json={
            "id": int(id),
            "title": title,
            "author": author,
            "available": True
        })
        st.success(res.json())

# ---------------- VIEW BOOKS ----------------
elif menu == "View Books":
    res = requests.get(f"{API}/books")
    data = res.json()

    if data:
        st.dataframe(pd.DataFrame(data))
    else:
        st.warning("No books")

# ---------------- ADD USER ----------------
elif menu == "Add User":
    st.subheader("Add User")

    id = st.number_input("User ID", step=1)
    name = st.text_input("Name")

    if st.button("Add User"):
        res = requests.post(f"{API}/users", json={
            "id": int(id),
            "name": name
        })
        st.success(res.json())

# ---------------- ISSUE BOOK ----------------
elif menu == "Issue Book":
    st.subheader("Issue Book")

    book_id = st.number_input("Book ID", step=1)
    user_id = st.number_input("User ID", step=1)

    if st.button("Issue"):
        res = requests.post(f"{API}/issue", json={
            "book_id": int(book_id),
            "user_id": int(user_id)
        })
        st.success(res.json())

# ---------------- RETURN BOOK ----------------
elif menu == "Return Book":
    st.subheader("Return Book")

    book_id = st.number_input("Book ID", step=1)

    if st.button("Return"):
        res = requests.put(f"{API}/return/{int(book_id)}")
        st.success(res.json())

# ---------------- TRANSACTIONS ----------------
elif menu == "Transactions":
    res = requests.get(f"{API}/transactions")
    st.write(res.json())
