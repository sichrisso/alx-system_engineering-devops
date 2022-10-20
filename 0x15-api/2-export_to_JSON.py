#!/usr/bin/python3
''' task 2 module'''


if __name__ == '__main__':
    import json
    import requests
    from sys import argv

    emp_id = argv[1]
    file_name = emp_id + '.json'
    total_todos = 0
    done_todos = 0
    done_todos_titles = []

    res = requests.get(
                   'https://jsonplaceholder.typicode.com/users/' +
                   emp_id)
    emp_username = res.json().get('username', 'user name not found')

    res = requests.get(
                   'https://jsonplaceholder.typicode.com/users/' +
                   emp_id + '/todos')
    emp_todos = res.json()

    records = {str(emp_id): []}

    for todo in emp_todos:
        total_todos += 1
        records[str(emp_id)].append({"task": todo.get('title'),
                                     "completed": todo.get('completed'),
                                     "username": emp_username
                                     })

    with open(file_name, 'w') as jsonfile:
        json.dump(records, jsonfile)
