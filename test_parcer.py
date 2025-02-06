import requests
import pandas as pd
import re
from IPython.display import clear_output
import sys
import matplotlib.pyplot as plt
import seaborn as se
import numpy as np
from IPython.core.display import display, HTML



# принимает: 
# 'dfs' - список с таблицами
# 'captions' - подписи к таблицам
# 'space_width' - отступы между таблицами

# возвращает:
# выводит в консоль таблицы рядом с друг другом

def display_side_by_side(dfs:list, captions:list, space_width=10):
    output = ""
    combined = dict(zip(captions, dfs))
    
    for caption, df in combined.items():
        output += (df.style.set_properties(**{'text-align': 'left'})
                   .set_table_attributes("style='display:inline'")
                   .set_caption(caption)._repr_html_())
        output += "\xa0" * space_width
    
    display(HTML(output))
    
    
    
    # принимает: 
# 'count' - значение статус бара на данный момент
# 'total' - количество всех значений 100%
# 'status' - строка с описание статуса

# возвращает:
# выводит в консоль статус бар

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
    
    
    
    
    # принимает: 
# 'job_title' - название (или ключевые слова) для поиска вакансий
# 'pages_number' - количество страниц с вакансиями (pages_number * 100 - всего вакансий)
# 'area' - регион для поиска вакансий
# 'url' - адрес API

# возвращает:
# список со всеми id вакансий по заданным параметрам

def find_ids(job_title='Analyst', pages_number = 20, area=113, url = 'https://api.hh.ru/vacancies/'):
    # список в который добавляем все найденые id
    ids = []
    # счетчик для вывода на экран прогресса обработки
    count = 0
    # проверка не выходит количество страниц с вакансиями за предельное значение
    if pages_number > 20:
        pages_number = 20
    # посчет общего количества вакансий
    ids_sum = pages_number*100

    
    print(f'Start loading {ids_sum} job vacancies ')
    
    # проходимся по заданному количеству страниц с вакансиями
    for i in range(pages_number):
        # задаем параметры за запроса
        par = {'text': job_title, 'area': area, 'per_page': 100, 'page':i}
        # делаем запрос
        r = requests.get(url, params=par)        
        e = r.json()
        
        # поиск всех id на одной странице и добавление их в список ids
        for i in range(len(e['items'])):
            count += 1
            progress(count ,ids_sum, 'loaded')
            
            try:
                ids.append(e['items'][i].get('id'))
            except:
                print('Going beyond the allowed number of vacancies!')
                print(f'Uploaded {len(ids)} vacancies')
                return ids

    print('\nEverything OK')
    print(f'Uploaded {len(ids)} vacancies')
    
    # возварт списка с id всех найденых вакансий
    return ids



# принимает:
# 'm' - все данные в list(dict) полученные по id вакансии 

# возвращает:
# список с искомыми (чистыми) данными

def fill_row(m):
    
    d = []
    # проверка заполнености данных в выбранном поле.
    def name_none(data):
        # если ЕСТЬ данные заполняем из значения name
        if data != None:
            d.append(data.get('name'))
        # если данные отсутсвуют заполняем None
        else:
            d.append(None)
    
    # формирования данных по зарплате
    def salary_none(data):
        # если ЕСТЬ данные по зарплате, заполняем ОТ, ДО, ВАЛЮТА
        if data != None:
            d.append(True)
            d.append(data.get('from'))
            d.append(data.get('to'))
            d.append(data.get('currency'))
        # если данные отсутсвуют заполняем None
        else:
            d.append(False)
            d.append(None)
            d.append(None)
            d.append(None)
    
    # очистка данных "описание вакансии" от ненужных тегов
    def celar_description(data):
        # возращаем чистую строку
        return re.sub(r"<[^>]+>", "", data, flags=re.S)
    
    # формирование массива с "ключевыми навыками"
    def key_skills_fill(data):
        res = []
        # если ЕСТЬ данные формируем и возращаем масиив со всеми ключевыми навыками
        if data != None and len(data) != 0:
            return [el["name"] for el in data]
        # если данные отсутсвуют возращаем None
        else:
            return None
    
    # обработка строки с "датой публикации вакансии"
    def fill_date(data):
        return 'time' 
    # поиск и заполнение данных одной строки в масиив
    d.append(int(m.get('id')))
    d.append(m.get('premium'))
    d.append(m.get('name'))
    name_none(m.get('area'))
    
    salary_none(m.get('salary'))
       
    name_none(m.get('experience'))
    name_none(m.get('schedule'))
    name_none(m.get('employment'))
    
    d.append(celar_description(m.get('description')))
    d.append(key_skills_fill(m.get('key_skills')))
    
    name_none(m.get('employer'))
    
    d.append(fill_date(m.get('published_at')))
    
    d.append(m.get('alternate_url'))
    d.append(m.get('has_test'))
    
    # возращаем массив с данными по одной строке
    return d


# принимает:
# 'ids' - список со всеми id искомых вакансий
# 'url' - адрес API

# возвращает:
# итоговая таблица со всем искомыми вакансиями

def ceate_df(ids, url):
    # список с названиями колонок таблицы
    columns = [ 'id',
                'premium',
                'vacancy_name',
                'city',
                'salary',
                'salary_from',
                'salary_to',
                'currency',
                'experience',
                'schedule',
                'employment',
                'description',
                'skills',
                'employer',
                'publish_date',
                'vacancy_url',
                'has_test']
    
    # создание итоговой таблицы
    df = pd.DataFrame(columns = columns)
    count = 0
    
    # заполнение итоговой таблицы искомыми данными, с помощью списка со всем id вакансий
    print(f'\nStart adding {len(ids)} job vacancies ')
    for i in range(len(ids)):
        # запрос данных по вакансии по найденому id
        data = requests.get(url+ids[i]).json()
        # заполение данными 1 строки в итоговой таблице
        df.loc[i] = fill_row(data)
        count += 1
        progress(count ,len(ids), 'added')
    
    # возращаем итоговую таблицу
    print(f'\nAdded {len(df)} vacancies')
    return df

#job_title - название для фильтра на сайте

arry = find_ids(job_title='Электропривод',pages_number=100,area=72,url='https://api.hh.ru/vacancies/')
df = ceate_df(ids=arry,url='https://api.hh.ru/vacancies/')
file_name = 'df_hh_ru_privod.xlsx'
df.to_excel(file_name, index=False)