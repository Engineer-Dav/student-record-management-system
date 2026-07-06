CREATE TABLE students (
    id TEXT, 
    name TEXT NOT NULL, 
    age SMALLINT NOT NULL, 
    department TEXT NOT NULL,
    PRIMARY KEY(id),
    CHECK(id ~ '^[A-Z][0-9]{3}$')
);
CREATE TABLE courses (
    course_id TEXT,
    course_name TEXT NOT NULL,
    credit_units SMALLINT NOT NULL,
    PRIMARY KEY(course_id),
    CHECK(course_id ~ '^[A-Z]{3}[0-9]{3}$')
);
CREATE TABLE enrollments (
    student_id TEXT NOT NULL,
    course_id TEXT NOT NULL,
    score SMALLINT,
    PRIMARY KEY(student_id,course_id),
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
);