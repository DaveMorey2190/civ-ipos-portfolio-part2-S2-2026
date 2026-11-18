from src.task import Task
from dateutil.parser import parse, ParserError
from datetime import datetime, date
from src.file_handler import save_tasks


def notify_due_tasks(tasks):
    """
    Check tasks and notify the user about tasks
    that are due today or overdue.
    """

    today = date.today()

    for task in tasks:

        # Access attributes from the Task object
        due_date = task.due_date

        if not due_date:
            continue

        try:
            parsed_date = datetime.strptime(
                str(due_date), "%d-%m-%Y"
            ).date()

            if parsed_date == today:
                print(
                    f"\nNOTIFICATION: Task due today: {task.title}"
                )

            elif parsed_date < today:
                print(
                    f"\nREMINDER: Task overdue: {task.title}"
                )

        except ValueError:
            print(f"Invalid due date for task: {task.title}")


def add_task(tasks, title, description, due_date):
    """
    Add a new task to the task list.

    Args:
        tasks (list): The list of existing Task objects.
        title (str): The title of the new task.
        description (str): A brief description of the task.
        due_date (str): The due date of the task in 'DD-MM-YYYY' format.

    Returns:
        bool: True if the task is added successfully, False otherwise.

    Raises:
        ValueError: If the due date is not in the correct format.

    Side Effects:
        - Saves the updated task list to a file using `save_tasks`.
    """
    # Prevent duplicate tasks
    if any(task.title == title for task in tasks):
        print("Error: A task with this title already exists.")
        return False

    # Validate the due date using dateutil.
    try:
        # Parse the supplied date, interpreting the day first.
        parsed_date = parse(
            due_date,
            dayfirst=True,
            yearfirst=False,
            fuzzy=False
        ).date()

        # Ensure the input uses the required DD-MM-YYYY format.
        if parsed_date.strftime("%d-%m-%Y") != due_date:
            print("Error: Invalid date format. Use DD-MM-YYYY.")
            return False

        # Reject past dates.
        if parsed_date < date.today():
            print("Error: The due date cannot be in the past.")
            return False

    except (ParserError, ValueError, OverflowError):
        print("Error: Invalid date format. Use DD-MM-YYYY.")
        return False

    tasks.append(Task(title, description, due_date))
    save_tasks(tasks)
    return True


def delete_task(tasks, title):
    """
    Delete a task from the task list based on its title.

    Args:
        tasks (list): The list of existing Task objects.
        title (str): The title of the task to be deleted.

    Returns:
        bool: True if the task was found and deleted, False otherwise.

    Side Effects:
        - Saves the updated task list to a file using `save_tasks`.
    """
    for task in tasks:
        if task.title == title:
            tasks.remove(task)
            save_tasks(tasks)
            return True
    return False


def list_tasks(tasks, status=None):
    """
    Display tasks in the task list, optionally filtered by status.

    Args:
        tasks (list): The list of existing Task objects.
        status (str, optional): The status to filter tasks
        by (e.g., "pending" or "completed").

    Returns:
        None

    Side Effects:
        - Prints the list of tasks to the console.
    """
    if not status:
        # If status is not set
        filtered = tasks
    else:
        # Filter tasks based on their status
        filtered = []
        for task in tasks:
            if task.status == status:
                filtered.append(task)

    if not filtered:
        print("No tasks found.")
        return
    for task in filtered:
        print(
            f"{task.title} | {task.description} | "
            f"Due: {task.due_date} | Status: {task.status}"
        )


def filter_tasks_by_status(tasks, status):
    """
    Filter tasks by their status.

    Args:
        tasks (list): The list of existing Task objects.
        status (str): The status to filter tasks by (e.g., "pending" or "completed").

    Returns:
        list: A list of Task objects that match the specified status.
    """
    return [task for task in tasks if task.status == status]
