from sqlalchemy import String, func, desc, select, and_

from conf.models import Grade, Teacher, Student, Group, Subject
from conf.db import session

def select_01():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 5;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result

def select_02():
    """
    SELECT
        s.id,
        s.fullname,
        ROUND(AVG(g.grade), 2) AS average_grade
    FROM grades g
    JOIN students s ON s.id = g.student_id
    where g.subject_id = 1
    GROUP BY s.id
    ORDER BY average_grade DESC
    LIMIT 1;
    """
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subject_id == 1).group_by(Student.id).order_by(
        desc('average_grade')).limit(1).all()
    return result

def select_03():
    """
    SELECT s.group_id, ROUND(AVG(g.grade), 2) AS average_grade
    FROM students s
    JOIN grades g ON s.id = g.student_id
    WHERE g.subject_id = 1
    GROUP BY s.group_id
    ORDER BY average_grade DESC;
    """
    result = session.query(Student.group_id, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Student).join(Grade).filter(Grade.subject_id == 1).group_by(Student.group_id).order_by(
            desc('average_grade')).all()
    return result

def select_04():
    """
    SELECT ROUND(AVG(grade), 2) AS average_grade
    FROM grades;
    """
    result = session.query(func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).all()
    return result

def select_05():
    """
    SELECT t.fullname AS teacher_name, string_agg(s.name, ', ') AS courses_taught
    FROM teachers t
    JOIN subjects s ON t.id = s.teacher_id
    where t.id = 1
    GROUP BY t.fullname;
    """
    result = session.query(Teacher.fullname, func.aggregate_strings(Subject.name, ',').label('courses_taught')) \
        .select_from(Teacher).join(Subject).filter(Teacher.id == 1).group_by(Teacher.fullname).all()
    return result
def select_06():
    """
    SELECT g.name AS group_name, string_agg(s.fullname, ', ') AS students_list
    FROM students s
    JOIN groups g ON s.group_id = g.id
    where g.id = 1
    GROUP BY g.name;
    """
    result = session.query(Group.name, func.aggregate_strings(Student.fullname, ',').label('students_list')) \
        .select_from(Student).join(Group).filter(Group.id == 1).group_by(Group.name).all()
    return result
def select_07():
    """
    SELECT s.fullname AS student_name, g.name AS group_name,
    sub.name AS subject_name,
    STRING_AGG(CAST(gr.grade AS TEXT), ', ') AS student_grades
    FROM students s
    JOIN groups g ON s.group_id = g.id
    JOIN grades gr ON s.id = gr.student_id
    JOIN subjects sub ON gr.subject_id = sub.id
    where sub.id = 1
    GROUP BY s.fullname, g.name, sub.name;
    """
    
    result = session.query(Student.fullname, Group.name, Subject.name, func.aggregate_strings(func.cast(Grade.grade, String), ',').label('student_grades')) \
        .select_from(Student).join(Group).join(Grade).join(Subject).filter(Subject.id == 1).group_by(Student.fullname).group_by(Group.name) \
        .group_by(Subject.name).all()
    return result
def select_08():
    """
    SELECT s.id, s.fullname, ROUND(AVG(m.grade), 2) AS average_grade
    FROM teachers s
    JOIN subjects subj ON subj.teacher_id = s.id
    JOIN grades m ON s.id = m.subject_id
    WHERE s.id = 1
    GROUP BY s.id;
    """
    result = session.query(Teacher.id, Teacher.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Teacher).join(Subject).join(Grade).filter(Teacher.id == 1).group_by(Teacher.id).all()
    return result
def select_09():
    """
    SELECT DISTINCT s.id, s.fullname, subj.id , subj.name
    FROM students s
    JOIN grades m ON s.id = m.student_id
    JOIN subjects subj ON m.subject_id = subj.id
    WHERE s.id = 1;
    """
    
    result = session.query(func.distinct(Student.id, Student.fullname, Subject.name, Subject.id)) \
        .select_from(Student).join(Grade).join(Subject).filter(Student.id == 1).all()
    return result
def select_10():
    """
    SELECT DISTINCT s.id, s.fullname, subj.id , subj.name, t.id, t.fullname
    FROM students s
    JOIN grades m ON s.id = m.student_id
    JOIN subjects subj ON m.subject_id = subj.id
    JOIN teachers t ON subj.teacher_id = t.id
    WHERE s.id = 1 AND t.id = 1;
    """
    result = session.query(func.distinct(Student.id, Student.fullname, Subject.name, Subject.id, Teacher.id, Teacher.fullname)) \
        .select_from(Student).join(Grade).join(Subject).join(Teacher).filter(and_(Student.id == 1, Teacher.id == 1)).all()
    return result
def select_11():
    """
    SELECT s.id, s.fullname, t.id, t.fullname, ROUND(AVG(m.grade), 2) AS average_grade 
    FROM teachers t
    JOIN subjects subj ON t.id = subj.teacher_id
    JOIN grades m ON subj.id = m.subject_id
    JOIN students s ON m.student_id = s.id
    WHERE s.id = 1 AND t.id = 1
    GROUP BY s.id, t.id, s.fullname, t.fullname;
    """
    
    result = session.query(Student.id, Student.fullname, Teacher.id, Teacher.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Teacher).join(Subject).join(Grade).join(Student).filter(and_(Student.id == 1, Teacher.id == 1)).group_by(Student.id) \
        .group_by(Teacher.id).group_by(Student.fullname).group_by(Teacher.fullname).all()
    return result
def select_12():
    """
    SELECT s.id, s.fullname, MAX(m.grade_date) AS max_date
    FROM students s
    JOIN grades m ON s.id = m.student_id
    JOIN subjects subj ON m.subject_id = subj.id
    JOIN groups g ON s.group_id = g.id
    WHERE g.id = 1 AND subj.id = 1 
    GROUP BY s.id, s.fullname
    ORDER BY s.id, max_date DESC;
    """
    
    result = session.query(Student.id, Student.fullname, func.max(Grade.grade_date).label('max_date')) \
        .select_from(Student).join(Grade).join(Subject).join(Group).filter(and_(Group.id == 1, Subject.id == 1)).group_by(Student.id) \
        .group_by(Student.fullname).order_by(Student.id).order_by(desc('max_date')).all()
    return result


if __name__ == '__main__':
    print("______________01_________________")
    print(select_01())
    print("______________02_________________")
    print(select_02())
    print("______________03_________________")
    print(select_03())
    print("______________04_________________")
    print(select_04())
    print("______________05_________________")
    print(select_05())
    print("______________06_________________")
    print(select_06())
    print("______________07_________________")
    print(select_07())
    print("______________08_________________")
    print(select_08())
    print("______________09_________________")
    print(select_09())
    print("______________10_________________")
    print(select_10())
    print("______________11_________________")
    print(select_11())
    print("______________12_________________")
    print(select_12())
    