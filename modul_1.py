# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 14:30:23 2024

@author: night

Этот файл содержит функции, которые нужны для работы программы
"""
import sqlite3 as sql
import re 
import matplotlib.pyplot as plt


def select_rows_from_table(table_name, *names_of_rows, condition=""):
    """
    Возвращает столбцы names_of_rows из таблицы table_name в виде списка кортежей
    condition - условие, по которому будет выборка
    """
    if len(condition) == 0:
        return [i for i in cursor.execute(f"SELECT {','.join(names_of_rows)} from {table_name}")]
    else:
        return [i for i in cursor.execute(f"SELECT {','.join(names_of_rows)} from {table_name} WHERE {condition}")]

def check_input(value, func):
    try:
        return func(value)
    except:
        return 'not'


def print_rows_from_table(data, colums_names=[]):
    """
    Печатает все содержимое data, полученное функцией select_rows_from_table
    Выводит названия колонок colums_names
    """
    [print(str(i).ljust(30), end="") for i in colums_names]
    print()
    for line in data:
        [print(str(cells).ljust(30), end="") for cells in line]
        print()
        
def print_all_from_dairy(condition=""):
     """
     Функция вывода всего дневника тренировок
     """
     colums_names = ["Дата", "Упражнение", "Номер подхода", "Повторения", "Вес"]
     [print(str(i).ljust(20), end="") for i in colums_names]
     print()
     for i in cursor.execute(f"""
                             SELECT Dates.Date, Exercise, ApprNum, Reps, Weight
                             FROM Journal
                             LEFT JOIN Dates ON Journal.Date = Dates.ID
                             LEFT JOIN Exercises ON Journal.ExID = Exercises.ID {condition}
                             """):
         [print(str(j).ljust(20), end="") for j in i]
         print()


def delete_line_from_table(value_id, table_name):
    """Удалить запись под номером value_id из таблицы table_name"""
    cursor.execute(f"DELETE FROM {table_name} WHERE ID = {value_id}")

def check_id(id_, table_name):
    """
    Проверяет ID в таблице. А зачем?
    """
    if id_ not in [int(*i) for i in select_rows_from_table(f"{table_name}", "ID")]:
        return 1
    else:
        return 0
    
def add_new_exercise():
    """
    Добавить упражнение в список упражнений
    """
    check = False
    while check == False:
        print("\nСПИСОК ДОСТУПНЫХ УПРАЖНЕНИЙ")
        print_rows_from_table(select_rows_from_table("Exercises", "ID", "Exercise"))
        print()
        exer = input("Введите название упражнения: ")
        while exer in ["".join(i) for i in select_rows_from_table("Exercises", "Exercise")]:
            exer = input("Данное упражнение есть в списке. Повторите ввод: ")
        app_count = int(input("Введите количество подходов: "))
        while type(app_count) != int:
            app_count = input("Количество повторений должно быть целым числом. Повторите ввод: ")
        case = int(input(f"""Вы ввели:
Упражнение - {exer}
Количество подходов - {app_count}
Сохранить?
[1]Сохранить
[2]Повторить ввод
"""))
        while case != 1 and case != 2:
            case = int(input(f"""Повторите ввод.
