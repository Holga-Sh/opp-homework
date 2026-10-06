class Mentor:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class GradeComparableMixin:

    def _average_grade(self):
        all_grades = [grade for grades in self.grades.values() for grade in grades]
        return sum(all_grades) / len(all_grades) if all_grades else 0.0

    def __eq__(self, other):
        if not isinstance(other, GradeComparableMixin):
            return NotImplemented
        return self._average_grade() == other._average_grade()

    def __lt__(self, other):
        if not isinstance(other, GradeComparableMixin):
            return NotImplemented
        return self._average_grade() < other._average_grade()

    def __le__(self, other):
        if not isinstance(other, GradeComparableMixin):
            return NotImplemented
        return self._average_grade() <= other._average_grade()


class Lecturer(Mentor, GradeComparableMixin):

    def __init__(self, name, surname):
            super().__init__(name, surname)
            self.grades = {}

    def __str__(self):
        avg = self._average_grade()
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {avg:.1f}"
        )

class Reviewer(Mentor):

    def rate_hw(self, student, course, grade):
        if (
            isinstance(student, Student)
            and course in self.courses_attached
            and course in student.courses_in_progress
        ):
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}"
        )

class Student(GradeComparableMixin):

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if (
            isinstance(lecturer, Lecturer)
            and course in self.courses_in_progress
            and course in lecturer.courses_attached
            and 1 <= grade <= 10
        ):
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        avg = self._average_grade()
        in_progress = ", ".join(self.courses_in_progress)
        finished = ", ".join(self.finished_courses)
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {avg:.1f}\n"
            f"Курсы в процессе изучения: {in_progress}\n"
            f"Завершенные курсы: {finished}"
        )    


def get_avg_student_grade(students_list, course_name):
    """
    Подсчёт средней оценки за домашние задания по всем студентам 
    в рамках конкретного курса.
    Аргументы: список студентов и название курса.
    """
    all_grades = []
    for student in students_list:
        if course_name in student.grades:
            all_grades.extend(student.grades[course_name])
    
    return sum(all_grades) / len(all_grades) if all_grades else 0.0


def get_avg_lecturer_grade(lecturers_list, course_name):
    """
    Подсчёта средней оценки за лекции всех лекторов в рамках курса. 
    АргументЫ: список лекторов и название курса.
    """
    all_grades = []
    for lecturer in lecturers_list:
        if course_name in lecturer.grades:
            all_grades.extend(lecturer.grades[course_name])
    
    return sum(all_grades) / len(all_grades) if all_grades else 0.0


# Задача №1. Наследование

# lecturer = Lecturer('Иван', 'Иванов')
# reviewer = Reviewer('Пётр', 'Петров')

# print(isinstance(lecturer, Mentor)) # True
# print(isinstance(reviewer, Mentor)) # True
# print(lecturer.courses_attached)    # []
# print(reviewer.courses_attached)    # []


# Задача №2. Атрибуты и взаимодействие классов.

lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')

student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']

print(student.rate_lecture(lecturer, 'Python', 7))   # None
print(student.rate_lecture(lecturer, 'Java', 8))     # Ошибка
print(student.rate_lecture(lecturer, 'C++', 8))      # Ошибка
print(student.rate_lecture(reviewer, 'Python', 6))   # Ошибка

print(lecturer.grades)  # {'Python': [7]}


# Задача №3. Полиморфизм и магические методы.

lecturer_1 = Lecturer('Иван', 'Иванов')
lecturer_2 = Lecturer('Алексей', 'Алексеевич')

reviewer = Reviewer('Пётр', 'Петров')

student_1 = Student('Ruoy', 'Eman', 'M')
student_2 = Student('Ольга', 'Алёхина', 'F')

student_1.courses_in_progress += ['Python', 'Git']
student_1.finished_courses += ['Introduction to programming']

student_2.courses_in_progress += ['Python']

lecturer_1.courses_attached += ['Python']
lecturer_2.courses_attached += ['Python']

reviewer.courses_attached += ['Python', 'Git']


student_1.rate_lecture(lecturer_1, 'Python', 8)
student_1.rate_lecture(lecturer_2, 'Python', 9)

reviewer.rate_hw(student_1, 'Python', 8)
reviewer.rate_hw(student_1, 'Git', 5)
reviewer.rate_hw(student_2, 'Python', 9)


print()
print(reviewer)

print()
print(lecturer_1)

print()
print(student_1)

print()
print(lecturer_1 > lecturer_2)
print(student_1 < student_2)


# Задача №4. Полевые испытания.

student_1 = Student('Ruoy', 'Eman', 'M')
student_1.courses_in_progress += ['Python', 'Git']
student_1.grades['Python'] = [7, 9, 8]
student_1.grades['Git'] = [6, 5]

student_2 = Student('Ольга', 'Алёхина', 'F')
student_2.courses_in_progress += ['Python']
student_2.grades['Python'] = [10, 8]

lecturer_1 = Lecturer('Иван', 'Иванов')
lecturer_1.courses_attached += ['Python']
lecturer_1.grades['Python'] = [9, 3]

lecturer_2 = Lecturer('Алексей', 'Алеексеевич')
lecturer_2.courses_attached += ['Python']
lecturer_2.grades['Python'] = [8, 10]


students = [student_1, student_2]
lecturers = [lecturer_1, lecturer_2]


avg_student_python = get_avg_student_grade(students, 'Python')
avg_lecturer_python = get_avg_lecturer_grade(lecturers, 'Python')

print()
print(f"Средняя оценка студентов по курсу Python: {avg_student_python:.1f}")
print(f"Средняя оценка лекторов по курсу Python: {avg_lecturer_python:.1f}")