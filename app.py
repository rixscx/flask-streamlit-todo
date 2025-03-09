import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# Set up page configuration
st.set_page_config(page_title="To-Do App", page_icon="✅", layout="wide")

# Database setup
def init_db():
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            due_date TEXT,
            priority TEXT,
            category TEXT,
            completed INTEGER DEFAULT 0,
            date_added TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Custom CSS for improved UI
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5em;
        font-weight: bold;
        color: #1E90FF;
        text-align: center;
        margin-bottom: 20px;
    }
    .todo-item {
        font-size: 1.2em;
        padding: 10px;
        background-color: #2c2f33;
        color: #ffffff;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .stButton>button {
        background-color: #1E90FF;
        color: white;
        border-radius: 5px;
        padding: 8px 16px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">To-Do List</div>', unsafe_allow_html=True)

# Function to get tasks
def get_tasks():
    conn = sqlite3.connect("todos.db")
    df = pd.read_sql_query("SELECT * FROM todos", conn)
    conn.close()
    return df

# Function to add a task
def add_task(task, due_date, priority, category):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task, due_date, priority, category, date_added) VALUES (?, ?, ?, ?, ?)",
                   (task, due_date, priority, category, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

# Function to delete a task
def delete_task(task_id):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    st.rerun()

# Function to mark task as completed
def toggle_task(task_id, completed):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET completed = ? WHERE id = ?", (completed, task_id))
    conn.commit()
    conn.close()

# Input section with priority and category
with st.form(key='todo_form', clear_on_submit=True):
    new_todo = st.text_input("Add a new task", placeholder="Enter task here...")
    due_date = st.date_input("Due Date")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    category = st.text_input("Category", placeholder="Work, Personal, Study, etc.")
    submit_button = st.form_submit_button(label="Add Task")

if submit_button and new_todo:
    add_task(new_todo, due_date, priority, category)
    st.success(f"Added: {new_todo}")
    st.rerun()

# Display tasks
tasks = get_tasks()
st.subheader("Your Tasks")

if not tasks.empty:
    for index, row in tasks.iterrows():
        col1, col2, col3, col4, col5 = st.columns([0.1, 0.5, 0.1, 0.1, 0.2])
        with col1:
            completed = st.checkbox("", value=bool(row["completed"]), key=f"check_{row['id']}",
                                    on_change=toggle_task, args=(row['id'], not row['completed']))
        with col2:
            st.markdown(f'<div class="todo-item">{row["task"]} - {row["priority"]} Priority ({row["due_date"]})</div>', unsafe_allow_html=True)
        with col3:
            if st.button("Delete", key=f"delete_{row['id']}"):
                delete_task(row['id'])
else:
    st.write("No tasks yet. Add one above!")

# Clear all tasks button
if not tasks.empty and st.button("Clear All Tasks"):
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos")
    conn.commit()
    conn.close()
    st.rerun()
