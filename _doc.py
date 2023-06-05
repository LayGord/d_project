'''

24.05.23

Реализация класса документа

Документ - совокупность ячеек с возможностью:
- их загрузки
- сохранения
- изменения

помимо этого, документ имеет название и метаданные:
- дату создания
- опционально устройство с которого документ был изменен в последний раз

'''

import tkinter as tk
from tkinter import ttk
import json
import _cell_1 as cl
import os

class Document():
    #  создание документа
    def __init__(self, metadata={}, cells={}, doc_name=''):

        self.doc_name = doc_name
        self.cells = cells
        self.metadata = metadata

    #  загрузка документа из файла
    def load(self, filepath):
        isfile = os.path.isfile(filepath)  # не создан ли файл?
        if (isfile):
            with open(filepath, 'r') as fp:
                data = json.load(fp)
                self.doc_name = data['doc_name']
                self.metadata = data['metadata']
                self.cells = data['cells']
        else:
            pass

    #  создание файла под документ
    def create(self, filepath):
        isfile = os.path.isfile(filepath)  # не создан ли файл?
        if not isfile:
            with open(filepath, 'w') as fp:
                json.dump({'doc_name': self.doc_name, 'metadata': self.metadata, 'cells': self.cells}, fp, indent=4)
        else:
            pass

    #  сохранение документа в файл
    def save(self, filepath, queue={}):
        #isfile = os.path.isfile(filepath)  # создан ли файл?
        #print(isfile)

        isfile =True
        if isfile:
            # собираем ячейки на экспорт в файл
            cells = {}

            for elem in queue:
                cells[elem] = queue[elem].export_data()

            print(f"Ячейки упакованные для записи в файл:\n{cells}")
            self.cells = cells

            with open(filepath, 'w') as fp:
                json.dump({'doc_name': self.doc_name, 'metadata': self.metadata, 'cells': self.cells}, fp, indent=4)
        else:
            pass
