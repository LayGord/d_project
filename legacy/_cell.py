import tkinter
from tkinter import *
from tkinter import ttk
import _shunting_yard as sy


class Cell(ttk.Frame):
    def __init__(self, name='name', number=None, text_exp=('', 4), output=('', 1), namespace={}, cell_type=0, engine_name='default', state='created', **kwargs):
        super().__init__(**kwargs)
        # заносим все атрибуты ячейки

        self.name = name  # имя ячейки
        self.number = number  # номер ячейки

        self.text_rows = text_exp[1]  # высота текста
        self.text_data = text_exp[0]  # текст выражения

        self.output_rows = output[1]  # высота вывода
        self.output_data = output[0]  # текст вывода

        self.namespace = namespace  # поле имён {'key': float(value), ... }
        self.cell_type = cell_type  # тип ячейки (calc, text, markdown, media)

        self.engine_name = engine_name  # обработчик выражений [default, none, symbolic?, python_evaluate]
        self.state = state  # состояние

    def get_data(self):  # получение данных из ячейки
        res = {'name': self.name, 'text_exp': (self.text_data, self.text_rows), 'output': (self.output_data, self.output_rows),
               'namespace': self.namespace, 'cell_type': self.cell_type, 'engine': self.engine_name, 'state': self.state}
        return res


# формируем ячейку
def showFrame(cell):
    def evaluate(cell):
        pass

    fr = Cell(borderwidth=2, relief='solid', height=100)
    fr.pack(fill='x', pady=3)

    # Верхняя панель ячейки
    cell_name_field = tkinter.Entry(fr, width=16, bg='white')
    cell_name_field.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    btn_run = tkinter.Button(fr, text='Запустить ячейку', width=16, height=1, bg='white', command=lambda: evaluate(fr))
    btn_run.grid(row=0, column=3, padx=5, pady=5)

    btn_delete = tkinter.Button(fr, text='Удалить ячейку', width=16, height=1, bg='white', command=fr.destroy)
    btn_delete.grid(row=0, column=2, padx=5, pady=5)

    # нижняя часть ячейки
    text = tkinter.Text(fr, height=cell.text_rows, width=100)
    text.insert(1.0, cell.text_data)
    text.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

    label_var = tkinter.Text(fr, width=30, height=cell.text_rows)
    label_var.grid(row=1, column=2, columnspan=2, padx=5, pady=5)

    output_field = tkinter.Text(fr, width=130, height=cell.output_rows)
    output_field.insert(1.0, cell.output_data)
    output_field.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="w")

