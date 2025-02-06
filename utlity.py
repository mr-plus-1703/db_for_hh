import pandas as pd
import re

def experience_number(s):
    s = s.split()
    
    if len(s) < 2:
        return 0
    
    try:
        return int(s[1])
    except:
        return 0

def education(input_file: str, output_file: str, column_name: str = "Образование 2"):
    df = pd.read_excel(input_file)
    if column_name in df.columns:
        df[column_name] = df[column_name].astype(str).str.replace(".", "", regex=False)

        # Сохраняем обновленный файл
        df.to_excel(output_file, index=False)
        print(f"Файл сохранен: {output_file}")


def exp(input_file: str, output_file: str, source_column: str = "Опыт работы", new_column: str = "Опыт работы 2"):
     # Загружаем данные
    df = pd.read_excel(input_file)

    # Проверяем, есть ли нужный столбец
    if source_column in df.columns:
        # Функция для поиска первого числа
        def find_first_number(text):
            if pd.isna(text):  # Если строка пустая
                return 0
            match = re.search(r"\d+", str(text))  # Ищем первое число
            return int(match.group()) if match else 0  # Если число найдено, возвращаем его, иначе 0

        # Создаем новый столбец с найденными числами
        df[new_column] = df[source_column].apply(find_first_number)

        # Сохраняем обработанный файл
        df.to_excel(output_file, index=False)


def merge(input_file: str, output_file: str, columns_to_merge: list, new_column: str = "Что мы ожидаем от Вас (Объединённое)"):
    # Загружаем данные
    df = pd.read_excel(input_file)

    # Проверяем, есть ли все нужные столбцы
    missing_columns = [col for col in columns_to_merge if col not in df.columns]
    if missing_columns:
        return

    # Объединяем содержимое столбцов в новый столбец (разделяя переносом строки)
    df[new_column] = df[columns_to_merge].astype(str).agg(lambda x: "&".join(x.dropna().unique()), axis=1)

    # Удаляем возможные строки с "nan" после преобразования
    df[new_column] = df[new_column].str.replace("nan", "").str.strip()

    # Сохраняем обработанный файл
    df.to_excel(output_file, index=False)


def clean_text(text):
    if pd.isna(text):  # Если пусто, возвращаем пустую строку
        return ""

    text = re.sub(r"\.", "", str(text))  # Убираем точки
    parts = text.split("&")  # Разбиваем по переносам строк

    if len(parts) > 1:  
        parts.pop(-1)  # Удаляем последний элемент

    return "&".join(parts).strip()  # Объединяем обратно


def clean_merged(input_file: str, output_file: str, column_name: str = "Что мы ожидаем от Вас (Объединённое)"):
     # Загружаем данные
    df = pd.read_excel(input_file)

    # Проверяем, есть ли нужная колонка
    if column_name in df.columns:
        # Применяем функцию к столбцу
        df[column_name] = df[column_name].apply(clean_text)

        # Сохраняем обработанный файл
        df.to_excel(output_file, index=False)


def split_and_expand(input_file: str, output_file: str, id_column: str = "id", text_column: str = "Умения"):
        # Загружаем данные
    df = pd.read_excel(input_file)

    # Проверяем, есть ли нужные столбцы
    if id_column not in df.columns or text_column not in df.columns:
        print(f"Один из столбцов '{id_column}' или '{text_column}' не найден в файле.")
        return

    
    # Удаляем пробелы после разделителей и заменяем их на запятую
    df[text_column] = df[text_column].astype(str)
    df[text_column] = df[text_column].apply(lambda x: re.sub(r"\s*[,;&]\s*", ",", x).strip())

    # Разделяем строки по запятым
    exploded_df = df[[id_column, text_column]].dropna().copy()
    exploded_df[text_column] = exploded_df[text_column].str.split(",")

    # Разворачиваем список значений в новые строки
    final_df = exploded_df.explode(text_column).reset_index(drop=True)

    # Сохраняем обработанный файл
    final_df.to_excel(output_file, index=False)



# df = pd.read_excel("filtr_for_id_all.xlsx")

# df["experience_min"] = df["experience"].apply(experience_number)

# df.to_excel("filtr_for_id_all.xlsx", index=False)

input_path = "exl/MRSK+PCBK_new_sills.xlsx"
output_path = "exl/MRSK+PCBK_id_skills.xlsx"

# education(input_path, output_path)

# exp(input_path, output_path)


# columns_to_merge = [
#     "Что мы ожидаем от Вас 3",
#     "Что мы ожидаем от Вас 4",
#     "Что мы ожидаем от Вас 5",
#     "Что мы ожидаем от Вас 6",
#     "Что мы ожидаем от Вас 8",
#     "Что мы ожидаем от Вас 9"
# ]

# merge(input_path, output_path, columns_to_merge)


# clean_merged(input_path, output_path)


split_and_expand(input_path, output_path)