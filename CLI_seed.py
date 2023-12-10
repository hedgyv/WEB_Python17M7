import argparse
from conf.models import Teacher, Student, Group, Subject, Grade
from conf.db import session


import configparser
import pathlib

def create(args):
    
    teacher = Teacher(fullname=args.fullname)
    session.add(teacher)
    session.commit()
    
    print(f'Создан учитель с именем {args.fullname}')

def list(args):
    ...
    # Логіка для читання запису з бази даних

def update(args):
    ...
    # Логіка для оновлення запису у базі даних

def remove(args):
    ...
    # Логіка для видалення запису з бази даних

def main():
    parser = argparse.ArgumentParser(description='CLI для управления учителями')

    # subparsers = parser.add_subparsers(title='Доступные операции', dest='action')
    # subparsers.required = True

    # create_parser = subparsers.add_parser('create', help='Создать учителя')
    parser.add_argument('--action', '-a', choices=['create', 'list', 'update', 'remove'], help='CRUD операции')
    parser.add_argument('--model', '-m', choices=['Teacher'], help='Укажите модель')
    parser.add_argument('--fullname','-n', required=True, help='Имя учителя')
    parser.set_defaults(func=create)

    # list_parser = subparsers.add_parser('list', help='Вывести всех учителей')
    # list_parser.set_defaults(func=list)

    # update_parser = subparsers.add_parser('update', help='Обновить учителя')
    # update_parser.add_argument('--id','-i', required=True, help='ID учителя для обновления')
    # update_parser.add_argument('--fullname','-n', required=True, help='Новое имя учителя')
    # update_parser.set_defaults(func=update)

    # remove_parser = subparsers.add_parser('remove', help='Удалить учителя')
    # remove_parser.add_argument('--id','-i', required=True, help='ID учителя для удаления')
    # remove_parser.set_defaults(func=remove)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
