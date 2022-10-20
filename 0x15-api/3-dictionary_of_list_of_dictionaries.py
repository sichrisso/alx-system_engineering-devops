#!/usr/bin/python3
''' task 3 module'''


if __name__ == '__main__':
    import json
    import requests

    file_name = 'todo_all_employees.json'

    res = requests.get(
                   'https://jsonplaceholder.typicode.com/users/')
    users = res.json()

    res = requests.get(
                   'https://jsonplaceholder.typicode.com/todos')
    todos = res.json()

    records = dict()

    for todo in todos:
        user_id = str(todo.get('userId'))
        user = list(filter(lambda user: str(user.get('id')) == user_id, users))
        username = user[0].get('username')

        if user_id not in records.keys():
            records[user_id] = [{"username": username,
                                 "task": todo.get('title'),
                                 "completed": todo.get('completed')
                                 }]
        else:
            records[user_id].append({"username": username,
                                     "task": todo.get('title'),
                                     "completed": todo.get('completed')
                                     })

    with open(file_name, 'w') as jsonfile:
        json.dump(records, jsonfile)
