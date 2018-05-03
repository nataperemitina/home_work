import sys

from my_calendar import storage

get_connection = lambda: storage.connect('calendar.sqlite')

def action_find_all():
    with get_connection() as conn:
        print(storage.get_all(conn))

def action_find_opened():
    with get_connection() as conn:
        print(storage.get_opened(conn))

def action_add():
    title = input('\nВведите название задачи: ')
    description = input('\nВведите описание задачи: ')
    due_date = input('\nВведите срок исполнения задачи в формате \'YYYY-MM-DD HH:MM::SS\': ')
    with get_connection() as conn:
        print(storage.add_task(conn, title, description, due_date))

def action_edit():
    id = input('\nВведите номер задачи: ')

    def edit_title():
        with get_connection() as conn:
            new_title = input('\nВведите новое название задачи: ')
            storage.update_task_title(conn, id, new_title)
        return 0

    def edit_description():
        with get_connection() as conn:
            new_desc = input('\nВведите новое описание задачи: ')
            storage.update_task_description(conn, id, new_desc)
        return 0

    def edit_due_date():
        with get_connection() as conn:
            new_due_date = input('\nВведите новый срок исполнения задачи в формате \'YYYY-MM-DD HH:MM::SS\': ')
            storage.update_task_due_date(conn, id, new_due_date)
        return 0

    def edit_nothing():
        with get_connection() as conn:
            print("Задача была обновлена:")
            print(storage.get_task(conn,id))
        return 1

    edit_actions = {
        '1': edit_title,
        '2': edit_description,
        '3': edit_due_date,
        '4': edit_nothing,
    }

    def show_edit_menu():
        print('''
Выберите поле для редактирования:
        
1. Название задачи
2. Описание задачи
3. Срок выполнения задачи
4. Завершить редактирование

''')

    while 1:
        show_edit_menu()
        cmd = input()
        action = edit_actions.get(cmd)
        if action:
            rc = action()
            if rc:
                break;
        else:
            print('Неизвестное действие')

def action_complete():
    id = input('\nВведите номер выполненной задачи: ')
    with get_connection() as conn:
        storage.complete_task(conn, id)

def action_reopen():
    id = input('\nВведите номер переоткрываемой задачи: ')
    with get_connection() as conn:
        storage.reopen_task(conn, id)

def action_show_menu():
    print('''
Ежедневник. Выберите действие:
        
1. Вывести список всех задач
2. Вывести список незавершенных задач
3. Добавить новую задачу
4. Отредактировать задачу
5. Завершить задачу
6. Начать задачу сначала
7. Выход

''')

def action_exit():
    sys.exit(0)

def main():
    with get_connection() as conn:
        storage.initialize(conn)

    actions = {
        '1': action_find_all,
        '2': action_find_opened,
        '3': action_add,
        '4': action_edit,
        '5': action_complete,
        '6': action_reopen,
        '7': action_exit,
    }

    while 1:
        action_show_menu()
        cmd = input()
        action = actions.get(cmd)
        if action:
            action()
        else:
            print('Неизвестное действие')












             
