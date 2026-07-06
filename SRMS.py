import re
from tabulate import tabulate
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv("srms.env")
# print(os.getenv("DB_PASSWORD"))

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")



def connect():
    connection  = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
            )
    cursor = connection.cursor()
    return connection, cursor


class Student:
    def __init__(self, student_id, age, name, department):
        self.student_id = student_id
        self.age = age
        self.name = name
        self.department = department

    @classmethod
    def student_info(cls):
        name = input("What's your name? ")
        while True:
            try:
                age = int(input("What's your age? "))
                if age > 15:
                    break
                else:
                    print("You must be Above 15")
            except ValueError:
                print("Please enter a valid number for age")
        department = input("What's your department? ").strip().title()
        while True:
                student_id = input("What's your student ID number? ").strip()
                pattern = r"^[A-Z]\d{3}$"
                if re.match(pattern, student_id):
                    break
                else:
                     print("Invalid Student ID. Must be a capital letter followed by 3 digits")       
        return cls(student_id,age,name,department)


def add_student():
    student = Student.student_info()
    connection, cursor = connect()
    cursor.execute("""INSERT INTO students (id, name, age, department) VALUES(%s, %s, %s, %s)""",
                    (student.student_id, student.name, student.age, student.department)   
                        )
    connection.commit()
    connection.close()
    print("Student added successfully")


def view_student():
    connection, cursor = connect()
    cursor.execute("SELECT * FROM students")
    results = cursor.fetchall()
    connection.close()
    return results

def search_student_by_id(student_id):
    while True:
        pattern = r"^[A-Z]\d{3}$"
        if re.match(pattern, student_id):
            break
        else:
            print("Invalid Student ID. Must be a capital letter followed by 3 digits")
            student_id = input("What's your student ID number? ").strip() 
    connection , cursor = connect()
    cursor.execute("SELECT id, name, age, department FROM students WHERE id = %s", (student_id,))
    student_result = cursor.fetchone()
    connection.close()
    if student_result is not None:
        a,b,c,d = student_result
        print(f"ID: {a} | Name: {b} | Age: {c} | Department: {d}")
        return True
    else:
        print("Student ID not found")
        return False


def search_student_by_name(student_name):
    connection , cursor = connect()
    cursor.execute("SELECT id, name, age, department FROM students WHERE name = %s", (student_name,))
    student_result= cursor.fetchone()
    if student_result is not None:
        a,b,c,d = student_result
        print(f"ID: {a} | Name: {b} | Age: {c} | Department: {d}")
    else:
        print("Student name not found")
    connection.close()

def update_student_name(student_name,student_id):
    connection, cursor = connect()
    cursor.execute("UPDATE students SET name = %s "
    "WHERE id = %s",(student_name, student_id,)) 
    connection.commit()
    connection.close()
    print("Student name updated successfully")

def update_student_age(student_id):
    while True:
        try:
            student_age = int(input("What's your age? "))
            if student_age > 15:
                break
            else:
                print("You must be Above 15")
        except ValueError:
            print("Please enter a valid number for age")
    connection, cursor = connect()
    cursor.execute("UPDATE students SET age = %s"
    "WHERE id = %s",(student_age, student_id,)) 
    connection.commit()
    connection.close()
    print("Student age updated successfully")

def student_id_by_name(student_name):
    connection, cursor = connect()
    cursor.execute("SELECT id FROM students WHERE name = %s",(student_name,))
    result = cursor.fetchone()
    connection.close()
    return result

def update_student_department(student_id,student_department):
    connection, cursor = connect()
    cursor.execute("UPDATE students SET department = %s WHERE id = %s",(student_department,student_id,)) 
    connection.commit()
    connection.close()

def delete_student():
    while True:
            student_id = input("What's your student ID number ").strip()
            pattern = r"^[A-Z]\d{3}$"
            if re.match(pattern, student_id):
                break
            else:
                print("Invalid Student ID. Must be a capital letter followed by 3 digits")       
    connection,cursor = connect()
    cursor.execute("DELETE FROM students WHERE id = %s",(student_id,))
    info = cursor.rowcount
    if info == 0:
        print("No record mached")
    else:
        print("Deleted sucessfully")
    connection.commit()
    connection.close()

