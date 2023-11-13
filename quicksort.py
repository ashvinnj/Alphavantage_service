""" quicksort.py script to sort student grades and compare to dictionary built-in sorted function"""


def quicksort_grades(student_dict, sort_order_in='Asc'):
    sort_order = False if sort_order_in == 'Desc' else True

    if len(student_dict) <= 1:
        return list(student_dict.keys())
    else:
        pivot_id = next(iter(student_dict))
        pivot_grade = student_dict[pivot_id]

        upper = [key for key, grade in student_dict.items() if grade is not None
                 and ((sort_order and grade > pivot_grade) or (not sort_order and grade < pivot_grade))]
        equal = [key for key, grade in student_dict.items() if grade == pivot_grade]
        lower = [key for key, grade in student_dict.items() if grade is not None
                 and ((sort_order and grade < pivot_grade) or (not sort_order and grade > pivot_grade))]

        sorted_upper = quicksort_grades({k: student_dict[k] for k in upper}, sort_order_in) if upper else []
        sorted_lower = quicksort_grades({k: student_dict[k] for k in lower}, sort_order_in) if lower else []

        return sorted_lower + equal + sorted_upper


def print_grades(sorted_students, student_grades):
    for student in sorted_students:
        print(f"{student}: {student_grades[student]}")
    # _ = [print(f"{student}: {student_grades[student]}") for student in sorted_students]


def main():
    student_grades = {
        'student1': 68,
        'student2': 48,
        'student3': 18,
        'student4': 88,
        'student5': 98,
        'student6': 68,
        'student7': 37,
        'student8': 99,
        'student9': 91
    }

    print("Ascending Sort using Quicksort :")
    sorted_students_ascending = quicksort_grades(student_grades)
    print_grades(sorted_students_ascending, student_grades)

    print("\nDescending Sort using Quicksort:")
    sorted_students_descending = quicksort_grades(student_grades, sort_order_in='Desc')
    print_grades(sorted_students_descending, student_grades)

    print('-----------------------------------------------------------------------------------------------')
    print("\nAscending Sort (using sorted function):")
    sorted_students_ascending = sorted(student_grades, key=student_grades.get)
    print_grades(sorted_students_ascending, student_grades)

    print("\nDescending Sort (using sorted function):")
    sorted_students_descending = sorted(student_grades, key=student_grades.get, reverse=True)
    print_grades(sorted_students_descending, student_grades)


if __name__ == '__main__':
    main()
