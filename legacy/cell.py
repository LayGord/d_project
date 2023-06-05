"""

Описание структуры и атрибутов ячейки.
Ячейка - логически изолированный блок документа, документ - совокупность ячеек.
Ячейка может быть вычислимой, текстовой, так же рассматривается возможность создания специфических ячеек.
У каждой ячейки предполагается наличие своей коллекции локальных переменных, если такие необходимы, но так же ячейка
    может использовать глобальные переменные и константы документа.

Компоненты ячейки:
    атрибуты: название, тип, локальное поле имён, доступ, строка с результатом, статус ячейки.
    фрэйм: интерфейс ячейки, состоит из управляющих кнопок, текстового поля.

"""
import tkinter
from tkinter import *
from tkinter import ttk
import _shunting_yard as sy


types = ['Calculations', 'Text', 'Others']  # словарь с типами ячеек
amount = 0

class Cell(ttk.LabelFrame):
    def __init__(self, name='Untitled', text='', namespace={}, cell_type=0, **kwargs):
        super().__init__(**kwargs)
        # заносим все атрибуты ячейки
        self.name = name
        self.text = text
        self.namespace = namespace
        self.cell_type = cell_type
        # формируем ячейку


    def get_info(self):
        cell_data = {'name': self.name,
                     'text': self.text,
                     'namespace': self.namespace,
                     'cell_type': self.cell_type,
        }
        return cell_data


def createFrame(self):
    def evaluate(self):
        data = text.get(1.0, END).splitlines()
        print(data)

        #токенизация
        res = sy.tokenize(data[0])[1]
        print(res)

        #Фильтрация
        res = sy.purifier(res)
        print(res)

        #Вычисление
        res = sy.sh_yard(res)
        print(res)

        output_field.insert(1.0, '= ' +  str(res[0][0]) + '\n')
        self.namespace['res'] = res[0][0]
        label_var['state'] = 'normal'
        label_var.delete(1.0, END)
        label_var.insert(1.0, 'res=' + str(res[0][0]) + '\n')
        label_var['state'] = 'disabled'

    fr = Cell(text="Ячейка", borderwidth=2, relief='solid', height=100)
    fr.pack(fill='x', pady=5)

    btn_run = tkinter.Button(fr, text='Запустить ячейку', width=16, height=1, bg='white', command=lambda: evaluate(fr))
    btn_run.grid(row=0, column=3, padx=5, pady=5)

    btn_delete = tkinter.Button(fr, text='Удалить ячейку', width=16, height=1, bg='white', command=fr.destroy)
    btn_delete.grid(row=0, column=2, padx=5, pady=5)

    text = tkinter.Text(fr, height=5, width=100)
    text.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

    label_var = tkinter.Text(fr, width=30, height=5, state="disabled")
    label_var.grid(row=1, column=2, columnspan=2, padx=5, pady=5)

    output_field = tkinter.Text(fr, width=130, height=1)
    output_field.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="w")
