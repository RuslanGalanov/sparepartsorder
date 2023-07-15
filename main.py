from collections import Counter

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

from src.functions import parse, save_data
from src.models import Spare
from src.config import years, ranges




out_from_files = []

# Вытаскиваем данные из бухгалтерских отчетов
for year in years:
    out_from_files += parse(str(year)+'.xlsx', ranges[year])

# Вытаскиваем производственные артикулы
refs = [x.ref for x in out_from_files]

# Вытаскиваем наименования товаров
names = [x.name for x in out_from_files]

# Считаем повторения артикулов 
# эта информация даст понимание о движении конкретного товара в конкретный год
c = Counter(refs)
data = dict(c)


# Подготовка данных для анализа
# Составляем соответствие товаров и их движение по годам
# На выходе получаем товары и количество их продаж по годам
spares = []

for item in data:
    if item:

        # Товары продаваемые в одном году из 6-ти
        if data[item] == 1:

            idx = refs.index(item)
            el = out_from_files[idx]
            spares.append(
                (el.ref, el.name, {el.year: el.amount})
            )
        
        else:

            idxes = [i for i,j in enumerate(refs) if j == item]
            elements = [out_from_files[v] for v in idxes]
            counts = {el.year: el.amount for el in elements}
            spares.append(
                (item, elements[0].name, counts)
            )
    # В таблицах есть товары без артикулов, эти позиции нужно вычленить
    else:
        indexes = [i for i,j in enumerate(refs) if j == None]
        
        common_none = [out_from_files[v] for v in indexes]

        for item in common_none:

            spares.append(
                (None, item.name, {item.year: item.amount})
            )


# Обработка подготовленных данных 
# Построение точечных функций движения по каждому товару в отдельности
results = []

# Ось абсцисс - года
x = years.copy()
_ = x.pop(-1) # Удаляем последний год, для статистики он не нужен

# Методы апроксимации не работают на списке из натуральных чисел
x = [1.0 * c for c in x]
x = np.array(x)

for spare in spares:

    if spare[0]:
        y = []

        if '2018' in spare[2]:
            y.append(spare[2]['2018'])
        else:
            y.append(0)

        if '2019' in spare[2]:
            y.append(spare[2]['2019'])
        else:
            y.append(0)

        if '2020' in spare[2]:
            y.append(spare[2]['2020'])
        else:
            y.append(0)

        if '2021' in spare[2]:
            y.append(spare[2]['2021'])
        else:
            y.append(0)

        if '2022' in spare[2]:
            y.append(spare[2]['2022'])
        else:
            y.append(0)

        """ if '2023' in spare[2]:
            y.append(spare[2]['2023'])
        else:
            y.append(0) """

        if '2023' in spare[2]:
            # Оборот за последние полгода
            half_year = spare[2]['2023']
        else:
            half_year = 0

        # Методы апроксимации не работают на списке из натуральных чисел
        y = [1.0 * c for c in y]
        y = np.array(y)

        # Линейная аппроксимация для определения тенденции будущих движений товаров
        def fit(x, a, b):
            return a*x+b

        A, B = curve_fit(fit, x, y)[0]

        """ 
        Построение графика усредненной функции для визуального теста

        plt.plot(x, fit(x, A, B))
        plt.plot(x, y, 'r+')
        name_file = ' '.join(spare[0].split('/'))
        plt.savefig('img/'+name_file+'.png')

        plt.clf()
        plt.cla()
        plt.close() 
        """

        yy = [ss for ss in y if int(ss) != 0]

        if yy:
            # Средний оборот товаров за год
            average_annual_amount = round(sum(yy) / len(yy))
        else:
            average_annual_amount = 0

        # Прогноз движения на год на основании линейной функции (тенденция)
        function_prediction = round(fit(2023, A, B))

        results.append(
            (spare[0], spare[1], spare[2], half_year, average_annual_amount, function_prediction, map(str, yy))
        )

save_data(filename='data.xlsx', data=results)







        

