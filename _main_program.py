"""
24/05/23
Описание структуры интерфейса и логики приложения.
Интерфейс приложения состоит из панели управления, Основного пространства - в нём будет отображаться и изменяться
    содержимое документа.

"""

import tkinter as tk
import tkinter.scrolledtext
from tkinter import ttk
from datetime import datetime as t
from tkinter import filedialog as fd
from tkinter.messagebox import showerror, showwarning, showinfo, askyesno


import _components as com
import _cell_1 as cell
import _doc as doc

from sys import stdout, stderr

stdout = open('log.txt', 'a')
stderr = open('log_errors.txt', 'a')


#  ---преднастройка
root = tk.Tk()

QUEUE_LOADED = {}  # очередь загруженных ячеек на отрисовку
QUEUE_ACTIVE = {}  # очередь отрисованных ячеек

DOCUMENT = None #doc.Document()  # текущий активный документ
PATH_CURRENT = ''

#  properties
root.title("тестовая сборка")
root.minsize(1080, 720)
root.maxsize(1920, 1080)


# отрисовщик сообщений системы
def open_popup(text):
    showinfo(title='Сообщение системы', message=text)


# методы работы с файлами

# создание документа
def create_doc_file():
    global DOCUMENT
    global PATH_CURRENT

    print(100 * '-')

    # получаем имя файла и путь к нему
    filename = fd.asksaveasfilename(title='Выберите директорию для создаваемого файла')  # получаем директорию для сохранения
    PATH_CURRENT = filename
    name = filename.split('/')[-1]

    if DOCUMENT:
        mb = askyesno(title='Сообщение системы', message="Сохранить изменения текущем документе?")
        if mb:
            save_doc_tofile()
            close_doc(skip_dial=1)
        else:
            close_doc(skip_dial=1)

    # вызываем пустой конструктор умышленно
    DOCUMENT = doc.Document(doc_name=name)

    # инициализируем метаданные и создаем сам файл
    DOCUMENT.metadata['amm_of_cells'] = 0
    DOCUMENT.create(filepath=filename)
    DOCUMENT.save(filepath=filename)
    print('! Это первичная упаковка при создании ячейки, программа работает корректно !')

    # сообщения системы
    open_popup(f'Документ {name} создан!')
    print(f'{t.now().time()} Документ {name} создан!\n')


def close_doc(skip_dial=0):
    global DOCUMENT
    global QUEUE_ACTIVE
    global QUEUE_LOADED
    global PATH_CURRENT

    print(100 * '-')

    # сохранять ли документ?
    if DOCUMENT and (skip_dial==0):
        mb = askyesno(title='Сообщение системы', message="Сохранить изменения текущем документе?")
        if mb:
            save_doc_tofile()
        else:
            pass

    # сообщение о запуске процесса
    print(f'{t.now().time()} Закрытие документа {DOCUMENT.doc_name}:')

    # стираем ячейки с экрана
    for elem in QUEUE_ACTIVE:
        QUEUE_ACTIVE[elem].delete()

    # чистим очереди ячеек
    QUEUE_ACTIVE.clear()
    QUEUE_LOADED.clear()

    # закрытие доукмента
    DOCUMENT = None
    PATH_CURRENT = ''

    # информация о процессе
    print(f'{t.now().time()} Очереди вычищены, документ успешно закрыт\n')

# загрузка документа
def open_doc_from_file():
    global DOCUMENT
    global PATH_CURRENT

    print(100 * '-')

    # если открытый документ уже существует
    if DOCUMENT:
        mb = askyesno(title='Сообщение системы', message="Сохранить изменения текущем документе?")
        print(mb)
        if mb == True:
            save_doc_tofile()
            close_doc()
        else:
            close_doc()

    DOCUMENT = doc.Document()

    # получаем имя файла и директорию
    filename = fd.askopenfilename(title='Выберите файл')
    PATH_CURRENT = filename
    name = filename.split('/')[-1]

    # загружаем данные в класс !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    DOCUMENT.load(filename)
    print(f"Файл {name} успешно открыт и подгружен! Рисуем ячейки!\n")

    # выгружаем ячейки из документа в загрузочную очередь, затем в активную
    global QUEUE_LOADED
    QUEUE_LOAD = DOCUMENT.cells
    QUEUE_ACTIVE = DOCUMENT.cells

    # отрисовка всех ячеек
    for elem in QUEUE_ACTIVE:
        create_cell(DOCUMENT, QUEUE_ACTIVE[elem])

    # сообщения системы
    open_popup(f'Документ {name} загружен!')
    print(f'{t.now().time()} Документ {name} полностью загружен!\n')

