import sqlite3,os
from random import randint,choice
from colorama import init,Fore
import time,re

#БАЗОВЫЕ ПРОЦЕДУРЫ И КОНФИГУРАЦИЯ
DATABASE=sqlite3.connect("database.db")
CURSOR=DATABASE.cursor()
SQL=lambda text:CURSOR.execute(str(text))
CLEAR=lambda:os.system('cls' if os.name == 'nt' else 'clear')
PAUSE=lambda:input("Для возвращения в меню нажмите ENTER...")
SQL("""SELECT * FROM peoples""")
FULL_DUMP=[i for i in list(CURSOR.fetchall())]
FETCH=lambda:CURSOR.fetchall()
P=lambda text,col:exec(f"print(Fore.GREEN+text[:10]+Fore.{col}+text[12:]+Fore.WHITE)")
days=["ПН","ВТ","СР","ЧТ","ПТ","СБ","ВС",]

#ПРОЦЕДУРЫ КОММАНДНОЙ ОБОЛОЧКИ
def SHOW_ALL():
    print("Ctrl+Z - остановить программу\nСtrl+C - остановить комманду")
    P("Комманда 1 - просмотр всей базы данных" ,"BLUE")
    P("Комманда 2 - добавление человека"       ,"CYAN")
    P("Комманда 3 - редактировать пользователя по айди","YELLOW")
    P("Комманда 4 - сгенерировать рассписание" ,"MAGENTA")
    P("Комманда 5 - показать рассписание"      ,"BLUE")
    P("Комманда 6 - сгенерировать воссточку"   ,"MAGENTA")
    P("Комманда 7 - показать восточку"         ,"BLUE")
    P("Комманда 8 - сменить данные человека по фамилии","YELLOW")
    P("Комманда 9 - рестарт программы"        ,"RED")

def PROCEDURE_1():
    print("Комманда 1 - просмотр всей базы данных\n"+10*"-")
    for col in FULL_DUMP:
        print(f"|{col}")
def PROCEDURE_2():
    print("Комманда 2 - добавление человека")
    name    =input("Введите имя: ")
    surname =input("Введите фамилию: ")
    lastname=input("Введите отчество: ")
    lvl     =input("Введите ранг: ")
    status=False
    print("Проверка введенных данных...")
    for data in [name,surname,lastname]:
        for lett in list(data):
            try:
                int(lett)
                print("Ошибка вводимых данных...")
                staus=False
                return False
            except:
                status=True
    if(len(name) > 0 and len(surname) > 0
        and len(name) > 0 and int(lvl) >= 1
        and int(lvl) <= 6
        and status):
        sql="""INSERT INTO peoples (name,surname,lastname,lvl)  VALUES('{}','{}','{}',{})"""
        SQL(sql.format(name,surname,lastname,lvl))
        DATABASE.commit()
        return True
    else:
        print("ОШИБКА!")
def PROCEDURE_3():
    print("Комманда 3 - редактировать пользователя")
    idtcng  =input("Введите id человека для редактирования: ")
    name    =input("Введите имя: ")
    surname =input("Введите фамилию: ")
    lastname=input("Введите отчество: ")
    lvl     =input("Введите ранг: ")
    print("Проверка введенных данных...")
    sql="""UPDATE peoples SET id={}, name='{}',surname='{}',lastname='{}',lvl={} WHERE id={};"""
    SQL(sql.format(idtcng,name,surname,lastname,lvl,idtcng))
    return DATABASE.commit()
def SAVE_TO_WEEK(data,t):
    f=open("week.txt",t)
    f.write(data)
    return f.close()
def PROCEDURE_4():
    print("Комманда 4 - сгенерировать рассписание\n")
    print("Внимание,  это действие уничтожит")
    print("предыдущее рассписание!!!")
    input("Нажмите ENTER, чтобы подтвердить")
    used=[]
    ti=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    SAVE_TO_WEEK(5*"\n"+f"РАССПИСАНИЕ: {ti}\n","w")
    for day in days:
        SAVE_TO_WEEK(10*"-"+day+10*"-"+"\n","a")
        while len(used) <= 6:
            i=choice(FULL_DUMP)
            if i not in used:
                SAVE_TO_WEEK(str(i)+"\n","a")
                used.append(i)
        used=[]
    print("Рассписание успешно сгенерированно!")
