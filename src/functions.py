import sqlite3


def delete_end_of_string(string):
    if string[len(string) - 1] == '\n':
        string = string[0 : len(string) - 1]
    return string

def get_class_list_name(class_number):
    return "student_lists\\" + class_number + ".txt"

def get_activity_list_name(activity_name):
    return "activity_lists\\" + activity_name + ".txt"

def get_activity_description_name(activity_name):
    return "activity_description\\" + activity_name + ".txt"

def create_database():
    connection = sqlite3.connect("student_database.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students
        (ID INTEGER, ФИО TEXT, Класс TEXT, Бонусы INTEGER)
    """)

    with open("all_classes.txt", "r", encoding="utf-8") as all_classes:
        id = 0
        for cur_class_name in all_classes:
            cur_class_name = delete_end_of_string(cur_class_name)
            with open(get_class_list_name(cur_class_name), "r", encoding="utf-8") as file:
                for student_name in file:
                    student_name = delete_end_of_string(student_name)
                    cursor.execute("INSERT INTO students VALUES ((?), (?), (?), 0)", (id, student_name, cur_class_name, ))
                    id += 1

    connection.commit()
    connection.close()