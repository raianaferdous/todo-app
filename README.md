# To-Do App

A full-stack To-Do application built with Python, Flask, SQLAlchemy, SQLite, HTML, and CSS.

The application allows users to create, edit, complete, delete, search, filter, categorize, prioritize, and sort tasks.

## Features

- Add tasks
- Edit tasks
- Delete tasks
- Mark tasks as completed
- Undo completed tasks
- Search tasks
- Filter by:
  - All
  - Active
  - Completed
  - Category
- Set task categories
- Set task priority
  - High
  - Medium
  - Low
- Set due dates
- Sort tasks by:
  - Newest
  - Oldest
  - Due date
  - Priority
- Task statistics
- Responsive user interface
- SQLite database
- SQLAlchemy ORM

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite
- HTML
- CSS
- Jinja2

## Project Structure

```text
todo-app/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   └── edit.html
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md