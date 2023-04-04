#!/usr/bin/python3

import requests
import sys
import csv


def get_employee_todo_progress(employee_id):
    """
    Retrieves the TODO list progress for a given employee ID from a REST API.

    Args:
        employee_id (int): The ID of the employee.

    Returns:
        A tuple containing:
        - The employee name
        - The number of completed tasks
        - The total number of tasks (completed + non-completed)
        - A list of completed task titles
    """

    # Make API requests to get todos and employee information
    url = "https://jsonplaceholder.typicode.com/todos?userId={}".format
    (employee_id)
    response = requests.get(url)
    todos = response.json()

    # Calculate the number of completed and total tasks
    num_total_tasks = len(todos)
    num_completed_tasks = sum(todo.get('completed', False) for todo in todos)

    # Get the list of completed task titles
    completed_tasks = [todo.get('title', '') for todo in todos if todo.get
                       ('completed', False)]

    url = "https://jsonplaceholder.typicode.com/users/{}".format(employee_id)
    response = requests.get(url)
    employee_json = response.json()

    # Get the employee's name
    employee_name = employee_json.get('name', '')

    # Return the employee's name, number of completed tasks,
    # total number of tasks, and list of completed task titles
    return employee_name, num_completed_tasks, num_total_tasks, completed_tasks


def export_employee_todo_to_csv(employee_id):
    """
    Exports the TODO list progress for a given employee ID to a CSV file.

    Args:
        employee_id (int): The ID of the employee.
    """

    # Call the get_employee_todo_progress function
    # to get the necessary information
    employee_name, num_completed_tasks, num_total_tasks, completed_tasks = \
        get_employee_todo_progress(employee_id)

    # Create a new file with the employee ID as the filename
    filename = "{}.csv".format(employee_id)

    # Use csv.writer to write the data to the new CSV file
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        # Write the header row
        csvwriter.writerow
        (["USER_ID", "USERNAME", "TASK_COMPLETED_STATUS", "TASK_TITLE"])

        # Iterate over the todos and write each one
        # to a new row in the CSV file
        for todo in requests.get("https://jsonplaceholder.typicode.com/todos?userId={}".format(employee_id)).json():
            # Write each todo as a row in the CSV file
            csvwriter.writerow([
                employee_id,
                employee_name,
                "YES" if todo.get("completed") else "NO",
                todo.get("title")
            ])

    # Print a message indicating how many tasks the employee has completed
    print("Employee {} is done with tasks({}/{})".format
          (employee_name, num_completed_tasks, num_total_tasks))

    # Print the list of completed tasks
    for task in completed_tasks:
        print("\t{}".format(task))


if __name__ == "__main__":
    # Get the employee ID from the command line arguments
    # and call the export_employee_todo_to_csv function
    employee_id = int(sys.argv[1])
    export_employee_todo_to_csv(employee_id)
