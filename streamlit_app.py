import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:5000"
GITHUB_REPO_URL = "https://github.com/YOUR_USERNAME/flask-streamlit-todo"

st.set_page_config(page_title="To-Do App", page_icon="✅", layout="centered")

st.markdown("<h1 style='text-align: center;'>📋 Streamlit To-Do App</h1>", unsafe_allow_html=True)

# GitHub Fork Button
st.markdown(
    f'<a href="{GITHUB_REPO_URL}" target="_blank">'
    '<button style="background-color:#4CAF50;color:white;padding:10px 20px;'
    'border:none;border-radius:5px;cursor:pointer;font-size:16px;">'
    '⭐ Fork on GitHub</button></a>',
    unsafe_allow_html=True,
)

# Task Input
task_input = st.text_input("Add a new task")
if st.button("Add Task"):
    if task_input:
        response = requests.post(f"{BASE_URL}/tasks", json={"task": task_input})
        if response.status_code == 201:
            st.success("Task added successfully!")
            st.experimental_rerun()
        else:
            st.error("Error adding task")

# Display Tasks
st.subheader("Your Tasks")
tasks = requests.get(f"{BASE_URL}/tasks").json()
for task in tasks:
    col1, col2 = st.columns([4, 1])
    col1.write(task["task"])
    if col2.button("❌", key=task["id"]):
        requests.delete(f"{BASE_URL}/tasks/{task['id']}")
        st.experimental_rerun()
