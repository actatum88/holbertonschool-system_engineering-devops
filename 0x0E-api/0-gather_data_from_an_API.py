#!/usr/bin/python3

import requests
import sys


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
    url = "https://jsonplaceholder.typicode.com/todos?userId={}".format(employee_id)
    response = requests.get(url)
    todos = response.json()
    num_total_tasks = len(todos)
    num_completed_tasks = sum(todo.get('completed', False) for todo in todos)
    completed_tasks = [todo.get('title', '')
                       for todo in todos if todo.get('completed', False)]

    url = "https://jsonplaceholder.typicode.com/users/{}".format(employee_id)
    response = requests.get(url)
    employee_json = response.json()
    employee_name = employee_json.get('name', '')

    return employee_name, num_completed_tasks, num_total_tasks, completed_tasks


if __name__ == '__main__':
    employee_id = int(sys.argv[1])
    employee_name, num_completed_tasks, num_total_tasks, completed_tasks = get_employee_todo_progress(employee_id)
    print("Employee {} is done with tasks({}/{}):".format
          (employee_name, num_completed_tasks, num_total_tasks))
    for task in completed_tasks:
        print("\t{}".format(task))
