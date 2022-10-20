#!/usr/bin/python3
''' task 1 module'''


if __name__ == '__main__':
    import requests
    from sys import argv

    emp_id = argv[1]
    file_name = emp_id + '.csv'
    total_todos = 0
    done_todos = 0
    done_todos_titles = []

    res = requests.get(
                   'https://jsonplaceholder.typicode.com/users/' +
                   emp_id)
    emp_name = res.json().get('username', 'user name not found')

    res = requests.get(
                   'https://jsonplaceholder.typicode.com/users/' +
                   emp_id + '/todos')
    emp_todos = res.json()

    with open(file_name, 'w') as csvfile:
        for todo in emp_todos:
            total_todos += 1
            csvfile.write(
                    '"{}","{}","{}","{}"\n'.format(
                                            todo.get('userId'),
                                            emp_name,
                                            todo.get('completed'),
                                            todo.get('title')
                                            ))

        #    if todo.get('completed') is True:
        #        done_todos += 1
        #        done_todos_titles.append(todo.get(
        #                                    'title',
        #                                    'no title found'
        #                                    ))

    # print('Employee {} is done with tasks({}/{}):'.format(
    #                                                emp_name,
    #                                                done_todos,
    #                                                total_todos
    #                                                ))

    # for title in done_todos_titles:
    #     print('\t ' + title)