def PROCEDURE_5():
    print("Комманда 5 - показать рассписание")
    f=open("week.txt","r")
    print(f.read())
def PROCEDURE_6():
    print("Комманда 6 - сгенерировать воссточку")
    SQL("SELECT id FROM peoples")
    importuserids=list(FETCH())
    userids=[]
    useridsob=[]
    while len(userids) <= 10:
        id = input(f"Введите id человека.(Введено {len(userids)} из 11): ")
        if id not in userids:
            userids.append(f"({id},)")
        else:
            print("Этот айди уже присутствует!")
    print("Проверка введенных айди:")
    print(userids)
    print("Импорт айди из базы данных...")
    print(importuserids)
    for ind in range(len(userids)):
        if str(userids[ind]) in str(importuserids):
            useridsob.append(str(userids[ind]))
    input("Нажмите ENTER чтобы продолжить...")
    CLEAR()
    print("Результат:")
    if len(useridsob) == len(userids):
        print("Айди людей успешно добавлены в кэш:")
        f = open("восточка.txt","w")
        t=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
        f.write(f"Рассписание Воссточного наряда - {t}\n")
        f.write("\n"+10*"-"+"\nПН-ВТ-СР\n")
        f.close
        f=open("восточка.txt","a+")
        counter=0
        for userid in userids:
            counter=counter+1
            if len(userid) == 4:
                userid = userid[1]
            else:
                userid = userid[1]+userid[2]
            SQL("""SELECT * FROM peoples WHERE id={}""".format(userid))
            userdata=FETCH()
            print(userid)
            print(userdata)
            input("Нажмите ENTER чтобы продолжить...")
            print("Данные успешно записаны в файл 'восточка.txt'")
            f.write("\n"+str(userdata))
        f.close()
    else:
        print("Произошла ошибка: введенные данные отсутсвуют в базе данных")
def PROCEDURE_7():
    print("Комманда 7 - показать восточку")
    f=open("восточка.txt","r")
    print(f.read())
def PROCEDURE_8():
    print("Комманда 8 - сменить данные человека по фамилии")
    surname=input("Введите фамилию: ")
    sql="""SELECT * FROM peoples WHERE surname='{}'"""
    SQL(sql.format(surname))
    dbdump=FETCH()
    print(f"По запросу с фамилией {surname} найден(-о) {len(dbdump)} человек")
    if len(dbdump) <= 0:
        print("Введена несуществующая фаимилия. Попробуйте \nперезагрузить или проверить наличие")
        print("введенной фамилии с помощью комманды 1")
    else:
        print("которые доступны для редактирования")
        for p in range(len(dbdump)):
            print(f"[{p+1}]{dbdump[p]}")
        p=input("Введите [номер] человека для редактирования: ")
        txt="Вы выбрали человека под номером {}\n{}"
        print(txt.format(str(p),str(dbdump[int(p)-1])))
        print("Редактируйте:")
        uid=0
        try:
            uid=int(str(dbdump[int(p)-1])[1:3])
        except:
            uid=int(str(dbdump[int(p)-1])[1:2])
        name    =input("Введите имя: ")
        surname =input("Введите фамилию: ")
        lastname=input("Введите отчество: ")
        lvl     =input("Введите ранг: ")
        sql="""UPDATE peoples SET id={}, name='{}',surname='{}',lastname='{}',lvl={} WHERE id={};"""
        SQL(sql.format(uid,name,surname,lastname,lvl,uid))
        return DATABASE.commit()
def PROCEDURE_9():
    print("Комманда 9 - рестарт прогрраммы")
    input("Подтвердите нажав на ENTER...")
    os.system("python3 main.py")

#-----------------------------------------------------------------------------------------------
def TRY_RUN(PROC):
    try:
        FETCH()
        CLEAR()
        exec(f"{PROC}()")
        PAUSE()
        return True
    except:
        return False

#КОММАНДНАЯ ОБОЛОЧКА
def SHELL():
    init()
    CLEAR()
    print(Fore.GREEN+"---"+"Главное меню""---"+Fore.WHITE)
    SHOW_ALL()
    try:
        INPUT_DATA=input(">")
        TRY_RUN(f"PROCEDURE_{INPUT_DATA}")
        SHELL()
    except:
        SHELL()
try:
  SHELL()
except:
  SHELL()









