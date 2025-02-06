from bs4 import BeautifulSoup
import pandas as pd

# Открываем файл
with open('123', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Парсим HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Ищем данные о вакансиях
vacancies = []
data = {}
data['Должность'] = soup.select_one('body > div.wrapper-improved > div:nth-child(2) > div.head-block > div.head-block-header > h1').get_text(strip=True)
data['График работы'] = soup.select_one('div.info-block div:nth-child(5) .info-item-value').get_text(strip=True)
data['Тип занятости'] = soup.select_one('div.info-block div:nth-child(6) .info-item-value').get_text(strip=True)

headers_raw = soup.select('body > div.wrapper-improved > div.job-page-wrapper.base__wrapper > div.job-page > div.content-block > p')
headers = list(map(lambda x: x.get_text(strip=True), headers_raw))
print(headers)
index = len(headers) - headers.index('Что мы ожидаем от Вас:') - 1
print(index)

print(len(soup.select('body > div.wrapper-improved > div.job-page-wrapper.base__wrapper > div.job-page > div.content-block > ul')))

expectations_raw = soup.select('body > div.wrapper-improved > div.job-page-wrapper.base__wrapper > div.job-page > div.content-block > ul')
expectations = expectations_raw[len(expectations_raw) - index].select('li')

for i,expctation in  enumerate(expectations):
    data[f'Что мы ожидаем от Вас {i+1}'] = expctation.get_text(strip=True)
vacancies.append(data)


df = pd.DataFrame(vacancies)

# Сохраняем в Excel
output_path = 'MRSK_test.xlsx'
df.to_excel(output_path, index=False)
print(f"Данные сохранены в файл: {output_path}")