class Course:
    def __init__(self,course_id,course_name,credit_units):
        self.course_id = course_id
        self.course_name = course_name
        self.credit_units = credit_units

    @classmethod
    def course_info(cls):
        while True:
            course_id = input("Course ID? ")
            pattern = r"^[A-Z]{3}\d{3}$"
            if re.match(pattern,course_id):
                break
            else:
                print("Invalid Course ID. Must be three capital letters followed by three numbers")
        course_name = input("Course name? ").strip().title()
        while True:
            try:
                credit_units = int(input("Credit unit? "))
                if credit_units > 3 or credit_units < 1:
                   print("Credit unit must be between 1 and 3")
                else:
                    break
            except ValueError:
                print("Please enter a valid number for course credit unit")

        return cls(course_id,course_name,credit_units)
        
def add_course():
    course = Course.course_info()
    connection, cursor = connect()
    cursor.execute("""INSERT INTO courses (course_id, course_name , credit_units)
                     VALUES (%s, %s, %s)""",(course.course_id, course.course_name, course.credit_units,))
    connection.commit()
    connection.close()
    print("Course added successfully")

def view_courses():
    connection, cursor = connect()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    connection.close()
    print(tabulate(courses,headers=["Course ID","Course Name","Credit Units"]))

def update_course_name():
    while True:
            course_id = input("Course ID? ")
            pattern = r"^[A-Z]{3}\d{3}$"
            if re.match(pattern,course_id):
                break
            else:
                print("Invalid Course ID. Must be three capital letters followed by three numbers")
    course_name = input("Course name? ").strip().title()
    connection, cursor = connect()
    cursor.execute("UPDATE courses SET course_name = %s WHERE course_id = %s",(course_name,course_id,))
    connection.commit()
    connection.close()

def update_credit_unit():
    while True:
        course_id = input("Course ID? ")
        pattern = r"^[A-Z]{3}\d{3}$"
        if re.match(pattern,course_id):
            break
        else:
            print("Invalid Course ID. Must be three capital letters followed by three numbers")
    while True:
        try:
            credit_units = int(input("Credit unit? "))
            if credit_units > 3 or credit_units < 1:
                print("Credit unit must be between 1 and 3")
            else:
                    break
        except ValueError:
            print("Please enter a valid number for course credit unit")

    connection, cursor = connect()
    cursor.execute("UPDATE courses SET credit_units = %s WHERE course_id = %s",(credit_units,course_id,))
    connection.commit()
    connection.close()

def delete_course():
    while True:
        course_id = input("Course ID? ")
        pattern = r"^[A-Z]{3}\d{3}$"
        if re.match(pattern,course_id):
            break
        else:
            print("Invalid Course ID. Must be three capital letters followed by three numbers")
    connection ,cursor = connect()
    cursor.execute("DELETE FROM courses WHERE course_id = %s",(course_id,))
    info = cursor.rowcount
    if info == 0:
        print("No record mached")
    else:
        print("Deleted sucessfully")
    connection.commit()
    connection.close()

def enroll_student():
    while True:
        course_id = input("Course ID? ")
        pattern = r"^[A-Z]{3}\d{3}$"
        if re.match(pattern,course_id):
            break
        else:
            print("Invalid Course ID. Must be three capital letters followed by three numbers")
    while True:
        student_id = input("Student ID number? ").strip()
        pattern = r"^[A-Z]\d{3}$"
        if re.match(pattern, student_id):
            break
        else:
            print("Invalid Student ID. Must be a capital letter followed by 3 digits") 
    connection, cursor = connect()
    cursor.execute("INSERT INTO enrollments (student_id,course_id) VALUES (%s , %s )",(student_id,course_id))
    connection.commit()
    connection.close()
    print("Student enrolled successfully")

def view_enrollments():
    connection, cursor = connect()
    cursor.execute("SELECT student_id,course_id FROM enrollments")
    enrollments = cursor.fetchall()
    connection.close()
    print(tabulate(enrollments,headers=["Student ID","Course ID"]))


def get_course_id():
    while True:
        course_id = input("Course ID? ")
        pattern = r"^[A-Z]{3}\d{3}$"
        if re.match(pattern,course_id):
            return course_id
        else:
            print("Invalid Course ID. Must be three capital letters followed by three numbers")

def get_student_id():
    while True:
        student_id = input("What's your student ID number? ").strip()
        pattern = r"^[A-Z]\d{3}$"
        if re.match(pattern, student_id):
            return student_id
        else:
            print("Invalid Student ID. Must be a capital letter followed by 3 digits") 

