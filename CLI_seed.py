import argparse
from conf.models import Teacher, Student, Group, Subject, Grade
from conf.db import session


import configparser
import pathlib

def create_teacher(args):

    teacher = Teacher(fullname=args.fullname)
    session.add(teacher)
    session.commit()

    print(f'A teacher has been created {args.fullname}')
    
def create_group(args):

    group = Group(name=args.name)
    session.add(group)
    session.commit()

    print(f'A group has been created {args.name}')
    
def create_subject(subject_name, teacher_id):

    group = Subject(name=subject_name, teacher_id=teacher_id)
    session.add(group)
    session.commit()

    print(f'A subject has been created {subject_name, teacher_id}')

def create_student(student_name, group_id):

    student = Student(fullname=student_name, group_id=group_id)
    session.add(student)
    session.commit()

    print(f'A student has been created {student_name, group_id}')
    
def create_grade(grade, grade_date, student_id, subject_id):
    st_grade = Grade(grade=grade, grade_date=grade_date, student_id=student_id, subject_id=subject_id)
    session.add(st_grade)
    session.commit()

    print(f'A grade has been created {grade, grade_date, student_id, subject_id}')

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
    parser.add_argument('--action', '-a', choices=['create', 'list', 'update', 'remove'], help='CRUD operations')
    parser.add_argument('--model', '-m', choices=['Student','Teacher', 'Group', 'Subject', 'Grade'], help='Specify the model')
    parser.add_argument('--stfullname', '-stn', nargs=2, required=False, help='Student name')
    parser.add_argument('--fullname', '-n', required=False, help='Teacher name')
    parser.add_argument('--name','-gn', required=False, help='Group name')
    parser.add_argument('--sname','-sn', nargs=2, required=False, help='Subject name')
    parser.add_argument('--graname','-grn', nargs=4, required=False, help='Grade name')
    
    
    #__________________Will be created later_________________________________________
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
    
    if args.action == 'create':
        if args.model == 'Teacher':
            if args.fullname:
                create_teacher(args)
            else:
                print("To create a teacher the name should be specified.")
        elif args.model == 'Group':
            if args.name:
                create_group(args)
            else:
                print("To create a group the name should be specified.")
        elif args.model == 'Subject':
            if args.sname:
                subject_name, teacher_id = args.sname
                create_subject(subject_name, teacher_id)
            else:
                print("To create a subject the name should be specified.")
        elif args.model == 'Student':
            if args.stfullname:
                student_name, group_id = args.stfullname
                create_student(student_name, group_id)
            else:
                print("To create a student the name should be specified.")
        elif args.model == 'Grade':
            if args.graname:
                grade, grade_date, student_id, subject_id = args.graname
                create_grade(grade, grade_date, student_id, subject_id)
            else:
                print("To create a student the name should be specified.")
        

if __name__ == '__main__':
    main()
