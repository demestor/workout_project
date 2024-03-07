# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 15:16:20 2024

@author: night

Этот файл содержит меню программы
"""

import modul_1 as m1

print("Дневник тренировок\nВведите цыфру для выбора действия")
case = 0
while case != 10:
    case = int(input("""
[1]Вывести список доступных упражнений
[2]Добавить новое упражнений
[3]Удалить упражнениe
[4]Вывести дневник тренировок
[5]Добавить новую запись в дневник
[6]Удалить запись в дневнике
[7]Максимальные показатели по упражнению
[8]Вывести записи по дате
[9]Графики по прогрессу в упражнениях
[10]Выход
Выбор: """))
    print()
    if case == 1:
        print("\nСПИСОК ДОСТУПНЫХ УПРАЖНЕНИЙ")
        m1.print_rows_from_table(m1.select_rows_from_table("Exercises", "Exercise"))
    elif case == 2:
        if m1.add_new_exercise() == 0:
            print("Упражнение успешно добавлено")
            m1.conection.commit()
    elif case == 3:
        m1.delete_exercise()
    elif case == 4:
        m1.print_all_from_dairy()
    elif case == 5:
        m1.add_new_line_in_diary()
    elif case == 6:
        m1.delete_line_in_journal()
        m1.cursor.execute("DELETE FROM Dates WHERE Dates.ID NOT IN (SELECT Date FROM Journal)")
    elif case == 7:
        m1.max_exercise_indicator()
    elif case == 8:
        m1.lines_by_date()
    elif case == 9:
        m1.exercise_plot()

# Удалить даты в таблице Dates, которые не привязаны ни к одной записи в таблице Journal
m1.cursor.execute("DELETE FROM Dates WHERE Dates.ID NOT IN (SELECT Date FROM Journal)")

m1.conection.commit()
m1.conection.close()