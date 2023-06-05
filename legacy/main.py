"""

Описание структуры интерфейса и логики приложения.
Интерфейс приложения состоит из панели управления, Основного пространства - в нём будет отображаться и изменяться
    содержимое документа.

"""

import tkinter as tk
import _cell

# MAINWINDOW (создаем экземпляр главного окна приложения)
win = tk.Tk()

# PROPERTIES (конфигурация интерфейса. загружается из config.json)
ver = 0.01
h, w = 720, 1080
num_of_cells = 0


# STRUCTURE (Описание структуры программы с указанием свойств)
win.title(f"Test sample ver.{ver}")
win.geometry(f'{w}x{h}+100+100')
win['bg'] = 'white'
# Навбар
navbar = tk.Frame(height=40, bg='white')
navbar.pack(anchor='nw', fill='x')

btn_open = tk.Button(navbar, text='Открыть', width=8, height=1, bg='white')
btn_open.pack(side='left')

btn_create = tk.Button(navbar, text='Создать документ', width=16, height=1, bg='white')
btn_create.pack(side='left')

btn_save = tk.Button(navbar, text='Сохранить', width=8, height=1, bg='white')
btn_save.pack(side='left')


btn_add_cell = tk.Button(navbar, text='Добавить ячейку', width=16, height=1, bg='white', command=lambda: _cell.showFrame(
    _cell.Cell()))
btn_add_cell.pack(side='right')

# поле ячеек
#cell.createFrame()


win.mainloop()