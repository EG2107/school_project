import os
import sqlite3
import pandas as pd


def delete_end_of_string(string):
    if string[len(string) - 1] == '\n':
        string = string[0 : len(string) - 1]
    return string

def get_cwd():
    return os.getcwd()

def get_class_list_path(class_number):
    return get_cwd() + "\\student_lists\\" + class_number + " список.xlsx"

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

def check_student_name(student_name):
    return (type(student_name) == str) and (student_name != "ФИО учащегося")

def create_student_database():
    connection = sqlite3.connect("student_database.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students
        (ID INTEGER, ФИО TEXT, Класс TEXT, Количество_мероприятий INTEGER, Мероприятия TEXT)
    """)

    with open(get_all_classes_path(), "r", encoding="utf-8") as all_classes:
        id = 0
        for cur_class_name in all_classes:
            cur_class_name = delete_end_of_string(cur_class_name)
            df = pd.read_excel(get_class_list_path(cur_class_name))
            for student_name in df['Unnamed: 2']:
                if (check_student_name(student_name)):
                    cursor.execute("INSERT INTO students VALUES ((?), (?), (?), 0, '')", (id, student_name, cur_class_name, ))
                    id += 1

    connection.commit()
    connection.close()
    
def set_to_str(st):
    if (len(st) == 0):
        return None
    s = str(st)
    return s[1:-1]