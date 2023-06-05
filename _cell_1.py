'''

24.05.23

Реализация класса ячейки

Ячейка хранит в себе:
- имя
- номер порядковый (нужен для вывода)
- Основной текст ( если есть ) + его высота
- Текст строки вывода ( если есть ) + его высота
- Поле имён ( словарь с именами переменных и их значениями )
- имя обработчика ( определяет по сути своей тип ячейки: вычисления, медиа, тест и тд)
- состояние
- область видимости
- доп инфо (словарь)

методы ячейки:
- создание (новой или на базе переданных в конструктор данных)
- выгрузка данных из ячейки
- удаление
- изменение видимости поля имен
- смена обработчика
- отображение в интерфейсе программы ( сборка ячейки перед отрисовкой - отрисовку делает pack() )
'''



import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext

c_font = ('Consolas 11')
EXECUTORS = ['sh_yard()', 'sh_yard() + trace', 'eval()', 'eval() + trace', 'linal_exec()', 'linal_exec() + trace', 'Text']

class Cell(ttk.Frame):
    #  создание ячейки (с нуля или на базе переданных данных)
    def __init__(self, name='<default_name>', number='№ - ', text='', text_height=10, out='', out_height=1, namespace={}, engine_name='default', state='created', scope='inner', **kwargs):
        super().__init__(**kwargs)  # инит тткшной рамки
        self.name = name
        self.number = number
        self.text = text
        self.text_height = text_height
        self.out = out
        self.out_height = out_height
        self.namespace = namespace
        self.engine_name = engine_name
        self.state = state
        self.scope = scope

    #  выгрузка данных (нужно для сохранения в документ)
    def export_data(self):
        result = {
            "name": self.name,
            "number": self.number,
            "text": self.text,
            "text_height": self.text_height,
            "out": self.out,
            "out_height": self.out_height,
            "namespace": self.namespace,
            "engine_name": self.engine_name,
            "state": self.state,
            "scope": self.scope
        }
        return result

    #  удаление ячейки
    def delete(self):
        print(f'Ячейка {self.number} ', end='')
        self.destroy()
        print('удалена!\n')

    # изменение видимости поля имен
    def change_scope(self, scope):
        self.scope = scope

    #  смена обработчика
    def change_exec(self, exec_name):
        self.engine_name = exec_name

    #  сборка ячейки для отрисовки
    def build(self):

        global EXECUTORS

        # row 0
        cell_num_field = tkinter.Entry(self, width=3, bg='white', font=c_font)
        cell_num_field.grid(row=0, column=0, padx=5, pady=5, sticky='nesw')
        cell_num_field.insert(index=1, string=self.number)

        cell_name_field = tkinter.Entry(self, width=100, bg='white', font=c_font)
        cell_name_field.insert(index=1, string=self.name)
        cell_name_field.grid(row=0, column=1, padx=5, pady=5, columnspan=13, sticky='nesw')

        cell_exec = ttk.Combobox(self, values=EXECUTORS, font=c_font)
        cell_exec.grid(row=0, column=15, padx=5, pady=5, sticky='nesw')

        btn_run = tkinter.Button(self, text='Запустить', width=12, height=1, bg='white', font=c_font, command=lambda: update_cell_data(self))
        btn_run.grid(row=0, column=16, padx=5, pady=5, sticky='nesw')

        btn_delete = tkinter.Button(self, text='X', width=4, height=1, bg='white', font=c_font)
        btn_delete.grid(row=0, column=17, padx=5, pady=5, sticky='nesw')


        # row 1

        cell_text = scrolledtext.ScrolledText(self, height=self.text_height, width=130, undo=True, font=c_font)
        cell_text.insert(tkinter.INSERT, self.text)
        cell_text.grid(row=1, column=0, padx=5, pady=5, columnspan=13, sticky='nesw')

        label_var = tkinter.Text(self, width=10, height=self.text_height, font=c_font)
        label_var.grid(row=1, column=14, columnspan=4,  padx=5, pady=5, sticky='nesw')


        # row 2

        cell_output = scrolledtext.ScrolledText(self, height=self.out_height, width=160, undo=True)
        cell_output.insert(tkinter.INSERT, self.out)
        cell_output.grid(row=2, column=0, padx=5, pady=5, columnspan=18, sticky='nesw')


    # пересчет всех данных ячейки. вызывать при запуске обработчика!
        def update_cell_data(self):
            self.number = cell_num_field.get()
            self.name = cell_name_field.get()
            self.text = cell_text.get('0.0', 'end-1c')
            self.engine_name = cell_exec.get()
            self.out = cell_output.get('0.0', 'end-1c')

        def calculate(self):
            pass