# сохранение документа
def save_doc_tofile():
    global DOCUMENT
    global QUEUE_ACTIVE
    global PATH_CURRENT

    print(100*'-')
    print(f'Сохраняем данные в {PATH_CURRENT}')

    if not DOCUMENT:
        open_popup(text='Нет открытых файлов!')
    else:
        DOCUMENT.save(filepath=PATH_CURRENT, queue=QUEUE_ACTIVE)

        # сообщения системы
        open_popup(text=f'Файл {DOCUMENT.doc_name} сохранен!')
        print(f'{t.now().time()} Сохранение {DOCUMENT.doc_name} завершено!\n')


# --- Ниже идут методы работы с ячейками

def create_cell(document, data={}):
    '''
        Внешняя процедура создания ячейки
        При создании ячейки мы отслеживаем - ячейка создается с нуля, или на базе данных из файла.
        При создании ячейки с нуля мы сначала генерируем новый индекс для нее, затем создаем ячейку и
            присваиваем ей новый, только что сгенерированный индекс.
        После этого ячейка ячейка отрисовывается и помещается в активную очередь.

        При создании ячейки на базе данных из файла, мы помещаем словарь с данными при генерации ячейки, затирая тем
            самым значения по-умолчанию предусмотренные для новых ячеек.
    '''

    print(100 * '-')

    #  создаем ячейку с нуля
    if not data:
        #  создаем ячейке новый документный номер
        document.metadata['amm_of_cells'] += 1

        new_cell = cell.Cell(master=frame.scrollable_frame, borderwidth=4, relief='solid', number=DOCUMENT.metadata['amm_of_cells'])
        new_cell.build()
        new_cell.pack(fill='y')

        #  добавляем ячейку в активную очередь минуя загрузочную
        QUEUE_ACTIVE[document.metadata['amm_of_cells']] = new_cell

    #  загружаем уже существующую ячейку на базе словаря из файла
    else:
        new_cell = cell.Cell(master=frame.scrollable_frame, name=data['name'],
                             number=data['number'], text=data['text'],
                             text_height=data['text_height'], out=data['out'],
                             out_height=data['out_height'], namespace=data['namespace'],
                             state=data['state'], scope=data['scope']
                             )
        new_cell.build()
        new_cell.pack(fill='y')

        #  добавляем ячейку в активную очередь
        QUEUE_ACTIVE[new_cell.number] = new_cell

    # биндим кнопку удаления на ячейку
    del_btn = new_cell.winfo_children()[4]
    del_btn.config(command=lambda: delete_cell_from_doc(new_cell))
    print(f'{t.now().time()} Ячейка {new_cell.number} создана!')
    print('Текущая очередь: ', QUEUE_ACTIVE, '\n')


def delete_cell_from_doc(cell_):
    '''
        Внешняя процедура даление ячейки:
            - удаляем ячейку из очереди
            - удаляем саму ячейку
    '''

    print(100 * '-')

    QUEUE_ACTIVE.pop(cell_.number)  # удаляем ячейку из очереди
    print(f'{t.now().time()} Ячейка {cell_.number} удалена из активной очереди!')
    cell_.delete()  # вызов встроенного в ячейку деструктора


#  ----- Гуи  -----
#  menu
mainmenu = tk.Menu(root)

#  файлы
filemenu = tk.Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Новый", command=lambda: create_doc_file())
filemenu.add_command(label="Открыть...", command=lambda: open_doc_from_file())
filemenu.add_command(label="Сохранить...", command=lambda: save_doc_tofile())
filemenu.add_command(label='Закрыть', command=lambda: close_doc())

#  справка
helpmenu = tk.Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="Помощь")
helpmenu.add_command(label="О программе")


#  настройки
configmenu = tk.Menu(mainmenu, tearoff=0)
configmenu.add_command(label="Интерфейс")
configmenu.add_command(label="Логирование")


#  действия
actionsmenu = tk.Menu(mainmenu, tearoff=0)
actionsmenu.add_command(label="Обработчик")
actionsmenu.add_command(label="Работа с ячейками")


#  цепляем все подменю к родительскому
mainmenu.add_cascade(label="Файл", menu=filemenu)
mainmenu.add_cascade(label="Настройки", menu=configmenu)
mainmenu.add_cascade(label="Действия", menu=actionsmenu)
mainmenu.add_cascade(label="Справка", menu=helpmenu)

mainmenu.add_command(label="Создать ячейку", command= lambda: create_cell(DOCUMENT))  # отладочная кнопка
mainmenu.add_command(label=' ')

#  добавляем меню в приложение
root.config(menu=mainmenu)


#  ----- рабочая область программы -----
#  главный холст
frame = com.ScrollableFrame(root)
frame.pack(fill='both', expand=True)


#  главный цикл обработчика
root.mainloop()