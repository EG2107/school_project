import os
import sqlite3


def get_cwd():
    #return os.getcwd()
    return os.getcwd()[0:-14]

def delete_end_of_string(string):
    if string[len(string) - 1] == '\n':
        string = string[0 : len(string) - 1]
    return string

def get_class_list_path(class_number):
    return get_cwd() + "\\student_lists\\" + class_number + ".txt"

def get_activity_list_path(activity_name):
    return get_cwd() + "\\activity_lists\\" + activity_name + ".txt"

def get_activity_description_path(activity_name):
    return get_cwd() + "\\activity_description\\" + activity_name + ".txt"

def get_all_classes_path():
    return get_cwd() + "\\all_classes.txt"

def get_all_activities_path():
    return get_cwd() + "\\all_activities.txt"

def get_merch_list_path():
    return get_cwd() + "\\merch_list.txt"

def get_guide_path():
    return get_cwd() + "\\guide.txt"

def create_student_database():
    connection = sqlite3.connect("student_database.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students
        (ID INTEGER, ФИО TEXT, Класс TEXT, Бонусы INTEGER)
    """)

    with open(get_all_classes_path(), "r", encoding="utf-8") as all_classes:
        id = 0
        for cur_class_name in all_classes:
            cur_class_name = delete_end_of_string(cur_class_name)
            with open(get_class_list_path(cur_class_name), "r", encoding="utf-8") as file:
                for student_name in file:
                    student_name = delete_end_of_string(student_name)
                    cursor.execute("INSERT INTO students VALUES ((?), (?), (?), 0)", (id, student_name, cur_class_name, ))
                    id += 1

    connection.commit()
    connection.close()

def create_merch_database():
    connection = sqlite3.connect("merch_database.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS merch
        (ID INTEGER, Название товара TEXT, Количество INTEGER)
    """)

    id = 0
    with open(get_merch_list_path(), "r", encoding="utf-8") as merch_list:
        for item_name in merch_list:
            item_name = delete_end_of_string(item_name)
            cursor.execute("INSERT INTO merch VALUES ((?), (?), 0)", (id, item_name, ))
            id += 1

    connection.commit()
    connection.close()