Вы ввели:Упражнение - {exer}
Количество подходов - {app_count}
Сохранить?
[1]Сохранить
[2]Повторить ввод
"""))
        if case == 1:
            break
        elif case == 2:
            continue
    if cursor.execute(f"INSERT INTO Exercises(Exercise, AppCount, MaxWeight, MaxRep) VALUES ('{exer}', {app_count}, 0, 0)"):
        conection.commit()
        return 0
    else: 
        print("Ошибка какая-то...")

def select_one_value_from_table_by_id(table_name, row_name, id_):
    """
    Возвращает одно значение из столбца row_name таблицы table_name с id = id_
    """
    cursor.execute(f"SELECT {row_name} FROM {table_name} WHERE ID = {id_}")
    return cursor.fetchone()

def add_new_line_in_diary():
    """
    Добавить новую запись в дневник
    Запись состоит из:
    Даты
    Названия упражнения
    Количеста повторений
    Вес
    """
    
    #Ввод даты
    case = input("Ввод даты:\n[1]Текущая дата\n[2]Выбор записанной даты\n[3]Ввод даты вручную (дд.мм.гггг)\n")
    while check_input(case, int) == 'not':
        case = input("Ошибка, повторите ввод.\n[1]Текущая дата\n[2]Выбор записанной даты\n[3]Ввод даты вручную (дд.мм.гггг)\n")
    case = int(case)
    while case not in [1, 2, 3]:
        case = input("Ошибка. Повторите ввод.\n[1]Текущая дата\n[2]Выбор записанной даты\n[3]Ввод даты вручную (дд.мм.гггг)\n")
        while check_input(case, int) == 'not':
            case = input("Ошибка, повторите ввод.\n[1]Текущая дата\n[2]Выбор записанной даты\n[3]Ввод даты вручную (дд.мм.гггг)\n")
        case = int(case)
    if case == 1:
        date = next(cursor.execute("SELECT CURRENT_DATE"))[0]
        date_inp = ".".join(date.split("-")[::-1])
    elif case == 2:
        date = next(cursor.execute(f'SELECT Date FROM Dates WHERE ID = {choice_date()}'))[0]
        date_inp = ".".join(date.split("-")[::-1])
        print(date)
    else:
        date_inp = input("Введите дату: ")
        while re.match(r'\d{2}.\d{2}.\d{4}', date_inp) == None:
            date_inp = input("Ошибка, введите дату в формате дд.мм.гггг\nВведите дату: ")
        date = "-".join(date_inp.split(".")[::-1])
    if date not in [i[0] for i in select_rows_from_table("Dates", "Date")]:
        cursor.execute(f"INSERT INTO Dates(Date) VALUES ('{date}')")
        conection.commit()
    date_id = int(list(cursor.execute(f"SELECT ID FROM Dates where date = '{date}'"))[0][0])
    
    case = 3
    while True:
        #Выбор упражнения
        print_rows_from_table(select_rows_from_table("Exercises", "ID", "Exercise"), ["ID", "Exercise"])
        exer_id = input("Выберите номер упражнения: ")
        while check_input(exer_id, int) == 'not':
            print_rows_from_table(select_rows_from_table("Exercises", "ID", "Exercise"), ["ID", "Exercise"])
            exer_id = input("Ошибка, повторите ввод.\nВыберите номер упражнения: ")
        exer_id = int(exer_id)
        #Если упражнения нет в списке
        while check_id(exer_id, "Exercises") != 0:
            print()
            print_rows_from_table(select_rows_from_table("Exercises", "ID", "Exercise"), ["ID", "Exercise"])
            exer_id = input("Ошибка ввода, повторите выбор: ")
            while check_input(exer_id, int) == 'not':
                exer_id = input("Ошибка, повторите ввод.\nВыберите номер упражнения: ")
            exer_id = int(exer_id)
        # Если упражнение по дате уже добавлено
        if (date_id, exer_id) in select_rows_from_table("Journal", "Date", "ExID"):
            case = input(f"""