def remove_enrollment():
    course_id = get_course_id()
    student_id = get_student_id()
    connection, cursor = connect()
    cursor.execute("DELETE FROM enrollments WHERE course_id = %s AND student_id = %s ",(course_id,student_id))
    connection.commit()
    connection.close()
    print(f"{student_id} have sucessfully Unenrolled from {course_id}")

def add_score():
    student_id = get_student_id()
    course_id = get_course_id()
    while True:
        try:
            score = int(input("Score:"))
            if score >= 0 and score <= 100:
                break
            else:
                print("Score must be between 0 and 100")
        except ValueError:
            print("Please enter a valid number for score")     
    connection, cursor = connect()
    cursor.execute("""UPDATE enrollments SET score = %s WHERE student_id = %s
                    AND course_id = %s""",(score,student_id,course_id))
    connection.commit()
    connection.close()

def update_score():
    add_score()

def view_results():
    student_id = get_student_id()
    connection, cursor = connect()
    cursor.execute("""SELECT student_id,course_id,score FROM enrollments
                    WHERE student_id = %s """,(student_id,))
    enrollments = cursor.fetchall()
    connection.close()
    print(tabulate(enrollments,headers=["Student ID","Course ID","Score"]))

def get_grade_points(score):
    if score >= 70:
        return 5
    elif score >= 60:
        return 4
    elif score >= 50:
        return 3
    elif score >= 45:
        return 2
    elif score >= 40:
        return 1
    else:
        return 0

def calculate_cgpa(student_id):
    connection, cursor = connect()
    cursor.execute("""SELECT * FROM enrollments
                    JOIN 
                    courses ON enrollments.course_id = courses.course_id
                   WHERE student_id = %s
                    """, (student_id,))
    results = cursor.fetchall()
    total_grade_points = 0
    total_credit_units = 0
    connection.close()
    for result in results:
        score = result[2]
        credit = result[5]
        grade_points = get_grade_points(score)
        total_grade_points += grade_points * credit
        total_credit_units += credit
    try:
        return total_grade_points / total_credit_units
    except ZeroDivisionError:
        print("This student wasn't enrolled")
        return None

def top_students():
    connection, cursor = connect()
    cursor.execute("""SELECT enrollments.student_id, 
       SUM(CASE 
           WHEN score >= 70 THEN 5
           WHEN score >= 60 THEN 4
           WHEN score >= 50 THEN 3
           WHEN score >= 45 THEN 2
           WHEN score >= 40 THEN 1
           ELSE 0
        END * credit_units) / SUM(credit_units) AS cgpa
        FROM enrollments
        JOIN courses ON enrollments.course_id = courses.course_id
        GROUP BY enrollments.student_id
        ORDER BY cgpa DESC
        LIMIT 5""")
    top_students = cursor.fetchall()
    connection.close()
    print(tabulate(top_students,headers=["Student ID", "CGPA"]))

def failed_courses():
    student_id = get_student_id()
    connection, cursor = connect()
    cursor.execute("""SELECT student_id, course_id, score, course_name FROM enrollments
                   JOIN
                   courses ON enrollments.course_id = courses.course_id
                   WHERE student_id = %s AND score < 40
                   """,(student_id,))
    failed_courses = cursor.fetchall()
    connection.close()
    print(tabulate(failed_courses,headers=["Student ID","Course ID", "Score", "Course Name"]))

def department_stats():
    connection, cursor = connect()
    cursor.execute("""SELECT students.department,
       SUM(CASE 
           WHEN score >= 70 THEN 5
           WHEN score >= 60 THEN 4
           WHEN score >= 50 THEN 3
           WHEN score >= 45 THEN 2
           WHEN score >= 40 THEN 1
           ELSE 0
        END * credit_units) / SUM(credit_units) AS avg_cgpa
        FROM students
        JOIN enrollments ON students.id = enrollments.student_id
        JOIN courses ON enrollments.course_id = courses.course_id
        GROUP BY students.department
        ORDER BY avg_cgpa DESC""")
    department_stats = cursor.fetchall()
    connection.close()
    print(tabulate(department_stats,headers=["Department", "Average CGPA"]))
    

