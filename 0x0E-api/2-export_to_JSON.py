import requests
import sys
import json


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
    # create URL for getting the todos for the given employee_id
    url = "https://jsonplaceholder.typicode.com/todos?userId={}".format(employee_id)
    response = requests.get(url)
    # get the todos as a json object
    todos = response.json()
    # get the total number of tasks
    num_total_tasks = len(todos)
    # count the number of completed tasks
    num_completed_tasks = sum(todo.get('completed', False) for todo in todos)
    # create a list of completed task titles
    completed_tasks = [todo.get('title', '') for todo in todos if todo.get('completed', False)]

    # create URL for getting the user details for the given employee_id
    url = "https://jsonplaceholder.typicode.com/users/{}".format(employee_id)
    response = requests.get(url)
    # get the user details as a json object
    employee_json = response.json()
    # get the employee name
    employee_name = employee_json.get('name', '')

    # return a tuple containing the employee name, the number of completed tasks,
    # the total number of tasks, and the list of completed task titles
    return employee_name, num_completed_tasks, num_total_tasks, completed_tasks


def export_employee_todo_to_json(employee_id):
    """
    Exports the TODO list progress for a given employee ID to a JSON file.

    Args:
        employee_id (int): The ID of the employee.
    """
    # get the employee name, number of completed tasks, total number of tasks,
    # and completed task titles using the get_employee_todo_progress function
    employee_name, num_completed_tasks, num_total_tasks, completed_tasks = get_employee_todo_progress(employee_id)

    # create the dictionary to be exported to the json file
    todos_dict = {}
    todos_dict["USER_ID"] = []
    # for each todo, add a dictionary to the list with the task title,
    # completed status, and employee name
    for todo in requests.get("https://jsonplaceholder.typicode.com/todos?userId={}".format(employee_id)).json():
        todos_dict["USER_ID"].append({
            "task": todo.get("title"),
            "completed": "YES" if todo.get("completed") else "NO",
            "username": employee_name
        })

    # create the filename as USER_ID.json
    filename = "{}.json".format(employee_id)
    # write the todos_dict to the json file
    with open(filename, 'w') as json_file:
        json.dump(todos_dict, json_file)

    # print a message indicating the employee's progress and a list of completed tasks
    print("Employee {} is done with tasks({}/{})".format(employee_name, num_completed_tasks, num_total_tasks))
    for task in completed_tasks:
        print("\t{}".format(task))


if __name__ == "__main__":
    employee_id = int(sys.argv[1])
    export_employee_todo_to_json(employee_id)
