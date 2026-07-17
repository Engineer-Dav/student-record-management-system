# Student Record Management System (SRMS)

A command-line Student Record Management System (SRMS) built with **Python** and **PostgreSQL**. This application allows users to manage students, courses, enrollments, and academic results through an interactive menu-driven interface.

## Features

### Student Management

* Add new students
* View all students
* Search students by ID or name
* Update student information
* Delete students

### Course Management

* Add new courses
* View available courses
* Update course information
* Delete courses

### Enrollment Management

* Enroll students in courses
* Remove student enrollments
* View all enrollments

### Results Management

* Add and update student scores
* View student results
* Calculate student CGPA
* Display top-performing students
* View failed courses
* Generate department CGPA statistics

## Technologies Used

* Python 3
* PostgreSQL
* psycopg2
* python-dotenv
* tabulate

## Database Schema

The project uses three related tables:

* **students**
* **courses**
* **enrollments**

The database includes:

* Primary Keys
* Composite Primary Keys
* Foreign Keys
* CHECK constraints for ID validation using regular expressions

## Installation

1. Clone the repository.
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a PostgreSQL database named `srms`.

4. Import the database schema:

```bash
psql -U your_username -d srms -f srms.sql
```

5. Create a `srms.env` file using `srms.env.example` and update it with your PostgreSQL credentials.

6. Run the application:

```bash
python SRMS.py
```

## Project Structure

```text
├── SRMS.py
├── srms.sql
├── requirements.txt
├── README.md
├── .gitignore
├── srms.env.example
```

## Future Improvements

* Graphical User Interface (GUI)
* Web API integration
* Authentication and user roles
* Automated testing
* Docker support

## Author

DAVID MIKE
