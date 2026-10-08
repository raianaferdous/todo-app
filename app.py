from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Task database model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    # Due date
    due_date = db.Column(db.Date, nullable=True)

    # Priority
    priority = db.Column(db.String(20), default="Medium")

    # Category
    category = db.Column(db.String(50), default="Personal")


# Home page
@app.route("/")
def home():

    # Get filters
    current_filter = request.args.get("filter", "all")
    search_query = request.args.get("search", "")
    current_category = request.args.get("category", "all")

    # Get sorting option
    current_sort = request.args.get("sort", "newest")

    # Get all tasks
    all_tasks = Task.query.all()

    # Count statistics
    total_tasks = len(all_tasks)

    completed_tasks = len(
        [task for task in all_tasks if task.completed]
    )

    remaining_tasks = total_tasks - completed_tasks

    # Start with all tasks
    tasks = all_tasks

    # Apply completion filter
    if current_filter == "active":

        tasks = [
            task for task in tasks
            if not task.completed
        ]

    elif current_filter == "completed":

        tasks = [
            task for task in tasks
            if task.completed
        ]

    # Apply category filter
    if current_category != "all":

        tasks = [
            task for task in tasks
            if task.category == current_category
        ]

    # Apply search
    if search_query:

        tasks = [
            task for task in tasks
            if search_query.lower() in task.title.lower()
        ]

    # Apply sorting
    if current_sort == "due_date":

        # Tasks without a due date go to the end
        tasks = sorted(
            tasks,
            key=lambda task: (
                task.due_date is None,
                task.due_date
                if task.due_date
                else datetime.max.date()
            )
        )

    elif current_sort == "priority":

        priority_order = {
            "High": 1,
            "Medium": 2,
            "Low": 3
        }

        tasks = sorted(
            tasks,
            key=lambda task: priority_order.get(
                task.priority,
                2
            )
        )

    elif current_sort == "oldest":

        tasks = sorted(
            tasks,
            key=lambda task: task.id
        )

    else:
        # Default: newest first
        tasks = sorted(
            tasks,
            key=lambda task: task.id,
            reverse=True
        )

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        remaining_tasks=remaining_tasks,
        current_filter=current_filter,
        search_query=search_query,
        current_category=current_category,
        current_sort=current_sort
    )


# Add task
@app.route("/add", methods=["POST"])
def add_task():

    task_title = request.form["task"]

    due_date_text = request.form.get("due_date")

    priority = request.form.get(
        "priority",
        "Medium"
    )

    category = request.form.get(
        "category",
        "Personal"
    )

    due_date = None

    if due_date_text:

        due_date = datetime.strptime(
            due_date_text,
            "%Y-%m-%d"
        ).date()

    new_task = Task(
        title=task_title,
        due_date=due_date,
        priority=priority,
        category=category
    )

    db.session.add(new_task)
    db.session.commit()

    return redirect("/")


# Complete / undo task
@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):

    task = Task.query.get_or_404(task_id)

    task.completed = not task.completed

    db.session.commit()

    return redirect("/")


# Delete task
@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):

    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return redirect("/")


# Edit task page
@app.route("/edit/<int:task_id>")
def edit_task(task_id):

    task = Task.query.get_or_404(task_id)

    return render_template(
        "edit.html",
        task=task
    )


# Update task
@app.route("/edit/<int:task_id>", methods=["POST"])
def update_task(task_id):

    task = Task.query.get_or_404(task_id)

    task.title = request.form["task"]

    due_date_text = request.form.get("due_date")

    task.priority = request.form.get(
        "priority",
        "Medium"
    )

    task.category = request.form.get(
        "category",
        "Personal"
    )

    if due_date_text:

        task.due_date = datetime.strptime(
            due_date_text,
            "%Y-%m-%d"
        ).date()

    else:

        task.due_date = None

    db.session.commit()

    return redirect("/")


# Run application
if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)