Запись об этом упражнии за {date_inp} уже есть в дневнике.
Желаете добавить еще одну запись?
[1]Выбрать другое упражнение для записи
[2]Добавить упражнение ещё раз
""")
            while check_input(exer_id, int) == 'not':
                case = input("Ошибка. Повторите ввод.")
            case = int(case)
            while case != 1 and case != 2:
                case = int(input("Ошибка. Повторите ввод."))
            if case == 1:
                case = 3
                continue
            elif case == 2:
                break
        if case == 3:
            break
    
    #Достать имя упражнения из таблицы упражнений
    exer_name = "".join(select_one_value_from_table_by_id("Exercises", "Exercise", exer_id))
    #Достать количество подходов из таблицы упражнений
    count_of_app = int(select_one_value_from_table_by_id("Exercises", "AppCount", exer_id)[0])
    #Получить id записи (всех подходов)
    k = select_rows_from_table("Journal", "LineID")
    if len(k) != 0:
        max_line_id = max(k)
        max_line_id = max_line_id[0]+1
    else:
        max_line_id = 1
    
    #Ввод подходов
    input_lines = []
    for i in range(1, count_of_app+1):
        print(f"\nПодход №{i}")
        count_of_reps = input("Введите количество повторений: ")
        while check_input(count_of_reps, int) == 'not':
            count_of_reps = input("Ошибка, повторите ввод.\nВведите количество повторений:")
        count_of_reps = int(count_of_reps)
        weight_for_rep = input("Введите вес: ")
        while check_input(weight_for_rep, float) == 'not':
            weight_for_rep = input("Ошибка, повторите ввод.\nВведите вес: ")
        weight_for_rep = float(weight_for_rep)
        input_lines.append((date_id, max_line_id, exer_id, i, count_of_reps, weight_for_rep))
    
    print(f"\nВаша запись:\nДата - {date_inp}\nУпражнение - {exer_name}")
    print("Подход\tПовторения\tВес")
    [print(*i[3:], sep="\t\t\t") for i in input_lines]
    max_reps = sorted(input_lines, key=lambda x: x[-2])[-1][-2]
    max_weight = sorted(input_lines, key=lambda x: x[-1])[-1][-1]
    
    case = input("Сохранить запись в дневнике?\n[1]Да\n[2]Нет\n")
    while check_input(case, int) == 'not':
        case = input("Ошибка, повторите ввод.\nСохранить запись в дневнике?\n[1]Да\n[2]Нет\n")
    case = int(case)
    while case != 1 and case != 2:
        case = input("Ошибка, повторите ввод.\nСохранить запись в дневнике?\n[1]Да\n[2]Нет\n")
        while check_input(case, int) == 'not':
            case = input("Ошибка, повторите ввод.\nСохранить запись в дневнике?\n[1]Да\n[2]Нет\n")
        case = int(case)
    if case == 1:
        try:
            cursor.executemany("INSERT INTO Journal(Date, lineID, ExID, ApprNum, Reps, Weight) VALUES (?, ?, ?, ?, ?, ?)", input_lines)
            conection.commit()
            for i in select_rows_from_table("Exercises", "ID", "MaxWeight", "MaxRep"):
                if exer_id == i[0]:
                    if max_reps > i[1]:
                        cursor.execute(f"UPDATE Exercises SET MaxRep = {max_reps} WHERE ID = {exer_id}")
                    if max_weight > i[2]:
                        cursor.execute(f"UPDATE Exercises SET MaxWeight = {max_weight} WHERE ID = {exer_id}")
            conection.commit()
            print("Запись успешно сохранена.\n")
        except:
            print("Ошибка\n")
    elif case == 2:
        print("Запись не сохранена.\n")

def delete_exercise():
    check = input("ВНИМАНИЕ!\nУдаление упражнение также сотрет информацию о нем в дневнике. Хотите продлжить?\n[1]Да\n[2]Нет\n")
    while check_input(check, int) == 'not':
        check = input('Ошибка, повторите ввод.\nХотите продлжить?\n[1]Да\n[2]Нет\n')
    check = int(check)
    while check != 1 and check != 2:
        check = input("Ошибка, повторите ввод.\nХотите продлжить?\n[1]Да\n[2]Нет\n")
        while check_input(check, int) == 'not':
            check = input('Ошибка, повторите ввод.\nХотите продлжить?\n[1]Да\n[2]Нет\n')
        check = int(check)
    if check == 2:
        return 
    
    print("\nСПИСОК ДОСТУПНЫХ УПРАЖНЕНИЙ")
    print_rows_from_table(select_rows_from_table("Exercises", "ID", "Exercise"), ["Id", "Упражнение"])
    ex = input(("Выберите номер упражнения для удаления: "))
    while check_input(ex, int) == 'not':
        ex = input("Ошибка, повторите ввод.\nВыберите номер упражнения для удаления: ")
    ex = int(ex)
    while check_id(ex, 'Exercises'):
        print("\nСПИСОК ДОСТУПНЫХ УПРАЖНЕНИЙ")
        print_rows_from_table(select_rows_from_table("Exercises", "ID", "Exercise"), ["Id", "Упражнение"])
        ex = input(("Ошибка, повторите ввод.\nВыберите номер упражнения для удаления: "))
        while check_input(ex, int) == 'not':
            ex = input("Ошибка, повторите ввод.\nВыберите номер упражнения для удаления: ")
        ex = int(ex)
    name_ex = select_one_value_from_table_by_id('Exercises', 'Exercise', ex)
    
    check = input(f"Удалить упражнение {name_ex[0]}?\n[1]Да\n[2]Нет\n")
    while check_input(check, int) == 'not':
        check = input(f"Ошибка, повторите ввод.\nУдалить упражнение {name_ex[0]}?\n[1]Да\n[2]Нет\n")
    check = int(check)
    while check != 1 and check != 2:
        check = input(f"Ошибка, повториет ввод.\nУдалить упражнение {name_ex[0]}?\n[1]Да\n[2]Нет\n")
        while check_input(check, int) == 'not':
            check = input(f"Ошибка, повторите ввод.\nУдалить упражнение {name_ex[0]}?\n[1]Да\n[2]Нет\n")
        check = int(check)
    if check == 1:
        delete_line_from_table(ex, 'Exercises')
        cursor.execute(f"DELETE FROM Journal WHERE ExID = {ex}")
        print("Упражнение удалено.")
        conection.commit()
    elif check == 2:
        print("Упражнение не удалено.")

def delete_line_in_journal():
    while True:
        print_rows_from_table(select_rows_from_table("Dates", "ID", "Date"), ["ID", "Date"])
        date = input("Выберите номер даты: ")
        while check_input(date, int) == 'not':
            date = input("Ошибка, повторите ввод.\nВыберите номер даты: ")
        date = int(date)
        while check_id(date, "Dates"):
            date = int(input("Ошибка, повторите ввод. Выберите номер даты: "))
            while check_input(date, int) == 'not':
                date = input("Ошибка, повторите ввод.\nВыберите номер даты: ")
            date = int(date)
        sliced = list(cursor.execute(f"""
                          SELECT Journal.ID, LineID, Exercise, ApprNum, Reps, Weight, AppCount
                          FROM Journal
                          LEFT JOIN Exercises ON Journal.ExID = Exercises.ID
                          WHERE Date = {date}"""))
        if len(sliced) == 0:
            print("Журнал пуст")
            return
        [print(str(i).ljust(20), end="") for i in ["Номер", "Название", "Подход", "Повторений", "Вес"]]
        print()
        for i, line in enumerate(sliced, 1):
            #print(str(i).ljust(20), end="")
            [print(str(cells).ljust(20), end="") for cells in line[1:-1]]
            print()
        check = input("Выберите номер записи для удаления\nВНИМАНИЕ!\nУдаление сотрет все записи об этом упражнении за текущую дату.\n")
        while check_input(check, int) == 'not':
            check = input("Ошибка, повторите ввод.\nВыберите номер даты: ")
        check = int(check)
        while check not in list(map(lambda x: x[0], select_rows_from_table("Journal", "LineID"))):
            check = input("Ошибка, повторите ввод.\nВыберите номер записи для удаления\n")
            while check_input(check, int) == 'not':
                check = input("Ошибка, повторите ввод.\nВыберите номер даты: ")
            check = int(check)
        check_2 = input("Вы уверены, что хотите удалить эту запись?\n[1]Да\n[2]Нет, выбрать другую запись\n[3]Нет, отменить удаление\n")
        while check_input(check_2, int) == 'not':
            check_2 = input("Ошибка, повторите ввод.\n[1]Да\n[2]Нет, выбрать другую запись\n[3]Нет, отменить удаление\n ")
        check_2 = int(check_2)
        while check_2 not in [1, 2, 3]:
            check_2 = input("Ошибка, повторите ввод.\nВы уверены, что хотите удалить эту запись?[1]Да\n[2]Нет, выбрать другую запись\n[3]Нет, отменить удаление\n")
            while check_input(check_2, int) == 'not':
                check_2 = input("Ошибка, повторите ввод.\n[1]Да\n[2]Нет, выбрать другую запись\n[3]Нет, отменить удаление\n ")
            check_2 = int(check_2)
        if check_2 == 3:
            return 
        elif check_2 == 2:
            continue
        #line_id = sliced[check-1][0]
        for i in range(sliced[check][-1]):
            cursor.execute(f"DELETE FROM Journal WHERE LineID = {check}")
        print("Запись успешно удалена")
        return

def max_exercise_indicator():
    print("\nСПИСОК ДОСТУПНЫХ УПРАЖНЕНИЙ")
    print_rows_from_table(select_rows_from_table("Exercises", "ID", "Exercise"))
    check = input("Выберите упражнение: ")
    while check_input(check, int) == 'not':
        check = input("Ошибка, повторите ввод.Выберите упражнение: ")
    check = int(check)
    while check_id(check, "Exercises"):
        check = input("Ошибка, повторите ввод.\nВыберите упражнение: ")
        while not check_input(check, int):
            check = input("Ошибка, повторите ввод.Выберите упражнение: ")
        check = int(check)
    print()
    print_rows_from_table(select_rows_from_table("Exercises", "Exercise", "AppCount", "MaxWeight", "MaxRep", condition=f"ID = {check}"), ["Упражнение", "Подходы", "Вес", "Повторения"])

def lines_by_date():
    date = choice_date()
    print_all_from_dairy(condition=f"WHERE Journal.Date = {date}")

def choice_date():
    print_rows_from_table(map(lambda x: (x[0], ".".join(x[1].split("-")[::-1])),
        [i for i in cursor.execute("SELECT * from Dates ORDER BY julianday(Date)")]), ["ID", "Дата"])
    date = input("Выберите номер даты: ")
    while check_input(date, int) == 'not':
        date = input("Ошибка, повторите ввод.\nВыберите номер даты: ")
    date = int(date)
    while check_id(date, "Dates"):
        date = input("Ошибка, повторите ввод.\nВыберите номер даты: ")
        while check_input(date, int) == 'not':
            date = input("Ошибка, повторите ввод.\nВыберите номер даты: ")
        date = int(date)
    return date

def exercise_plot():
    check = input("Выберите режим графика\n[1]График для всех сохраненных дат\n[2]График начиная с даты\n")
    while check_input(check, int) == 'not':
        check = input("Ошибка, повторите ввод.\n[1]График для всех сохраненных дат\n[2]График начиная с даты\n")
    check = int(check)
    while check != 1 and check != 2:
        check = input("Ошибка, повторите ввод.\nВыберите режим графика\n[1]График для всех сохраненных дат\n[2]График начиная с даты\n")
        while check_input(check, int) == 'not':
            check = input("Ошибка, повторите ввод.\n[1]График для всех сохраненных дат\n[2]График начиная с даты\n")
        check = int(check)
        
    print("\nСПИСОК ДОСТУПНЫХ УПРАЖНЕНИЙ")
    print_rows_from_table(select_rows_from_table("Exercises", "ID", "Exercise"), ["Id", "Упражнение"])
    ex = input(("Выберите номер упражнения: "))
    while check_input(ex, int) == 'not':
        ex = input("Ошибка, повторите ввод.\nВыберите номер упражнения: ")
    ex = int(ex)
    while check_id(ex, 'Exercises'):
        print_rows_from_table(select_rows_from_table("Exercises", "ID", "Exercise"), ["Id", "Упражнение"])
        ex = input(("Ошибка, повторите ввод.\nВыберите номер упражнения: "))
        while check_input(ex, int) == 'not':
            ex = input("Ошибка, повторите ввод.\nВыберите номер упражнения: ")
        ex = int(ex)
    voc_data = dict()
    for i in set(map(lambda x: x[0], cursor.execute(f"SELECT LineID FROM Journal WHERE ExID = {ex}"))):
        max_reps = 0
        max_weight = 0
        for j in cursor.execute(f"""SELECT Dates.Date, Reps, Weight 
                                   FROM Journal 
                                   LEFT JOIN Dates ON Journal.Date = Dates.ID 
                                   WHERE LineID = {i}"""):
            if j[-2] > max_reps:
                max_reps = j[-2]
            if j[-1] > max_weight:
                max_weight = j[-1]
            voc_data[i] = (j[0], max_reps, max_weight)
    same_dates = dict()
    for value in voc_data.values():
        same_dates.setdefault(value[0], [])
        same_dates[value[0]].append((value[-2], value[-1]))
    print(same_dates)
    if check == 2:
        date = choice_date()
        date = "".join(reversed(next(cursor.execute(f"SELECT Date FROM Dates WHERE ID = {date}"))[0].split(".")))
        same_dates = {".".join(reversed(i[0].split("-"))): i[1] for i in sorted(list(filter(lambda x: x[0] >= date, same_dates.items())), key=lambda x: x[0].split("."))}
    else:
        same_dates = {".".join(reversed(i[0].split("-"))): i[1] for i in sorted(same_dates.items(), key=lambda x: x[0])}
    reps = [max(value, key=lambda x: x[0]) for value in same_dates.values()]
    weights = [max(value, key=lambda x: x[1]) for value in same_dates.values()]
    plt.plot(same_dates.keys(), list(map(lambda x: x[0], reps)), color="green", marker="*")
    plt.title("Повторения")
    plt.show()
    plt.plot(same_dates.keys(), list(map(lambda x: x[1], weights)), color="red", marker="*")
    plt.title("Вес")
    plt.show()

conection = sql.connect('test.db', timeout=10)
cursor = conection.cursor()
#print(next(one_row_from_table(1, "Exercises")))