def main():
    while True:
        print("\nStudent Result Management System")
        print("\n1. Student Management")
        print("2. Course Management")
        print("3. Enrollment Management")
        print("4. Results Management")
        print("5. Reports")
        print("6. Exit")

        main_choice = input("Choose an option: ")

        if main_choice == "1":
            print("1. Add Student")
            print("2. View Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Back")

            student_choice = input("Choose an option: ")
            # Add Student
            if student_choice == "1":
                add_student()
            # View Students 
            elif student_choice == "2":
                student_list = view_student()
                print(tabulate(student_list, headers=["Student ID", "Name", "Age", "Department"]))

            # Search Student 
            elif student_choice == "3":
                print("1. Search by ID")
                print("2. Search by Name")

                student_search = input("Choose an option: ")
                if student_search == "1":
                    student_id = input("What's your student ID number? ").strip()
                    search_student_by_id(student_id)

                elif student_search == "2":
                    student_name = input("What's your name? ").strip().title()
                    search_student_by_name(student_name)

                else:
                    print("Invalid Option")
            # Update Student info
            elif student_choice == "4": 
                print("1. Update by ID Number")
                print("2. Update by Name")

                student_update = input("Choose an option: ")

                if student_update == "1":
                    student_id = input("What's your student ID number? ").strip()
                    result = search_student_by_id(student_id)
                    if result:
                        print("\nWhat would you like to Update?")
                        print("1. Name")
                        print("2. Age")
                        print("3. Department")
                    
                        update_choice = input("Choose an option: ")

                        if update_choice == "1":
                            student_name = input("What's your new name? ")
                            update_student_name(student_name,student_id)

                        elif update_choice == "2":
                            update_student_age(student_id)

                        elif update_choice == "3":
                            student_department = input("What's your new department? ").strip().title()
                            update_student_department(student_id,student_department)
            
                elif student_update == "2":
                    student_name = input("What's your new name? ")
                    result = student_id_by_name(student_name)
                    if result is not None:
                        search_student_by_name(student_name)
                        student_id = result[0]
                        print("\nWhat would you like to Update?")
                        print("1. Name")
                        print("2. Age")
                        print("3. Department")

                        update_choice = input("Choose an option: ")

                        if update_choice == "1":
                            student_name = input("What's your new name? ")
                            update_student_name(student_name,student_id)

                        elif update_choice == "2":
                            update_student_age(student_id)

                        elif update_choice == "3":
                            student_department = input("What's your new department? ")
                            update_student_department(student_id,student_department)
                    else:
                        print("Student not found")
            #Delete Student
            elif student_choice == "5":
                delete_student()
            #Back Botton
            elif student_choice == "6":
                continue       
        elif main_choice == "2":
            print("1. Add Course")
            print("2. View Courses")
            print("3. Update Course")
            print("4. Delete Course")
            print("5. Back")
            
            course_choice = input("Choose an Option: ")
            if course_choice == "1":
                add_course()
            elif course_choice == "2":
                view_courses()
            elif course_choice == "3":
                print("1. Update Course name")
                print("2. Update Credit unit")

                update_choice = input("Choose an Option: ")
                if update_choice == "1":
                    update_course_name()
                elif update_choice =="2":
                    update_credit_unit()
            elif course_choice =="4":
                delete_course()
            elif course_choice =="5":
                continue
        elif main_choice == "3":
            print("1. Enroll Student in Course")
            print("2. View Student Courses")
            print("3. Remove Enrollment")
            print("4. Back")

            enroll_choice = input("Choose an Option: ")

            if enroll_choice =="1":
                enroll_student()
            elif enroll_choice == "2":
                view_enrollments()
            elif enroll_choice == "3":
                remove_enrollment()
            elif enroll_choice == "4":
                continue
        
        elif main_choice == "4":
            print("1. Add Score")
            print("2. Update Score")
            print("3. View Results")
            print("4. Back")   

            result_choice = input("Choose an Option: ")   
            if result_choice == "1":
                add_score()
            elif result_choice == "2":
                update_score()
            elif result_choice == "3":
                view_results()
            elif result_choice == "4":
                continue
        #Reports
        elif main_choice == "5":
            print("1. Calculate Student CGPA")
            print("2. Top Performing Students")
            print("3. Failed Courses")
            print("4. Department Statistics")
            print("5. Back")
            
            report_choice = input("Choose an Option: ")
            if report_choice == "1":
                student_id = get_student_id()
                cgpa = calculate_cgpa(student_id)
                if cgpa is not None:
                    print(f"CGPA: {cgpa}")

            elif report_choice == "2":
                top_students()
            elif report_choice == "3":
                failed_courses()
            elif report_choice == "4":
                department_stats()
            elif report_choice == "5":
                continue
        elif main_choice == "6":
            break

if __name__ == "__main__":
    main()