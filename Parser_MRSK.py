import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL страницы с вакансиями
base_url = "https://rosseti-ural.ru"
vacancies_url = f"{base_url}/vacancies/?f=&nbc_search=&area_id%5B%5D=2&filial_id%5B%5D=2&activity_id%5B%5D=2&activity_id%5B%5D=23&level_id%5B%5D=1#filter"

# Получаем HTML страницы
response = requests.get(vacancies_url)
response.raise_for_status()  # Проверяем, что запрос выполнен успешно
soup = BeautifulSoup(response.text, 'html.parser')

# Находим ссылки на все вакансии
vacancy_links = []

for i,el in enumerate(soup.select('body > div.wrapper-improved > div.job-items-section-wrapper.items-section-wrapper > div > a')):
     if i%2==1:
        vacancy_links.append(base_url + el['href'])

# Ищем данные о вакансиях
vacancies = []

# Обходим каждую ссылку и собираем данные
for link in vacancy_links:
    vacancy_response = requests.get(link)
    vacancy_response.raise_for_status()
    vacancy_soup = BeautifulSoup(vacancy_response.text, 'html.parser')

    # Извлекаем данные о вакансии
    try:
        data = {}
        
        data['Должность'] = vacancy_soup.select_one('body > div.wrapper-improved > div:nth-child(2) > div.head-block > div.head-block-header > h1').get_text(strip=True)
        data['График работы'] = vacancy_soup.select_one('div.info-block div:nth-child(5) .info-item-value').get_text(strip=True)
        data['Тип занятости'] = vacancy_soup.select_one('div.info-block div:nth-child(6) .info-item-value').get_text(strip=True)        

        headers_raw = vacancy_soup.select('body > div.wrapper-improved > div.job-page-wrapper.base__wrapper > div.job-page > div.content-block > p')
        headers = list(map(lambda x: x.get_text(strip=True), headers_raw))
        index = len(headers) - headers.index('Что мы ожидаем от Вас:') - 1

        expectations_raw = vacancy_soup.select('body > div.wrapper-improved > div.job-page-wrapper.base__wrapper > div.job-page > div.content-block > ul')
        expectations = expectations_raw[len(expectations_raw) - index].select('li')

        for i,expctation in  enumerate(expectations):
            data[f'Что мы ожидаем от Вас {i+1}'] = expctation.get_text(strip=True)
 
        vacancies.append(data)

        print(f"Сделал {len(vacancies)} раз")
    except Exception as e:
        print(f"Ошибка при обработке {link}: {e}")

# Создаем DataFrame
df = pd.DataFrame(vacancies)

# Сохраняем в Excel
output_path = 'MRSK_nach.xlsx'
df.to_excel(output_path, index=False)